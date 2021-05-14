# coding: UTF-8
import time
import torch
import numpy as np
from train_eval import train, init_network
from importlib import import_module
import argparse

import torch
import numpy
import pandas as pd
file=open('dataset/data/class.txt',encoding='utf-8')
lins=file.readlines()
mapidtoname={}
i=0
for line in lins:
    temp=line.strip()
    if temp!='':
        mapidtoname[str(i)]=temp
    i=i+1

if __name__ == '__main__':
    np.random.seed(1)
    torch.manual_seed(1)
    torch.cuda.manual_seed_all(1)
    torch.backends.cudnn.deterministic = True  # 保证每次结果一样
    dataset = 'dataset'  # 数据集

    model_name = 'bert'  # bert
    x = import_module(model_name)
    config = x.Config(dataset)
    model = x.Model(config)
    model.load_state_dict(torch.load(config.save_path,map_location='cpu'))
    PAD, CLS = '[PAD]', '[CLS]'  # padding符号, bert中综合信息符号
    pad_size = config.pad_size
    print('加载完毕')
    # df=pd.read_excel('待预测.xlsx',encoding='utf-8')
    datas=open('learn.txt',encoding='utf-8').readlines()
    df=pd.DataFrame()
    results=[]
    contents=[]
    idtolabelmap={0:'no',1:'yes'}

    for data in datas:
        content=data.strip()
        print(content)
        contents.append(content)
        token = config.tokenizer.tokenize(content)
        token = [CLS] + token
        seq_len = len(token)
        mask = []
        token_ids = config.tokenizer.convert_tokens_to_ids(token)

        if pad_size:
            if len(token) < pad_size:
                mask = [1] * len(token_ids) + [0] * (pad_size - len(token))
                token_ids += ([0] * (pad_size - len(token)))
            else:
                mask = [1] * pad_size
                token_ids = token_ids[:pad_size]
                seq_len = pad_size
        x = torch.LongTensor([token_ids]).to(config.device)
        seq_len = torch.LongTensor([seq_len]).to(config.device)
        mask = torch.LongTensor([mask]).to(config.device)
        text=(x,seq_len,mask)
        y=model(text)
        # print(y)
        # print(y[0])
        predc = torch.max(y.data, 1)[1].cpu().numpy()   #定义最大预测结果

        result = predc[0]
        print('预测结果:',idtolabelmap[result])
        results.append(idtolabelmap[result])

    df['content']=contents
    df['pre_label']=results

    df.to_excel('预测结果.xlsx',index=False,encoding='utf-8')
    print('done!')



