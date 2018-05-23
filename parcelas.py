from tkinter import *
from tkinter import messagebox
from scipy.optimize import linprog
from tkinter.filedialog import askopenfilename
from simplex import Simplex


#------------------------------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------------------------
class Optimizador:

    mensajeArchivo = "" #Texto contenido en el archivo
    cant = 0            #Cantidad de parcelas
    d = []              #Duracion de cosechar en la parcela i
    dmax = 0            #Duracion maxima de cosecha (Suma de duraciones de cada parcela)
    utilidades = []     #Utilidades de cada cosecha en cada instante de tiempo
    flag = False        #Bandera para ver si el archivo fue leido exitosamente
    y = []

    def abrirArchivo(self):
        name = askopenfilename(initialdir="",
                               filetypes=(("Text File", "*.txt"), ("All Files", "*.*")),
                               title="Elija un archivo"
                               )
        # Se usa try en caso de que se elija un archivo desconocido o cierre la ventana sin elegir uno.
        try:
            with open(name, 'r') as myFile:
                i = 0
                for linea in myFile:
                    if (i == 0):
                        self.cant = int(linea)
                    if (i == 1):
                        self.d = linea.split()
                    if (i == 2):
                        self.dmax = int(linea)
                    if (i > 2):
                        self.utilidades.append(linea.split())
                    i += 1
                myFile.seek(0)
                self.mensajeArchivo = myFile.read()
                # Obtiene lo que está en el archivo
                myFile.close()
                self.flag = True

        except:
            self.flag = False


    def optimizar(self):
    
        c = [-1, 4]
        A = [[-3, 1], [1, 2]]
        b = [6, 4]
        x0_bnds = (None, None)
        x1_bnds = (-3, None)
        res = linprog(c, A, b, bounds=(x0_bnds, x1_bnds))
        return res


class Interfaz:

    def __init__(self, master):

        self.optimizador = Optimizador()
        master.title("Cosecha de parcelas")
        master.geometry("850x400")
        master.resizable(width=False, height=False)

        # Se crea la ventana principal
        ventana = Frame(master)
        ventana.grid(column=0, row=0, padx=(60, 60), pady=(20, 20))
        ventana.columnconfigure(0, weight=1)
        ventana.rowconfigure(0, weight=1)

        # TextArea
        self.my_text_area = Text(ventana, height=20, width=60)
        self.my_text_area.grid(column=2, row=1, padx=50)

        # Label
        self.my_label_info = Label(ventana, text="Presione el botón para elegir el archivo")
        self.my_label_info.place(x=10, y=20)

        # Botón de abrir
        self.btn_abrir = Button(ventana, command= self.abrir_archivo, text="Abrir",)
        self.btn_abrir.place(x=90, y=60)

        # Label
        self.my_label_run = Label(ventana, text="Presione el botón para hallar la solución")
        self.my_label_run.grid(column=0, row=1, pady=60)


        # Botón de Run
        self.btn_run = Button(ventana, text="Go!", command=self.correr)
        self.btn_run.place(x=90, y=190)


    # Borra el contenido del my_text_area
    def eliminar_contenido(self):
        self.my_text_area.config(state=NORMAL)
        self.my_text_area.delete(1.0, END)

    def abrir_archivo(self):
        self.optimizador.abrirArchivo()
        if(self.optimizador.flag):
            text = "Contenido del txt: \n \n" + self.optimizador.mensajeArchivo
            self.insertar_texto(text)
        else:
            messagebox.showinfo("Alerta", "Error al cargar archivo")

    def correr(self):
        #if(self.optimizador.flag):
        self.insertar_texto(self.optimizador.optimizar())
        #else:
            #messagebox.showinfo("Alerta", "Archvo no cargado")


    # Se inserta un texto dado en el TEXT
    def insertar_texto(self, texto):
        self.my_text_area.config(state=NORMAL)
        self.my_text_area.insert(END, texto)
        self.my_text_area.config(state=DISABLED)


# Creamos una ventana
app = Tk()
interfaz = Interfaz(app)
app.mainloop()
