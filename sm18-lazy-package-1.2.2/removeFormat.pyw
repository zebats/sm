import pyperclip
import re
pyperclip.copy(re.sub(r'\s','',pyperclip.paste()))