import os
import time
from tkinter import filedialog as fd
from tkinter import ttk
from pygame import mixer
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
import _thread
from tkinter import *


class Reproductor:
    def __init__(self):
        self.ventana = Tk()
        self.ventana.geometry("500x300")
        self.ventana.title("Reproductor")
        self.ventana.resizable(0, 0)
        self.titulo = StringVar(self.ventana)
        self.duracion = StringVar(self.ventana)
        self.transcurrio = StringVar(self.ventana)
        self.colocarElementos()
        self.propiedades()
        self.listaCanciones = list()
        self.reproductor = mixer
        self.reproductor.init(44100, -16, 2, 2048)
        self.ventana.mainloop()

    def propiedades(self):
        self.ruta = "c:/"
        self.tabla.column("#0", width=398)
        self.tabla.heading("#0", text='PlayList')
        self.sldVolumen.set(50)
        self.sldDuracion.bind("<ButtonRelease-1>", self.buscar)
        self.volumen = 0.5
        self.pausa = False
        self.detenido = False
        self.index = 0

    def colocarElementos(self):
        self.lblTranscurrido = Label(
            self.ventana, textvariable=self.transcurrio
        ).place(x=0, y=20, width=50)
        self.lblduracion = Label(self.ventana, textvariable=self.duracion
                                 ).place(x=450, y=20, width=50)
        self.btnAbrirCancion = Button(
            self.ventana, text="Abrir", command=self.abrirCancion
        ).place(x=130, y=270)
        self.btnAbrirCarpeta = Button(
            self.ventana, text="Carp", command=self.abrirCarpeta
        ).place(x=170, y=270)
        self.btnPrev = Button(
            self.ventana, text="Prev", command=self.anterior
        ).place(x=210, y=270)
        self.btnPlay_Pause = Button(
            self.ventana, text="Play", command=self.reproducir
        ).place(x=250, y=270)
        self.btnStop = Button(
            self.ventana, text="Stop", command=self.detener
        ).place(x=290, y=270)
        self.btnNext = Button(
            self.ventana, text="Next", command=self.siguiente
        ).place(x=330, y=270)
        self.sldVolumen = Scale(self.ventana, from_=100,
                                to=0, command=self.setVolumen)
        self.sldVolumen.place(x=450, y=50)
        self.sldDuracion = Scale(self.ventana, orient=HORIZONTAL, length=390)
        self.sldDuracion.place(x=50, y=0)
        self.lblTitulo = Label(self.ventana, textvariable=self.titulo).place(
            x=0, y=0, width=500)
        self.tabla = ttk.Treeview(self.ventana)
        self.tabla.place(x=0, y=50, width=400, height=200)

    def abrirCancion(self):
        archivos = fd.askopenfilenames(
            filetypes={("all files", "*.*"), ("Archivo mp3", "*.mp3")},
            initialdir=self.ruta)
        for cancion in archivos:
            if self.reproductor.music.get_busy() == 0:
                self.listaCanciones.append(cancion)
                self.cargarCancion()
                _thread.start_new_thread(self.cambiar, ())
            else:
                self.listaCanciones.append(cancion)
            self.ruta = os.path.dirname(cancion)
            self.tabla.insert('', END, text=os.path.basename(
                cancion), iid=(len(self.listaCanciones) - 1))

    def abrirCarpeta(self):
        carpeta = fd.askdirectory()
        for archivo in os.listdir(carpeta):
            if archivo.endswith(".mp3"):
                if self.reproductor.music.get_busy() == 0:
                    self.listaCanciones.append(carpeta + "/" + archivo)
                    self.cargarCancion()
                    _thread.start_new_thread(self.cambiar, ())
                else:
                    self.listaCanciones.append(carpeta + "/" + archivo)

    def siguiente(self):
        self.index += 1
        if self.index < len(self.listaCanciones):
            self.cargarCancion()
        else:
            self.index = 0
            self.cargarCancion()

    def anterior(self):
        self.index -= 1
        if self.index >= 0:
            self.cargarCancion()
        else:
            self.index = len(self.listaCanciones) - 1
            self.cargarCancion()

    def detener(self):
        self.reproductor.music.stop()
        self.pausa = False
        self.detenido = True

    def reproducir(self):
        if self.reproductor.music.get_busy() == 0:
            try:
                self.reproductor.music.play()
                self.reproductor.music.play()
            except Exception:
                pass
        else:
            if not self.pausa:
                self.reproductor.music.pause()
                self.pausa = True
            else:
                self.reproductor.music.unpause()
                self.pausa = False
                self.actualizarTiempo()
                self.buscar(None)

    def cambiar(self):
        while True:
            if not self.detenido:
                if self.reproductor.music.get_busy() == 0:
                    self.index += 1
                    if self.index < len(self.listaCanciones):
                        self.cargarCancion()
                    else:
                        self.sldDuracion.set(0)
                        self.detenido = True
                else:
                    time.sleep(1)
                    self.actualizarTiempo()

    def cargarCancion(self):
        self.reproductor.quit()
        self.reproductor.init(
            MP3(self.listaCanciones[self.index]).info.sample_rate, 16, 2, 2048)
        self.reproductor.music.load(self.listaCanciones[self.index])
        self.calcularTiempo()
        try:
            audio = ID3(self.listaCanciones[self.index])
            self.ventana.title(str(audio['TPE1']) + " - " + str(audio['TIT2']))
            self.titulo.set(str(audio['TPE1']) + " - " + str(audio['TIT2']))
        except Exception as e:
            self.ventana.title(os.path.basename(
                self.listaCanciones[self.index]))
            self.titulo.set(os.path.basename(self.listaCanciones[self.index]))
        self.reproductor.music.set_volume(self.volumen)
        self.reproductor.music.play()
        self.detenido = False

    def actualizarTiempo(self):
        if not self.pausa:
            self.sldDuracion.set(self.sldDuracion.get() + 1)
            self.transcurrio.set(self.formatoTiempo(self.sldDuracion.get()))

    def calcularTiempo(self):
        tiempoTotal = MP3(self.listaCanciones[self.index]).info.length
        self.sldDuracion.config(from_=0, to=tiempoTotal)
        self.sldDuracion.set(0)
        self.transcurrio.set("00:00")
        self.duracion.set(self.formatoTiempo(tiempoTotal))

    def formatoTiempo(self, tiempoTotal):
        horas = 0
        segundos = int(tiempoTotal % 60)
        tiempoTotal -= segundos
        minutos = int(tiempoTotal / 60)
        while minutos > 60:
            horas += 1
            minutos -= 60
        if not horas == 0:
            if minutos >= 10:
                return str(horas) + ":" + str(minutos) + ":" + str(segundos)
            else:
                return str(horas) + ":0" + str(minutos) + ":" + str(segundos)
        else:
            if minutos >= 10:
                if segundos >= 10:
                    return str(minutos) + ":" + str(segundos)
                else:
                    return str(minutos) + ":0" + str(segundos)
            else:
                if segundos >= 10:
                    return "0" + str(minutos) + ":" + str(segundos)
                else:
                    return "0" + str(minutos) + ":0" + str(segundos)

    def buscar(self, Event):
        self.sldDuracion.set(self.sldDuracion.get() - 2)
        self.reproductor.music.rewind()
        self.actualizarTiempo()
        self.reproductor.music.set_pos(self.sldDuracion.get() - 1)

    def setVolumen(self, Event):
        self.volumen = int(self.sldVolumen.get()) * 0.01
        self.reproductor.music.set_volume(self.volumen)


if __name__ == '__main__':
    rep = Reproductor()
