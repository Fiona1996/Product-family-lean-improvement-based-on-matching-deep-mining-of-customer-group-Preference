import numpy as np
import re
import jieba
import jieba.posseg as pseg
import string
punc = string.punctuation
punc+="。；！"

file1 = open('middle_file/star&review1.txt','r',encoding='utf-8')
reviewlist1=list()
for c in file1.readlines():
    c=c.replace('\ufeff', '')
    c=c.replace('\n', '')
    c_array=c.split("\t")
    reviewlist1.append(c_array)

file2 = open('middle_file/attr_lec.txt','r',encoding='utf-8')
attrlist=list()
for c in file2.readlines():
    c=c.replace('\ufeff', '')
    c=c.replace('\n', '')
    c_array=c.split("\t")
    attrlist.append(c_array)

file2.close()

file4 = open('middle_file/req_lec.txt','r',encoding='utf-8')
reqlist=list()
for c in file4.readlines():
    c=c.replace('\ufeff', '')
    c=c.replace('\n', '')
    c_array=c.split("\t")
    reqlist.append(c_array)
#print(reqlist[0])
file4.close()

#%%

#删除任何不含属性需求、情感的评论
print (len(reviewlist1))
wordlist=list()
for item in attrlist:
    wordlist.append(item[1])
for item in reqlist:
    wordlist.append(item[1])
#去掉不规则数据
for review in reviewlist1:
    if len(review)!=3:
        reviewlist1.remove(review)
for review in reviewlist1:
    flag = 0
    for item in wordlist:
        if item.lower() in review[2].lower():
            flag = 1
            break
    if flag == 0:
        reviewlist1.remove(review)
print (len(reviewlist1))

#%%

def hasDeny(sentence_list,i):
    deny_dict=['不','不是','没','防','没有','很不','无','无法','不能']
    #print (i,'____',sentence_list[i])
    for index in range(i-1,-1,-1):
        if sentence_list[index] in deny_dict:
            #print ('hahaha','____',sentence_list[index] )
            return -1
        if len(sentence_list[index])==0:
            break
    return 1

#%%

def reviewMat(sentence):
    array = list()
    sentence+='。'
    sentence_list=jieba.lcut(str(sentence.lower()),cut_all=True)
    #for i in range(0,len(sentence_list),1):print (i,'  ',sentence_list[i])
    a1=searchReq("boot speed",finaAttr("boot speed",sentence_list),sentence_list)
    a2=searchReq("screen",finaAttr("screen",sentence_list),sentence_list)
    a3=searchReq("system",finaAttr("system",sentence_list),sentence_list)
    a4=searchReq("price",finaAttr("price",sentence_list),sentence_list)
    a5=searchReq("peripherals",finaAttr("peripherals",sentence_list),sentence_list)
    a6=searchReq("services",finaAttr("services",sentence_list),sentence_list)
    #a7=searchReq("bluetooth",finaAttr("bluetooth",sentence_list),sentence_list)
    a8=searchReq("memory",finaAttr("memory",sentence_list),sentence_list)
    #a9=searchReq("gps",finaAttr("gps",sentence_list),sentence_list)
    a10=searchReq("appearance",finaAttr("appearance",sentence_list),sentence_list)
    a11=searchReq("features",finaAttr("features",sentence_list),sentence_list)
    #a12=searchReq("app",finaAttr("app",sentence_list),sentence_list)
    a13=searchReq("cooling",finaAttr("cooling",sentence_list),sentence_list)
    a14=searchReq("logistics",finaAttr("logistics",sentence_list),sentence_list)
    a15=searchReq("CPU",finaAttr("CPU",sentence_list),sentence_list)
    a16=searchReq("battery",finaAttr("battery",sentence_list),sentence_list)
    #a1...添加进array,并转化成矩阵
    array.append(a1)
    array.append(a2)
    array.append(a3)
    array.append(a4)
    array.append(a16)
    array.append(a5)
    array.append(a6)
    #array.append(a7)
    array.append(a8)
    #array.append(a9)
    array.append(a10)
    array.append(a11)
    #array.append(a12)
    array.append(a13)
    array.append(a14)
    array.append(a15)

    newarray=list()
    for item in array:
        mysum=0
        for num in item:
            mysum+=num
        if mysum<0:
            newarray.append(0)
            newarray.append(mysum)
        else:
            newarray.append(mysum)
            newarray.append(0)
    return newarray

