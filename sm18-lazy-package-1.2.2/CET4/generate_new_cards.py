import requests
import re
from bs4 import BeautifulSoup
import json
import os
import jieba
from fake_useragent import UserAgent
import datetime
from time import strftime
import html

headers = {"User-Agent": UserAgent().firefox}

# 从本地文件中读取单词列表和中文释义
with open('word_list_CET4.txt', 'r') as f:
    word_list = json.loads(f.read())
    sample_word_list = word_list.copy()
with open('Chinese_meanings_CET4.txt', 'r', encoding='utf-8') as f:
    chinese_meanings = json.loads(f.read())

# 好像是补全中文释义的key
for sentence_current_word in word_list:
    if not sentence_current_word in chinese_meanings:
        chinese_meanings[sentence_current_word] = ''

# 将中文释义按照词性分类
for sentence_current_word in chinese_meanings:
    chinese_meanings[sentence_current_word] = chinese_meanings[sentence_current_word].split("；")

# 定义比较函数，用于将词频统计结果按照词频排序
def cmp(a):
    return len(a[0])

# 从有道词典获取单词的释义和例句（不要试图去理解它，一半抄的一半写得狗都不认识）
def get_translation(word):
    '''Get the translation of a word from dic.youdao.com

    Args:
        word (str): The word that will be got translation.

    Returns:
        list: [simplified,full]simplified means the first meaning the website shows, and full means the full meanings the website provides.
            example:['adj. 范围广的，影响大的', 'adj. 范围广的，影响大的；过于笼统的；弧线的，弯曲的；包含丰富信息的；（投票等中的）大胜\n     n. 打扫，清扫；扫集的尘土（或垃圾）（sweepings）\n     v. 打扫，清除；（目光）扫视，（灯光）掠过；（快速地）带走，卷 走（sweep 的现在分词）']
    '''
    con = requests.get(
        url=f'https://dict.youdao.com/w/eng/{word}/#keyfrom=dict2.index', headers=headers).text
    return [re.search(r'(?<=<li>)[a-z]+\.[^；]+?(?=(<\/li>|\n|；))', con).group(), re.search(r'(?<=<ul>\n     <li>)(.|\s)+?(?=<\/li>\n    <\/ul>)', con).group().replace('</li>', '').replace('<li>', '')]

def get_sentence(word):
    '''Returns a list of sentences&Chinese meanings that contain the word.

    Args:
        word (str): Words used to find the corresponding example sentences

    Returns:
        list: Contains several list, each of the list consist of an English sentence and a Chinese translation.
            example:
    '''
    con = requests.get(
        url=f'https://dict.youdao.com/w/eng/lj:{word}/#keyfrom=dict2.index', headers=headers).text
    soup = BeautifulSoup(con, "html.parser")
    a = soup.find('ul', class_="ol").contents
    b = [i for i in a if i != '\n']
    c = []
    for i in range(len(b)):
        c.append([' '.join(b[i].p.stripped_strings).replace(" '", "'").replace(
            " .", ".").replace(" ?", "?"), ''.join(b[i].findAll('p')[1].stripped_strings)])
    c.sort(key=cmp)
    for i in range(len(c)-1):
        if c[i][0] == c[i+1][0]:
            c.pop(i)
            break
    return c

def get_local_meanings(word):
    '''根据传入的word返回其在本地词典中的释义

    Args:
        word (str): 要查询释义的单词,无需转为小写

    Returns:
        list: 返回一个包含多个list的list其中每个list的0位为该单词的一个词性+释义，1位为0时，说明这个释义的例句还未被添加过，
              添加过释义的例句后需要手动将其改为1以进行标记(虽然事实上在这个程序中用过的直接被pop了)
              eg.[['adj.过多的，极度的', 0], ['', 1]]
    '''
    local_meanings = []
    for j in chinese_meanings[word.lower()]:
        #这个地方是判断j是不是词性
        if not re.search(r'[一-龟]', j):
            part_of_speech = j
        else:
            local_meanings.append([part_of_speech+j, 0])
    local_meanings.append(['', 1])
    return local_meanings

def count_word_freq(sentences):
    '''输入上方get_stence函数返回的stences,返回stences中中文翻译里的中文的词频

    Args:
        sentences (list): 上方get_stence函数返回的stences

    Returns:
        dic: {中文分词:词频}
    '''
    word_freq = {}
    for sentence in sentences:
        seg_list = jieba.cut(sentence[1])
        for seg in seg_list:
            if not re.search("[一-龟]", seg):
                break
            if seg not in word_freq:
                word_freq[seg] = 1
            else:
                word_freq[seg] += 1
    high_frequency_words = ['的', '是', '在', '和', '我', '他', '有', '了','你', '我们', '和', '会', '她', '又', '他们', '我']
    for word in high_frequency_words:
        word_freq.pop(word, None)
    return word_freq

