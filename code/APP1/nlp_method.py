import json
import os
import os.path


crime_key=['crime']
court_key=['court']

#词性筛选
noun_pos=['n','nh','ni','ns','nl','nz','b','i','r','m','q','ws'] #一般名词，地点名词，时间名词，位置，机构，其他专有名词，名词修饰词
time_pos=['nt']
loc_pos=['ns']
gender_pos=['b']
nationality_pos=['nz']
verb_pos=['v']
adj_adv_pos=['a','d']
#命名实体
name_net=['S-Nh']
loc_net=['S-Ni','S-Ns']

def cut(content):

    #定义一些信息框
    true_gender = []
    true_nationality = []

    """
    数据处理方法.preprocess_data(filepath,filepath,False)
    """

    #jieba分词
    self_dic() #加入自定义词典
    """idf_path() #加入idf词库"""
    stopwords() #加入停用词

    #ltp分词
    words=ltp_cut(content)
    postags=ltp_pos(words)

    #获得罪名和法院（jieba方法更加可靠）
    crime=get_pos(content,crime_key)
    court=get_pos(content,court_key)

    #获得姓名（ltp命名识别）
    name_ltp=get_net(words=words,postags=postags,list=name_net)

    #获得地区（ltp命名识别）
    loc_ltp=list(select_POS(words=words,postags=postags,list=loc_pos)) #得到词性为位置的词表

    # 性别和民族（种类少 可以进行选择）
    gender = list(select_POS(words=words, postags=postags, list=gender_pos))
    for x in gender:
        if '男'==x :
            true_gender.append(x)
        if '女'==x:
            true_gender.append(x)
    nationality = list(select_POS(words=words, postags=postags, list=nationality_pos))
    for x in nationality:
        if '族' in x:
            true_nationality.append(x)
    print(true_gender)
    print(true_nationality)

    #额外的名词筛选
    noun_ltp=list(select_POS(words=words,postags=postags,list=noun_pos))
    noun_list1=find_all(noun_pos,dict_wordpos(words,postags))
    noun_list2=find_continuous(noun_pos,words,postags)
    print(noun_ltp)
    print(noun_list1)
    print(noun_list2)

    #动词提取
    verb_ltp=list(select_POS(words=words,postags=postags,list=verb_pos))

    # 动词提取
    adj_adv_ltp=list(select_POS(words=words, postags=postags, list=adj_adv_pos))

    #获得大部分的词类
    result_dict={}
    result_dict['name']=name_ltp
    result_dict['gender']=true_gender
    result_dict['nationality']=true_nationality
    result_dict['birthplace']=loc_ltp
    result_dict['crime']=crime
    result_dict['court']=court
    result_dict['extra1']=noun_ltp
    result_dict['extra2']=noun_list2
    result_dict['extra3']=noun_list1
    result_dict['verb']=verb_ltp
    result_dict['adj_adv']=adj_adv_ltp



    return result_dict


import pyltp
from pyltp import SentenceSplitter
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer
from pyltp import Parser
from pyltp import SementicRoleLabeller

#中文分词模型路径
ldir = r'D:\DATA SCIENCE\djangoProject1\APP2\nlp\ltp_data_v3.4.0\cws.model'
#词性标注模型路径
pdir = r'D:\DATA SCIENCE\djangoProject1\APP2\nlp\ltp_data_v3.4.0\pos.model'
#命名实体模型路径
math1_path = r'D:\DATA SCIENCE\djangoProject1\APP2\nlp\ltp_data_v3.4.0\ner.model'  #LTP命名实体识别模型库

#文件路径
filepath1='/Users/hanjiaxi/PycharmProjects/nlp/pre_data/test'
filepath2='/Users/hanjiaxi/PycharmProjects/nlp/pre_data/text'
filepath3='result'
filepath4=r'D:\DATA SCIENCE\djangoProject1\APP2\nlp\中文分词\分词算法\jieba_cutter\stopwords'

#找到所有名词
noun=['n','nh','ni','ns','nl','nz','b','i','r','m'] #一般名词，地点名词，时间名词，位置，机构，其他专有名词，名词修饰词
time=['nt']
loc=['ns']

#命名实体
name_net=['S-Nh']
loc_net=['S-Ni','S-Ns']

#设置stopwords
stop_words=[]
def stopwords(filepath):
	with open(filepath,'rt',encoding='GB18030') as f1:
		for line in f1.readlines():
			line = line.strip('\n')
			stop_words.append(line)

