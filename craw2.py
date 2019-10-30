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
import time

def main():
    start = 37930 
    end = 38943
    
    payload = {
        'from':'/bbs/Gossiping/index.html',
        'yes':'yes'
    }
    
    rs = requests.session()
    res = rs.post('https://www.ptt.cc/ask/over18', data = payload)    
# =============================================================================
#     res = rs.get('https://www.ptt.cc/bbs/Gossiping/index.html')
#     soup = BeautifulSoup(res.text,'lxml')
#     data = soup.find_all('div','r-ent')
#     for r_ent in data:
#         title = r_ent.find('div','title').text
#         print(title)
# =============================================================================
    article =[]
    link = []
    for i in range(start,end):
        url = 'https://www.ptt.cc/bbs/Gossiping/index' + str(i) + '.html'
        res = rs.get(url)
        soup = BeautifulSoup(res.text,'lxml')
        data = soup.find_all('div','r-ent')
        for r_ent in data:
            title = r_ent.find('div','title').text
            if(title.find(u"柯文哲") > 0):
                for a in r_ent.find_all('a', href=True): #ignore the articles which doesn't exist           
                    #print(a['href'])
                    article.append(title)
                    link.append(a['href'])
                    
    
    df = pd.DataFrame({'article':article, 'link':link})
    
    #print(df.head())
    #print(df.article[1])
    
    df['push_content'] = Series(np.random.randn(len(df.article)), index=df.index)
    for i in range(len(df.article)):
        each_page = 'https://www.ptt.cc' + str(link[i])
        print(df.article[i])
        #print(each_page)
        res2 = rs.get(each_page)
        soup = BeautifulSoup(res2.text,'lxml')
        push = soup.find_all('div','push') 
        
        tmp_list = []
        for p in push:            
            push_content = p.find('span','f3 push-content').text
            tmp_list.append(push_content)
        #print(len(tmp_list[1]))
        df.push_content[i] = tmp_list
# =============================================================================
#         for i in range(len(df.article)): 
#             df.push_content[i] = tmp_list[i]
# =============================================================================
        
    df.to_csv('title2.csv')
    
if __name__ == '__main__':
    start = time.time()    
    p = Process(target = main)
    p.start()
    p.join()
    end = time.time()    
    print("ececution time : ",end - start)
