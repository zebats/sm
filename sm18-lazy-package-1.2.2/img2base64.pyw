from PIL import Image, ImageGrab
import base64,os
from pyperclip import copy
import time

im = ImageGrab.grabclipboard()
if isinstance(im, Image.Image):
    width, height = im.size
    if width > 800:
        im = im.resize((800, int(800 * height / width)))
    width, height = im.size
    if height > 250:
        im = im.resize((int(250 * width / height), 250))
    im.save( r".\deleteMe.jpg")
    image_path = r'.\deleteMe.jpg'
    with open(image_path, 'rb') as f:
        image = f.read()
        image_base64 = str(base64.b64encode(image), encoding='utf-8')
        s='<BR><img class="imgCloze" style="BACKGROUND-IMAGE: url(data:image/jpeg;base64,'+image_base64+f'); BACKGROUND-REPEAT: no-repeat" width={im.width} height={im.height}><SPAN style="display:none">{str(time.time())}</SPAN><BR>'
        print(s)
        copy(s)
    os.remove('deleteMe.jpg')
