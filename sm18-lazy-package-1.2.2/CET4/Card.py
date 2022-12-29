import requests
import re
from bs4 import BeautifulSoup
import json
import os
import urllib.request
import jieba
from subprocess import Popen
from fake_useragent import UserAgent
import datetime
from time import strftime
import html

headers={"User-Agent":UserAgent().firefox}

with open('dic.txt','r') as f:
    dic=json.loads(f.read())
with open('sdic.txt','r',encoding='utf-8') as f:
    sdic=json.loads(f.read())

for i in dic:
    if not i in sdic :
        sdic[i]=''
for i in sdic:
    sdic[i]=sdic[i].split('；')

def cmp(a):
    return len(a[0])

def getTranslation(word):
    con=requests.get(url=f'https://dict.youdao.com/w/eng/{word}/#keyfrom=dict2.index',headers=headers).text
    return [re.search(r'(?<=<li>)[a-z]+\.[^；]+?(?=(<\/li>|\n|；))',con).group(),re.search(r'(?<=<ul>\n     <li>)(.|\s)+?(?=<\/li>\n    <\/ul>)',con).group().replace('</li>','').replace('<li>','')]#[simplified/full]

def getSentence(word):
    con=requests.get(url=f'https://dict.youdao.com/w/eng/lj:{word}/#keyfrom=dict2.index',headers=headers).text
    soup=BeautifulSoup(con,"html.parser")
    a=soup.find('ul',class_="ol").contents
    b=[i for i in a if i!='\n'] 
    c=[]
    for i in range(len(b)):
        c.append([' '.join(b[i].p.stripped_strings).replace(" '","'").replace(" .",".").replace(" ?","?"),''.join(b[i].findAll('p')[1].stripped_strings)])
    c.sort(key=cmp)
    for i in range(len(c)-1):
        if c[i][0]==c[i+1][0]:
            c.pop(i)
            break
    return c
tempdic=dic.copy()
count=0
totalc=0
oneCharacter='"'
for i in dic:
    if dic[i]==0:
        totalc+=1
for key in dic: #选词
    if dic[key]==0:
        os.system(r"start download_pronunciation.pyw")
        ci={}
        count+=1
        n=0
        try:
            sentence=getSentence(key)
        except:
            print(f'no sentences found!({key})')
            continue
        meaning=getTranslation(key)
        meaningskey=[]
        for j in sdic[key.lower()]:
            if not re.search(r'[一-龟]',j):
                wordType=j
            else :
                meaningskey.append([wordType+j,0])
        meaningskey.append(['',1])
        for i in sentence:#词频统计
            j=jieba.cut(i[1])
            for k in j:
                if not re.search('[一-龟]',k):
                    break
                if not k in ci:
                    ci[k]= 1
                else:
                    ci[k]+=1
        lj=['的','是','在','和''我','他','有','了','你','我们','和','会','她','又','他们','我']
        for i in lj:
            ci.pop(i,None)
        rank=[(k,v) for k,v in ci.items()]
        rank.sort(key=lambda x : x[1],reverse=True)#rank是把ci转化为list后按词频降序
        top=''
        for i in range(5):
            top+=rank[i][0]+str(rank[i][1])+' '
        while True: #选句子1
            print('-'*20+'\n高频词: '+top+'\n'+sentence[n][0],'|',key,'|','  '.join(sdic[key]),'|',re.sub(r'\n',rf"\n{' '*(9+len(sentence[n][0])+len(key)+len('  '.join(sdic[key])))}",meaning[1]),'\n',sentence[n][1])
            #1:切换下一个句子 2:选择当前的句子 3：回到第一个句子 4:切换到下一个单词 直接回车也是2
            change=input('change?(1/2/3/4)')
            if change=='1':
                if n==len(sentence)-2:
                    print('-'*20+'\n  over!\n'+'-'*20+'/n')
                    n=0
                else:
                    n+=1
            #2无了(改else里了)
            elif change == '3':
                n = 0
            elif change == '4':
                tempdic[key]=1
                with open('dic.txt','w') as f:
                    f.write(json.dumps(tempdic))
                break
            else:#原来的2
                for i in sentence[n][0].replace('.','').replace('?','').split(): #处理句子
                    if i.lower() in tempdic and tempdic[i.lower()]==1 or i in tempdic and tempdic[i]==1 or re.search(r"'",i.lower()):
                        continue
                    if not re.search(r'^[a-zA-Z]+$',i):
                        continue
                    print(i)
                    if not i.lower() in tempdic:
                        inpu=input('"0N/1Y/2Pass"\n')
                        if inpu=='2':
                            continue
                        if inpu!='0':
                            tempdic[i.lower()]=1
                            continue
                    if i.lower() != key and i.lower() in sdic:
                        meaningsnow=[]
                        for j in sdic[i.lower()]:
                            if not re.search(r'[一-龟]',j):
                                wordType=j
                            else :
                                meaningsnow.append([wordType+j,0])
                        meaningsnow.append(['',1])
                        meanings=meaningsnow
                    elif i.lower() == key:
                        meanings=meaningskey
                    trans=getTranslation(i)
                    print(trans[1])
                    transWrite=(re.sub(r'\s','',re.sub(r'\n','<BR>',html.escape(trans[1]))))
                    with open('eng.htm','a',encoding="utf-8") as f: #保存数据
                        if i.lower() in sdic:
                            for j in range(len(meanings)):
                                print(j,meanings[j][0])
                            an=input('which?')
                            if an=='':
                                an='0'
                            f.write(f'Q: {sentence[n][0].replace(i,f"<a style={oneCharacter}display:none{oneCharacter}>.</a><b><u>{i}</u></b><a style={oneCharacter}display:none{oneCharacter}>.</a>")}<BR><DIV class=footer><BR>-------------------<BR>Content:CET-4<BR>Date:{datetime.datetime.now().strftime("%Y/%m/%d")}</DIV>\nA: {meanings[int(an)][0]}<BR><DIV class=footer><BR>-------------------<BR>{transWrite}</DIV>\n<hr>\n\n')
                            meanings.pop(int(an))
                        else:
                            f.write(f'Q: {sentence[n][0].replace(i,f"<a style={oneCharacter}display:none{oneCharacter}>.</a><b><u>{i}</u></b><a style={oneCharacter}display:none{oneCharacter}>.</a>")}<BR><DIV class=footer><BR>-------------------<BR>Content:CET-4<BR>Date:{datetime.datetime.now().strftime("%Y/%m/%d")}</DIV>\nA: {trans[0]}<BR><DIV class=footer><BR>-------------------<BR>{transWrite}</DIV>\n<hr>\n\n')
                    #这段是为了在写入的过程中不影响程序运行后手动对dic.txt的修改，但是逻辑有点问题，上面的case4的保存也需要修改
                    with open('dic.txt','r') as f:
                        temptempdic=json.loads(f.read())
                    for j in tempdic:
                        if not j in temptempdic:
                            temptempdic[j]=tempdic[j]
                    if i.lower() == key :
                        temptempdic[i.lower()]=1
                    with open('dic.txt','w') as f:
                        f.write(json.dumps(temptempdic))
                completed=1
                for i in meaningskey:
                    completed &= i[1]
                if completed :
                    break
                n+=1
                with open('dic.txt','r') as f:
                    temptempdic=json.loads(f.read())
                for j in tempdic:
                    if not j in temptempdic:
                        temptempdic[j]=tempdic[j]
                with open('dic.txt','w') as f:
                    f.write(json.dumps(temptempdic))
dic=tempdic.copy()
with open('dic.txt','w') as f:
    f.write(json.dumps(dic))