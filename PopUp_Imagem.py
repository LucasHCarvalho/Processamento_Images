import io
import os
from pickletools import optimize
import requests
import PySimpleGUI as sg
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from pathlib import Path

file_types = [("(JPEG (*.jpg)","*.jpg"),
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

def get_exif_data(path):
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

def ImageInfos(filename):
    layout = []

    image_path = Path(filename)
    exif_data = get_exif_data(image_path.absolute())

    for ifield, field in enumerate(fields):
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
    imagem.thumbnail((500,500))
    bio = io.BytesIO()
    imagem.save(bio, "PNG")
    imagem.save("Imagens\\temp.png", format="PNG")
    window["imageKey"].update(data=bio.getvalue(), size=(500,500))

def LoadImage(filename, window):
    imagem = OpenImage(filename)
    mostrar_imagem(imagem, window)

def SaveThumbnail(filename):
    imagem = OpenImage(filename)
    imagem.thumbnail((75,75))
    imagem.save('Imagens\\thumbnail.png', format="PNG", optimize=True)

def SaveLowQuality(filename, qualidade):
    imagem = OpenImage(filename)
    imagem.save("Imagens\\baixa_qualidade.jpg", format="JPEG", optimize=True, quality=int(qualidade))

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
    sg.PopupOK('Lorem ipsum dolor sit amet, consectetur adipiscing elit. \n' 
    'Praesent mollis sem sed nunc dictum gravida. Proin elementum pellentesque dui, eget mollis est egestas ut. \n'
    'Ut at urna quam. Sed in tellus massa. Nulla magna nulla, sodales id efficitur sit amet, fermentum eu nisl. \n'
    'Aliquam lacinia nunc eget risus rhoncus malesuada. Donec ornare felis nec sapien pellentesque, in vestibulum velit efficitur. \n'
    'Morbi consectetur pellentesque tortor ut viverra. \n'
    'Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos.')

def main():
    layout = [
        [sg.Menu([
                ['File', 
                    ['Open',
                     'Save',
                        ['Normal', 'Thumnail', 'Low Quality'],
                     'Exit',]
                ],
                ['Edit', 
                    ['Theme', 
                     'Filter',
                        ['no filter' , 'Sépia', 'Black and White', 'Colors'], 
                    'Undo'],
                ],
                ['Help', 'About'],
                ['Infos', 'infos']
                ])
        ],
        [
            sg.Image(key = "imageKey", size = (500, 500))
        ]
    ]

    window = sg.Window("Image viewer", layout = layout)

    isScreenOpen = True

    while isScreenOpen: 
        event, value = window.read()

        try:
            if event == "Open":
                fileName = sg.popup_get_file('Paste a URL or search in the browser')
                LoadImage(fileName, window)
            
            if event == "Theme":
                SetTheme(window, ChoiceTheme())

            if event == "no filter":           
                    LoadImage(fileName, window)

            if event == "Sépia":          
                    ConvertSepia("Imagens\\temp.png", window)

            if event == "Black and White":
                    BlackWhite("Imagens\\temp.png", window)
            
            if event == "Colors":
                    QtdColor = sg.popup_get_text('Set number of colors to filter your image')
                    Colors("Imagens\\temp.png", window, int(QtdColor))
                
            if event == "Normal":
                    imagem = OpenImage("Imagens\\temp.png")
                    imagem.save("Imagens\imagem.PNG")
            
            if event == "Thumnail":
                    SaveThumbnail("Imagens\\temp.png")
            
            if event == "Low Quality":
                quality = sg.popup_get_text('Select image quality')
                SaveLowQuality("Imagens\\temp.png", quality)     
            
            if event == "infos":
                ImageInfos(fileName)
        except Exception as e:
                sg.popup_error(e)

        if event == "About":
            About()

        if event == "Exit" or event == sg.WINDOW_CLOSED:
            isScreenOpen = False
    
    window.close()
    os.remove('Imagens\\temp.png')

if __name__ == "__main__":
    main()