def get_top_freq_words(word_freq, frequency = 3):
    '''将word_freq中出现频率大于等于于frequency的词汇以及它们的出现频率转变为字符串的形式

    Args:
        word_freq (dic): jieba cut后的中文频率，需使用上面的count_word_freq函数的返回值
        frequency (int, optional): 要转化的频率最低的词汇的频率. Defaults to 3.

    Returns:
        str: word_freq中出现频率高于等于frequency的词语+出现频率，每个词语之间用空格隔开
             eg."过度12 导致4 过多4 可能3 对3"
    '''
    sorted_word_freq = [(k, v) for k, v in word_freq.items()]
    sorted_word_freq.sort(key=lambda x: x[1], reverse=True)  # sorted_word_freq是把word_freq转化为元组后按词频降序
    high_frequency_words = ''
    for i in sorted_word_freq:
        if i[1] >= frequency:
            high_frequency_words += f"{i[0]}{i[1]} "
        else:
            break
    return high_frequency_words

def print_word_info(word, sentence, frequency = 3, max_length = 90):
    '''展示单词以及相关的句子，释义，翻译出现的词频等相关信息
    eg. --------------------
        高频词: 过度12 导致4 过多4 对4 可能3
        It may lead to excessive spending. | excessive | adj.  过多的，极度的 | adj. 过度的，过多的
        它可能会导致过度消费。

    Args:
        word (str): 单词
        sentence (list): 单词对应的句子，要get_sentence函数返回的
        frequency (int, optional): 要转化的频率最低的词汇的频率. Defaults to 3.
        max_length (int, optional): 每行限制的最大长度. Defaults to 100.
    '''
    print(f'{"-"*20}\n高频词: {get_top_freq_words(count_word_freq(sentence), frequency)}')
    space_length = (len(sentence[sentence_index][0]) + 3 + len(word) + 3 + len('  '.join(chinese_meanings[word])) + len(re.findall(r'([一-龟]|，)', ' '.join(chinese_meanings[word]))) + 3)
    #对出来最后屁股不准是因为中英文宽度不同，懒得改了太麻烦了
    youdao_meaning_info_list = get_translation(word)[1].split('\n')
    for line in range(len(youdao_meaning_info_list)):
        youdao_meaning_info_list[line] = youdao_meaning_info_list[line].replace(' ','')
        for l in range(max_length - space_length, 9999, max_length):
            if len(youdao_meaning_info_list[line]) >= l:
                youdao_meaning_info_list[line] = youdao_meaning_info_list[line][:l] + '\n' + ' ' * (space_length + 2) + youdao_meaning_info_list[line][l:]#space_length+2是为了换行时往后缩两格
            else:
                break
        youdao_meaning_info_list[line] = ' ' * space_length + youdao_meaning_info_list[line]
    youdao_meaning_info_list[0] = youdao_meaning_info_list[0][space_length:]
    youdao_meaning_info_str = '\n'.join(youdao_meaning_info_list)
                                                                     
    print(f'{sentence[sentence_index][0]} | {word} | {"  ".join(chinese_meanings[word])} | {youdao_meaning_info_str}')
    print(sentence[sentence_index][1])

def save():
    '''保存word_list里的数据，同时会保留手动在文件里修改的数据
    '''
    temp_sample_word_list = sample_word_list.copy()
    with open('word_list_CET4.txt', 'r') as f:
        current_local_word_list = json.loads(f.read())
    for word in word_list:
        if not word in sample_word_list or word_list[word] != sample_word_list[word]:
            sample_word_list[word] = word_list[word]
    for word in current_local_word_list:
        if (not word in sample_word_list) or (current_local_word_list[word] != sample_word_list[word] and current_local_word_list[word] != temp_sample_word_list[word]):
            sample_word_list[word] = current_local_word_list[word]
    with open('word_list_CET4.txt', 'w') as f:
        f.write(json.dumps(sample_word_list))

