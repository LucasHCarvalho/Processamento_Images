from email.mime import image
from PIL import Image

def PegaCoresImagem(imagem):
    imagem = Image.open(imagem)
    colors = imagem.getcolors(imagem.size[0]*imagem.size[0])
    for color in colors:
        print(color)

if __name__ == "__main__":
    PegaCoresImagem("Imagens\house.jpg")