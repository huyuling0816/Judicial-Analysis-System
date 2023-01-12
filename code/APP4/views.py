from django.shortcuts import render
from django.http import JsonResponse
import json
# Create your views here.


def fun(request):
    json_dict = json.loads(request.body.decode()).get("0", None)
    key = json_dict.get("key")
    text = json_dict.get("text")
    list_temp = find_max(key, text)
    dict_similar = {
        "title": list_temp[0],
        "text": list_temp[1]
    }
    return JsonResponse(dict_similar)

# _*_coding:utf-8 _*_
# 欲实现将传入的text转换为计算的text
# 将所有单词的词向量相加求平均值，得到的向量即为句子的向量
import logging
import sqlite3

from gensim.models import word2vec
import numpy as np
from scipy import linalg
from word2evc import word_process
import unicodedata as ucd

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s',
    level=logging.INFO)

def getText(filename):
    f = open(filename, encoding='GB18030')
    content = []
    for line in f.readlines():
        temp = ucd.normalize('NFKC', line.strip('\n')).replace(' ', '')
        content.append(temp.replace('"',''))  # 去掉列表中每一个元素的换行符
    f.close()
    return ''.join(content)

def write_in(text):
    # 此路径需要修改
    with open('D:\\DATA SCIENCE\\djangoProject1\\word2evc\\案件.txt','a',encoding='utf-8') as f1:
        f1.write(text)
    # 使用gensim中的word2vec模块(此路径也需修改)
    sentences = word2vec.LineSentence('D:\\DATA SCIENCE\\djangoProject1\\word2evc\\案件.txt')
    model = word2vec.Word2Vec(sentences, hs=1, min_count=1, window=5, vector_size=100)
    words = text.split(" ")
    v = np.zeros(100)
    for word in words:
        if word=='': break
        else:
            v += model.wv[word]
    v /= len(words)
    return v

def getv(text):
    text1=word_process.word_process(text)
    return write_in(text1)

def vector_similarity(v1, v2):
    return np.dot(v1, v2) / (linalg.norm(v1) * linalg.norm(v2))

def strToV(str):
    # 字符串转为list
    v3 = str.split(",")
    v4 = np.array(v3)
    # 将list里的str转为float
    a_float = []
    for num in v4:
        a_float.append(float(num))
    # 返回最终得到的向量
    return np.array(a_float)

def find_max(searchword,text):
    """
    :param searchword（即爬虫时用户输入的搜索关键词word，用于减小搜索范围，且目前主要局限于交通肇事）,
           text（前端传过来的需要寻找相似案件的文书）:
    :return: 返回一个列表，第0个元素是标题，第1个元素是正文内容
    """
    # 找到最大相似度的案件
    # 遍历数据库 得到每个v2
    # 用vector——similarity方法算出最大值
    # 取出对应案件

    # 创建与数据库的连接
    connection = sqlite3.connect('D:\\DATA SCIENCE\\djangoProject1\\database.db')
    # 创建一个游标
    cur = connection.cursor()
    # 计算text对应的v1(向量)
    v1 = getv(text)
    # 寻找同一关键字的所有文书向量值，计算相似度
    cur.execute("select v from rawWrit where searchWord = '%s';" % searchword)
    list = cur.fetchall()
    # 先计算找到的第一个文书的向量和相似度
    v2 = strToV(list[0][0])
    similarity = vector_similarity(v1,v2)
    # 遍历数据库中符合条件的文书，找到最大值
    for i in range(1, len(list)):
        print(i)
        if list[i][0] == None:
            pass
        else:
            v = strToV(list[i][0])
            sim = vector_similarity(v1,v)
            if sim>similarity:
                similarity = sim
                v2 = v
    # v2即为最相似文书的向量,并将其转化为字符串
    temp = v2.tolist()
    str = ''
    for x in temp:
        str += '{:.10f}'.format(x)+','
    str = str[0:len(str)-1]
    # 根据字符串形式的向量在数据库中取出对应的title和content，显示在前端（或者保存到本地也可以？）
    cur.execute("select title from rawWrit where v = '%s';" % str)
    title = cur.fetchone()[0]
    cur.execute("select content from rawWrit where v = '%s'" % str)
    content = cur.fetchone()[0]
    list = [title,content]
    return list     # 列表（标题 正文）

def returnV(text):
    v = getv(text)
    v1 = v.tolist()
    msg = ''
    for x in v1:
        msg += '{:.10f}'.format(x)+','
    msg = msg[0:len(msg)-1]
    return msg

# 测试max函数
# text = getText('D:\南京大学0\数据科学大作业相关\爬取文书文件\交通肇事\交通事故\季益军交通肇事罪刑事一审刑事判决书.txt')
# find_max("交通肇事",text)


