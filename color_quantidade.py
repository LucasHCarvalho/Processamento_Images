from PIL import Image

def MudaParaCinza(imagemEntrada, imagemSaida):
    imagem = Image.open(imagemEntrada)
    imagem = imagem.convert("P", palette=Image.Palette.ADAPTIVE, colors=0)
    imagem.save(imagemSaida)

if __name__ == "__main__":
    MudaParaCinza("Imagens\house.jpg", "Imagens\houseCores.png")