import tkinter as tk
from tkinter import ttk
from urllib.request import urlopen
from bs4 import BeautifulSoup 
import mysql.connector as mysql
from tkinter import messagebox as Messagebox


def analisis():
    global base 
    base=""
    conexion = mysql.connect( host='localhost', user= 'root', passwd='', db='paginas' )
    sql="insert into enlaces(link, estado) values (%s,%s)"
    operacion = conexion.cursor()
    url = urlopen(paginaC.get())
    bs = BeautifulSoup(url.read(), 'html.parser')
    for enlaces in bs.find_all("a"):
        pag = "{}".format(enlaces.get("href"))
        datos=(pag, False)
        operacion.execute(sql, datos)
        conexion.commit
    operacion.execute( "SELECT * FROM enlaces" )
    for link,estado in operacion.fetchall() :
        if(estado==0 and  "http" in link):
            url = urlopen(link)
            base += "      --" + link + "\n"
            bs1 = BeautifulSoup(url.read(), 'html.parser')
            for enlaces in bs1.find_all("a"):
               base += "{}".format(enlaces.get("href"))
               base += "\n"
            print("\nFin de enlaces encontrados\n")
    operacion.execute("update enlaces set estado=1 where estado=0")
    conexion.commit   
    conexion.close()
    Bd()
    #accion1.configure(state='enable')
def Bd():
    ventana1=tk.Tk()
    ventana1.title("Paginas Analizadas")
    texto11= ttk.Label(ventana1, text=base )
    texto11.grid(column=0,row=0)
    
   



    
   

ventana=tk.Tk()
ventana.title("Practica 3")
texto1= ttk.Label(ventana, text="URL: ")
texto1.grid(column=0,row=2)
pagina = tk.StringVar()
paginaC = ttk.Entry(ventana, width=34, textvariable=pagina)
paginaC.grid(column=1,row=2, columnspan=3)
accion = ttk.Button(ventana,text="Analizar", command = analisis)
accion.grid(column=3,row=4)
#accion1 = ttk.Button(ventana,text="Base de datos", command = Bd)
#accion1.grid(column=1,row=4)
#accion1.configure(state='disabled')
ventana.mainloop()