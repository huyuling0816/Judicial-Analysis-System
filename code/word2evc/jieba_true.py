import jieba
import jieba.posseg as pseg  # 词性标注
import jieba.analyse as anls  # 关键词提取
"""
from 预处理数据 import 数据处理方法


# 加入停用词库
def stopwords():
    jieba.analyse.set_stop_words('/Users/hanjiaxi/PycharmProjects/分词/中文分词/分词算法/jieba_cutter/stopwords')

# 加入idf词库
def idf_path():
    jieba.analyse.TFIDF(idf_path='../词典合集/lawa_term.dic')

# 加入自定义词典
def self_dic():
    jieba.load_userdict('/Users/hanjiaxi/PycharmProjects/分词/中文分词/分词算法/词典合集/new_dict')

"""

# jieba分词精确模式
def jieba_exact(content):
        words = jieba.cut(content, cut_all=False)
        return words


# jieba词性标注
def jieba_pos(content):
        name_list = jieba.posseg.cut(content)
        # 创建分词字典
        dict = {x.word: x.flag for x in name_list}
        return dict


# 基于tfidf算法的关键词提取
def tfidf(content, topK, withWeight, list):
        if list == None:
            tfidf_text = anls.extract_tags(content, topK=topK, withWeight=withWeight)
        else:
            tfidf_text = anls.extract_tags(content, topK=topK, withWeight=withWeight, allowPOS=list)
        tfidf_dict = {x[0]: x[1] for x in tfidf_text}
        return (tfidf_dict)


# 基于textrank算法的关键词提取
def textrank(content, topK, withWeight, list):
        if list == None:
            textrank_text = anls.textrank(content, topK=topK, withWeight=withWeight)
        else:
            textrank_text = anls.textrank(content, topK=topK, withWeight=withWeight, allowPOS=list)
        textrank_dict = {x[0]: x[1] for x in textrank_text}
        return (textrank_dict)


# 以上两种算法结合
def mix_tfidf_textrank(content, topK, withWeight, list, percent):
    tfidf_dict = tfidf(content, topK, withWeight, list)
    textrank_dict = textrank(content, topK, withWeight, list)
    all_dict = {}
    for key in tfidf_dict.keys():
        all_dict[key] = tfidf_dict.get(key)
    for key in textrank_dict.keys():
        if key in all_dict.keys():
            all_dict[key] = percent * tfidf_dict.get(key) + (1 - percent) * textrank_dict.get(key)
        else:
            all_dict[key] = textrank_dict.get(key)
    return (all_dict)


# 获得对应属性的分词
def get_pos(content, pos):
    jieba_dict = jieba_pos(content=content)
    result = []
    for x in jieba_dict.keys():
        if jieba_dict.get(x) in pos:
            result.append(x)
    return result

'''
self_dic()
idf_path()
stopwords()
filepath1 = '/Users/hanjiaxi/PycharmProjects/分词/预处理数据/test'
filepath2 = '/Users/hanjiaxi/PycharmProjects/分词/预处理数据/text'
jieba_pos(filepath2)
'''

'''
tfidf(filepath2,20,True,None)
textrank(filepath2,20,True,None)
mix_tfidf_textrank(filepath2,20,True,None,0.3)
'''
