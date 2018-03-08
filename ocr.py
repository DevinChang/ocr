# -*- coding: utf-8 -*-

from config import *
from aip import AipOcr
import json
import csv
import os
from wand.image import Image
#from introduction import format_introduction
import introduction


"""
__version__: 1.0
__application__: ocr识别说明书，药品许可证等证件
__author__: DevinChang
__date__: 2018/1/23
"""

"""
__version__: 1.1
__application__: ocr识别说明书，药品许可证等证件
__author__: DevinChang
__date__: 2018/1/27
__modify__: 1).增加提取药品说明书关键信息模块
            2).支持选择多个精度识别
            3).整合pdf转jpg模块
__bug__: 仅支持一些常见的说明书文件;提取的字段精度不高，时有混乱的字段。
"""






class MyOcr(object):
    """
    文字识别
    @app_id @api_key @secret_key 为百度ai平台上申请的值
    @typeid 精度的选择
            1--调用通用文字识别
            2--含位置信息的通用文字识别
            3--高精度的文字识别
            4--含位置信息的高精度文字识别
    """
    def __init__(self, app_id, api_key, secret_key, typeid):
        self.client = AipOcr(app_id, api_key, secret_key)
        self.typeid = typeid
        self.codepath = os.path.dirname(__file__)
        self.datapath = self.codepath + '\data'
        os.makedirs(self.datapath, exist_ok=True)
    

    def _get_file_content(self, filePath):
        """读取图片"""
        with open(filePath, 'rb') as fp:
            return fp.read()

    def _write_json_file(self, filepath, data):
        """写入json文件"""
        with open(filepath, 'w', encoding = 'utf-8') as fw:
            fw.write(json.dumps(data, ensure_ascii=False))
        
    

    def _ocr(self):
        """
        识别img文件下的图片
        @输出json数据，保存到data文件夹下
        """
        imgpath = self.codepath + '\IMG'+'\国控天星'
        #for root, dirname, filename in os.walk(imgpath):
        #    continue

        options = {}
        options["detect_direction"] = "true" 
        options["detect_language"] = "true"
        options["probability"] = "true"
        #rootdir = os.listdir(imgpath)
        #dirs = os.listdir(imgpath + '\\' + rootdir[0])
        #cur_path = imgpath + '\\' + rootdir[0]
        #for dirname in dirs:
        #    files = os.listdir(cur_path + '\\' + dirname)
        #    for (file, i) in zip(files, range(0, 5)):
        #        if (file[-3:] != 'Jpg') and (file[-3:] != 'jpg'):
        #            continue
        #        print('Current img: {}'.format(file))
        #        img = self._get_file_content(cur_path + '\\' + dirname + '\\' + file)
        #        if self.typeid == 1:
        #            data = self.client.basicGeneral(img, options)
        #        elif self.typeid == 2:
        #            data = self.client.general(img, options)
        #        elif self.typeid == 3:
        #            data = self.client.basicAccurate(img, options)
        #        elif self.typid == 4:
        #            data = self.client.accurate(img, options)
        #        #self._write_json_file((self.datapath +'\{}.json').format(str.split(file, '.')[0]), data)
        #        self._write_json_file((self.datapath +'\{}_{}.json').format(dirname, i), data)
        
        for file in os.walk(imgpath):
            #2018/3/5 modify: 修改读取文件流程，使得保存数据的路径与图片的路径相同
            for file_name in file[2]:
                if '说明书' in file_name:
                    print('Current img: {}'.format(file_name))
                    index = file[0].rfind('国控天星')
                    tmpath = file[0][index:]
                    curpath = self.datapath + '\\' + tmpath + '\\' + '说明书'
                    if not os.path.exists(curpath):
                        os.makedirs(curpath)

                    img = self._get_file_content(file[0] + '\\' + file_name)
                    if self.typeid == 1:
                        data = self.client.basicGeneral(img, options)
                    elif self.typeid == 2:
                        data = self.client.general(img, options)
                    elif self.typeid == 3:
                        data = self.client.basicAccurate(img, options)
                    elif self.typid == 4:
                        data = self.client.accurate(img, options)
                    
                    self._write_json_file((curpath +'\{}.json').format(str.split(file_name, '.')[0]), data)       
        #options = {}
        #options["detect_direction"] = "true" 
        #options["detect_language"] = "true"
        #options["probability"] = "true"
        #for file in files:
        #    print('Current img: {}'.format(file))
        #    img = self._get_file_content(imgpath + '\\' + file)
        #    if self.typeid == 1:
        #        data = self.client.basicGeneral(img, options)
        #    elif self.typeid == 2:
        #        data = self.client.general(img, options)
        #    elif self.typeid == 3:
        #        data = self.client.basicAccurate(img, options)
        #    elif self.typid == 4:
        #        data = self.client.accurate(img, options)
        #    self._write_json_file((self.datapath +'\{}.json').format(str.split(file, '.')[0]), data)

        #data_files = os.listdir(datapath)
        #for dfile in datas:
        #    self._write_dict(datapath + dfile) 
        
    def _write_dict(self):
        files = os.listdir(self.datapath)
        for file in files:
            format_data = introduction.format_introduction(self.datapath + '\\' + file)
            print(format_data)

    def pdf2img(self):
        """pdf转jpg"""
        file_dir = self.codepath + '/PDF/说明书/'
        save_dir = self.codepath + '/IMG/图片/'
        for files in os.walk(file_dir):
            for file_name in files[2]:
                file_path = file_dir
                [file_name_prefix, file_name_suffix] = file_name.split('.')
                file = file_dir + file_name
                with(Image(filename=file, resolution=300)) as img:
                    images = img.sequence
                    pages = len(images)
                    for i in range(pages):
                        images[i].type = 'truecolor'
                        save_name = save_dir + file_name_prefix + str(i) + '.jpg'
                        Image(images[i]).save(filename=save_name)
    
    def run(self):
        """入口函数"""
        print('********Start Identify********')
        self._ocr()
        print('********End********')
        print('=================Format Data================')
        self._write_dict()
        print('======================End===================')