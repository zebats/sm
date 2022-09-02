import copy
import re
# <!--sm导入时问题的文本不能相同(忽略html与空格),否则问题统一会被替换为最后一个(html被替代)-->
# n=0
# print('I needed to <b><u>accommodate</u></b> to the new schedule .'+ f'<span style="display: none;">{n}</span>')
with open('eng.htm','r',encoding='utf_8') as f:
    stences=f.read().split(r'<hr>')
for i in range(len(stences)-1):
    stences[i]=[j for j in stences[i].split('\n') if j!='']
stences.pop(len(stences)-1)
st=copy.deepcopy(stences)
for i in range(len(stences)):
    stences[i][0]=re.sub(r'<.+?>','',stences[i][0])
n=0
for i in range(len(stences)-1):
    if stences[i][0] == stences[i+1][0]:
        print(stences[i][0])
        st[i][0] += f'<span style="display: none;">{n}</span>'
        n+=1
    else:
        n=0
with open('eng1.htm','w',encoding='utf_8') as f:
    for i in st:
        f.write(f'{i[0]}\n{i[1]}\n<hr>\n\n')