def finaAttr(attrtype,sentence_list):
    #print (sentence_list)
    attrIndex=list()
    for item in attrlist:
        if item[0] == attrtype:
            i = -1
            for seq in sentence_list:
                i = i+1
                seqstr = seq.strip()
                #if len(seqstr)>0 and (item[1].lower() in seqstr or seqstr in item[1].lower()):
                if len(seqstr)>0 and item[1].lower() in seqstr == seqstr:
                    attrIndex.append(i)
    attrIndex = list(set(attrIndex))
    return attrIndex
# 找这些属性词对应的需求词，返回对应该类属性的一行数组
def searchReq(attrtype,attrindex_list,sentence_list):
    #向左找，定位上一个属性词，该属性词到上一属性词后的标点为搜索范围
    #向右找，定位下一个属性词，该属性词到下一属性词前的标点为搜索范围
    #print(attrindex_list)
    req_temlist=list()
    req_senti=[0,0,0,0,0,0,0,0]
    if len(attrindex_list)>0:
        for index in attrindex_list:
            left=0
            right=index
            for left in range(index-1,-1,-1):
                if isAttr(sentence_list[left]):
                    #print (left,"___",sentence_list[left])
                    break
            for right in range(index+1,len(sentence_list),1):
                if isAttr(sentence_list[right]):
                    break
            for x in range(left+1,index,1):
                #print (sentence_list[x],isStop(sentence_list[x]))
                if isStop(str(sentence_list[x])):
                    left = x+1
                    break
            for x in range(right-1,index,-1):
                if isStop(str(sentence_list[x])):
                    right =x
                    break
            #print ("寻找属性",attrtype,"位置为：",left,"___",right)
            for i in range(left,right,1):
                if isReq(sentence_list[i]):
                    reqtype = reqType(sentence_list[i])
                    req_temlist.append([sentence_list[i],reqtype,i])
    if len(req_temlist)>0:
        #print ("对应de 属性词为：",attrtype,"_____",req_temlist)
        for req in req_temlist:
            if req[1]=="pos":req_senti[0]=hasDeny(sentence_list,req[2])*isPorN(str(req[0]))
            if req[1]=="neg":req_senti[1]=hasDeny(sentence_list,req[2])*isPorN(str(req[0]))
            if req[1]=="net":req_senti[2]=hasDeny(sentence_list,req[2])*isPorN(str(req[0]))
    return req_senti
def isPorN(req):
    #情感词典中判断，不在情感词典中默认积极为1
    flag = 1
    for item in reqlist:
        if req.lower() == item[1].lower():
            #print (req,"  hahah  ", item[5])
            if "N" in item[5]: flag=-1
            break
    #print (req , flag)
    return flag
def isAttr(word):
    flag=0
    for item in attrlist:
        if word.lower() == item[1].lower():
            flag=1
            break
    if flag ==1:return 1
    else: return 0
def isReq(word):
    flag=0
    for item in reqlist:
        if word.lower() == item[1].lower():
            flag=1
            break
    if flag ==1:return 1
    else: return 0
def reqType(req):
    type="basic"
    for item in reqlist:
        if req.lower() == item[1].lower():
            type = item[0]
            break
    return type
# 结巴分词把所有标点替换成空项
def isStop(word):
    flag = 0
    if len(word)<1 or word.strip() in punc:
        flag = 1
    return flag

#%%


file = open('reviews.txt','w',encoding='utf-8')
reviewarray=list()
for review in reviewlist1:
    #print (review)
    if len(review)==3:
        array=reviewMat(review[2])
        reviewarray.append([review[0],review[1],review[2],array])
        tmparray=[review[0],review[1],str(review[2]),str(array)]
        file.write("?/?/".join(tmparray) +'\n')
#print (reviewarray)
file.close()