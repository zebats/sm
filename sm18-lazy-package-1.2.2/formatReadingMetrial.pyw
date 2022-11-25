import pyperclip
import re
import os

s=pyperclip.paste()
s=re.sub(r'°','。',s)
s=re.sub(r' ?Notes ?','',s)
s=re.sub(r'）',')',s)
s=re.sub(r' \)',')',s)
s=re.sub(r'\) ',')',s)
s=re.sub(r'（','(',s)
s=re.sub(r'\( ','(',s)
s=re.sub(r'C02','CO2',s)
s=re.sub(r'[O0]\?','O2',s)
s=re.sub(r'(?<![a-zA-Z])o(?![a-zA-Z0-9])','。',s)
s=re.sub(r'\r\n','',s)
s=re.sub(r'\r','',s)
s=re.sub(r'(.)(\([1-9]\))',r'\1\r\n\2',s)
s=re.sub(r'lOO',r'100',s)
s=re.sub(r'\)。',r'\) 。',s)
# print(s)
# os.system("pause")
pyperclip.copy(s)