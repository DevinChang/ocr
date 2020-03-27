# -*- coding:utf-8 -*-


import os
import json
import hashlib
from log import LogMgr
from DatabaseToolsNew import cxOracle
from job import JobTable
from json2word import json2word


class Tools(object):
    """
    工具类，一些通用函数
    """
    def __init__(self):
        #self.logmgr = LogMgr()
        self.db = cxOracle()
        self.job = JobTable()
        self.codepath = os.path.dirname(__file__)
    
    def _data_to_db(self, table, datadict, flag = 1):
        """
        将提取好的数据入库
        @table      ----数据库表名
        @datadict   ----提取出的字典
        @flag       ----是否需要将字典的key转换成英文的标识，默认为1需要
                        2为不需要，若直接命名的key为数据库中的英文，应设置为2
        """
        addsql, param = self.db.getsavesql(table, datadict, flag)
        self.db.insert(addsql, param)
       
    def _update_item(self, table, find_key, find_value, update_key, update_value):
        '''
        修改工作表的某个字段的值
        @find_key       ----定位所需的关键字
        @find_value     ----定位所需关键字的值
        @update_key     ----需要修改的关键字
        @update_value   ----需修改关键字的值
        '''
        self.db.update(table,find_key, find_value, update_key, update_value)

    def _generatemd5(self, strid):
        """
        生成md5码做jobid
        """
        md5 = hashlib.md5()
        md5.update(strid.encode('utf-8'))
        return md5.hexdigest()[:20]

    def _middict(self, datas, middatapath, filename):
        """
        生成中间数据
        """
        if not os.path.exists(middatapath):
            os.makedirs(middatapath)
        relist = []
        for word in datas:
            relist.append(word['words'])
        json2word(relist, middatapath, filename)
        return middatapath + '\\' + filename

    def _getscore(self, datas, nums):
        """打分"""
        scores = 0
        if nums == 0:
            return 0
        for data in datas:
            scores += data['probability']['average']
        return (scores / nums) * 100

    def _load_json(self, file):
        """
        读取json文件
        @file       ------文件路径
        """
        try:
            with open(file, 'r', encoding='utf-8') as f:
                return json.loads(f.read())
        except:
            with open(file,'rb')as f:
                return json.loads(f.read())
    def _sort_index(self, strword):
        """
        针对一些短关键字(如成份等),控制每段信息的识别范围
        @strword    -----读取到信息
        """
        if len(strword) <= 2:
            return len(strword)
        else:
            return 4     

    def _short_index(self, strword):
        if len(strword) <= 2:
            return len(strword)
        else:
            return 4
            
    def _cleandata(self, datadict, data, num):
        """
        初始化识别函数运行过程中的一些变量
        @datadict   -----存放识别结果的字典
        @data       -----读取到的结果
        @num        -----每张图片ocr的结果数目
        """
        if datadict:
            datadict.clear()
        if data:
            data.clear()
        if num != 0:
            num = 0
        return num
