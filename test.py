# -*- coding : utf-8 -*-

import os
import json
from DatabaseToolsNew import cxOracle
import re
from FindKeyword import findImportWords
import HowManyColumn4 as hmc
#import openpyxl
import xlwings as xw
from log import LogMgr

logmgr = LogMgr()

'''
使用openpyxl太慢了,改用xlwings
wb = openpyxl.load_workbook('C:\\Users\\DevinChang\\Desktop\\四家分公司影印件清单_去重匹配版.xlsx')
sheets = wb.sheetnames
sheet = wb.get_sheet_by_name(sheets[0])
shopid = sheet['B']
name = sheet['C']
strength = sheet['D']
mfrs = sheet['F']
'''

def load_excel(excel):
    wb = xw.Book(excel)
    sheet = wb.sheets[0]
    shopid = sheet['B:B'].value
    name = sheet['C:C'].value
    strength = sheet['D:D'].value
    mfrs = sheet['F:F'].value
    return shopid, name, strength, mfrs




def load_json(file):
    with open(file, 'r', encoding='utf-8') as f:
        return json.loads(f.read())

def sort_index(strword):
    if len(strword) <= 2:
        return len(strword)
    else:
        return 4


def judge_keywords(strword):
    '''判断关键字'''
    re_otc = re.compile(r'OTC*|O*TC|OT*C')
    re_common_name = re.compile(r'通?用名称?|通?用名?称')
    re_product_name = re.compile(r'商?品名称?|商?品名?称')
    re_english = re.compile(r'英文?名称?|英文名?称')
    re_pinyin = re.compile(r'汉语?拼音?|汉?语拼?音')
    re_element = re.compile(r'.?成份?[】\]]|.?成?份[】\]]')
    re_element_accu = re.compile(r'.?成份')
    re_traits = re.compile(r'.?性状?[】\]]|.?性?状[】\]]')
    re_traits_accu = re.compile(r'.?性状')
    re_function_category = re.compile(r'作用?类别?')
    re_indication = re.compile(r'.?适?应症[】\]]|.适应?症[】\]]|.适.??症[】\]]|.功?能主治?[】\]]|.功?能主?治[】\]]')
    re_indication_accu = re.compile(r'.?适?应症|.适应?症|.功?能主治?|.功?能主?治')
    re_specification = re.compile(r'.?规格?[】\]]|.?规?格[】\]]')
    re_specification_accu = re.compile(r'.?规格')
    re_dosage = re.compile(r'.?用?法用量?[】\]]|.?用?法用?量[】\]]')
    re_dosage_accu = re.compile(r'.?用?法用量?|.?用?法用?量')
    re_reaction = re.compile(r'.?不?良反应?[】\]]|.?不?良反?应[】\]]')
    re_reaction_accu = re.compile(r'.?不?良反应?|.?不?良反?应')
    re_prohibition = re.compile(r'.?禁忌?[】\]]|.?禁?忌[】\]]')
    re_prohibition_accu = re.compile(r'.?禁忌')
    re_precautions = re.compile(r'.?注?意事项?[】\]]|.?注?意事?项[】\]]|.?注?意事顶?[】\]]|.?注?意事?顶[】\]]')
    re_precautions_accu = re.compile(r'.?注?意事项?|.?注?意事?项')
    re_registeraddr = re.compile(r'注?册地址?|注?册地?址')
    re_qualitytel = re.compile(r'质?量电话|质量?电话')
    re_saletel = re.compile(r'销?售电话|销售?电话')
    #TODO:新增OTC,外的匹配

    if len(strword) >= 8: 
        index = 6
    else:
        index = len(strword)

    if re.match(r'.+?(?:】)|.+?(?:])', strword[:index]):
        #FIXME: 成份，性状字段缺失
        if re_element.search(strword[:sort_index(strword)]):
            return ['成份' , strword[re_element.search(strword).span()[1]:], re_element.search(strword).group()]
        elif re_function_category.search(strword[:index]):
            return ['作用类别' , strword[re_function_category.search(strword).span()[1] + 1:], re_function_category.search(strword).group()]
        elif re_traits.search(strword[:sort_index(strword)]):
            return ['性状' , strword[re_traits.search(strword).span()[1]:],re_traits.search(strword).group()]
        elif re_indication.search(strword[:index]):
            return ['功能主治' , strword[re_indication.search(strword).span()[1]:],re_indication.search(strword).group()]
        elif re_specification.search(strword[:sort_index(strword)]):
            return ['规格' , strword[re_specification.search(strword).span()[1]:],re_specification.search(strword).group()]
        elif re_dosage.search(strword[:index]):
            return ['用法用量' , strword[re_dosage.search(strword).span()[1]:],re_dosage.search(strword).group()]
        elif re_reaction.search(strword[:index]):
            return ['不良反应' , strword[re_reaction.search(strword).span()[1]:],re_reaction.search(strword).group()]
        elif re_prohibition.search(strword[:sort_index(strword)]):
            return ['禁忌' , strword[re_prohibition.search(strword).span()[1]:],re_prohibition.search(strword).group()]
        elif re_precautions.search(strword[:index]):
            return ['注意事项' , strword[re_precautions.search(strword).span()[1]:],re_precautions.search(strword).group()]
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
        elif re_qualitytel.search(strword[:index]):
            return ['质量电话' , strword[re_qualitytel.search(strword).span()[1] + 1:], re_qualitytel.search(strword).group()]
        elif re_saletel.search(strword[:index]):
            return ['销售电话' , strword[re_saletel.search(strword).span()[1] + 1:], re_saletel.search(strword).group()]
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
        elif re_element_accu.search(strword[:sort_index(strword) - 1]):
            return ['成份' , strword[re_element_accu.search(strword).span()[1]:], re_element_accu.search(strword).group()]
        elif re_function_category.search(strword[:index]):
            return ['作用类别' , strword[re_function_category.search(strword).span()[1]:], re_function_category.search(strword).group()]
        elif re_traits_accu.search(strword[:sort_index(strword) - 1]):
            return ['性状' , strword[re_traits_accu.search(strword).span()[1]:],re_traits_accu.search(strword).group()]
        elif re_indication_accu.search(strword[:index]):
            return ['功能主治' , strword[re_indication_accu.search(strword).span()[1]:],re_indication_accu.search(strword).group()]
        elif re_specification_accu.search(strword[:sort_index(strword) - 1]):
            return ['规格' , strword[re_specification_accu.search(strword).span()[1]:],re_specification_accu.search(strword).group()]
        elif re_dosage_accu.search(strword[:index]):
            return ['用法用量' , strword[re_dosage_accu.search(strword).span()[1]:],re_dosage_accu.search(strword).group()]
        elif re_reaction_accu.search(strword[:index]):
            return ['不良反应' , strword[re_reaction_accu.search(strword).span()[1]:],re_reaction_accu.search(strword).group()]
        elif re_prohibition_accu.search(strword[:sort_index(strword) - 1]):
            return ['禁忌' , strword[re_prohibition_accu.search(strword).span()[1]:],re_prohibition_accu.search(strword).group()]
        elif re_precautions_accu.search(strword[:index]):
            return ['注意事项' , strword[re_precautions_accu.search(strword).span()[1]:],re_precautions_accu.search(strword).group()]
        elif re_registeraddr.search(strword[:index]):
            return ['注册地址' , strword[re_registeraddr.search(strword).span()[1]:], re_registeraddr.search(strword).group()]
        elif re.match(r'[0oO]T[CO0]*|[0oO]*T[CO0]', strword[:3]):
            return ['OTC', '是', 'otc']
        elif len(strword) == 1 and strword == '外':
            return ['外', '是', '外']
        else:
            return None
        
