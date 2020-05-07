import math
import jieba #结巴分词
import os
import re
import codecs

data_path = 'C:/Users/黎月明/Desktop/毕业论文/匹配.csv'
text = data_input.get_search_data(data_path, train_size, test_size)

f = [] # 列表的每一个元素是一个dict，dict存储着一个文档中每个词的出现次数
tf = {} # 储存每个词以及该词出现的文本数量
idf = {} # 储存每个词的idf值
k1 = 1.5
b = 0.75
def inition(docs):
    D = len(docs)
    avgdl = sum([len(doc)+ 0.0 for doc in docs]) / D
    for doc in docs:
        tmp = {}
        for word in doc:
            tmp[word] = tmp.get(word, 0) + 1  # 存储每个文档中每个词的出现次数
        f.append(tmp)
        for k in tmp.keys():
            tf[k] = tf.get(k, 0) + 1
    for k, v in tf.items():
        idf[k] = math.log(D - v + 0.5) - math.log(v + 0.5)
    return D, avgdl
def sim(doc, index):
    score = 0.0
    for word in doc:
        if word not in f[index]:
            continue
        d = len(document[index])
        score += (idf[word] * f[index][word] * (k1 + 1) / (f[index][word] + k1 * (1 - b + b * d / avgdl)))
    return score

def simall(doc):
    scores = []
    for index in range(D):
            score = sim(doc, index)
            scores.append(score)
    return scores

stop = set()
fr = codecs.open('C:/Users/黎月明/Desktop/word_bag/train_word_bag/hlt_stop_words.txt', 'r', 'utf-8')
for word in fr:
    stop.add(word.strip())
fr.close()
re_zh = re.compile('([\u4E00-\u9FA5]+)')

def filter_stop(words):
    return list(filter(lambda x: x not in stop, words))

def get_sentences(doc):
    line_break = re.compile('[\r\n]')
    delimiter = re.compile('[，。？！；]')
    sentences = []
    for line in line_break.split(doc):
        line = line.strip()
        if not line:
            continue
        for sent in delimiter.split(line):
            sent = sent.strip()
            if not sent:
                continue
            sentences.append(sent)
    return sentences

sents = get_sentences(text)
doc = []
for sent in sents:
    words = list(jieba.cut(sent))
    words = filter_stop(words)
    doc.append(words)
print(doc)
document = doc