# -*- coding : utf-8 -*-

import os
import json
from databaseTools import cxOracle
import re
from FindKeyword import findImportWords

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

    if len(strword) >= 6: 
        index = 6
    else:
        index = len(strword)

    if re.match(r'.+?(?:】)|.+?(?:])', strword):
        if re_element.search(strword[:sort_index(strword)]):
            return ['成份' , strword[re_element.search(strword).span()[1] + 1:], re_element.search(strword).group()]
        elif re_function_category.search(strword[:index]):
            return ['作用类别' , strword[re_function_category.search(strword).span()[1] + 1:], re_function_category.search(strword).group()]
        elif re_traits.search(strword[:sort_index(strword)]):
            return ['性状' , strword[re_traits.search(strword).span()[1] + 1:],re_traits.search(strword).group()]
        elif re_indication.search(strword[:index]):
            return ['功能主治' , strword[re_indication.search(strword).span()[1] + 1:],re_indication.search(strword).group()]
        elif re_specification.search(strword[:sort_index(strword)]):
            return ['规格' , strword[re_specification.span()[1] + 1:],re_specification.search(strword).group()]
        elif re_dosage.search(strword[:index]):
            return ['用法用量' , strword[re_dosage.search(strword).span()[1] + 1:],re_dosage.search(strword).group()]
        elif re_reaction.search(strword[:index]):
            return ['不良反应' , strword[re_reaction.search(strword).span()[1] + 1:],re_reaction.search(strword).group()]
        elif re_prohibition.search(strword[:sort_index(strword)]):
            return ['禁忌' , strword[re_prohibition.search(strword).span()[1] + 1:],re_prohibition.search(strword).group()]
        else:
            return None
    elif re.match(r'.+?(?:\:)', strword):
        if re_common_name.search(strword[:index]):
            return ['通用名称' , strword[re_common_name.search(strword).span()[1] + 1:], re_common_name.search(strword).group()] 
        elif re_product_name.search(strword[:index]):
            return ['商品名称', strword[re_product_name.search(strword).span()[1] + 1:],re_product_name.search(strword).group()]
        elif re_english.search(strword[:index]):
            return ['英文名称' , strword[re_english.search(strword).span()[1] + 1:], re_english.search(strword).group()]
        elif re_pinyin.search(strword[:index]):
            return ['汉语拼音' , strword[re_pinyin.search(strword).span()[1] + 1:], re_pinyin.search(strword).group()]
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
        else:
            return None
        
def inrtroduction_judge(strword):
    keyword = judge_keywords(strword)
    if not keyword:
        return findImportWords(strword)
    else:
        return keyword


def inrtroduction_test(file):
    datajson = load_json(file)
    datadict = {}
    keylist = []
    datas = datajson['words_result']
    i = 0
    for (word, i) in zip(datas, range(0, datajson['words_result_num'])):
        list_result = inrtroduction_judge(word['words'])
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
    


