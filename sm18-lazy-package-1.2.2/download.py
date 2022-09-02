import os
from tokenize import group
import urllib.request
import re
from pyperclip import copy, paste

#word = re.sub(r'\w*\[sound:(\w*)\.mp3\]',r"\1",paste())
word = re.search(r'(?<=<(U|u)>).+?(?=</(U|u)>)',paste()).group()
print(word)
word.lower()
word = re.sub('\s','',word)
copy(word)
urllib.request.urlretrieve("http://dict.youdao.com/dictvoice?type=1&audio="+word,filename= word+".mp3")
