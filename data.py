from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename


#Creamos una ventana
app = Tk()
app.title("Cosecha de parcelas")
app.geometry("850x400")
#app.resizable(width=False, height=False)

#Se crea la ventana principal
ventana = Frame(app)
ventana.grid(column=0, row=0, padx=(60,60), pady=(20,20))
ventana.columnconfigure(0, weight=1)
ventana.rowconfigure(0, weight=1)

#Bandera, para la elección del archivo
existe_archivo = False;


#Borra el contenido del my_text_area
def EliminarContenido():
    my_text_area.config(state=NORMAL)
    my_text_area.delete(1.0, END)

#Se inserta un texto dado en el TEXT
def InsertText(texto):
    my_text_area.config(state=NORMAL)
    my_text_area.insert(END,texto)
    my_text_area.config(state=DISABLED)

#Aquí se activa el fileDialog
def OpenFile():
    global existe_archivo
    name = askopenfilename(initialdir="C:/Users/fabioacd/Desktop/",
                           filetypes =(("Text File", "*.txt"),("All Files","*.*")),
                           title = "Elija un archivo"
                           )
    #Se usa try en caso de que se elija un archivo desconocido o cierre la ventana sin elegir uno.
    try:
        with open(name,'r') as myFile:
            #Obtiene lo que está en el archivo
            info_message = myFile.read()
            #Limpia lo que haya
            EliminarContenido()
            #Imprime en el Text lo que haya en el archivo
            InsertText("El archivo dice:\n"+info_message)
            existe_archivo = True
    except:
        my_text_area.insert(END,"No existe el archivo")


def RunApp():
    if  existe_archivo:
        # Limpia lo que haya
        EliminarContenido()
        InsertText("Se ha elegido un archivo, se puede proceder a desarrollar el proyecto")

    else:
        # Limpia lo que haya
        EliminarContenido()
        InsertText("Debe elegir un archivo")


#Label
my_label_info = Label(ventana, text="Presione el botón para elegir el archivo")
my_label_info.place(x= 10, y=20)

#Botón de abrir
btn_abrir = Button(ventana, text="Abrir", command=OpenFile)
btn_abrir.place(x= 90, y=60)


#Label
my_label_run = Label(ventana, text="Presione el botón para hallar la solución")
my_label_run.grid(column=0, row=1, pady=60)

#Botón de Run
btn_run = Button(ventana, text="Go!", command=RunApp)
btn_run.place(x= 90, y=190)

#TextArea
my_text_area = Text(ventana, height=20, width=60)
my_text_area.grid(column=2, row=1, padx=50)


ventana.mainloop()