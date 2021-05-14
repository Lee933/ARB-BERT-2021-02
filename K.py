# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 22:51:36 2020

@author: 10474
"""


import pandas as pd
import re
import numpy as np  # 导入numpy包
from sklearn.model_selection import KFold  # 从sklearn导入KFold包
from Kfold import K_Flod_spilt
if __name__ == '__main__':

    datas = pd.read_excel('0705.xlsx',encoding='utf-8')
    d1=datas['description'].values.tolist()
    d2=datas['REGRESSION'].values.tolist()
    i=0
    yesdata=[]
    nodata=[]

    while i<len(d1):
        if d2[i]=='NO':
            if str(d1[i]).count('\t')==0:
                nodata.append(d1[i])
        if d2[i]=='YES':
            if str(d1[i]).count('\t')==0:
                yesdata.append(d1[i])
        i=i+1
    print('yes',len(yesdata))
    print('no',len(nodata))


    labelset=['no','yes']
    labelmap={'no':0,'yes':1}
    idtolabelmap={0:'no',1:'yes'}

    i=0
    file=open('class.txt','w+',encoding='utf-8')
    while i<len(labelset):
        file.write(idtolabelmap[i])
        if i+1==len(labelset):
            break
        file.write('\n')
        i=i+1
    file.close()
    alldata=[]
    i=0

    while i<2000:
        if i<len(yesdata):
            print(i)
            print(yesdata[i],nodata[i])
            line=str(yesdata[i])+'\t'+'1'
            alldata.append(line)
            line = str(nodata[i]) + '\t' + '0'
            alldata.append(line)
            
        else:
            print(i)
            print(nodata[i])
            line = str(nodata[i]) + '\t' + '0'
            alldata.append(line)
        i=i+1
             

    file1=open('train.txt','w+',encoding='utf-8')
    file2=open('dev.txt','w+',encoding='utf-8')
    file3=open('test.txt','w+',encoding='utf-8')
    i=0
    import random
    Kdata=[]
    while i<len(alldata):
        index=random.randint(0,len(alldata)-1)
        item=alldata[i]
        if i%9==0:
            file3.write(item)
            file3.write('\n')
        else:
            line=str(alldata[i])
            Kdata.append(line)
        i=i+1
    print('done!')
    a=len(Kdata)
    b=int((a/10)*2)
    i=0
    index=random.randint(0,a-1)
    
    for i in range(a):
        
        if i<b:
            item=Kdata[i]
            file2.write(item)
            file2.write('\n')
        else:
            item=Kdata[i]
            file1.write(item)
            file1.write('\n')
        i=i+1
    
    print('dev done!')
    print('train done!')
        
 

    # train=[]
    # test=[]
   # K_Flod_spilt(10,5,Kdata,labelset)



