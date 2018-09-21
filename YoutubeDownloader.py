import youtube_dl
from tkinter import *
from tkinter import filedialog as fd
import _thread


class YoutubeDownloader(object):
    def __init__(self):
        self.ventana = Tk()
        self.ventana.geometry("500x100")
        self.ventana.title("YoutubeDownloader")
        self.ventana.resizable(0, 0)
        self.lblUrl = Label(text="Enlace").place(x=5, y=10)
        self.u = StringVar()
        self.url = Entry(width=70, textvariable=self.u)
        # self.url.bind("<Button-3><ButtonRelease-3>", self.descargarMp3)
        self.url.place(x=55, y=10)
        self.lblRuta = Label(text="Ruta").place(x=5, y=35)
        self.r = StringVar()
        self.ruta = Entry(width=70, textvariable=self.r)
        self.ruta.place(x=55, y=35)
        self.btnDescargar = Button(
            self.ventana, text="Descargar", command=self.descargar
        ).place(x=415, y=60)
        self.btnCarpeta = Button(
            self.ventana, text="Ruta", command=self.seleccionarCarpeta
        ).place(x=370, y=60)
        self.selec = BooleanVar()
        self.mp3 = Checkbutton(text="MP3", variable=self.selec)
        self.mp3.place(x=300, y=60)
        self.ventana.mainloop()

    def descargar(self):
        if not self.selec.get():
            _thread.start_new_thread(self.youtube, (self.u.get(),))
        else:
            _thread.start_new_thread(self.descargarMp3, (self.u.get(),))

    def descargarMp3(self, url):
        ydl_opts = {
            'outtmpl': 'C:/Users/Fran Gomez/Desktop/%(title)s.%(ext)s',
            'format': 'bestaudio',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    def youtube(self, url):
        ydl_opts = {
            'outtmpl': self.r.get() + '%(title)s.%(ext)s',
            'format': '133+140'
        }
        with youtube_dl.YoutubeDL() as ydl:
            info = ydl.extract_info(url, download=False)
            formatos = info['formats']
            for elemento in formatos:
                if elemento['ext'] == 'mp4':
                    print(elemento['format'])

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    def facebook(self, url):
        pass

    def seleccionarCarpeta(self):
        self.r.set(fd.askdirectory() + "/")


if __name__ == '__main__':
    y = YoutubeDownloader()
