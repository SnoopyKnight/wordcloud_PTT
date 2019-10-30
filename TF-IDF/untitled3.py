# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 15:56:55 2018

@author: Chunbi
"""
import pandas as pd
import jieba.analyse
import numpy as np
import csv
import operator
from itertools import combinations
a = jieba.analyse.extract_tags("", topK=20, withWeight=True, allowPOS=())
x = []
xx = ''
df = pd.read_csv("gossiping.csv" )
for i in range(0,len(df)):
    if(type(df['word'][i]) == str):
        df2 = df['word'][i]
        df2 = jieba.analyse.extract_tags(df2, topK=10, withWeight=False, allowPOS=())
#        df2 = df2.replace("\"","")
#        df2 = df2.replace('\'','')
#        df2 = df2.replace(' , ,,  , , :,  , ','')
#        df2 = df2.replace(' ','')
#        df2 = df2.replace('[[,,:,,','')
#        df2 = df2.replace(',/','')
#        df2 = df2.replace('\\','')
#        df2 = df2.replace(':','')
#        df2 = df2.replace('.','')
#        df2 = df2.replace(']]','')
#        df2 = df2.replace(',',' ')
#        
#        df2 = ' '.join(map(str, df2))
#    print(i)
        x += df2
        
from sklearn.feature_extraction.text import TfidfTransformer  
from sklearn.feature_extraction.text import CountVectorizer  

output = ''
list_of_tuple = list(combinations(set(x), 1)) #任兩人一組合的組合數.
for j in range(0,len(list_of_tuple)):
    output += list_of_tuple[j][0]+ '\n'

lot = list_of_tuple
output2 = ''
for i in range(0,len(lot)):
    count = output.count(lot[i][0])
    if(count != 0):
        output2 += lot[i][0]
        output2 += ',' + str(count)
        output2 += '\n'


with open('output2.csv', 'w',encoding = 'utf8') as f:
    f.write(output2)
    
df3 = pd.read_csv('output2.csv', header=None,encoding = 'utf8').sort_values ([1],0,False)
df3.to_csv('output2.csv' ,header=None,index = False)

corpus = x
# =============================================================================
# vectorizer=CountVectorizer()
# 
# transformer = TfidfTransformer()
# tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))  
# #print (tfidf)
# 
# from sklearn.feature_extraction.text import TfidfVectorizer
# tfidf2 = TfidfVectorizer()
# re = tfidf2.fit_transform(corpus)
# #print (re)
# =============================================================================
# =============================================================================
# 
# 
# corpus=["我,来到,北京,清华大学",#第一类文本切词后的结果，词之间以空格隔开  
#     "他,来到,了,网易,杭研,大厦",#第二类文本的切词结果  
#     "小明,硕士,毕业,与,中国,科学院",#第三类文本的切词结果  
#     "我,爱,北京,天安门"]#第四类文本的切词结果  
# =============================================================================

#vectorizer=CountVectorizer()#该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频  
#transformer=TfidfTransformer()#该类会统计每个词语的tf-idf权值  
#tfidf=transformer.fit_transform(vectorizer.fit_transform(corpus))#第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵  
#word=vectorizer.get_feature_names()#获取词袋模型中的所有词语  
#weight=tfidf.toarray()#将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重  
#dic = {}
#
#for i in range(len(weight)):#打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重  
##    print (u"-------这里输出第",i,u"类文本的词语tf-idf权重------")  
#    for j in range(len(word)):  
#        if(weight[i][j] != 0):
#            dic[word[j]] = weight[i][j]
##            print (word[j],weight[i][j] )
#sorted_x = sorted(dic.items(), key=operator.itemgetter(1))
#sorted_x.reverse()
#print(sorted_x)
#
#with open('dfidf.txt', 'w',encoding = 'utf8') as fp:
#    fp.write('\n'.join('%s %s' % x for x in sorted_x))