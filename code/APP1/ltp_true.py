import pyltp
from pyltp import SentenceSplitter
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer
import unicodedata as ucd
from pyltp import Parser
from pyltp import SementicRoleLabeller
"""
from 预处理数据 import 数据处理方法
"""

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

def getText(filename):
    f = open(filename, encoding='GB18030')
    content = []
    for line in f.readlines():
        temp = ucd.normalize('NFKC', line.strip('\n')).replace(' ', '') # 去掉列表中每一个元素的换行符
        content.append(temp.replace('"',''))  # 去掉双引号
    f.close()
    return ''.join(content)


#相关内容
"""

数据处理方法.preprocess_data(filepath1=filepath1,filepath2=filepath2,choice=False)
select_POS(noun)
get_net(name_net)
"""

"""
#依存分析
math2_path = '/Users/hanjiaxi/ltp_data_v3.4.0/parser.model'#LTP依存分析模型库
parser = Parser() # 初始化实例
parser.load(math2_path)#加载依存分析库
arcs = parser.parse(words, postags) # 句法分析，这里的words是分词的结果，postags是词性标注的结果
print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs) )



#语义角色
math2_path = "/Users/hanjiaxi/ltp_data_v3.4.0/pisrl.model"#LTP语义角色标注模型库
labeller = SementicRoleLabeller() # 初始化实例
labeller.load(math2_path)#加载语义标注库
roles = labeller.label(words, postags, arcs) # 语义角色标注,这里的words是分词结果，postags是词性标注结果，arcs是依存句法分析结果

"""

# content = getText('D:/南京大学0/数据科学大作业相关/爬取文书文件/交通肇事/交通事故/季益军交通肇事罪刑事一审刑事判决书.txt')
# print(ltp_cut(content=content))