from PIL import Image

def MudaParaCinza(imagemEntrada, imagemSaida):
    imagem = Image.open(imagemEntrada)
    imagem = imagem.convert("L")
    imagem.save(imagemSaida)

if __name__ == "__main__":
    MudaParaCinza("Imagens\house.jpg", "Imagens\houseCinza.jpg")