def inrtroduction_judge(strword):
    keyword = judge_keywords(strword)
    if not keyword:
        return findImportWords(strword)
    else:
        return keyword

def GetRightStrength(strength):
    '''
    调整excle读取规格问题
    '''
    pattren = r'[0-9]+[TS丸袋片贴]'
    if '*'  in strength:
        strength = strength.split('*')[0]
    if 'IU' in strength:
        strength = strength.replace('IU','国际单位')
    elif 'iu' in strength:
        strength =strength.replace('iu','国际单位')
    elif ('U' in strength) and ('Ug' not in strength):
        strength =strength.replace('U','单位')
    elif ('u' in strength) and ('ug' not in strength):
        strength = strength.replace('u','单位')
    elif re.match(pattren,strength):
        if 'T' in strength:
            strength =strength.replace('T','人份')
        elif 'S' in strength:
            strength =''
        elif '丸' in strength:
            strength =''
        elif '袋' in strength:
            strength =''
        elif '片' in strength:
            strength =''
        elif '贴' in strength:
            strength =''
    print(strength)
    return strength


def inrtroduction(datas, nums):
    datadict = {}
    keylist = []
    i = 0
    flag = 1
    for (word, i) in zip(datas, range(0, nums)):
        list_result = inrtroduction_judge(word['words'])
        #阈值
        #if (word['probability']['average'] * 0.8 + word['probability']['min'] * 0.2) < 0.85:
        #    continue
        #if list_result != None and len(keylist) > 0:
        #    #此处有bug
        #    if list_result[0] in datadict and keylist[-1][0] != list_result[0]:
        #        #list_result = None
        #        datadict[list_result[0]] += list_result[1]
        #        continue
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
                if ("英文名称" in keylist[-1][0]) or ("汉语拼音" in keylist[-1][0]):
                    if re.match(r'[a-zA-z]+', word['words']):
                        flag = 1 
                    else:
                        break 
                elif "日期" in keylist[-1][0]:
                    if re.match(r'[0-9]{4}年?[0-9]{2}月?[0-9]{2}日?', word['words']):
                        flag = 1 
                    else:
                        break 
                elif "号码" in keylist[-1][0]:
                    if re.match(r'\d', word['words']):
                        if re.match(r'.+[\u4e00-\u9fa5]', word['words']):
                            break
                        else:
                            flag = 1
                    else:
                        break 
                elif "传真" in keylist[-1][0]:
                    if re.match(r'\d', word['words']):
                        if re.match(r'[\u4e00-\u9fa5]', word['words']):
                            break
                        else:
                            flag = 1
                elif "邮政编码" == keylist[-1][0]:
                    if re.match(r'\d', word['words']):
                        flag = 1             
                    else:
                        break 
                elif "网址" == keylist[-1][0]:
                    if re.match(r'.?[a-zA-Z]', word['words']):
                        flag = 1
                    else:
                        break
                elif "批准文号" == keylist[-1][0]:
                    if re.match(r'国?药准?字', word['words']):
                        flag = 1
                    elif re.match(r'.?[a-zA-Z][0-9]', word['words']) and (keylist[-1][1]
                                                                    in datadict['批准文号']):
                        flag = 1
                    else:
                        break
                elif "OTC" == keylist[-1][0]:
                    break
                elif "外" == keylist[-1][0]:
                    break
                #TODO:OTC，外，以及字段追加问题
                if re.match(r'[【\[]|.?[】\]]', word['words'][:8]):
                    flag = 0
                    break
                if flag:
                    if keylist[-1][1] in datas[j]['words']:
                        datadict[keylist[-1][0]] += word['words']
                        break
                j -= 1  
    return datadict
            

