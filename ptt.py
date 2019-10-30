#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 13:49:48 2018

@author: snoopyknight
"""

from bs4 import BeautifulSoup
import requests 
import pandas as pd
from pandas import Series
import numpy as np
from multiprocessing import Process
import jieba
import jieba.posseg
import time



def Gossip_craw(start,end):    
    payload = {
        'from':'/bbs/Gossiping/index.html',
        'yes':'yes'
    }
    
    rs = requests.session()
    res = rs.post('https://www.ptt.cc/ask/over18', data = payload)
    
    article =[]
    link = []
    for i in range(start,end):
        url = 'https://www.ptt.cc/bbs/HatePolitics/index' + str(i) + '.html'
        res = rs.get(url)
        soup = BeautifulSoup(res.text,'lxml')
        data = soup.find_all('div','r-ent')
        for r_ent in data:
            title = r_ent.find('div','title').text
            if(title.find(u"柯文哲") >=0 or title.find(u"柯P") >= 0 or title.find(u"柯") >= 0 or title.find(u"柯市長")>=0):
                for a in r_ent.find_all('a', href=True): #ignore the articles which was deleted           
                    print(title)
                    #print(a['href'])
                    article.append(title)
                    link.append(a['href'])
        
                        
    df = pd.DataFrame({'article':article, 'link':link}) 
    
    #df['push_content'] = Series(np.random.randn(len(df.article)), index=df.index)
    df['push_content'] = Series()
    for i in range(len(df.article)):
        each_page = 'https://www.ptt.cc' + str(link[i])
        print(df.article[i])
        res2 = rs.get(each_page)
        soup = BeautifulSoup(res2.text,'lxml')
        push = soup.find_all('div','push') 
        
        tmp_list = []
        for p in push:
            try:            
                push_content = p.find('span','f3 push-content').text
                tmp_list.append(push_content)
                df.push_content[i] = tmp_list
            except AttributeError:
                continue
    return(df)



def cut(filename):
    jieba.initialize('Jieba_tutorial-master/dict/dict.txt.big')
    
    df = pd.read_csv(filename)
    jieba.load_userdict('Jieba_tutorial-master/dict/PTTdict.txt')
    
    seg_list = []    
    for i in range(len(df.article)):
        try:
            string = df.push_content[i]
            seg = jieba.lcut(string)
            seg_list.append(seg)    
        except AttributeError:
            continue
        
    df['word'] = Series()    
    for i in range(len(df.article)):
        try:
            df.word[i] = seg_list[i]
        except IndexError:
            continue
         
    print(df.tail())
    return df



def main():
    start = 1
    end = 4032
    data = Gossip_craw(start,end)
    data.to_csv('ptt1.csv')
    result = cut('ptt1.csv')
    result = result.drop(columns = ['push_content'])
    #result.to_csv('ptt_' , str(start) , ' - ' , str(end) ,'.csv')
    result.to_csv('hate.csv')

        
    
if __name__ == '__main__':
    start = time.time()
    p = Process(target = main)
    p.start()
    p.join()
    end = time.time()
    print("Total time:", end-start)

