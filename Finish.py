import numpy as np
import tkinter as tk
from tkinter import ttk
import sys
import csv
from bs4 import BeautifulSoup
import threading
import requests
import re
import time as tm
import collections
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
URL='https://www.etax.nat.gov.tw/etw-main/web/ETW183W2_'
URLStatic='https://www.etax.nat.gov.tw/etw-main/web/ETW183W3_'
lock=threading.Lock()
#主選頁
class menu:
    def __init__(self,master):
        self.master=master
        master.title('發票')
        master.geometry("400x400")
        label=tk.Label(master,text='請選擇以下功能')
        label.pack(side=tk.TOP)
        top_frame = tk.Frame(master)
        top_frame.pack()
        bottom_frame = tk.Frame(master)
        bottom_frame.pack(side=tk.BOTTOM)
    
        receipt_lottery_button = tk.Button(top_frame, text='發票對獎', fg='green',command=self.operating_receipt_lottery)
        receipt_lottery_button.pack()

        tk.Button(top_frame, text='發票統計', fg='blue',command=self.operating_receipt_statistics_page).pack()


        exit_button = tk.Button(bottom_frame, text='離開', fg='black',command=sys.exit)
        exit_button.pack(side=tk.BOTTOM)
    
    def operating_receipt_lottery(self):
        self.master.quit
        page_receipt_lottery=tk.Tk()
        receipt_lottery_page(page_receipt_lottery)
        page_receipt_lottery.mainloop()
    def operating_receipt_statistics_page(self):
        self.master.quit
        page_receipt_statistics=tk.Tk()
        receipt_statistics_page(page_receipt_statistics)
        page_receipt_statistics.mainloop()
    
#對發票頁面
class receipt_lottery_page:
    def __init__(self,master):
        self.master=master
        result_list=lottery()

        master.title('發票')
        master.geometry("400x400")
        label=tk.Label(master,text='對中的發票').pack()
        top_frame = tk.Frame(master)
        top_frame.pack()
        bottom_frame = tk.Frame(master)
        bottom_frame.pack(side=tk.BOTTOM)
        result=tk.Label(top_frame,text=result_list).pack()

        back_menu_button=tk.Button(bottom_frame, text='回上一頁', fg='green',command=master.destroy).pack(side=tk.LEFT)

        exit_button=tk.Button(bottom_frame,text='離開',command=sys.exit)
        exit_button.pack(side=tk.RIGHT)
#發票統計頁面
class receipt_statistics_page:
    def fetch(entries):
        Static(entries[0][1].get(),entries[1][1].get())
        print('OK')
    def makeform(root, fields):
        entries = []
        for field in fields:
            row = tk.Frame(root)
            lab = tk.Label(row, width=25, text=field, anchor='w')
            ent = tk.Entry(row)
            row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
            lab.pack(side=tk.LEFT)
            ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
            entries.append((field, ent))
        return entries
    def __init__(self,master):
        global landString
        global cityString
        master.title('發票')
        master.geometry("400x400")
        label=tk.Label(master,text='請選取查詢範圍').pack()
        top_frame = tk.Frame(master)
        top_frame.pack()

        fields = ['請樹入起始日期(YYY/MM)', '請輸入結束日期(YYY/MM)']
        ents = receipt_statistics_page.makeform(top_frame, fields)
        top_frame.bind('<Return>', (lambda event, e=ents: receipt_statistics_page.fetch(e)))
        b1 = tk.Button(top_frame, text='Show', command=(lambda e=ents: receipt_statistics_page.fetch(e)))
        b1.pack(side=tk.LEFT, padx=5, pady=5)


def lottery():
    global data
    global winmoney
    global user
    global datalist
    global year
    global month
    winmoney={}
    user=[]
    datalist=[]
    year=[]
    month=[]
    with open('發票號碼.csv', newline='') as csvfile:
        # 讀取 CSV 檔案內容
        rows = csv.reader(csvfile)
        # 以迴圈將每一列存入list
        for row in rows:
            datalist.append(row)
        # 建立二維陣列(data[i][0]為日期)
        data=np.array(datalist)
        del(datalist)
        data=data.T
        for time in range(len(data)):
            year.append(data[time][0].split('/')[0])
            month.append(data[time][0].split('/')[1])
        datayear=np.array(year)
        datamonth=np.array(month)
        del(year)
        del(month)
    return(CatchNum(datayear,datamonth))

def CatchNum(year,month):
    for i in range(len(year)):
        numberlist=[]
        if(int(month[i])<10):
            temp='0'+str(month[i])
            website=URL+year[i]+temp
        else:
            website=URL+year[i]+month[i]
        html = requests.get(website).content.decode('utf-8')
        sp = BeautifulSoup(html,'html.parser')
        for number in sp.find_all(class_='number',headers=re.compile("Prize$")):
            number=set(number.text.split(' '))
            if('' in number):
                number=list(number)
                number.remove('')
            numberlist.append(number)
        for j in range(1,len(data[i])):
            checkWin(data[i][j],numberlist)
    return(winmoney)

