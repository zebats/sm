import pyperclip

clip=pyperclip.paste().split('\n')
result=clip[-5:]
pyperclip.copy('\n'.join(result))
