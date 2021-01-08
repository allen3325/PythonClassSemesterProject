from bs4 import BeautifulSoup
import threading
import requests
import re
import csv
import numpy as np
import time as tm
import pandas as pd
import collections
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
URLStatic='https://www.etax.nat.gov.tw/etw-main/web/ETW183W3_'
lock=threading.Lock()
def Static():
    global SpecialPrizeitemlist
    global SpecialPrizearealist
    global SpecPrizeitemlist
    global SpecPrizearealist
    global start
    global CatchedSite
    visitedSite=[]
    S_year=[str(x) for x in range(102,110)]
    S_month=[str(x) for x in range(1,13)]
    for a in range(len(S_month)):
        if(int(S_month[a])<10):
            S_month[a]='0'+S_month[a]
    S_begin=input('請輸入要統計的起始(yyy/mm):').split('/')
    S_end=input('請輸入要統計的結束點(yyy/mm):').split('/')
    start=tm.time()
    '''
    print(S_year.index(S_begin[0]))
    print(S_year.index(S_end[0]))
    print(range(int(S_year.index(S_begin[0])),int(S_year.index(S_end[0]))+1))
    print(range(int(S_month.index(S_begin[1])),int(S_month.index(S_end[1]))+1))
    '''
    
    #將要抓的年度月份區間存入list
    for i in range(int(S_year.index(S_begin[0])),int(S_year.index(S_end[0])+1)):
        #只抓單年度
        if(S_begin==S_end):
            for j in range(int(S_month.index(S_end[1])),int(S_month.index(S_end[1])+1)):
                if(int(S_month[j])%2==0):
                    idxmth=j-1
                else:
                    idxmth=j
                website=URLStatic+S_year[i]+S_month[idxmth]
                if(website not in visitedSite):
                    visitedSite.append(website)
        else:
            if(S_year[i]==S_begin[0]):
                if(S_year[i]==S_end[0]):
                    for j in range(int(S_month.index(S_begin[1])),int(S_month.index(S_end[1])+1)):
                        if(int(S_month[j])%2==0):
                            idxmth=j-1
                        else:
                            idxmth=j
                        website=URLStatic+S_year[i]+S_month[idxmth]
                        if(website not in visitedSite):
                            visitedSite.append(website)
                else:
                    for j in range(int(S_month.index(S_begin[1])),len(S_month)):
                        if(int(S_month[j])%2==0):
                            idxmth=j-1
                        else:
                            idxmth=j
                        website=URLStatic+S_year[i]+S_month[idxmth]
                        if(website not in visitedSite):
                            visitedSite.append(website)
            else:
                if(S_end[0]==S_year[i]):
                    for j in range(0,int(S_month.index(S_end[1])+1)):
                        if(int(S_month[j])%2==0):
                            idxmth=j-1
                        else:
                            idxmth=j
                        website=URLStatic+S_year[i]+S_month[idxmth]
                        if(website not in visitedSite):
                            visitedSite.append(website)
                else:
                    for j in range(len(S_month)):
                        if(int(S_month[j])%2==0):
                            idxmth=j-1
                        else:
                            idxmth=j
                        website=URLStatic+S_year[i]+S_month[idxmth]
                        if(website not in visitedSite):
                            visitedSite.append(website)

    #做Thread多工抓    
    t_list = []
    #print(visitedSite)
    #lock = threading.Lock()
    for Site in visitedSite:
        t1 = threading.Thread(target=CatchStatic, args=(Site,))
        #print(t_Site)
        t_list.append(t1)
        t_list[len(t_list)-1].start()
        CatchStatic(Site)
    #print(len(visitedSite))
    #print(t_list)
    '''for t in t_list:
        t.start()'''
    for t in t_list:
        t.join()
    print(tm.time()-start)
    #print(SpecialPrizeitemlist)
    #print(SpecialPrizearealist)
    #print(SpecPrizeitemlist)
    #print(SpecPrizearealist)

    #抓完資料，畫圖
    #print(set(SpecialPrizeitemlist))
    #x_labels=[ item for item in x1] 
    Draw(SpecialPrizeitemlist,'SpecialPrizeitemlist')
    Draw(SpecialPrizearealist,'SpecialPrizearealist')
    Draw(SpecPrizeitemlist,'SpecPrizeitemlist')
    Draw(SpecPrizearealist,'SpecPrizearealist')

    

