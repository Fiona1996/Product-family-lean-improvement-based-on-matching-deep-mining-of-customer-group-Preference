import pickle
from sklearn.datasets.base import Bunch
from sklearn.feature_extraction.text import TfidfVectorizer
#from Tools import readbunchobj, writebunchobj

def readbunchobj(path):
   file_obj=open(path,"rb")
   bunch=pickle.load(file_obj)
   file_obj.close()
   return bunch
def writebunchobj(path,bunchobj):
   file_obj=open(path,"wb")
   pickle.dump(bunchobj,file_obj)
   file_obj.close()

def readfile(path):
    with open(path, "rb") as fp:
        content = fp.read()
    return content

def vector_space(stopword_path, bunch_path, space_path, train_tfidf_path=None):

    stpwrdlst = readfile(stopword_path).splitlines()

    bunch = readbunchobj(bunch_path)

    tfidfspace = Bunch(target_name=bunch.target_name, label=bunch.label, filenames=bunch.filenames, tdm=[],

                       vocabulary={})

    if train_tfidf_path is not None:

        trainbunch = readbunchobj(train_tfidf_path)

        tfidfspace.vocabulary = trainbunch.vocabulary

        vectorizer = TfidfVectorizer(stop_words=stpwrdlst, sublinear_tf=True, max_df=0.5,

                                     vocabulary=trainbunch.vocabulary)

        tfidfspace.tdm = vectorizer.fit_transform(bunch.contents)

    else:

        vectorizer = TfidfVectorizer(stop_words=stpwrdlst, sublinear_tf=True, max_df=0.5)

        tfidfspace.tdm = vectorizer.fit_transform(bunch.contents)

        tfidfspace.vocabulary = vectorizer.vocabulary_

    writebunchobj(space_path, tfidfspace)

    print("if-idf词向量空间实例创建成功！！！")

if __name__ == '__main__':

    stopword_path = "C:/Users/黎月明/Desktop/word_bag/train_word_bag/hlt_stop_words.txt"
    bunch_path = "C:/Users/黎月明/Desktop/word_bag/train_word_bag/train_set.dat"
    space_path = "C:/Users/黎月明/Desktop/word_bag/train_word_bag/tfdifspace.dat"
    vector_space(stopword_path, bunch_path, space_path)

    bunch_path = "C:/Users/黎月明/Desktop/word_bag/test_word_bag/test_set.dat"
    space_path = "C:/Users/黎月明/Desktop/word_bag/test_word_bag/testspace.dat"
    train_tfidf_path = "C:/Users/黎月明/Desktop/word_bag/train_word_bag/tfdifspace.dat"
    vector_space(stopword_path, bunch_path, space_path, train_tfidf_path)