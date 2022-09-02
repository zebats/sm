import json


with open('dic.txt','r') as f:
    dic=json.loads(f.read())
with open('wl.txt','r') as f:
    wl=f.read().splitlines()
lis=[]
res=[]
while True:
    a=input()
    if a != '1':
        lis.append(a.split())
    else:
        break
print('\nover\n')
count=1
for i in lis:
    count+=1
    try:
        if(i[0] in wl or dic[i[0]]==1):
            continue
    except:
        pass
    print(i[0],count,'/',len(lis))
    if input()=='0':
        with open('wl.txt','a') as f:
            f.write(i[0]+'\n')
    else: 
        dic[i[0]]=1
        with open('dic.txt','w') as f:
            f.write(json.dumps(dic))