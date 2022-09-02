import json

dic={}
with open('dic.txt','r') as f:
    dic=json.loads(f.read())
while True:
    sentence=input('sentence:')
    unknown = [i for i in sentence.replace('.','').split() if (not i.lower() in dic) or dic[i.lower()]==0]
    for i in unknown:
        word = i
        print(i,"?(1)")
        if input()!='1':
            break
    # word=input('word:').replace(' ','')
    meaning=input('meaning:')
    with open('eng.htm','a',encoding="utf-8") as f:
        f.write(f"Q: {sentence.replace(word,f'<b><u>{word}</u></b>')}\nA: {meaning}\n<hr>\n\n")
