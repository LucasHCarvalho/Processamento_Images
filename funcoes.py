import io
import os
import sys
import folium
import requests
import webbrowser
import PySimpleGUI as sg
from PIL import ImageFilter, Image, ImageEnhance
from PIL.ExifTags import TAGS, GPSTAGS
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView # pip install PyQtWebEngine
from datetime import datetime, date

file_types = [("(PNG (*.png)","*.png"),
              ("(JPEG (*.jpg)","*.jpg"),
              ("All files (*.*)", "*.*")]

fields = {
    "File name" : "File name",
    "File size" : "File size",
    "Model" : "Camera Model",
    "ExifImageWidth" : "Width",
    "ExifImageHeight" : "Height",
    "DateTime" : "Creating Date",
    "static_line" : "*",
    "MaxApertureValue" : "Aperture",
    "ExposureTime" : "Exposure",
    "FNumber" : "F-Stop",
    "Flash" : "Flash",
    "FocalLength" : "Focal Length",
    "ISOSpeedRatings" : "ISO",
    "ShutterSpeedValue" : "Shutter Speed"
}

filtros = {
        'blur': ImageFilter.BLUR,
        'BoxBlur': ImageFilter.BoxBlur(radius=9),
        'GaussianBlur': ImageFilter.GaussianBlur,
        'Contour': ImageFilter.CONTOUR,
        'Detail': ImageFilter.DETAIL,
        'Edge Enhance': ImageFilter.EDGE_ENHANCE,
        'Emboss': ImageFilter.EMBOSS,
        'Find Edges': ImageFilter.FIND_EDGES,
        'Sharpen': ImageFilter.SHARPEN,
        'Smooth': ImageFilter.SMOOTH
    }

mirror_options = {
        "FLIP_LEFT_RIGHT": Image.Transpose.FLIP_LEFT_RIGHT,
        "FLIP_TOP_BOTTOM": Image.Transpose.FLIP_TOP_BOTTOM,
        "TRANSPOSE": Image.Transpose.TRANSPOSE
    }


def Time():
    now = datetime.now()
    current_time = now.strftime("%H-%M")
    return "-" + date.today() + "-" + current_time

"""
    Padrão para carregar, abrir e mostrar na tela
"""
def OpenImage(filename): 
    try:
        if os.path.exists(filename):
            imagem = Image.open(filename)
        else: 
            imagem = requests.get(filename)
            imagem = Image.open(io.BytesIO(imagem.content))
        
        return imagem
    except:
        sg.popup_ok("Fill a path")
    
def mostrar_imagem(imagem, window):
    imagem.save("Imagens\\temp.png", format="PNG")
    imagem.thumbnail((800,800))
    bio = io.BytesIO()
    imagem.save(bio, "PNG")
    window["imageKey"].erase()
    window["imageKey"].draw_image(data=bio.getvalue(), location=(0,800))

def LoadImage(filename, window):
    imagem = OpenImage(filename)
    mostrar_imagem(imagem, window)
    
"""
    Formas de Salvar
"""
def SaveThumbnail(filename):
    imagem = OpenImage(filename)
    imagem.thumbnail((75,75))
    imagem.save(f'Imagens\\thumbnail.png{Time()}', format="PNG", optimize=True)

def SaveLowQuality(filename, qualidade):
    imagem = OpenImage(filename)
    imagem.save(f"Imagens\\baixa_qualidade{Time()}.png", format="PNG", optimize=True, quality=int(qualidade))

"""
    Filtros
"""
def Colors(input, window, quantidade):
    imagem = OpenImage(input)
    imagem = imagem.convert("P", palette=Image.Palette.ADAPTIVE, colors=quantidade)
    mostrar_imagem(imagem, window) 

def BlackWhite(input, window):
    imagem = OpenImage(input)
    imagem = imagem.convert("L")
    mostrar_imagem(imagem, window) 