def is_valuable_word(word):
    '''判断传入的word是否是一个未学过的单词

    Args:
        word (str): 传入的单词，大小写无所谓，是不是真的单词也无所谓，函数会出手

    Returns:
        boolen: 如果是未学过的单词返回True,如果是已学过的单词或不是单词则返回False
    '''
    if(word.lower() in word_list and word_list[word.lower()] == 1 
       or word in word_list and word_list[word] == 1 ):
        return False
    if re.search(r"'", word.lower()) or not re.search(r'^[a-zA-Z]+$', word):
        return False
    return True

current_run_processed_words_count = 0

# 计数未处理的单词
unprocessed_words_count = 0
for sentence_current_word in word_list:
    if word_list[sentence_current_word] == 0:
        unprocessed_words_count += 1

for current_word in word_list.copy():  # 选词
    if word_list[current_word] == 0:
        current_run_processed_words_count += 1
        sentence_index = 0

        os.system(r"start download_pronunciation.pyw")

        try:
            sentence = get_sentence(current_word)
        except:
            print(f'no sentences found!({current_word})')
            continue

        local_meanings = get_local_meanings(current_word)
        
        while True:  # 选句子1
            save()
            print_word_info(current_word, sentence, 3)
            
            # 1:切换下一个句子 2:选择当前的句子 3：回到第一个句子 4:切换到下一个单词 直接回车也是2
            change = input('change?(1/2/3/4)')
            if change == '1':
                if sentence_index == len(sentence)-1:
                    print('-'*20+'\n  over!\n'+'-'*20+'/n')
                    sentence_index = 0
                else:
                    sentence_index += 1
            # 2无了(改else里了)
            elif change == '3':
                sentence_index = 0
            elif change == '4':
                word_list[current_word] = 1
            else:  # 原来的2
                # 处理句子
                for sentence_current_word in sentence[sentence_index][0].replace('.', '').replace('?', '').split():

                    if not is_valuable_word(sentence_current_word):
                        continue

                    print(sentence_current_word)

                    if not sentence_current_word.lower() in word_list:
                        user_response = input('"0N/1Y/2Pass"\n')
                        if user_response == '2':
                            continue
                        if user_response != '0':
                            word_list[sentence_current_word.lower()] = 1
                            continue

                    if (sentence_current_word.lower() != current_word 
                      and sentence_current_word.lower() in chinese_meanings):
                        current_meanings = get_local_meanings(sentence_current_word)
                    elif sentence_current_word.lower() == current_word:
                        current_meanings = local_meanings

                    current_trans_to_write = get_translation(sentence_current_word)
                    print(current_trans_to_write[1])
                    current_trans_to_write[1] = (re.sub(r'\s', '', re.sub(
                        r'\n', '<BR>', html.escape(current_trans_to_write[1]))))
                    
                    with open('eng.htm', 'a', encoding="utf-8") as f:  # 保存数据
                        if sentence_current_word.lower() in chinese_meanings:
                            for meaning in range(len(current_meanings)):
                                print(meaning, current_meanings[meaning][0])
                            meaning_choice = input('which?')
                            if meaning_choice == '':
                                meaning_choice = '0'
                            f.write(f'Q: {sentence[sentence_index][0].replace(sentence_current_word,f"<a style={chr(34)}display:none{chr(34)}>.</a><b><u>{sentence_current_word}</u></b><a style={chr(34)}display:none{chr(34)}>.</a>")}<BR><DIV class=footer><BR>-------------------<BR>Content:CET-4<BR>Date:{datetime.datetime.now().strftime("%Y/%m/%d")}</DIV>\nA: {current_meanings[int(meaning_choice)][0]}<BR><DIV class=footer><BR>-------------------<BR>{current_trans_to_write[1]}</DIV>\n<hr>\n\n')
                            current_meanings.pop(int(meaning_choice))
                        else:
                            f.write(f'Q: {sentence[sentence_index][0].replace(sentence_current_word,f"<a style={chr(34)}display:none{chr(34)}>.</a><b><u>{sentence_current_word}</u></b><a style={chr(34)}display:none{chr(34)}>.</a>")}<BR><DIV class=footer><BR>-------------------<BR>Content:CET-4<BR>Date:{datetime.datetime.now().strftime("%Y/%m/%d")}</DIV>\nA: {current_trans_to_write[0]}<BR><DIV class=footer><BR>-------------------<BR>{current_trans_to_write[1]}</DIV>\n<hr>\n\n')
                        
                is_current_word_completed = 1
                for meaning in local_meanings:
                    is_current_word_completed &= meaning[1]
                if is_current_word_completed:
                    word_list[current_word] = 1
                    #别的情况下生词不标记为学过是因为可能有多种意思
                    break

                sentence_index += 1
save()