def Draw(Data,name):
    '''
    NPData=np.array(Data)
    a=collections.Counter(NPData)
    print(a)

    VALUE=list(a.values())
    KEY=list(a.keys())
    size=max(len(KEY),max(VALUE))
    if(size>=30):
        if('item' not in name):
            size/=10
        else:
            size/=5

    
    plt.figure()
    font = FontProperties(fname='msjh.ttc', size=10)
    plt.xticks(range(len(a.keys())),a.keys(),fontproperties=font)
    plt.yticks(range(max(a.values())),a.values(),fontproperties=font)
    #print(KEY,VALUE)
    plt.hist(dict(a))
    plt.tick_params(axis='x', rotation=90)
    plt.savefig(name+'.png')
    '''
    Data=sorted(Data)
    XT=sorted(set(Data))
    ATMP=len(XT)
    #print(Data)
    plt.figure(figsize=(ATMP,ATMP))
    font = FontProperties(fname='msjh.ttc', size=10)
    #print(XT)
    plt.xticks(range(ATMP),XT,fontproperties=font)
    plt.tick_params(axis='x', rotation=90)
    plt.hist(Data,bins=ATMP)
    plt.savefig(name+'test.png')

#抓資料
'''
WARNING!!!
103/01~105/11的item格式為'食品和飲料共88元,飲料2杯共65元,食品和飲料共70元,飲料20元'
106/01~10907的item格式為'食品*3，共371元'
'''
def CatchStatic(Site):
    
    if(Site not in CatchedSite):
        CatchedSite.append(Site)
        html = requests.get(Site).content.decode('utf-8')
        lock.acquire()
        global SpecialPrizeitemlist
        global SpecialPrizearealist
        global SpecPrizeitem
        global SpecPrizearea
        sp = BeautifulSoup(html,'html.parser')
        #SpecialPrize
        for SpecialPrizeitem,SpecialPrizearea in zip(sp.find_all('td',headers='tranItem'),sp.find_all('td',headers='companyAddress')):
            #print(item.text,area.text)
            SpecialPrizeItem=set(re.split(r"[元,*，、及和\d共項杯計。等盒瓶個組包開器 ]",SpecialPrizeitem.text))
            if('' in SpecialPrizeItem):
                SpecialPrizeItem=list(SpecialPrizeItem)
                SpecialPrizeItem.remove('')
            for temp in list(SpecialPrizeItem):
                SpecialPrizeitemlist.append(temp)
            SpecialPrizearealist.append(re.split(r"[市縣]",SpecialPrizearea.text)[0])
        #SpecPrize
        for SpecPrizeitem,SpecPrizearea in zip(sp.find_all('td',headers='tranItem2'),sp.find_all('td',headers='companyAddress2')):
            SpecPrizeItem=set(re.split(r"[元,*，、及和\d共項杯計。等盒瓶個組包開器 ]",SpecPrizeitem.text))
            if('' in SpecPrizeItem):
                SpecPrizeItem=list(SpecPrizeItem)
                SpecPrizeItem.remove('')
            for temp in list(SpecPrizeItem):
                SpecPrizeitemlist.append(temp)
            #SpecPrizeitemlist.append(list(SpecPrizeItem))
            SpecPrizearealist.append(re.split(r"[市縣]",SpecPrizearea.text)[0])
    #print(CatchedSite)
        lock.release()

#lock=threading.Lock()
SpecPrizeitemlist=[]
SpecPrizearealist=[]
SpecialPrizeitemlist=[]
SpecialPrizearealist=[]
CatchedSite=[]
Static()
print(tm.time()-start)