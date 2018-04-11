# -*- coding: utf-8 -*-
import os
import re
import json
from log import LogMgr

class GMP(object):
    def __init__(self, imgpath):
        self.imgpath = imgpath
        self.log = LogMgr()

    def _gmp(self,datas, nums):
        """
        识别GMP证书
        """
        keylist = []
        datadict = dict()
        for (word, i) in zip(datas, range(0, nums)):
            list_result = self._judge_keywords(word['words'])
            if list_result != None:
                if list_result[0] in datadict and keylist[-1][0] != list_result[0]:
                    datadict[list_result[0]] += list_result[1]
                    flag = 1
                else:
                    datadict[list_result[0]] = list_result[1]
                    flag = 1
                keylist.append([list_result[0],list_result[2]])
            else:
                j = i
                while j > 0:
                    if not keylist:
                        break
                    #FIXMEED:逻辑问题  4/10 DONE
                    if re.match(r'\s[a-zA-Z]+', word['words']):
                        break
                    #提取"有效期至"与"发证日期"字段
                    if re.match(r'\d{4}|\d{2}', word['words']):
                        if len(word['words']) <= 4:
                            break
                        elif '/' in word['words']:
                            if keylist[-1][0] == '发证机关':
                                datadict['发证日期'] = word['words']
                                keylist.append(['杂', '杂'])
                                break
                            if re.search(r'\d{4}|\d{2}', datadict['有效期至']):
                                break
                            else:
                                datadict['有效期至'] = word['words']
                                break
                    if flag:
                        if keylist[-1][0] == '地址':
                            is_scope = self._judge_keywords(datas[i + 1]['words'])
                            if is_scope != None and is_scope[0] == '认证范围':
                                datadict['认证范围'] = word['words']
                                break
                        if keylist[-1][1] in datas[j]['words']:
                            datadict[keylist[-1][0]] += word['words']
                            break
                    j -= 1  
        return datadict

    def _load_json(self, file):
        with open(file, 'r', encoding='utf-8') as f:
            return json.loads(f.read())
        
    def _sort_index(self, strword):
        if len(strword) <= 2:
            return len(strword)
        else:
            return 4
            
    def _judge_keywords(self, strword):
        '''判断关键字'''
        re_coname = re.compile(r"企业*名称*|企*业名*称")
        re_cernum = re.compile(r"证书*编号*|证*书编*号")
        re_addr = re.compile(r"地址")
        re_cerscope = re.compile(r"认证*范围*|认*证范*围")
        re_valid = re.compile(r"有效期至*|有效*期至")
        re_liceauth = re.compile(r"发证*机关*|发*证机*关")
        re_licedate = re.compile(r"发证*日期*|发*证日*期")
        re_abandon = re.compile(r"经审*查")

        if len(strword) >= 8: 
            index = 6
        else:
            index = len(strword)

        if(re.match(r'.+?(?:\:)', strword[:index])):
            if re_coname.search(strword[:index]):
                return ['企业名称', strword[re_coname.search(strword).span()[1]:], re_coname.search(strword).group()]
            elif re_cernum.search(strword[:index]):
                return ['证书编号' , strword[re_cernum.search(strword).span()[1] + 1:], re_cernum.search(strword).group()]
            elif re_addr.search(strword[:self._sort_index(strword)]):
                return ['地址' , strword[re_addr.search(strword).span()[1]:],re_addr.search(strword).group()]
            elif re_cerscope.search(strword[:index]):
                return ['认证范围' , strword[re_cerscope.search(strword).span()[1]:],re_cerscope.search(strword).group()]
            elif re_valid.search(strword[:index]):
                return ['有效期至' , strword[re_valid.search(strword).span()[1]:],re_valid.search(strword).group()]
            elif re_liceauth.search(strword[:index]):
                return ['发证机关' , strword[re_liceauth.search(strword).span()[1]:],re_liceauth.search(strword).group()]
            elif re_licedate.search(strword[:index]):
                return ['发证时间' , strword[re_licedate.search(strword).span()[1]:],re_licedate.search(strword).group()]
            else:
                return None
        else: 
            if re_coname.search(strword[:index]):
                return ['企业名称', strword[re_coname.search(strword).span()[1]:], re_coname.search(strword).group()]
            elif re_cernum.search(strword[:index]):
                return ['证书编号' , strword[re_cernum.search(strword).span()[1] + 1:], re_cernum.search(strword).group()]
            elif re_addr.search(strword[:self._sort_index(strword)]):
                return ['地址' , strword[re_addr.search(strword).span()[1]:],re_addr.search(strword).group()]
            elif re_cerscope.search(strword[:index]):
                return ['认证范围' , strword[re_cerscope.search(strword).span()[1]:],re_cerscope.search(strword).group()]
            elif re_valid.search(strword[:index]):
                return ['有效期至' , strword[re_valid.search(strword).span()[1]:],re_valid.search(strword).group()]
            elif re_liceauth.search(strword[:index]):
                return ['发证机关' , strword[re_liceauth.search(strword).span()[1]:],re_liceauth.search(strword).group()]
            elif re_licedate.search(strword[:index]):
                return ['发证时间' , strword[re_licedate.search(strword).span()[1]:],re_licedate.search(strword).group()]
            elif re_abandon.search(strword[:index]):
                return ['经审查', strword[re_abandon.search(strword).span()[1]:], re_abandon.search(strword).group()]
            else:
                return None

    def _cleandata(self, datadict, data, num):
        if datadict:
            datadict.clear()
        if data:
            data.clear()
        if num != 0:
            num = 0
        return num

    def recognize(self):
        flag = 0
        for file in os.walk(self.imgpath):
            for file_name in file[2]:
                if 'GMP证书' in file_name:
                    imgname = file_name.split('.')[0]
                    #curpath = file[0].split('data')[1]
                    #index = imgname.rfind('_')
                    #id = curpath[curpath.rfind('\\') + 1:]
                    #name_index_e = re.match(r'.*[A-Z]', id).span()[1]
                    #dragname = id[:name_index_e - 1]
                    #if dragname.find('(') > 0:
                    #    dragname = dragname[:dragname.find('(')]
                    #id_code = id[name_index_e - 1:]
                    datajson = self._load_json(file[0] + '\\' + file_name)
                    #图片过大或者一些原因，没有识别出来就会有error_code字段
                    if 'error_code' in datajson:
                        self.log.error(file[0] + '\\' + file_name + ": img size error!")
                        continue
                    #source_img_path = imgpaht_root_desktop + '\\' + curpath + '\\' + imgname[:index] + '.' + imgname[index:].split('_')[1]
                    #original_path = path_root + '\\' + curpath + '\\' + imgname[:index - 2] + '.' + 'pdf'
                    #FIXME:换工作环境这里也得改！
                    #try:
                    #    kindict = hmc.kinds(source_img_path, datajson)
                    #except Exception as e:
                    #    logmgr.error(file[0] + '\\' + file_name + ':' + str(e))
                    #    continue
                    #print('Current processing: {}'.format(imgpaht_root_desktop + '\\' + curpath + 
                    #                        '\\' + imgname[:index] + 
                    #                        '.' + imgname[index:].split('_')[1], 
                    #                        file[0] + '\\' + file_name))
                    datas = datajson['words_result']
                    nums = datajson['words_result_num']
                    flag = 1
            if flag:
                if len(datas) > 0 and nums > 0:
                    datadict = self._gmp(datas, nums)
                    print(datadict)
                    if not datadict:
                        nums = cleandata(datadict, datas, nums)
                        continue



if __name__ == '__main__':
    codepath = os.path.dirname(__file__)
    gmptest = GMP(codepath + '\data')
    gmptest.recognize()