def CalculatePalette(branco):
    paleta = []
    r, g, b = branco

    for i in range(255):
        newR = r * i // 255
        newG = g * i // 255
        newB = b * i // 255
        paleta.extend((newR, newG, newB))
    return paleta

def ConvertSepia(input, window):
    branco = (255, 240, 192)
    paleta = CalculatePalette(branco)

    imagem = OpenImage(input)
    imagem = imagem.convert("L")
    imagem.putpalette(paleta)

    sepia = imagem.convert("RGB")

    mostrar_imagem(sepia, window) 

def filter(imagem,filter,window):
        imagem = OpenImage(imagem)
        filtered_image = imagem.filter(filtros[filter])
        mostrar_imagem(filtered_image, window) 

"""
    Efeitos
"""
def brilho(imagem, fator, window):
    imagem = OpenImage(imagem)
    imagem.convert("RGB")
    enhancer = ImageEnhance.Brightness(imagem)
    edit_image = enhancer.enhance(fator)
    mostrar_imagem(edit_image, window) 

def contraste(imagem, fator, window):
    imagem = OpenImage(imagem)
    imagem = imagem.convert("RGB")
    enhancer = ImageEnhance.Contrast(imagem)
    edit_image = enhancer.enhance(fator)
    mostrar_imagem(edit_image, window) 

def cores(imagem, fator, window):
    imagem = OpenImage(imagem)
    imagem = imagem.convert("RGB")
    enhancer = ImageEnhance.Color(imagem)
    edit_image = enhancer.enhance(fator)
    mostrar_imagem(edit_image, window) 

def nitidez(imagem, fator, window):
    imagem = OpenImage(imagem)
    imagem = imagem.convert("RGB")
    enhancer = ImageEnhance.Sharpness(imagem)
    edit_image = enhancer.enhance(fator)
    mostrar_imagem(edit_image, window) 

"""
    Edições
"""
def rotate(image_path, degrees_to_rotate, window):
    image_obj = OpenImage(image_path)
    rotated_image = image_obj.rotate(degrees_to_rotate)
    mostrar_imagem(rotated_image, window) 

def mirror(image_path, mirrors, window):
    image = OpenImage(image_path)
    mirror_image = image.transpose(mirror_options[mirrors]) #FLIP_LEFT_RIGHT, FLIP_TOP_BOTTOM, TRANSPOSE
    mostrar_imagem(mirror_image, window) 

"""
    Localização mapa
"""
class MyApp(QWidget):
    def __init__(self, fileName):
        super().__init__()
        self.setWindowTitle('Localização')
        self.window_width, self.window_height = 600, 400
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QVBoxLayout()
        self.setLayout(layout)

        coordinate = GeoInfo(fileName)
        m = folium.Map(
        	location=coordinate
        )

        tooltip = "Location"

        folium.Marker(
            coordinate, tooltip=tooltip
        ).add_to(m)

        # save map data to data object
        data = io.BytesIO()
        m.save(data, close_file=False)

        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        layout.addWidget(webView)

