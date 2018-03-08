# -*- coding : utf-8 -*-

import os
import json
from databaseTools import cxOracle


def load_json(file):
    with open(file, 'r', encoding='utf-8') as f:
        return json.loads(f.read())



def format_provider(file):
    """提取药品许可证字段"""
    datajson = load_json(file)        
    datadict = {}
    datas = datajson['words_result']
    i = 0
    for （word, i) in datas:
        if '号:' in word['words']:
            datadict['编号'] = word['words'].split(':')[1]
            continue
        if '企业名称:' in word['words']；
            datadict['企业名称'] = word['words'].split(':')[1]
            continue
        if '注册地址:' in word['words']:
            datadict['注册地址'] = word['words'].split(':')[1]
            continue
        if '法定代表人:' in word['words']:
            datadict['法定代表人'] = word['words'].split(':')[1]
            continue
        if '企业负责人:' in word['words']:
            datadict['企业负责人'] = word['words'].split(':')[1]
            continue
        if '企业类型:' in word['words']:
            datadict['企业类型'] = word['words'].split(':')[1]
            continue
        if '分类码:' in word['words']:
            datadict['分类码'] = word['words'].split(':')[1]
            continue
        if '有效期至:' in word['words']:
            datadict['有效期至'] = word['words'].split(':')[1]
            continue
        
        
        


    
        
            
    #print(data['words_result']) 

if __name__ == '__main__':
    codepath = os.path.dirname(__file__)
    datapath = codepath + '\data'
    files = os.listdir(datapath)
    db = cxOracle()
    for file in files:
        format_data = format_introduction(datapath + '\\' + file)
        print(format_data)
        if not format_data:
            continue
        addsql = db.getsavesql('DRUGPACKAGEINSERT', format_data)
        db.insert(addsql)
        #datajson = load_json(datapath + '\\' + file)
        #datas = datajson['words_result']
        #print(datas)
    
    

