import logging
from gensim.models import word2vec
import numpy as np
from scipy import linalg

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s',
    level=logging.INFO)

# ʹ��gensim�е�word2vecģ��
sentences = word2vec.LineSentence('/Users/hanjiaxi/PycharmProjects/�ִ�/word2evc/����.txt')
model = word2vec.Word2Vec(sentences, hs=1, min_count=1, window=5, vector_size=100)

# �����е��ʵĴ����������ƽ��ֵ���õ���������Ϊ���ӵ�����
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

# ������������֮������ƶ�:�����������ļн�����ֵ��Ϊ�����ƶ�
def vector_similarity(s1, s2):
    v1, v2 = sentence_vector(s1), sentence_vector(s2)
    return np.dot(v1, v2) / (linalg.norm(v1) * linalg.norm(v2))


with open("/Users/hanjiaxi/PycharmProjects/�ִ�/word2evc/����.txt", "r", encoding="utf-8") as f:
    contents = f.readlines()
    matrix = np.zeros((len(contents), len(contents)))
    for i in range(len(contents)):
        for j in range(len(contents)):
            # ʹ�þ���洢���а���֮������ƶ�
            matrix[i][j] = vector_similarity(
                contents[i].strip(), contents[j].strip())

    f1 = open("/Users/hanjiaxi/PycharmProjects/�ִ�/word2evc/result", "w", encoding="utf-8")
    for j in range(len(contents)):
        # ��ȡ��Ϊ���Ƶİ���
        # ע�⣺ÿ���������Լ������ƶ�Ϊ1����˻�ȡ�������ƶȵڶ���İ���
        index = np.argsort(matrix[j])[-2]

        f1.writelines("����" + str(j + 1) + ":" + '\t')
        f1.writelines(contents[j])
        f1.writelines("����" + str(index + 1) + ":" + '\t')
        f1.writelines(contents[index])
        f1.writelines("���ƶȣ� " + str(matrix[j][index]) + '\n\n')


