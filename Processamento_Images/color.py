from PIL import ImageColor

def pegaValorRGBA(color):
    return ImageColor.getcolor(color, "RGBA")

if __name__ == "__main__":
    for color in ImageColor.colormap:
        print(f"{color} = {pegaValorRGBA(color)}")
