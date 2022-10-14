import os
import PySimpleGUI as sg
from funcoes import *

file_types = [("(PNG (*.png)","*.png"),
              ("(JPEG (*.jpg)","*.jpg"),
              ("All files (*.*)", "*.*")]

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
                     'Style',
                        ['no Style' , 'Sépia', 'Black and White', 'Colors'], 
                     'Filters',
                        ['blur', 'BoxBlur', 'GaussianBlur', 'Contour', 'Detail', 'Edge Enhance', 'Emboss', 'Find Edges', 'Sharpen', 'Smooth'],
                     'Rotate',
                        ['Rotate -90°', 'Rotate 90°', 'Rotate 180°'],
                     'Miror',
                        ['FLIP_LEFT_RIGHT', 'FLIP_TOP_BOTTOM', 'TRANSPOSE'],
                    'Undo'],
                ],
                ['Help', 'About'],
                ['Informations', 
                    ['Infos', 'Geo_Infos']]
                ])
        ],
        [
            sg.Image(key = "imageKey", size = (800, 800))
        ]
    ]

    window = sg.Window("Image viewer", layout = layout)

    isScreenOpen = True

    while isScreenOpen: 
        event, value = window.read()

        try:
            if event == "Open":
                fileName = sg.popup_get_file('Paste a URL or search in the browser', file_types=file_types)
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
            
            if event == "Infos":
               ImageInfos(fileName)

            if event == "Geo_Infos":
                GeoInfo(fileName)
            
            if event == "SBlur":
                filter("Imagens\\temp.png", 'blur', window)

            if event == "BoxBlur":
                filter("Imagens\\temp.png", 'BoxBlur', window)

            if event == "GaussianBlur":
                filter("Imagens\\temp.png", 'GaussianBlur', window)

            if event == "Contour":
                filter("Imagens\\temp.png", 'Contour', window)

            if event == "Find Edges":
                filter("Imagens\\temp.png", 'Find Edges', window)

            if event == "Detail":
                filter("Imagens\\temp.png", 'Detail', window)

            if event == "Edge Enhance":
                filter("Imagens\\temp.png", 'Edge Enhance', window)

            if event == "Emboss":
                filter("Imagens\\temp.png", 'Emboss', window)

            if event == "Sharpen":
                filter("Imagens\\temp.png", 'Sharpen', window)

            if event == "Smooth":
                filter("Imagens\\temp.png", 'Smooth', window)

            if event == "Rotate -90°":
                rotate("Imagens\\temp.png", -90, window)

            if event == "Rotate 90°":
                rotate("Imagens\\temp.png", 90, window)

            if event == "Rotate 180°":
                rotate("Imagens\\temp.png", 180, window)

            if event == "FLIP_LEFT_RIGHT":
                mirror("Imagens\\temp.png", "FLIP_LEFT_RIGHT", window)

            if event == "FLIP_TOP_BOTTOM":
                mirror("Imagens\\temp.png", "FLIP_TOP_BOTTOM", window)

            if event == "TRANSPOSE":
                mirror("Imagens\\temp.png", "TRANSPOSE", window)
                
            if event == "About":
                About()

        except Exception as e:
                sg.popup_error(e)

        if event == "Exit" or event == sg.WINDOW_CLOSED:
            isScreenOpen = False
    
    window.close()
    os.remove('Imagens\\temp.png')

if __name__ == "__main__":
    main()