from tkinter import *
from tkinter import messagebox
from scipy.optimize import linprog
from tkinter.filedialog import askopenfilename
import pulp
from scipy.stats import randint_gen


class Optimizador:

    mensajeArchivo = "" #Texto contenido en el archivo
    cant = 0            #Cantidad de parcelas
    d = []              #Duracion de cosechar en la parcela i
    dmax = 0            #Duracion maxima de cosecha (Suma de duraciones de cada parcela)
    utilidades = []     #Utilidades de cada cosecha en cada instante de tiempo
    flag = False        #Bandera para ver si el archivo fue leido exitosamente
    y = []              #Instante donde empieza cosecha parcela 'i'  ((Variable de decision))
    x = []              #1 si se siembra en la parcela 'i', 0 si no  ((Variable de decision))
    z = []              #Variables z que sirven para restringir con ayudita del BigM
    listaX = []         #Variables Xij en lista
    listaUtilidades = []#Utilidades en lista
    bigM = 0
    model = pulp.LpProblem("Maximizar parcelas", pulp.LpMaximize)


    def pulpSolution(self):
        model = pulp.LpProblem("Profit maximising problem", pulp.LpMaximize)

        #Definición de variables
        U = pulp.LpVariable('U', lowBound=0, cat='Integer')
        X = pulp.LpVariable('X', lowBound=0, upBound=1, cat='Integer')

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
                        self.d = (linea.split())
                    if (i == 2):
                        self.dmax = int(linea)
                    if (i > 2):
                        line = linea.split()
                        line =[int(numero) for numero in line]
                        self.utilidades.append(line)

                        for numero in line:
                            self.listaUtilidades.append(numero)

                    i += 1
                myFile.seek(0)
                self.mensajeArchivo = myFile.read()
                # Obtiene lo que está en el archivo
                myFile.close()
                # cast string into integer
                self.d = [int(numero) for numero in self.d]
                self.flag = True
                print(self.utilidades)

        except:
            self.flag = False

    def definirY(self):
        # Se crea lista para la variable Yi
        for i in range(1, (self.cant + 1)):
            label = 'y' + str(i)
            self.y.append(pulp.LpVariable(label, lowBound=0, cat='Integer'))


    def definirZ(self):
        # Se crea lista para la variable Yi
        for i in range(1, (self.cant + 1)):
            label = 'z' + str(i)
            self.z.append(pulp.LpVariable(label, lowBound=0, cat='Integer'))

    def definirX(self):
        # Se crea matriz para la variable Xij
        for i in range(1, (self.cant + 1)):
            lista = []
            for j in range (1 ,self.dmax):
                label = 'x' + str(i) + str(j)
                varAux = pulp.LpVariable(label, lowBound=0, upBound=1, cat='Integer')
                lista.append(varAux)
                self.listaX.append(varAux)
            self.x.append(lista)

    def definirFuncObjetivo(self):
        self.model += pulp.lpDot(self.listaUtilidades, self.listaX)

    def agregarRestricciones(self):

        #Restricción 1 Se recorre la matriz x por filas
        for i in range (0,self.cant):
            j=0
            lista = []
            while(j <= self.dmax):
                lista.append(self.x[i][j])
                j+=1
            self.model += pulp.lpSum(lista) == 1

        # Restricción 2 Se recorre la matriz x por columnas
        for j in range (0,self.cant):
            i=0
            lista = []
            while(i <= self.dmax):
                lista.append(self.x[i][j])
                i+=1
            self.model += pulp.lpSum(lista) <= 1

        #Restricción 3
        for i in range(0,self.cant):
            self.model += self.y[i]+ self.d[i] -1 <= self.dmax

        # Restriccion 4 Las de Y de todas con todas papeeeeee
        contadorZ = 0
        for i in range (0,self.cant):
            contador = 0
            while(contador < self.cant):
                if(contador == i):
                    contador +=1
                else:
                    self.model += self.y[i] + self.d[i] -1 < self.y[contador] + self.bigM * (1 - self.z[contadorZ])
                    contadorZ+=1
                    contador += 1

    def optimizar(self):

        self.definirX()
        self.definirY()
        self.definirZ()
        self.definirFuncObjetivo()     #Se añade la función objetivo al modelo

        #Se agregan las restricciones
        self.agregarRestricciones()
        self.model.solve()
        pulp.LpStatus[self.model.status]
        print(pulp.value(self.model.objective))
        print("Después del todo")



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
        self.optimizador.optimizar()
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