def format_introduction(file):
    """提取说明书字段"""
    datajson = load_json(file)
    datadict = {}
    datas = datajson['words_result']
    i = 0
    for (word, i) in zip(datas, range(0, datajson['words_result_num'])):
        if '通用名称:' in word['words']:
            datadict['通用名称'] = word['words'].split(':')[1]
            continue
        elif ('通用名称' in word['words']) and (':' not in word['words']):
            datadict['通用名称'] = word['words'].split('称')[1]
            continue
        if '商品名:' in word['words']:
            datadict['商品名'] = word['words'].split(':')[1]
            continue
        elif ('商品名' in word['words']) and (':' not in word['words']):
            datadict['商品名'] = word['words'].split('名')[1]
            continue
        if '汉语拼音:' in word['words']:
            datadict['汉语拼音'] = word['words'].split(':')[1]
            continue
        if ('OTC' or 'OT') in word['words']:
            datadict['OTC'] = 'OTC'
            continue
        if '份】' in word['words']:
            if len(word['words']) > 4:
                datadict['成份'] = word['words'].split('】')[1]
            continue
        elif '份]' in word['words']:
            if len(word['words']) > 4:
                datadict['成份'] = word['words'].split(']')[1]
            continue
        elif '【成' == word['words']:
            continue
        elif '[成' == word['words']:
            continue
        if '【性' in word['words'] == word['words']:
            continue
        elif '[性' in word['words'] == word['words']:
            continue
        elif '状】' in word['words']:
            if len(word['words']) > 4:
                datadict['性状'] = word['words'].split('】')[1]
            continue
        elif '状]' in word['words']:
            if len(word['words']) > 4:
                datadict['性状'] = word['words'].split(']')[1]
            else:
                datadict['性状'] = ''
            continue
        elif ('性状' in word['words'][4]) and ('】' not in word['words']):
            if len(word['words']) > 4:
                datadict['性状'] = word['words'].split('状')[1]
            else:
                datadict['性状'] = ''
                continue
        elif ('性状' in word['words'][4]) and (']' not in word['words']):
            if len(word['words']) > 4:
                datadict['性状'] = word['words'].split('状')[1]
            else:
                datadict['性状'] = ''
                continue
        if ('功能主治】' in word['words']) or ('适应症】' in word['words']):
            if len(word['words']) > 6:
                datadict['功能主治'] = word['words'].split('】')[1]
            else:
                datadict['功能主治'] = ''
            continue
        elif ('功能主治]' in word['words']) or ('适应症]' in word['words']):
            if len(word['words']) > 6:
                datadict['功能主治'] = word['words'].split(']')[1]
            else:
                datadict['功能主治'] = ''
            continue
        #elif ('功能主】' in word['words']) or ('')
        elif ('功能主治' in word['words']) and ('】' not in word['words']):
            if len(word['words']) > 6:
                datadict['功能主治'] = word['words'].split('治')[1]
            else:
                datadict['功能主治'] = ''
            continue

        if '格】' in word['words']:
            datadict['规格'] = word['words'].split('】')[1]
            continue
        elif '格]' in word['words']:
            datadict['规格'] = word['words'].split(']')[1]
            continue
        elif '【规' == word['words'] :
            continue
        elif '[规' == word['words']:
            continue
        if '用法用量】' in word['words']:
            datadict['用法用量'] = word['words'].split('】')[1]
            continue
        elif '用法用量]' in word['words']:
            datadict['用法用量'] = word['words'].split(']')[1]
            continue
        if '不良反应】' in word['words']:
            datadict['不良反应'] = word['words'].split('】')[1]
            continue
        elif '不良反应]' in word['words']:
            datadict['不良反应'] = word['words'].split(']')[1]
            continue
             
    #for (word, i) in zip(datas, range(0, datajson['words_result_num'])):
    #    if '通用名称:' in word['words']:
    #        datadict['通用名称'] = word['words'].split(':')[1]
    #        continue
    #    if '汉语拼音:' in word['words']:
    #        datadict['汉语拼音'] = word['words'].split(':')[1]
    #        continue
    #    if ('OTC' or 'OT') in word['words']:
    #        datadict['OTC'] = 'OTC'
    #        continue
    #    if '份】' in word['words']:
    #        datadict['成份'] = word['words'].split('】')[1]
    #        continue
    #    elif '份]' in word['words']:
    #        datadict['成份'] = word['words'].split(']')[1]
    #        continue
    #    elif '【成' == word['words']:
    #        continue
    #    elif '[成' == word['words']:
    #        continue
    #    if '【性' in word['words'] == word['words']:
    #        continue
    #    elif '[性' in word['words'] == word['words']:
    #        continue
    #    elif '状】' in word['words']:
    #        datadict['性状'] = word['words'].split('】')[1]
    #        continue
    #    elif '状]' in word['words']:
    #        datadict['性状'] = word['words'].split(']')[1]
    #        continue
    #    if '功能主治】' in word['words']:
    #        datadict['功能主治'] = word['words'].split('】')[1]
    #        continue
    #    elif '功能主治]' in word['words']:
    #        datadict['功能主治'] = word['words'].split(']')[1]
    #        continue
    #    if '格】' in word['words']:
    #        datadict['规格'] = word['words'].split('】')[1]
    #        continue
    #    elif '格]' in word['words']:
    #        datadict['规格'] = word['words'].split(']')[1]
    #        continue
    #    elif '【规' == word['words'] :
    #        continue
    #    elif '[规' == word['words']:
    #        continue
    #    if '用法用量】' in word['words']:
    #        datadict['用法用量'] = word['words'].split('】')[1]
    #        continue
    #    elif '用法用量]' in word['words']:
    #        datadict['用法用量'] = word['words'].split(']')[1]
    #        continue
    #    if '不良反应】' in word['words']:
    #        datadict['不良反应'] = word['words'].split('】')[1]
    #        continue
    #    elif '不良反应]' in word['words']:
    #        datadict['不良反应'] = word['words'].split(']')[1]
    #        continue
    #    if '忌】' in word['words']:
    #        datadict['禁忌'] = word['words'].split('】')[1]
    #        continue
    #    elif '忌]' in word['words']:
    #        datadict['禁忌'] = word['words'].split(']')[1]
    #        continue
    #    elif '【禁' == word['words']:
    #        continue
    #    elif '[禁' == word['words']:
    #        continue
    #    if '藏】' in word['words']:
    #        datadict['贮藏'] = word['words'].split('】')[1]
    #        continue
    #    elif '藏]' in word['words']:
    #        datadict['贮藏'] = word['words'].split(']')[1]
    #        continue
    #    elif '【贮' == word['words']:
    #        continue
    #    elif '[贮' == word['words']:
    #        continue
    #    if '有效期】' in word['words']:
    #        datadict['有效期'] = word['words'].split('】')[1]
    #        continue
    #    elif '有效期]' in word['words']:
    #        datadict['有效期'] = word['words'].split(']')[1]
    #        continue
    #    if '注意事项】' in word['words']:
    #        datadict['注意事项'] = word['words'].split('】')[1]
    #        continue
    #    elif '注意事项]' in word['words']:
    #        datadict['注意事项'] = word['words'].split(']')[1]
    #        continue
    #    if '包装】' in word['words']:
    #        datadict['包装'] = word['words'].split('】')[1]
    #        continue
    #    elif '包装]' in word['words']:
    #        datadict['包装'] = word['words'].split(']')[1]
    #        continue
    #    elif '【包' == word['words']:
    #        continue
    #    elif '[包' == word['words']:
    #        continue
    #    if '药物相互作用】' in word['words']:
    #        datadict['药物相互作用'] = word['words'].split('】')[1]
    #        continue
    #    elif '药物相互作用]' in word['words']:
    #        datadict['药物相互作用'] = word['words'].split(']')[1]
    #        continue
    #    if '执行标准】' in word['words']:
    #        datadict['执行标准'] = word['words'].split('】')[1]
    #        continue
    #    elif '执行标准]' in word['words']:
    #        datadict['执行标准'] = word['words'].split(']')[1]
    #        continue
    #    if '不良反应】' in word['words']:
    #        datadict['不良反应'] = word['words'].split('】')[1]
    #        continue
    #    elif '不良反应]' in word['words']:
    #        datadict['不良反应'] = word['words'].split(']')[1]
    #        continue
    #    if '批准文号】' in word['words']:
    #        datadict['批准文号'] = word['words'].split('】')[1]
    #        continue
    #    elif '批准文号]' in word['words']:
    #        datadict['批准文号'] = word['words'].split(']')[1]
    #        continue
    #    if '企业名称:'  in word['words']:
    #        datadict['企业名称'] = word['words'].split(':')[1]
    #        continue
    #    if '生产企业】' in word['words']:
    #        datadict['生产企业'] = word['words'].split('】')[1]
    #        continue
    #    elif '生产企业]' in word['words']:
    #        datadict['生产企业'] = word['words'].split(']')[1]
    #        continue
    #    if '生产地址:' in word['words']:
    #        datadict['生产地址'] = word['words'].split(':')[1]
    #        continue
    #    if '邮政编码:' in word['words']:
    #        datadict['邮政编码'] = word['words'].split(':')[1]
    #        continue
    #    if '电话号码:' in word['words']:
    #        datadict['电话号码'] = word['words'].split(':')[1]
    #        continue
    #    if '传真号码:' in word['words']:
    #        datadict['传真号码'] = word['words'].split(':')[1]
    #        continue
    #    if '注册地址】' in word['words']:
    #        datadict['注册地址'] = word['words'].split(':')[1]
    #        continue
    #    if '核准日期】' in word['words']:
    #        datadict['核准日期'] = word['words'].split('】')[1]
    #        continue
    #    elif '核准日期]' in word['words']:
    #        datadict['核准日期'] = word['words'].split(']')[1]
    #        continue
    #    if '修改日期】' in word['words']:
    #        datadict['修改日期'] = word['words'].split('】')[1]
    #        continue
    #    elif '修改日期]' in word['words']:
    #        datadict['修改日期'] = word['words'].split(']')[1]
    #        continue
    #    if ('【' not in word['words']) or ('】' not in word['words']) or ('[' not in word['words']) or (']' not in word['words']):
    #        if i > 0 and datadict:
    #            if ('份】' in datas[i - 1]['words']) and ('成份' in datadict.keys()):
    #                datadict['成份'] += word['words']
    #                continue
    #            elif ('份]' in datas[i - 1]['words'])and ('成份' in datadict.keys()):
    #                datadict['成份'] += word['words']
    #                continue
    #            if ('状】' in datas[i - 1]['words']) and ('性状' in datadict.keys()):
    #                datadict['性状'] += word['words']
    #                continue
    #            elif ('状]' in datas[i - 1]['words']) and ('性状' in datadict.keys()):
    #                datadict['性状'] += word['words']
    #                continue
    #            if ('功能主治】' in datas[i - 1]['words']) and ('功能主治' in datadict.keys()):
    #                datadict['功能主治'] += word['words']
    #                continue
    #            if (('功能主治]' in datas[i - 1]['words']) or ('功能主治】' in datas[i - 1]['words'])) and ('功能主治' in datadict.keys()):
    #                datadict['功能主治'] += word['words']
    #                continue
    #            elif (('功能主治]' in datas[i - 2]['words']) or ('功能主治】' in datas[i - 2]['words'])) and ('功能主治' in datadict.keys()):
    #                datadict['功能主治'] += word['words']
    #                continue
    #            if ('用法用量】' in datas[i - 1]['words']) and ('用法用量' in datadict.keys()):
    #                datadict['用法用量'] += word['words']
    #                continue
    #            if (('用法用量]' in datas[i - 1]['words']) or ('用法用量】' in datas[i - 1]['words'])) and ('用法用量' in datadict.keys()):
    #                datadict['用法用量'] += word['words']
    #                continue
    #            elif (('用法用量]' in datas[i - 2]['words']) or ('用法用量】' in datas[i - 2]['words'])) and ('用法用量' in datadict.keys()):
    #                datadict['用法用量'] += word['words']
    #                continue
    #            elif (('用法用量]' in datas[i - 3]['words']) or ('用法用量】' in datas[i - 3]['words'])) and ('用法用量' in datadict.keys()):
    #                datadict['用法用量'] += word['words']
    #                continue
    #            if ('注意事项]' in datas[i - 1]['words']) or ('注意事项】' in datas[i - 1]['words']):
    #                datadict['注意事项'] += word['words']
    #                continue
    #            elif ('注意事项]' in datas[i - 2]['words']) or ('注意事项】' in datas[i - 2]['words']):
    #                datadict['注意事项'] += word['words']
    #                continue
    #            elif ('注意事项]' in datas[i - 3]['words']) or ('注意事项】' in datas[i - 3]['words']):
    #                datadict['注意事项'] += word['words']
    #                continue
    #            elif ('注意事项]' in datas[i - 4]['words']) or ('注意事项】' in datas[i - 4]['words']):
    #                datadict['注意事项'] += word['words']
    #                continue
    #            elif ('注意事项]' in datas[i - 5]['words']) or ('注意事项】' in datas[i - 5]['words']):
    #                datadict['注意事项'] += word['words']
    #                continue
    #            elif ('注意事项]' in datas[i - 6]['words']) or ('注意事项】' in datas[i - 6]['words']):
    #                datadict['注意事项'] += word['words']
    #                continue
    #            elif ('注意事项]' in datas[i - 7]['words']) or ('注意事项】' in datas[i - 7]['words']):
    #                datadict['注意事项'] += word['words']
    #                continue
    #            elif ('注意事项]' in datas[i - 8]['words']) or ('注意事项】' in datas[i - 8]['words']):
    #                datadict['注意事项'] += word['words']
    #                continue
    #            elif ('注意事项]' in datas[i - 9]['words']) or ('注意事项】' in datas[i - 9]['words']):
    #                datadict['注意事项'] += word['words']
    #                continue
    #            elif ('注意事项]' in datas[i - 10]['words']) or ('注意事项】' in datas[i - 10]['words']):
    #                datadict['注意事项'] += word['words']
    #                continue
    #            elif ('注意事项]' in datas[i - 11]['words']) or ('注意事项】' in datas[i - 11]['words']):
    #                datadict['注意事项'] += word['words']
    #                continue
    #            elif ('注意事项]' in datas[i - 12]['words']) or ('注意事项】' in datas[i - 12]['words']):
    #                datadict['注意事项'] += word['words']
    #                continue
    #            elif ('注意事项]' in datas[i - 13]['words']) or ('注意事项】' in datas[i - 13]['words']):
    #                datadict['注意事项'] += word['words']
    #                continue
    #    print(datas[i]['words'])
    return datadict

        
        
            
    #print(data['words_result']) 

if __name__ == '__main__':
    codepath = os.path.dirname(__file__)
    datapath = codepath + '\data'
    files = os.listdir(datapath)
    #db = cxOracle()
    for file in files:
        #format_data = format_introduction(datapath + '\\' + file)
        format_data = inrtroduction_test(datapath + '\\' + file)
        print(format_data)
        if not format_data:
            continue
        #addsql = db.getsavesql('DRUGPACKAGEINSERT', format_data)
        #db.insert(addsql)
        #datajson = load_json(datapath + '\\' + file)
        #datas = datajson['words_result']
        #print(datas)
    
    

