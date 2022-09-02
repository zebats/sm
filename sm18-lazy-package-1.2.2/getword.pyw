import os
from tokenize import group
import urllib.request
import re
from pyperclip import copy, paste

word = re.search(r'(?<=<(U|u)>).+?(?=</(U|u)>)',paste()).group()
print(word)
word.lower()
word = re.sub('\s','',word)
copy(word)
