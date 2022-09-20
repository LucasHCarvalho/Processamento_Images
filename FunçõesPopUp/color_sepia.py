from PIL import Image

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

if __name__ == "__main__":
    converte_sepia("Imagens\house.jpg", "house_sepia.jpg")