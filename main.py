import tkinter as tk
from tkinter import font as tkFont
from PIL import Image, ImageTk, ImageEnhance
import pyscreenshot as ImageGrab
import sys
import pyautogui # Importante no borrar esta linea, hace que se vean bien los recortes

import os
import cv2
import pytesseract as tesseract

tesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Cosas por hacer por
# Usar inteligencia artificial para reescalar la imagen
# Crear un comando de teclado para abrir el programa
# Investigar como abrir el programa en todos los monitores

# Guarda el rectangualo creado adentro del canvas
images = []

class Customisation:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Menu')
        self.window.attributes('-fullscreen', True)
        self.window.attributes("-alpha", 0.2) # Cambia la opasidad de la ventana en general, cambia el brillo del recorte final
        self.window.resizable(0,0)
        self.window.config(cursor="crosshair white")

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # Creacion del canvas
        self.C = tk.Canvas(self.window, height=screen_height, width=screen_width)

        self.C.pack()

        # Dar la transparencia al canvas creando un rectangulo
        self.window.bind(self.create_rectangle(self.C, 0, 0, screen_width, screen_height, fill='black', alpha=0)) # El alpha cambia la opasidad del rectangulo

        # Propiedades del mouse
        exit_button = tk.Button(
            self.window, 
            text="x",
            relief="ridge",
            height=1,
            bd="0",
            bg="black",
            fg="white",
            width=3,
            cursor="hand1", 
            command=self.window.destroy)
        font_btn = tkFont.Font(family='Helvetica', size=20, weight='bold')
        exit_button['font'] = font_btn
        exit_button.place(x = (screen_width/2), y = 0)

        # Evento del click izquierdo
        self.window.bind("<ButtonPress-1>", self.on_button_press)
        self.window.bind("<B1-Motion>", self.on_move_press)
        self.window.bind("<ButtonRelease-1>", self.on_button_release)
        
        # Muestra la ventana
        self.window.mainloop()

        # Agregar un icono personalizado  
        #self.window.iconbitmap('./assets/pythontutorial.ico')

    def on_button_press(self,event):
        # Posicion inicial del mouse
        self.start_x = self.C.canvasx(event.x)
        self.start_y = self.C.canvasy(event.y)

        self.rect = self.C.create_rectangle(0, 0, 1, 1, outline='blue', fill='black')

    def on_move_press(self,event):
        self.curX = self.C.canvasx(event.x)
        self.curY = self.C.canvasy(event.y)

        # Crear el rectangulo mientras se arrastra el mouse
        self.C.coords(self.rect, self.start_x, self.start_y, self.curX, self.curY)

    def on_button_release(self, event):
        # Convertir todas las coordenadas a int
        first_x = int(self.start_x)
        first_y = int(self.start_y)
        final_x = int(self.curX)
        final_y = int(self.curY)

        try:
            # Validacion para ordenar las coordenadas

            # ↘↘↘↘↘ De arriba a la izquierda para abajo a la derecha
            if first_x < final_x and first_y < final_y:
                im = ImageGrab.grab(bbox=(first_x, first_y, final_x, final_y))
            # ↙↙↙↙↙ De arriba a la derecha a abajo a la izquierda
            elif first_x > final_x and first_y < final_y:
                im = ImageGrab.grab(bbox=(final_x, first_y, first_x, final_y))
            # ↗↗↗↗↗ De abajo a la izquierda a arriba a la derecha
            elif first_x < final_x and first_y > final_y: 
                im = ImageGrab.grab(bbox=(first_x, final_y, final_x, first_y))
            # ↖↖↖↖↖ De abajo a la derecha a arriba a la izquierda
            else:
                im = ImageGrab.grab(bbox=(final_x, final_y, first_x, first_y))
                
            # Abre la imagen
            #im.show()

            # Guardar la imagen
            im.save('crop.png')

            big_im = self.modify_image(im)
            big_im.show()

                                                                    #psm 4 o 1 para pruebas
            imageToText = tesseract.image_to_string(big_im, config="--oem 1 --psm 4")            

            txtFile = open('ML_Text.txt', 'w')
            txtFile.write(imageToText + '\n')
            txtFile.close()

            # Abre el bloc de notas
            os.startfile('ML_Text.txt')

            # Cierra el programa despues de hacer un recorte
            sys.exit()
        except:
            # Cierra el programa despues de hacer un recorte
            sys.exit()

    # Crea un rectangulo transparente y lo aplica en el canvas como imagen
    def create_rectangle(self, c, x1, y1, x2, y2, **kwargs):
        alpha = int(kwargs.pop('alpha') * 255)
        fill = kwargs.pop('fill')
        fill = self.window.winfo_rgb(fill) + (alpha,)
        image = Image.new('RGBA', (x2-x1, y2-y1), fill)
        images.append(ImageTk.PhotoImage(image))
        c.create_image(x1, y1, image=images[-1], anchor='nw')

    # Cambiar el tamaño y contraste de la imagen
    def modify_image(self, im):
        # Cambiar el tamaño de la imagen a 2x
        w, h = im.size
        w = int(w * 2)
        h = int(h * 2)
        big_im = im.resize((w, h))
        #im_copy.show()
        big_im.save('big_crop.png')

        # Contraste
        contrast = ImageEnhance.Contrast(big_im)
        contrast_image = contrast.enhance(4).copy()
        contrast_image.save('contrast_image.png')

        # Blanco y negro
        greyscale = contrast_image.convert('L')
        greyscale_image = greyscale.copy()
        greyscale_image.save('greyscale_image.png')

        # Color
        # color = ImageEnhance.Color(im_copy)
        # color.enhance(1.5).save('color.png')

        # Brillo
        # brightness = ImageEnhance.Brightness(im_copy)
        # brightness.enhance(1.5).save('brightness.jpg')

        # Nitidez
        sharpness = ImageEnhance.Sharpness(greyscale_image)
        final_image = sharpness.enhance(2).copy()
        final_image.save('sharpness_image.jpg')

        return final_image


if __name__ == '__main__':
    app = Customisation()