def subfiledata(direction, parameter, boundary, datas):
    leftdata = []
    rightdata = []
    for data in datas:
        if direction == 1 or direction == 2:
            if data['location'][parameter] >= boundary:
                #此处有bug
                leftdata.append(data)
            else:
                rightdata.append(data)
        else:
            if data['location'][parameter] <= boundary:
                leftdata.append(data)
            else:
                rightdata.append(data)
    return leftdata + rightdata

        


    

def cleandata(datadict, data, num):
    if datadict:
        datadict.clear()
    if data:
        data.clear()
    if num != 0:
        num = 0
    return num



        
        
def maxdata(datadict):
    if "通用名称" in datadict:
        datadict['通用名称'] = datadict['通用名称'][:50]
    if "英文名称" in datadict:
        datadict['英文名称'] = datadict['英文名称'][:50]
    if "商品名称" in datadict:
        datadict['商品名称'] = datadict['商品名称'][:50]
    if "汉语拼音" in datadict:
        datadict['汉语拼音'] = datadict['汉语拼音'][:25]
    if "成份" in datadict:
        datadict['成份'] = datadict['成份'][:500]
    if "性状" in datadict:
        datadict['性状'] = datadict['性状'][:250]
    if "作用类别" in datadict:
        datadict['作用类别'] = datadict['作用类别'][:250]
    if "贮藏" in datadict:
        datadict['贮藏'] = datadict['贮藏'][:250]
    if "包装" in datadict:
        datadict['包装'] = datadict['包装'][:250]
    if "有效期" in datadict:
        datadict['有效期'] = datadict['有效期'][:250]
    if "生产地址" in datadict:
        datadict['生产地址'] = datadict['生产地址'][:250]
    if "生产厂家" in datadict:
        datadict['生产厂家'] = datadict['生产厂家'][:250]
    if "企业名称" in datadict:
        datadict['企业名称'] = datadict['企业名称'][:250]
    if "企业地址" in datadict:
        datadict['企业地址'] = datadict['企业地址'][:250]
    if "邮政编码" in datadict:
        datadict['邮政编码'] = datadict['邮政编码'][:10]
    if "电话号码" in datadict:
        datadict['电话号码'] = datadict['电话号码'][:25]
    if "传真号码" in datadict:
        datadict['传真号码'] = datadict['传真号码'][:25]
    if "网址" in datadict:
        datadict['网址'] = datadict['网址'][:100]
    #if "委托方企业名称" in datadict:
    #    datadict['委托方企业名称'] = datadict['委托方企业名称'][:]
    return datadict
    
    
            

