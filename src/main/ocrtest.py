# -*- coding: utf-8 -*-

from aip import AipOcr
import json



def write_json_file(filepath, data):
        """写入json文件"""
        with open(filepath, 'w', encoding = 'utf-8') as fw:
            fw.write(json.dumps(data, ensure_ascii=False))




""" 你的 APPID AK SK """
APP_ID = '10723946'
API_KEY = 'AVKXrbaEYwStf7tGLdm7EbWE'
SECRET_KEY = 'hp8kP1Krqa19t7fMIQfQ4oDK5ScHGeK6'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)



""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

image = get_file_content('G:\IMG\国控盐城\保健药品\补气口服液J000000841\药品GMP证书_1.jpg')



""" 如果有可选参数 """
options = {}
options["language_type"] = "CHN_ENG"
options["detect_direction"] = "true"
options["detect_language"] = "true"
options["probability"] = "true"

""" 带参数调用通用文字识别, 图片参数为本地图片 """
datas = client.accurate(image, options)
print(datas['words_result'])
write_json_file('F:\data\Test\GMP证书.json',datas)

