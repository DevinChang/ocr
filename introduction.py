# -*- coding : utf-8 -*-

import os
import json
from DatabaseToolsNew import cxOracle
import re
from FindKeyword import findImportWords
import HowManyColumn as hmc

def load_json(file):
    with open(file, 'r', encoding='utf-8') as f:
        return json.loads(f.read())

def sort_index(strword):
    if len(strword) <= 2:
        return len(strword)
    else:
        return 4

gdatadict = {}

def judge_keywords(strword):
    '''判断关键字'''
    re_common_name = re.compile(r'通?用名称?|通?用名?称')
    re_product_name = re.compile(r'商?品名称?|商?品名?称')
    re_english = re.compile(r'英文?名称?|英文名?称')
    re_pinyin = re.compile(r'汉语?拼音?|汉?语拼?音')
    re_element = re.compile(r'.?成份?[】\]]|.?成?份[】\]]')
    re_element_accu = re.compile(r'.?成份?|.?成?份')
    re_traits = re.compile(r'.?性状?[】\]]|.?性?状[】\]]')
    re_traits_accu = re.compile(r'.?性状?|.?性?状')
    re_function_category = re.compile(r'作用?类别?')
    re_indication = re.compile(r'.?适?应症[】\]]|.适应?症[】\]]|.功?能主治?[】\]]|.功?能主?治[】\]]')
    re_indication_accu = re.compile(r'.?适?应症|.适应?症|.功?能主治?|.功?能主?治')
    re_specification = re.compile(r'.?规格?[】\]]|.?规?格[】\]]')
    re_specification_accu = re.compile(r'.?规格?|.?规?格')
    re_dosage = re.compile(r'.?用?法用量?[】\]]|.?用?法用?量[】\]]')
    re_dosage_accu = re.compile(r'.?用?法用量?|.?用?法用?量')
    re_reaction = re.compile(r'.?不?良反应?[】\]]|.?不?良反?应[】\]]')
    re_reaction_accu = re.compile(r'.?不?良反应?|.?不?良反?应')
    re_prohibition = re.compile(r'.?禁忌?[】\]]|.?禁?忌[】\]]')
    re_prohibition_accu = re.compile(r'.?禁忌?|.?禁?忌')
    re_precautions = re.compile(r'.?注?意事项?[】\]]|.?注?意事?项[】\]]')
    re_precautions_accu = re.compile(r'.?注?意事项?|.?注?意事?项')
    re_registeraddr = re.compile(r'注?册地址?|注?册地?址')
    if len(strword) >= 6: 
        index = 6
    else:
        index = len(strword)

    if re.match(r'.+?(?:】)|.+?(?:])', strword[:index]):
        if re_element.search(strword[:sort_index(strword)]):
            return ['成份' , strword[re_element.search(strword).span()[1] + 1:], re_element.search(strword).group()]
        elif re_function_category.search(strword[:index]):
            return ['作用类别' , strword[re_function_category.search(strword).span()[1] + 1:], re_function_category.search(strword).group()]
        elif re_traits.search(strword[:sort_index(strword)]):
            return ['性状' , strword[re_traits.search(strword).span()[1] + 1:],re_traits.search(strword).group()]
        elif re_indication.search(strword[:index]):
            return ['功能主治' , strword[re_indication.search(strword).span()[1] + 1:],re_indication.search(strword).group()]
        elif re_specification.search(strword[:sort_index(strword)]):
            return ['规格' , strword[re_specification.search(strword).span()[1] + 1:],re_specification.search(strword).group()]
        elif re_dosage.search(strword[:index]):
            return ['用法用量' , strword[re_dosage.search(strword).span()[1] + 1:],re_dosage.search(strword).group()]
        elif re_reaction.search(strword[:index]):
            return ['不良反应' , strword[re_reaction.search(strword).span()[1] + 1:],re_reaction.search(strword).group()]
        elif re_prohibition.search(strword[:sort_index(strword)]):
            return ['禁忌' , strword[re_prohibition.search(strword).span()[1] + 1:],re_prohibition.search(strword).group()]
        elif re_precautions.search(strword[:index]):
            return ['注意事项' , strword[re_precautions.search(strword).span()[1] + 1:],re_precautions.search(strword).group()]
        else:
            return None
    elif re.match(r'.+?(?:\:)', strword[:index]):
        if re_common_name.search(strword[:index]):
            return ['通用名称' , strword[re_common_name.search(strword).span()[1] + 1:], re_common_name.search(strword).group()] 
        elif re_product_name.search(strword[:index]):
            return ['商品名称', strword[re_product_name.search(strword).span()[1] + 1:],re_product_name.search(strword).group()]
        elif re_english.search(strword[:index]):
            return ['英文名称' , strword[re_english.search(strword).span()[1] + 1:], re_english.search(strword).group()]
        elif re_pinyin.search(strword[:index]):
            return ['汉语拼音' , strword[re_pinyin.search(strword).span()[1] + 1:], re_pinyin.search(strword).group()]
        elif re_registeraddr.search(strword[:index]):
            return ['注册地址' , strword[re_registeraddr.search(strword).span()[1] + 1:], re_registeraddr.search(strword).group()]
        else:
            return None
    else: 
        if re_common_name.search(strword[:index]):
            return ['通用名称' , strword[re_common_name.search(strword).span()[1]:], re_common_name.search(strword).group()] 
        elif re_product_name.search(strword[:index]):
            return ['商品名称', strword[re_product_name.search(strword).span()[1]:],re_product_name.search(strword).group()]
        elif re_english.search(strword[:index]):
            return ['英文名称' , strword[re_english.search(strword).span()[1]:], re_english.search(strword).group()]
        elif re_pinyin.search(strword[:index]):
            return ['汉语拼音' , strword[re_pinyin.search(strword).span()[1]:], re_pinyin.search(strword).group()]
        elif re_element_accu.search(strword[:sort_index(strword)]):
            return ['成份' , strword[re_element_accu.search(strword).span()[1]:], re_element_accu.search(strword).group()]
        elif re_function_category.search(strword[:index]):
            return ['作用类别' , strword[re_function_category.search(strword).span()[1]:], re_function_category.search(strword).group()]
        elif re_traits_accu.search(strword[:sort_index(strword)]):
            return ['性状' , strword[re_traits_accu.search(strword).span()[1]:],re_traits_accu.search(strword).group()]
        elif re_indication_accu.search(strword[:index]):
            return ['功能主治' , strword[re_indication_accu.search(strword).span()[1]:],re_indication_accu.search(strword).group()]
        elif re_specification_accu.search(strword[:sort_index(strword)]):
            return ['规格' , strword[re_specification_accu.search(strword).span()[1]:],re_specification_accu.search(strword).group()]
        elif re_dosage_accu.search(strword[:index]):
            return ['用法用量' , strword[re_dosage_accu.search(strword).span()[1]:],re_dosage_accu.search(strword).group()]
        elif re_reaction_accu.search(strword[:index]):
            return ['不良反应' , strword[re_reaction_accu.search(strword).span()[1]:],re_reaction_accu.search(strword).group()]
        elif re_prohibition_accu.search(strword[:sort_index(strword)]):
            return ['禁忌' , strword[re_prohibition_accu.search(strword).span()[1]:],re_prohibition_accu.search(strword).group()]
        elif re_precautions_accu.search(strword[:index]):
            return ['注意事项' , strword[re_precautions_accu.search(strword).span()[1]:],re_precautions_accu.search(strword).group()]
        elif re_registeraddr.search(strword[:index]):
            return ['注册地址' , strword[re_registeraddr.search(strword).span()[1]:], re_registeraddr.search(strword).group()]
        else:
            return None
        