def MapWindow(fileName):
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 35px;
        }
    ''')
    
    myApp = MyApp(fileName)
    myApp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')

def GetExifData(path):
    exif_data = {}
    try:
        image = Image.open(path)
        info = image._getexif()
    except OSError:
        info = {}

    #Se nÃ£o encontrar o arquivo
    if info is None:
        info = {}
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        if decoded == "GPSInfo":
            gps_data = {}
            for gps_tag in value:
                sub_decoded = GPSTAGS.get(gps_tag, gps_tag)
                gps_data[sub_decoded] = value[gps_tag]
            exif_data[decoded] = gps_data
        else:
            exif_data[decoded] = value

    return exif_data

def GeoInfo(filename):
    exif_data = {}
    try:
        image = Image.open(filename)
        info = image._getexif()
    except OSError:
        info = {}

    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for gps_tag in value:
                    sub_decoded = GPSTAGS.get(gps_tag, gps_tag)
                    gps_data[sub_decoded] = value[gps_tag]
                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value

    north = exif_data["GPSInfo"]["GPSLatitude"]
    east = exif_data["GPSInfo"]["GPSLongitude"]

    latitude = float(((north[0] * 60 + north[1]) * 60 + north[2]) / 3600)
    longitude = float(((east[0] * 60 + east[1]) * 60 + east[2]) / 3600)
    if sg.popup_yes_no(f'http://maps.google.com/maps?q={latitude}, -{longitude}') == "Yes":
        #return latitude, -longitude
        webbrowser.open(f'http://maps.google.com/maps?q={latitude}, -{longitude}')

"""
    Informações da Imagem
"""
def ImageInfos(filename):
    layout = []

    image_path = Path(filename)
    exif_data = GetExifData(image_path.absolute())

    for field in fields:
        if field == "File name":
            layout.append([sg.Text(fields[field], size=(10,1)), sg.Text(image_path.name, size=(25,1))])
        elif field == "File size":
            layout.append([sg.Text(fields[field], size=(10,1)), sg.Text(image_path.stat().st_size, size=(25,1))])
        else:
            layout.append([sg.Text(fields[field], size=(10,1)), sg.Text((exif_data.get(field, "No data")), size=(25,1))])

    window = sg.Window("Image information", layout)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break     


def ChoiceTheme():    
    layout = [
        [
            sg.Text('Escolha o tema da tela')
        ],
        [
            sg.Listbox(values = sg.theme_list(),
                        size =(50, 12),
                        key ='ThemeList',
                        enable_events = True)
        ],
        [
            sg.Button('Exit')
        ]
    ]
    
    window = sg.Window('Lista de Temas', layout)

    isScreenOpen = True
    
    # This is an Event Loop
    while isScreenOpen:  
        event, values = window.read()
        
        if event == "Exit" or event == sg.WINDOW_CLOSED:
            window.close()
        else:  
            sg.theme(values['ThemeList'][0])
            if sg.popup_yes_no("Aplicar esse tema?") == "Yes":
                window.close()
                return values['ThemeList'][0]

def SetTheme(window, new_theme):
    global CURRENT_THEME
    CURRENT_THEME = new_theme
    sg.theme(new_theme)
    window.TKroot.config(background=sg.theme_background_color())
    for element in window.element_list():
        element.Widget.config(background=sg.theme_background_color())
        element.ParentRowFrame.config(background=sg.theme_background_color())
        if 'text' in str(type(element)).lower():
            element.Widget.config(foreground=sg.theme_text_color())
            element.Widget.config(background=sg.theme_text_element_background_color())
        if 'input' in str(type(element)).lower():
            element.Widget.config(foreground=sg.theme_input_text_color())
            element.Widget.config(background=sg.theme_input_background_color())
        if 'progress' in str(type(element)).lower():
            element.Widget.config(foreground=sg.theme_progress_bar_color()[0])
            element.Widget.config(background=sg.theme_progress_bar_color()[1])
        if 'slider' in str(type(element)).lower():
            element.Widget.config(foreground=sg.theme_slider_color())
        if 'button' in str(type(element)).lower():
            element.Widget.config(foreground=sg.theme_button_color()[0])
            element.Widget.config(background=sg.theme_button_color()[1])
    window.Refresh()

def About():
    sg.PopupOK('***Oláa***\n'
    'Trabalho desenvolvido no curso de Ciência da Computação na disciplina de Processamento de Imagens, lecionado pelo professor Thiago Quintas.\n'
    'O projeto busca com auxilio de algumas funções mostar funções e meios para tratar imagens.\n'
    'o projeto foi desenvolvido em Python por: Lucas Henrique de Carvalho Pinto\n'
    'O código do projeto se encontra em: https://github.com/LucasHCarvalho/Processamento_Images')
