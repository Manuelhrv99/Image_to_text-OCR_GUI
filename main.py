import tkinter as tk
from tkinter import font as tkFont
from PIL import Image, ImageTk
import pyautogui

#Toma un screenshot para usar despues en el programa
myScreenshot = pyautogui.screenshot()
myScreenshot.save(r'C:\Users\mhrv9\Documents\Proyectos con python\Recortes de pantalla\screenshot.png')

# Guarda el rectangualo creado adentro del canvas
images = []

class Customisation:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Menu')
        self.window.attributes('-fullscreen', True)
        self.window.attributes("-alpha", 1)
        self.window.resizable(0,0)
        self.window.config(cursor="crosshair white")

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        #Creacion del canvas
        self.C = tk.Canvas(self.window, height=screen_height, width=screen_width)

        self.C.pack()

        #Poner el screenshot de fondo en el programa
        image = ImageTk.PhotoImage(file="C:/Users/mhrv9/Documents/Proyectos con python/Recortes de pantalla/screenshot.png")
        self.C.create_image(0, 0, image=image, anchor="nw")

        #Dar la transparencia al canvas creando un rectangulo
        self.window.bind(self.create_rectangle(self.C, 0, 0, screen_width, screen_height, fill='black', alpha=0.3))

        #Propiedades del mouse
        exit_button = tk.Button(
            self.window, 
            text="x",
            relief="ridge",
            height=1,
            bd="0",
            bg="#DA0037",
            fg="white",
            width=3,
            cursor="hand1", 
            command=self.window.destroy)
        font_btn = tkFont.Font(family='Helvetica', size=16, weight='bold')
        exit_button['font'] = font_btn

        # Pasar el boton dentro del canvas
        button1_window = self.C.create_window((screen_width / 2), 30, window=exit_button)

        self.x = 0
        self.y = 0

        """self.x2 = 0
        self.y2 = 0"""

        # Evento del click izquierdo
        #self.window.bind("<Button-1>", self.press_mouse)
        self.window.bind("<ButtonPress-1>", self.on_button_press)
        self.window.bind("<B1-Motion>", self.on_move_press)
        self.window.bind("<ButtonRelease-1>", self.on_button_release)
        
        # Muestra la ventana
        self.window.mainloop()

        #Agregar un icono personalizado  
        #self.window.iconbitmap('./assets/pythontutorial.ico')

    def on_button_press(self,event):
        # save mouse start position
        self.start_x = self.C.canvasx(event.x)
        self.start_y = self.C.canvasy(event.y)

        self.rect = self.C.create_rectangle(self.x, self.y, 1, 1, outline='grey')

    def on_move_press(self,event):
        curX = self.C.canvasx(event.x)
        curY = self.C.canvasy(event.y)

        w, h = self.C.winfo_width(), self.C.winfo_height()
        if event.x > 0.9*w:
            self.C.xview_scroll(1, 'units')
        elif event.x < 0.1*w:
            self.C.xview_scroll(-1, 'units')
        if event.y > 0.9*h:
            self.C.yview_scroll(1, 'units')
        elif event.y < 0.1*h:
            self.C.yview_scroll(-1, 'units')

        # expand rectangle as you drag the mouse
        self.C.coords(self.rect, self.start_x, self.start_y, curX, curY)
        self.im2 = self.im.crop((self.start_x, self.start_y, curX, curY))
        self.tk_im2 = ImageTk.PhotoImage(self.im2)

    def on_button_release(self, event):
        self.C.create_image(0,0,anchor="nw",image=self.tk_im2)

    # Evento que ocurre cada que se aprieta el boton izquierdo del mouse
    #def press_mouse(self, event):


    # Crea un rectangulo transparente y lo aplica en el canvas como imagen
    def create_rectangle(self, c, x1, y1, x2, y2, **kwargs):
        alpha = int(kwargs.pop('alpha') * 255)
        fill = kwargs.pop('fill')
        fill = self.window.winfo_rgb(fill) + (alpha,)
        image = Image.new('RGBA', (x2-x1, y2-y1), fill)
        images.append(ImageTk.PhotoImage(image))
        c.create_image(x1, y1, image=images[-1], anchor='nw')


if __name__ == '__main__':
    app = Customisation()  