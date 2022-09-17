from PIL import Image
from PIL import ImageFilter

def filter(input_image, output_image):
    image = Image.open(input_image)
    filtered_image = image.filter(ImageFilter.EDGE_ENHANCE)
    filtered_image.save(output_image)

if __name__ == "__main__":
    filter("raiox.jpg", "raiox1.jpg")