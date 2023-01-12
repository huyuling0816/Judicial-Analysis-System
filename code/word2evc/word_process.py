# -*- coding:GBK -*-
import os
import os.path
import re
import unicodedata as ucd
from word2evc import jieba_true
punctuation =  '''，。、:；（）ＸX×xa"“”,<《》'''

# 截取判决书
def getText(text):
    flag=0
    content1=re.findall(r"本院认为(.+?)本判决",text)[0]
    #处理标点
    tet = re.sub("[%s]+" % punctuation, "", content1)
    tet=tet.replace(" ","")
    return tet

#进行分词

def word_cut(text):
    content=[]
    words=jieba_true.jieba_exact(text)
    for word in words:
        content.append(word+" ")
    print("".join(content))
    return "".join(content)

def word_process(text):
    text1=getText(text)
    text2=word_cut(text1)
    return text2



