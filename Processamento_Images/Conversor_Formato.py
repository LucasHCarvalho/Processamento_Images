#python.exe -m pip install --upgrade pip
#python -m pip install --upgrade Pillow

from PIL import Image

#image = Image.open("dog.png")
#image.show("Dog")

def image_converter(input_file, output_file, formatType):
    imagem = Image.open(input_file)
    imagem.save(output_file, format=formatType, optimize=True, quality=1)
    imagem.thumbnail((75,75))
    imagem.save("Imagens/Thumb.png")
    
def image_format(file):
    imagem = Image.open(file)
    print(f"Image format: {imagem.format_description}")

if __name__ == "__main__":
    image_converter("Imagens/house.jpg", "Imagens/housex.png", "png")    
    image_format("Imagens/house.jpg")
    image_format("Imagens/housex.png")
    image_format("Imagens/Thumb.png")