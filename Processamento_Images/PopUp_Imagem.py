import io
import os
import PySimpleGUI as sg
from PIL import Image

def main():
    layout = [
        [
            sg.Image(
                key = "imageKey",
                size = (500, 500)
            )
        ],
        [
            sg.Text("Image file"),
            sg.Input(size = (25,1), key = "fileKey"),
            sg.FileBrowse(file_types = [("JPEG (*.jpg)", "*.jpg"), ("All", "*.*")]),
            sg.Button("Load image")
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
            if os.path.exists(fileName):
                image = Image.open(fileName)
                image.thumbnail((500, 500))
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                window["imageKey"].update(data = bio.getvalue(), size = (500,500))
    
    window.close()


if __name__ == "__main__":
    main()