def checkWin(user,Winnumberlist):
    if(user==''):
        return
    sevenTopWinnnum=[]
    sixTopWinnnum=[]
    fiveTopWinnnum=[]
    fourTopWinnnum=[]
    threeTopWinnnum=[]

    for i in range(len(Winnumberlist[2])):
        threeTopWinnnum.append(Winnumberlist[2][i][5:])
        fourTopWinnnum.append(Winnumberlist[2][i][4:])
        fiveTopWinnnum.append(Winnumberlist[2][i][3:])
        sixTopWinnnum.append(Winnumberlist[2][i][2:])
        sevenTopWinnnum.append(Winnumberlist[2][i][1:])
    eightnum=str(user[2:])
    sevennum=str(user[3:])
    sixnum=str(user[4:])
    fivenum=str(user[5:])
    fournum=str(user[6:])
    threenum=str(user[7:])
    if(eightnum in str(Winnumberlist[0])):
        winmoney[user]=10000000
    elif(eightnum in str(Winnumberlist[1])):
        winmoney[user]=2000000
    elif(eightnum in str(Winnumberlist[2])):
        winmoney[user]=200000
    elif(sevennum in str(sevenTopWinnnum)):
        winmoney[user]=40000
    elif(sixnum in str(sixTopWinnnum)):
        winmoney[user]=10000
    elif(fivenum in str(fiveTopWinnnum)):
        winmoney[user]=4000
    elif(fournum in str(fourTopWinnnum)):
        winmoney[user]=1000
    elif(threenum in str(threeTopWinnnum)):
        winmoney[user]=200
    elif(threenum in str(Winnumberlist[3])):
        winmoney[user]=200


def Static(S_begin,S_end):
    S_begin=S_begin.split('/')
    S_end=S_end.split('/')
    global SpecialPrizeitemlist
    global SpecialPrizearealist
    global SpecPrizeitemlist
    global SpecPrizearealist
    global CatchedSite
    global lock
    SpecPrizeitemlist=[]
    SpecPrizearealist=[]
    SpecialPrizeitemlist=[]
    SpecialPrizearealist=[]
    CatchedSite=[]
    visitedSite=[]
    S_year=[str(x) for x in range(102,110)]
    S_month=[str(x) for x in range(1,13)]
    for a in range(len(S_month)):
        if(int(S_month[a])<10):
            S_month[a]='0'+S_month[a]
    for i in range(int(S_year.index(S_begin[0])),int(S_year.index(S_end[0])+1)):
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
    t_list = []
    for Site in visitedSite:
        t1 = threading.Thread(target=CatchStatic, args=(Site,))
        t_list.append(t1)
        t_list[len(t_list)-1].start()
    for t in t_list:
        t.join()
        #CatchStatic(Site)
    Draw(SpecialPrizeitemlist,'SpecialPrizeitemlist')
    Draw(SpecialPrizearealist,'SpecialPrizearealist')
    Draw(SpecPrizeitemlist,'SpecPrizeitemlist')
    Draw(SpecPrizearealist,'SpecPrizearealist')

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
        print(tm.time())
        #print(tm.time())
        for SpecialPrizeitem,SpecialPrizearea in zip(sp.find_all('td',headers='tranItem'),sp.find_all('td',headers='companyAddress')):
            SpecialPrizeItem=set(re.split(r"[元,*，、及和\d共項杯計。等盒瓶個組包開器 ]",SpecialPrizeitem.text))
            if('' in SpecialPrizeItem):
                SpecialPrizeItem=list(SpecialPrizeItem)
                SpecialPrizeItem.remove('')
            for temp in list(SpecialPrizeItem):
                SpecialPrizeitemlist.append(temp)
            SpecialPrizearealist.append(re.split(r"[市縣]",SpecialPrizearea.text)[0])
        for SpecPrizeitem,SpecPrizearea in zip(sp.find_all('td',headers='tranItem2'),sp.find_all('td',headers='companyAddress2')):
            SpecPrizeItem=set(re.split(r"[元,*，、及和\d共項杯計。等盒瓶個組包開器 ]",SpecPrizeitem.text))
            if('' in SpecPrizeItem):
                SpecPrizeItem=list(SpecPrizeItem)
                SpecPrizeItem.remove('')
            for temp in list(SpecPrizeItem):
                SpecPrizeitemlist.append(temp)
            SpecPrizearealist.append(re.split(r"[市縣]",SpecPrizearea.text)[0])
        lock.release()

def Draw(Data,name):
    NPData=np.array(Data)
    a=collections.Counter(NPData)
    #print(a)
    VALUE=list(a.values())
    KEY=list(a.keys())
    size=max(len(KEY),max(VALUE))
    if('item' not in name):
        if(size>=100):
            size/=10
        elif(size>=50):
            size/=5
        elif(size>=30):
            size/=2
    else:
        if(size>=180):
            size/=6
        elif(size>=70):
            size/=4
        elif(size>=50):
            size/=3
        elif(size>=30):
            size/=2
    plt.figure(figsize=(int(size),int(size)))
    font = FontProperties(fname='C:\Windows\Fonts\msjh.ttc', size=10)
    plt.xticks(range(len(KEY)),KEY,fontproperties=font)
    plt.plot(KEY,VALUE)
    plt.tick_params(axis='x', rotation=90)
    plt.savefig('Finish'+name+'.png')


if __name__ == "__main__":
    page_menu=tk.Tk()
    menu(page_menu)
    page_menu.mainloop()