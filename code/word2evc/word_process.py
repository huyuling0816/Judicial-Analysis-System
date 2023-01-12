# -*- coding:GBK -*-
import os
import os.path
import re
import unicodedata as ucd
from word2evc import jieba_true
punctuation =  '''������:��������X��xa"����,<����'''

# ��ȡ�о���
def getText(text):
    flag=0
    content1=re.findall(r"��Ժ��Ϊ(.+?)���о�",text)[0]
    #������
    tet = re.sub("[%s]+" % punctuation, "", content1)
    tet=tet.replace(" ","")
    return tet

#���зִ�

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