def inrtroduction_judge(strword):
    keyword = judge_keywords(strword)
    if not keyword:
        return findImportWords(strword)
    else:
        return keyword


datadict = {}
keylist = []
def inrtroduction(datas, nums):
    i = 0
    for (word, i) in zip(datas, range(0, nums)):
        list_result = inrtroduction_judge(word['words'])
        #阈值
        if word['probability']['average'] * 0.6 + word['probability']['min'] * 0.4 < 0.85:
            continue
        if list_result != None and len(keylist) > 0:
            if list_result[0] in datadict and keylist[-1][0] != list_result[0]:
                list_result = None
        if list_result != None:
            datadict[list_result[0]] = list_result[1]
            keylist.append([list_result[0],list_result[2]])
        else:
            j = i
            while j > 0:
                if not keylist:
                    break
                if "日期" in keylist[-1][1]:
                    if re.match(r'[0-9]{4}年?[0-9]{2}月?[0-9]{2}日?', datas[j]['words']):
                        continue
                    else:
                        break
                if keylist[-1][1] in datas[j]['words']:
                    datadict[keylist[-1][0]] += word['words']
                    break
                j -= 1  
            

def subfiledata(direction, parameter, boundary, datas):
    leftdata = []
    rightdata = []
    for data in datas:
        if direction == 1 or direction == 2:
            if data['location'][parameter] >= boundary:
                #此处有bug
                leftdata += data['words']
            else:
                rightdata += data['words']
        else:
            if data['location'][parameter] <= boundary:
                leftdata += data['words']
            else:
                rightdata += data['words']
    return leftdata + rightdata

        


    


            



        
        
            

if __name__ == '__main__':
    codepath = os.path.dirname(__file__)
    datapath = codepath + '\data'
    files = os.listdir(datapath)
    db = cxOracle()
    imgpath_root = "F:\IMG"
    datas = []
    leftdata = []
    rightdata = []
    nums = 0
    flag = 0
    for file in os.walk(datapath):
        for file_name in file[2]:
            if '说明书' in file_name:
                imgname = file_name.split('.')[0]
                curpath = file[0].split('data')[1]
                index = imgname.rfind('_')
                kindict = hmc.kinds(imgpath_root + '\\' + curpath + 
                                        '\\' + imgname[:index] + 
                                        '.' + imgname[index:].split('_')[1], 
                                        file[0] + '\\' + file_name)

                datajson = load_json(file[0] + '\\' + file_name)
                datatmp = datajson['words_result']
                nums += datajson['words_result_num']

                if kindict['kinds'] == 2:
                    datas += subfiledata(kindict['direction'], kindict['parameter'], kindict['boundary'][0], datatmp)
                elif kindict['kinds'] == 1:
                    datas += datatmp

                flag = 1
        
        if flag:
            
            if len(datas) > 0 and nums > 0:
                inrtroduction(datas, nums)
                if not datadict:
                    continue
                addsql, param = db.getsavesql('DRUGPACKAGEINSERT', datadict)
                db.insert(addsql, param)
                print(datadict)
                datas.clear()
                datadict.clear()
        #print(datas)
    
    

