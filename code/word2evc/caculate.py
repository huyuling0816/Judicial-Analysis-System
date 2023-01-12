import logging
from gensim.models import word2vec
import numpy as np
from scipy import linalg

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s',
    level=logging.INFO)

# 使用gensim中的word2vec模块
sentences = word2vec.LineSentence('/Users/hanjiaxi/PycharmProjects/分词/word2evc/案件.txt')
model = word2vec.Word2Vec(sentences, hs=1, min_count=1, window=5, vector_size=100)

# 将所有单词的词向量相加求平均值，得到的向量即为句子的向量
def sentence_vector(s):
    print(s)
    words = s.split(" ")
    v = np.zeros(100)
    for word in words:
        v += model.wv[word]
    v /= len(words)
    print(type(v))
    print(v)
    return v

# 计算两个句子之间的相似度:将两个向量的夹角余弦值作为其相似度
def vector_similarity(s1, s2):
    v1, v2 = sentence_vector(s1), sentence_vector(s2)
    return np.dot(v1, v2) / (linalg.norm(v1) * linalg.norm(v2))


with open("/Users/hanjiaxi/PycharmProjects/分词/word2evc/案件.txt", "r", encoding="utf-8") as f:
    contents = f.readlines()
    matrix = np.zeros((len(contents), len(contents)))
    for i in range(len(contents)):
        for j in range(len(contents)):
            # 使用矩阵存储所有案件之间的相似度
            matrix[i][j] = vector_similarity(
                contents[i].strip(), contents[j].strip())

    f1 = open("/Users/hanjiaxi/PycharmProjects/分词/word2evc/result", "w", encoding="utf-8")
    for j in range(len(contents)):
        # 获取最为相似的案件
        # 注意：每个案件与自己的相似度为1，因此获取的是相似度第二大的案件
        index = np.argsort(matrix[j])[-2]

        f1.writelines("案件" + str(j + 1) + ":" + '\t')
        f1.writelines(contents[j])
        f1.writelines("案件" + str(index + 1) + ":" + '\t')
        f1.writelines(contents[index])
        f1.writelines("相似度： " + str(matrix[j][index]) + '\n\n')


