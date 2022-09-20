from PIL import Image
from PIL import ImageColor

def cria_imagem(filename, size):
    image = Image.new("RGBA", size)

    cor1 = ImageColor.getcolor("red", "RGBA")
    cor2 = ImageColor.getcolor("blue", "RGBA")
    cor = cor1

    count = 0

    for y in range(size[1]):
        for x in range(size[0]):
            if count == 5:
                cor = cor1 if cor2 == cor else cor2
                count = 0
            image.putpixel((x,y), cor)
            count += 1
    
    image.save(f"Imagens\{filename}")

if __name__ == "__main__":
    cria_imagem("imagem.png", (100,100))
