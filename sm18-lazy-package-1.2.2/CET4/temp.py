import json

dic={}
with open('word.txt','r',encoding='utf-8') as f:
    words=f.read()
words=words.split('\n')
# print(json.dumps(words, ensure_ascii=False))
for i in range(len(words)):
    words[i]=words[i].split()
    dic[words[i][0]]=words[i][1]
    print(words[i])
with open('sdic.txt','w',encoding= 'utf-8') as f:
    f.write(json.dumps(dic, ensure_ascii=False))