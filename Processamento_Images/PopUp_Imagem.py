import io
import os
from io import BytesIO
import urllib.request
import PySimpleGUI as sg
from PIL import Image
from urllib.request import urlopen

def main():
    sg.theme('DarkTeal9')
    
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
            isScreenOpen = False
        else:  
            sg.theme(values['ThemeList'][0])
            if sg.popup_yes_no("Aplicar esse tema?") == "Yes":
                window.close()
                imageViewer()

def imageViewer():    
    layout = [
        [
            sg.Image(key = "imageKey", size = (500, 500))
        ],
        [
            sg.Text("Insira um Caminho para Imagem"),
            sg.Input(size = (25,1), key = "fileKey"),
            sg.FileBrowse(file_types = [("JPEG (*.jpg)", "*.jpg"), ("All", "*.*")]),
            sg.Button("Load image")
        ],
        [
            sg.Text("Salvar Imagem:")
        ],        
        [
            sg.Text("Qualidade"),
            sg.Combo(['Imagem Original', 'Thumnail', 'Qualidade Reduzida'], key = "qualityComb", enable_events = True),
            sg.Text("Tamanho: "),
            sg.Input(size = (5,1), key = "widthSave"),
            sg.Input(size = (5,1), key = "heigthSave"),
            sg.Button("Salvar")
        ]
    ]

    window = sg.Window("Image viewer", layout = layout)

    isScreenOpen = True

    while isScreenOpen: 
        event, value = window.read()

        if event == "Exit" or event == sg.WINDOW_CLOSED:
            isScreenOpen = False

        if event == "Load image":
            fileName = value["fileKey"]
            if fileName == "":
                sg.popup_ok("Preencha um caminho")
            elif os.path.exists(fileName):
                url = 'https://cdn.wccftech.com/wp-content/uploads/2017/11/windows-10-iphone-1480x897-86x60.png'
                with urllib.request.urlopen(url) as i:
                    byteImg = io.BytesIO(i.read())
                    image = Image.open(byteImg)
                    image.save('out.png')
                image.thumbnail((500, 500))
                bio = io.BytesIO()
                image.save(bio, format="JPEG")
                window["imageKey"].update(data = bio.getvalue(), size = (500,500))

        if event == "Salvar":
            fileName = value["fileKey"]
            if fileName == "":
                sg.popup_ok("Preencha um caminho")
            elif value["qualityComb"] == "":
                sg.popup_ok("Escolhe a qualidade da imagem")
            elif value["qualityComb"] == "Imagem Original":
                if value["widthSave"] == "" or value["heigthSave"] == "":
                    sg.popup_ok("Preencha um tamanho")
                else:
                    imagem = Image.open(fileName)
                    imagem.save("imagem.jpg")
            elif value["qualityComb"] == "Thumnail":
                imagem = Image.open(fileName)
                imagem.save(fileName, format="jpg", optimize=True, quality=1)
                imagem.thumbnail((75,75))
                imagem.save("imagem.jpg")
            elif value["qualityComb"] == "Qualidade Reduzida":
                if value["widthSave"] == "" or value["heigthSave"] == "":
                    sg.popup_ok("Preencha um tamanho")
                else:
                    imagem = Image.open(fileName)
                    imagem.save(fileName, format="jpg", optimize=True, quality=1)
                    imagem = imagem.resize((int(value["widthSave"]),int(value["heigthSave"])))
                    imagem.save("imagem.jpg")
            

        if event == "qualityComb":
            if value["qualityComb"] == "Imagem Original":
                window['widthSave'].update(disabled=True)
                window['heigthSave'].update(disabled=True)
            elif value["qualityComb"] == "Thumnail":
                window['widthSave'].update(disabled=True)
                window['heigthSave'].update(disabled=True)
            elif value["qualityComb"] == "Qualidade Reduzida":  
                window['widthSave'].update(disabled=False)
                window['heigthSave'].update(disabled=False)
    window.close()

if __name__ == "__main__":
    main()
