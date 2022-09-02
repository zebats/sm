import requests
import re
from bs4 import BeautifulSoup
import json

with open('dic.txt','r') as f:
    dic=json.loads(f.read())

def getTranslation(word):
    con=requests.get(f'https://dict.youdao.com/w/eng/{word}/#keyfrom=dict2.index').text
    #print(con)
    #print(re.search(r'(?<=<li>)[a-z]+\.[^；]+?(?=(\n|；))',con).group())
    return [re.search(r'(?<=<li>)[a-z]+\.[^；]+?(?=(<\/li>|\n|；))',con).group(),re.search(r'(?<=<ul>\n     <li>)(.|\s)+?(?=<\/li>\n    <\/ul>)',con).group().replace('</li>','').replace('<li>','')]#[simplified/full]

def getSentence(word,n):
    con=requests.get(f'https://dict.youdao.com/w/eng/lj:{word}/#keyfrom=dict2.index').text
    #print(con) 
    #print(re.search(r'(?<=<li>)[a-z]+\.[^；]+?(?=(\n|；))',con).group())
    soup=BeautifulSoup(con,"html.parser")
    a=soup.find('ul',class_="ol").contents
    b=[i for i in a if i!='\n']#[3].p.stripped_strings
    d=b[n].p.stripped_strings
    # c=[i for i in b if getTranslation(word) in i.p.next_sibling.stripped_strings]
    print(' '.join(d).replace(" '","'").replace(" .","."),'|||',word,getTranslation(word)[1])
    print(''.join(b[n].findAll('p')[1].stripped_strings))
    # return re.findall(r'(?<=<li>)[a-z]+\.[^；]+?(?=(\n|；))',con).group()
    return ' '.join(b[n].p.stripped_strings).replace(" '","'").replace(" .",".")
tempdic=dic.copy()
count=0
for key in dic:
    count+=1
    if dic[key]==0:
        n=0
        while True:
            sentence=getSentence(key,n)
            if input('change?(1)')=='1':
                n+=1
            else:
                break
        print(f'{len(dic)-count} left')
        for i in sentence[:-1].split():
            if i.lower() in tempdic and tempdic[i.lower()]==1:
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
            with open('eng.htm','a',encoding="utf-8") as f:
                f.write(f'Q: {sentence.replace(i,f"<b><u>{i}</u></b>")}\nA: {trans[0]}\n<hr>\n\n')
            with open('dic.txt','r') as f:
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