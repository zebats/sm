import requests
import re
from bs4 import BeautifulSoup
import json
import os
import urllib.request

with open('F:\Desktop\SuperMemo_17_18破解版_17直接解压_18安装后把key粘贴上去后unlock就好\sm18-lazy-package-1.2.2\CET4\dic.txt','r') as f:
    dic=json.loads(f.read())

def cmp(a):
    return len(a[0])

def getTranslation(word):
    con=requests.get(f'https://dict.youdao.com/w/eng/{word}/#keyfrom=dict2.index').text
    return [re.search(r'(?<=<li>)[a-z]+\.[^；]+?(?=(<\/li>|\n|；))',con).group(),re.search(r'(?<=<ul>\n     <li>)(.|\s)+?(?=<\/li>\n    <\/ul>)',con).group().replace('</li>','').replace('<li>','')]#[simplified/full]

def getSentence(word):
    con=requests.get(f'https://dict.youdao.com/w/eng/lj:{word}/#keyfrom=dict2.index').text
    soup=BeautifulSoup(con,"html.parser")
    a=soup.find('ul',class_="ol").contents
    b=[i for i in a if i!='\n'] 
    # d=b[n].p.stripped_strings                                                                                                                                             
    # print(' '.join(d).replace(" '","'").replace(" .","."),'|||',word,getTranslation(word)[1])
    # print(''.join(b[n].findAll('p')[1].stripped_strings))
    c=[]
    for i in range(len(b)):
        c.append([' '.join(b[i].p.stripped_strings).replace(" '","'").replace(" .",".").replace(" ?","?"),''.join(b[i].findAll('p')[1].stripped_strings)])
        c.sort(key=cmp)
    return c
tempdic=dic.copy()
count=0
totalc=0
for i in dic:
    if dic[i]==0:
        totalc+=1
for key in dic: #选词
    if dic[key]==0:
        count+=1
        n=0
        sentence=getSentence(key)
        meaning=getTranslation(key)
        while True: #选句子1
            print(sentence[n][0],'|||',key,meaning[1],'\n',sentence[n][1])
            change=input('change?(1/2)')
            if change=='1':
                n+=1
            elif change=='2':
                for i in sentence[n][0].replace('.','').replace('?','').split(): #处理句子
                    if i.lower() in tempdic and tempdic[i.lower()]==1 or i in tempdic and tempdic[i]==1:
                        continue
                    if re.search(r'[0-9]',i) or re.search("'",i):
                        continue
                    print(i)
                    if not i.lower() in tempdic:
                        if re.match(r'^\w+$',i.lower()) and not os.path.exists(f'./pronunciation/{i.lower()}'):
                            os.makedirs(f'./pronunciation/{i.lower()}')
                            urllib.request.urlretrieve("http://dict.youdao.com/dictvoice?type=1&audio="+i.lower(),f".\pronunciation\{i.lower()}\{i.lower()}.mp3")
                        inpu=input('"0N/1Y/2Pass"\n')
                        if inpu=='2':
                            continue
                        if inpu!='0':
                            tempdic[i.lower()]=1
                            continue
                    # tempdic[i.lower()]=1
                    trans=getTranslation(i)
                    print(trans[1])
                    with open('eng.htm','a',encoding="utf-8") as f: #保存数据
                        if i == key:
                            a=re.search(r'[a-z]+?\.',trans[0]).group() #就是提取个词性
                            f.write(f'Q: {sentence[n][0].replace(i,f"<b><u>{i}</u></b>")}\nA: {a} \n<hr>\n\n')
                        else:
                            f.write(f'Q: {sentence[n][0].replace(i,f"<b><u>{i}</u></b>")}\nA: {trans[0]} \n<hr>\n\n')
                    with open('dic.txt','r') as f:
                        temptempdic=json.loads(f.read())
                    for j in tempdic:
                        if not j in temptempdic:
                            temptempdic[j]=tempdic[j]
                    temptempdic[i.lower()]=1
                    with open('dic.txt','w') as f:
                        f.write(json.dumps(temptempdic))
                n+=1
            else:
                break
        print(f'{totalc-count} left',count)
        for i in sentence[n][0].replace('.','').replace('?','').split(): #处理句子
            if i.lower() in tempdic and tempdic[i.lower()]==1 or i in tempdic and tempdic[i]==1:
                continue
            if re.search(r'[0-9]',i):
                continue
            print(i)
            if not i.lower() in tempdic:
                inpu=input('"0N/1Y/2Pass"\n')
                if inpu=='2':
                    continue
                if inpu!='0':
                    tempdic[i.lower()]=1
                    continue
            tempdic[i.lower()]=1
            trans=getTranslation(i)
            print(trans[1])
            with open('eng.htm','a',encoding="utf-8") as f: #保存数据
                f.write(f'Q: {sentence[n][0].replace(i,f"<b><u>{i}</u></b>")}\nA: {trans[0]}\n<hr>\n\n')
            with open('.\dic.txt','r') as f:
                temptempdic=json.loads(f.read())
            for j in tempdic:
                if not j in temptempdic:
                    temptempdic[j]=tempdic[j]
            temptempdic[i.lower()]=1
            with open('dic.txt','w') as f:
                f.write(json.dumps(temptempdic))
dic=tempdic.copy()
with open('dic.txt','w') as f:
    f.write(json.dumps(dic)) 