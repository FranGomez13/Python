import smtplib
from email.mime.text import MIMEText
from tkinter import *
from tkinter import messagebox
import _thread
from conexion import *
import re


class EnvioMensajes(object):
    def __init__(self):
        self.base = Conexion()
        self.ventana = Tk()
        self.ventana.geometry("500x125")
        self.ventana.title("Informacion Ingenieria En Sistemas")
        self.ventana.resizable(0, 0)
        self.lblNombre = Label(text="Nombre:").place(x=5, y=10)
        self.nombre = StringVar()
        self.txtNombre = Entry(width=70, textvariable=self.nombre)
        self.txtNombre.place(x=65, y=10)
        self.lblColegio = Label(text="Colegio:").place(x=5, y=35)
        self.colegio = StringVar()
        self.txtColegio = Entry(width=70, textvariable=self.colegio)
        self.txtColegio.place(x=65, y=35)
        self.lblCorreo = Label(text="Correo:").place(x=5, y=60)
        self.correo = StringVar()
        self.txtCorreo = Entry(width=70, textvariable=self.correo)
        self.txtCorreo.place(x=65, y=60)
        self.btnAceptar = Button(
            self.ventana, text="Aceptar", command=self.enviar
        ).place(x=365, y=85)
        self.btnLimpiar = Button(
            self.ventana, text="Limpiar", command=self.limpiar
        ).place(x=425, y=85)
        self.ventana.mainloop()

    def enviar(self):
        _thread.start_new_thread(
            self.envio,
            (self.nombre.get(), self.colegio.get(), self.correo.get(),)
        )

    def envio(self, nombre, colegio, correo):
        if (correo == ''):
            messagebox.showinfo("Alerta", "Favor ingrese Un correo valido")
            return
        emisor = "jfgomezf@unah.hn"
        mensaje = MIMEText("Estimado(a) " + nombre +
                           "\n\nReciba un cordial saludo de parte de las " +
                           "autoridades y estudientes de la carrera de " +
                           "ingeniería en sistemas " +
                           "\n\nPara mayor información:\n\n" +
                           "Sitio Web: is.unah.edu.hn \nEncontrara:\n" +
                           "*Información De La Carrera\n" +
                           "*Plan De Estudio\n" +
                           "*Detalle De Procedimientos\n" +
                           "*Información De Contacto\n\n" +
                           "Facebook: fb.com/is.unah.edu.hn")
        mensaje['From'] = emisor
        mensaje['To'] = correo
        mensaje['Subject'] = "Feria Vocacional UNAH-2018 IS"
        serverSMTP = smtplib.SMTP('smtp.live.com', 587)
        self.base.insertar(self.nombre.get(),
                           self.colegio.get(), self.correo.get())
        self.nombre.set("")
        self.colegio.set("")
        self.correo.set("")
        messagebox.showinfo("Gracias", "Gracias Por Visitarnos somos IS")
        serverSMTP.ehlo()
        serverSMTP.starttls()
        serverSMTP.ehlo()
        serverSMTP.login(emisor, "Francisco$13")
        serverSMTP.sendmail(emisor, correo, mensaje.as_string())
        serverSMTP.close()

    def limpiar(self):
        self.nombre.set("")
        self.colegio.set("")
        self.correo.set("")


if __name__ == '__main__':
    y = EnvioMensajes()
