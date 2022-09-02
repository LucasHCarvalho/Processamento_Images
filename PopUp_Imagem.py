import io
import os
from pickletools import optimize
import requests
import PySimpleGUI as sg
from PIL import Image

def abre_imagem(filename):
    try:
        if os.path.exists(filename):
            imagem = Image.open(filename)
        else: 
            imagem = requests.get(filename)
            imagem = Image.open(io.BytesIO(imagem.content))
        
        return imagem
    except:
        sg.popup_ok("Carregar uma imagem")

def mostrar_imagem(imagem, window):
    imagem.thumbnail((500,500))
    bio = io.BytesIO()
    imagem.save(bio, "PNG")
    window["imageKey"].update(data=bio.getvalue(), size=(500,500))

def carrega_imagem(filename, window):
    if os.path.exists(filename):
        imagem = Image.open(filename)
        mostrar_imagem(imagem, window)

def abre_url(url, window):
    imagem = abre_imagem(url)
    mostrar_imagem(imagem, window) 

def salvar_url(url):
    imagem = requests.get(url)
    imagem = Image.open(io.BytesIO(imagem.content))
    imagem.save("daweb.png", format="PNG", optimize=True)

def Cores(imagemEntrada, imagemSaida, quantidade):
    imagem = Image.open(imagemEntrada)
    imagem = imagem.convert("P", palette=Image.Palette.ADAPTIVE, colors=quantidade)
    imagem.save(imagemSaida)

def BlackWhite(imagemEntrada, imagemSaida):
    imagem = Image.open(imagemEntrada)
    imagem = imagem.convert("L")
    imagem.save(imagemSaida)

def calcula_paleta(branco):
    paleta = []
    r, g, b = branco

    for i in range(255):
        newR = r * i // 255
        newG = g * i // 255
        newB = b * i // 255
        paleta.extend((newR, newG, newB))
    return paleta

def converte_sepia(input, output):
    branco = (255, 240, 192)
    paleta = calcula_paleta(branco)

    imagem = Image.open(input)
    imagem = imagem.convert("L")
    imagem.putpalette(paleta)

    sepia = imagem.convert("RGB")

    sepia.save(f"Imagens\{output}")

def escolhe_tema():
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

def main():
    layout = [
        [sg.Menu([
                ['File', 
                    ['Open', 'Open URL', 'Save', 'Exit',]
                ],
                ['Edit', 
                    ['Paste', 
                        ['Special', 'Normal',], 
                    'Undo'],
                ],
                ['Help', 'About...']
                ])
        ],
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
            sg.Input(size = (5,1), key = "heigthSave")
        ]
    ]

    window = sg.Window("Image viewer", layout = layout)

    isScreenOpen = True

    while isScreenOpen: 
        event, value = window.read()
        fileName = ""

        if event == "Open":
            fileName = sg.popup_get_file('Get file')
            carrega_imagem(fileName, window)

        if event == "Open URL":
            fileName = sg.popup_get_text('Get URL')
            try:
                abre_url(fileName,window)
            except:
                    sg.popup_ok("Não é um link valido")

        
        
        """if value["qualityComb"] == "":
            sg.popup_ok("Escolhe a qualidade da imagem")
        elif value["qualityComb"] == "Imagem Original":
                imagem.save("imagem.PNG")
        elif value["qualityComb"] == "Thumnail":
            imagem.save("temp.png", format="PNG", optimize=True, quality=1)
            imagem.thumbnail((75,75))
            imagem.save("imagem.PNG")
        elif value["qualityComb"] == "Qualidade Reduzida":
            if value["widthSave"] == "" or value["heigthSave"] == "":
                sg.popup_ok("Preencha um tamanho")
            else:
                imagem.save("temp.png", format="PNG", optimize=True, quality=1)
                imagem = imagem.resize((int(value["widthSave"]),int(value["heigthSave"])))
                imagem.save("imagem.PNG")
        
        os.remove('temp.png')

        if event == "qualityComb":
            if value["qualityComb"] == "Imagem Original":
                window['widthSave'].update(disabled=True)
                window['heigthSave'].update(disabled=True)
            elif value["qualityComb"] == "Thumnail":
                window['widthSave'].update(disabled=True)
                window['heigthSave'].update(disabled=True)
            elif value["qualityComb"] == "Qualidade Reduzida":  
                window['widthSave'].update(disabled=False)
                window['heigthSave'].update(disabled=False)"""

        if event == "Exit" or event == sg.WINDOW_CLOSED:
            isScreenOpen = False

    window.close()

if __name__ == "__main__":
    main()
