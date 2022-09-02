while True:
    sentence=input('sentence:')
    word=input('word:').replace(' ','')
    meaning=input('meaning:')
    with open('eng.htm','a',encoding="utf-8") as f:
        f.write(f"Q: {sentence.replace(word,f'<b><u>{word}</u></b>')}\nA: {meaning}\n<hr>\n\n")