if __name__ == '__main__':
    datajson = load_json('F:\DevinChang\Code\Python\ocr\data\国控盐城\西药\葡萄糖酸钙锌口服溶液A000060279\\药品说明书_1_jpg.json')
    datas = datajson['words_result']
    nums = datajson['words_result_num']
    #kindict = hmc.kinds('C:\\Users\\dongd\\Desktop\\阿奇霉素颗粒A000021514\\药品说明书_2.jpg', datajson)
    #datas = subfiledata(kindict['direction'], kindict['parameter'], kindict['boundary'], datas)
    datadict = inrtroduction(datas, nums)
    
    #codepath = os.path.dirname(__file__)
    #datapath = codepath + '\data'
    #files = os.listdir(datapath)
    ##excel_path = 'C:\\Users\\DevinChang\\Desktop\\四家分公司影印件清单_去重匹配版.xlsx'
    ##这是笔记本上的路径
    #excel_path = 'C:\\Users\\dongd\\Desktop\\四家分公司影印件清单_去重匹配版.xlsx'
    ##shopid, name, strength, mfrs  = load_excel(excel_path)
    #db = cxOracle()
    #imgpath_root = "F:\IMG"
    ##笔记本上的是移动硬盘的路径
    #imgpaht_root_desktop = "G:\IMG"
    #datas = []
    #leftdata = []
    #rightdata = []
    #nums = 0
    #flag = 0
    #for file in os.walk(datapath):
    #    for file_name in file[2]:
    #        if '说明书' in file_name:
    #            imgname = file_name.split('.')[0]
    #            curpath = file[0].split('data')[1]
    #            index = imgname.rfind('_')
    #            id = curpath[curpath.rfind('\\') + 1:]
    #            datajson = load_json(file[0] + '\\' + file_name)
    #            #图片过大或者一些原因，没有识别出来就会有error_code字段
    #            if 'error_code' in datajson:
    #                continue
    #            #FIXME:换工作环境这里也得改！
    #            try:
    #                kindict = hmc.kinds(imgpaht_root_desktop + '\\' + curpath + 
    #                                        '\\' + imgname[:index] + 
    #                                        '.' + imgname[index:].split('_')[1], 
    #                                        datajson)
    #            except Exception as e:
    #                print("Error :", e)
    #                logmgr.error(file[0] + '\\' + file_name + ':' + str(e))
    #                continue
    #            print('Current processing: {}'.format(imgpaht_root_desktop + '\\' + curpath + 
    #                                    '\\' + imgname[:index] + 
    #                                    '.' + imgname[index:].split('_')[1], 
    #                                    file[0] + '\\' + file_name))
    #            
    #            datatmp = datajson['words_result']
    #            nums += datajson['words_result_num']
    #            if kindict['kinds'] == 2:
    #                datas += subfiledata(kindict['direction'], kindict['parameter'], kindict['boundary'][0], datatmp)
    #            elif kindict['kinds'] == 1:
    #                datas += datatmp
    #            flag = 1
    #    if flag:
    #        if len(datas) > 0 and nums > 0:
    #            datadict = inrtroduction(datas, nums)
    #            print(datadict)
    #            if not datadict:
    #                nums = cleandata(datadict, datas, nums)
    #                continue
    #            ##整个识别完后，再将excel表中对应的数据替换掉识别的结果
    #            #if id in shopid:
    #            #    index = shopid.index(id)
    #            #    #if "通用名称" in datadict:
    #            #    #    del datadict["通用名称"]
    #            #    #if "规格" in datadict:
    #            #    #    del datadict['规格']
    #            #    #if "生产厂家"in datadict:
    #            #    #    del datadict['生产厂家']
    #            #    if "通用名称" not in datadict:
    #            #        datadict.update({"通用名称" : name[index]})
    #            #    else:
    #            #        datadict["通用名称"] = name[index]
    #            #    #TODO:调整规格逻辑
    #            #    if "规格" not in datadict:
    #            #        strength_t = GetRightStrength(strength[index])
    #            #        if strength_t:
    #            #            datadict.update({"规格" : strength_t})
    #            #    else:
    #            #        strength_t = GetRightStrength(strength[index])
    #            #        if strength_t:
    #            #            datadict["规格"] = strength_t
    #            #    if "生产厂家" not in datadict:
    #            #        datadict.update({"生产厂家" : mfrs[index]})
    #            #    else:
    #            #        datadict["生产厂家"] = mfrs[index]
    #                
    #                
    #            datadict = maxdata(datadict)
    #            try:
    #                addsql, param = db.getsavesql('DRUGPACKAGEINSERT', datadict)
    #                db.insert(addsql, param)
    #                nums = cleandata(datadict, datas, nums)
    #            except Exception as e:
    #                print('Error: ', e)
    #                logmgr.error(file[0] + '\\' + file_name + "insert error!! : " + str(e))
    #                nums = cleandata(datadict, datas, nums)
    #                continue
    #    #print(datas)
    
    

