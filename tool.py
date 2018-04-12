# -*- coding:utf-8 -*-


from log import LogMgr
import json


class Tools(object):
    """
    工具类，一些通用函数
    """
    def __init__(self):
        self.log = LogMgr()

    def _load_json(self, file):
        """
        读取json文件
        @file       ------文件路径
        """
        with open(file, 'r', encoding='utf-8') as f:
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
