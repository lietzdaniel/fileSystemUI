import os
from PIL import Image

path = os.path.join("gui","fileLogos")
for imageB in os.listdir(path):
 
    if imageB[-4:] == ".png":
        image = Image.open(os.path.join(path,imageB))
        width, height = image.size
        paddingWidth = 2

        newImage = Image.new("RGBA", (width + paddingWidth,height),(0,0,0,0))
        newImage.paste(image,(0,0,width,height))
        newImage.save(os.path.join("gui","fileLogos",imageB))