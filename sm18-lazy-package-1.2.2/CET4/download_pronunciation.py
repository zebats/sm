import json
import re
import os
import urllib.request

with open('dic.txt','r') as f:
    dic=json.loads(f.read())

for word in dic:
    if re.match(r'^[a-zA-Z]+$',word.lower()) and not os.path.isfile(f'./pronunciation/{word.lower()}/{word.lower()}.mp3') and not os.path.isfile(f'./pronunciation/{word.lower()}/{word.lower()}.wav'):
        print(word.lower())
        if not os.path.exists(f"./pronunciation/{word.lower()}"):
            os.makedirs(f'./pronunciation/{word.lower()}')
        urllib.request.urlretrieve("http://dict.youdao.com/dictvoice?type=1&audio="+word.lower(),f"./pronunciation/{word.lower()}/{word.lower()}.mp3")