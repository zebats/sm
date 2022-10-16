from PIL import Image, ImageGrab
import base64,os
from pyperclip import copy

im = ImageGrab.grabclipboard()
if isinstance(im, Image.Image):
    im.save( r".\deleteMe.jpg")
    image_path = r'.\deleteMe.jpg'
    with open(image_path, 'rb') as f:
        image = f.read()
        image_base64 = str(base64.b64encode(image), encoding='utf-8')
        s='<BR><img class="imgCloze" style="BACKGROUND-IMAGE: url(data:image/jpeg;base64,'+image_base64+f'); BACKGROUND-REPEAT: no-repeat" width={im.width} height={im.height}><BR>'
        print(s)
        copy(s)
    os.remove('deleteMe.jpg')