#中文分词
def ltp_cut(content):
		segmentor = Segmentor()  # 初始化实例
		dicdir = 'D:\\DATA SCIENCE\\djangoProject1\\分词\\中文分词\\分词算法\\词典合集\\wiki_baike_law_doc.dic'
		segmentor.load_with_lexicon(ldir, dicdir)  # 加载模型
		words = segmentor.segment(content)  # 分词
		words = list(words)  # 转换list
		segmentor.release()  # 释放模型
		with open(filepath3, "w", encoding='utf8') as f3:
			for word in words:
				f3.write(word + "/")
		return words


#---------词性标注
def ltp_pos(words):
	pos = Postagger()  # 初始化实例
	pos.load(pdir)  # 加载模型
	postags = pos.postag(words)  # 词性标注
	postags = list(postags)
	pos.release()
	return postags

#---------生成分词和词性的字典
def dict_wordpos(words,postags):
	dict_data=dict(zip(words,postags))
	return dict_data

#---------在字典中删掉固定词性的词语
def delete_POS(words,postags,list):
	dict_data=dict_wordpos(words,postags)
	for x in dict_data.keys():
		if dict_data.get(x) in list:
			del dict_data[x]

#---------在words和字典中删掉stopwords（返回words 和 字典）
def delete_stopwords(words,posags):
	for x in words:
		if x in stop_words:
			words.remove(x)
	dict_data=dict_wordpos(words,posags)
	for x in dict_data.keys():
		if x not in words:
			del dict_data[x]
	return words

#筛选制定词性的词语
def select_POS(words,postags,list):
	all_list=find_all(list,dict_wordpos(words,postags))
	true_list=remove_repeat(find_continuous(list,words,postags))

	return true_list

#1.找出所有指定属性的词语
def find_all(list,dict):
	fixed_list=[]
	for x in dict.keys():
		if dict.get(x) in list:
			fixed_list.append(x)
	return fixed_list

#2.找到连续的指定词语词语
def find_continuous(list,words,postags):
	continuous_list=[]
	for i in range(0, len(words)):
		if postags[i] in list:
			j = i
			while (postags[j] in list):
				j = j + 1
				if j>=len(postags):break

			continuous_list.append(''.join(words[i:j]))
	return continuous_list

#3.去掉重复的词语
def remove_repeat(continuous_list):
	# 去除重复元素
	remove_list = []
	for x in continuous_list:
		for y in continuous_list:
			if x != y and x in y:
				remove_list.append(x)
	true_list = []
	for x in continuous_list:
		if x not in remove_list:
			true_list.append(x)
	true_list=set(true_list)
	return true_list


#----------命名实体识别
def ltp_net(words,postags):
	recognizer = NamedEntityRecognizer() # 初始化实例
	recognizer.load(math1_path)#加载实体识别库
	netags = recognizer.recognize(words, postags) # 命名实体识别，这里的words是分词的结果，postags是词性标注的结果
	return netags

#----------生成命名实体字典
def dict_wordnet(words,postags):
	dict_data2=dict(zip(words,ltp_net(words,postags)))
	return dict_data2

#-----------实体识别某些特定的属性
def get_net(list,words,postags):
	request_list = []
	dict=dict_wordnet(words,postags)
	for x in dict.keys():
		if dict.get(x) in list :
			request_list.append(x)
	return request_list


import jieba
import jieba.posseg as pseg  # 词性标注
import jieba.analyse as anls  # 关键词提取

# 加入停用词库
def stopwords():
    jieba.analyse.set_stop_words(r'D:\DATA SCIENCE\djangoProject1\APP2\nlp\中文分词\分词算法\词典合集\stopwords')

'''
# 加入idf词库
def idf_path():
    jieba.analyse.TFIDF(idf_path='../词典合集/lawa_term.dic')
'''



# 加入自定义词典
def self_dic():
    jieba.load_userdict(r'D:\DATA SCIENCE\djangoProject1\APP2\nlp\中文分词\分词算法\词典合集\new_dict')


# jieba分词精确模式
def jieba_exact(content, filepath3):
        words = jieba.cut(content, cut_all=False)
        with open(filepath3, "w", encoding='utf8') as f3:
            for word in words:
                f3.write(word + "/")


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
filepath1 = '/Users/hanjiaxi/PycharmProjects/nlp/pre_data/test'
filepath2 = '/Users/hanjiaxi/PycharmProjects/nlp/pre_data/text'
jieba_pos(filepath2)
'''

'''
tfidf(filepath2,20,True,None)
textrank(filepath2,20,True,None)
mix_tfidf_textrank(filepath2,20,True,None,0.3)
'''
