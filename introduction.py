# -*- coding : utf-8 -*-

import os
import json
from DatabaseToolsNew import cxOracle
import re
from FindKeyword import findImportWords
import HowManyColumn4 as hmc
#import openpyxl
import xlwings as xw
import time
import hashlib
from log import LogMgr
from job import JobTable
import random
from json2word import json2word

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




class inrtroduction(object):
    def __init__(self):
        pass
    
    

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

def short_index(strword):
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
        if re_element.search(strword[:short_index(strword)]):
            return ['成份' , strword[re_element.search(strword).span()[1]:], re_element.search(strword).group()]
        elif re_function_category.search(strword[:index]):
            return ['作用类别' , strword[re_function_category.search(strword).span()[1] + 1:], re_function_category.search(strword).group()]
        elif re_traits.search(strword[:short_index(strword)]):
            return ['性状' , strword[re_traits.search(strword).span()[1]:],re_traits.search(strword).group()]
        elif re_indication.search(strword[:index]):
            return ['功能主治' , strword[re_indication.search(strword).span()[1]:],re_indication.search(strword).group()]
        elif re_specification.search(strword[:short_index(strword)]):
            return ['规格' , strword[re_specification.search(strword).span()[1]:],re_specification.search(strword).group()]
        elif re_dosage.search(strword[:index]):
            return ['用法用量' , strword[re_dosage.search(strword).span()[1]:],re_dosage.search(strword).group()]
        elif re_reaction.search(strword[:index]):
            return ['不良反应' , strword[re_reaction.search(strword).span()[1]:],re_reaction.search(strword).group()]
        elif re_prohibition.search(strword[:short_index(strword)]):
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
        elif re_element_accu.search(strword[:short_index(strword) - 1]):
            return ['成份' , strword[re_element_accu.search(strword).span()[1]:], re_element_accu.search(strword).group()]
        elif re_function_category.search(strword[:index]):
            return ['作用类别' , strword[re_function_category.search(strword).span()[1]:], re_function_category.search(strword).group()]
        elif re_traits_accu.search(strword[:short_index(strword) - 1]):
            return ['性状' , strword[re_traits_accu.search(strword).span()[1]:],re_traits_accu.search(strword).group()]
        elif re_indication_accu.search(strword[:index]):
            return ['功能主治' , strword[re_indication_accu.search(strword).span()[1]:],re_indication_accu.search(strword).group()]
        elif re_specification_accu.search(strword[:short_index(strword) - 1]):
            return ['规格' , strword[re_specification_accu.search(strword).span()[1]:],re_specification_accu.search(strword).group()]
        elif re_dosage_accu.search(strword[:index]):
            return ['用法用量' , strword[re_dosage_accu.search(strword).span()[1]:],re_dosage_accu.search(strword).group()]
        elif re_reaction_accu.search(strword[:index]):
            return ['不良反应' , strword[re_reaction_accu.search(strword).span()[1]:],re_reaction_accu.search(strword).group()]
        elif re_prohibition_accu.search(strword[:short_index(strword) - 1]):
            return ['禁忌' , strword[re_prohibition_accu.search(strword).span()[1]:],re_prohibition_accu.search(strword).group()]
        elif re_precautions_accu.search(strword[:index]):
            return ['注意事项' , strword[re_precautions_accu.search(strword).span()[1]:],re_precautions_accu.search(strword).group()]
        elif re_registeraddr.search(strword[:index]):
            return ['注册地址' , strword[re_registeraddr.search(strword).span()[1]:], re_registeraddr.search(strword).group()]
        elif re.match(r'.?[0oO]T[CO0]*|.?[0oO]*T[CO0]', strword[:5]):
            return ['OTC', '是', 'otc']
        elif len(strword) == 1 and strword == '外':
            return ['外', '是', '外']
        elif re.match(r'.?说明书外', strword[-4:]):
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
                if re.match(r'[【\[]|.?[】\]]|.?[:：]', word['words'][:8]):
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
    

def generatemd5(strid):
    md5 = hashlib.md5()
    md5.update(strid.encode('utf-8'))
    return md5.hexdigest()
    
            
def getscore(datas, nums):
    scores = 0
    if nums == 0:
        return 0
    for data in datas:
        scores += data['probability']['average']
    return (scores / nums) * 100

def middict(datas, middatapath, filename):
    if not os.path.exists(middatapath):
        os.makedirs(middatapath)
    relist = []
    for word in datas:
        relist.append(word['words'])
    json2word(relist, middatapath, filename)
    return middatapath + '\\' + filename


def randomidcode():
    letter = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    randomnum = random.randint(1000, 99999)
    if randomnum < 10000:
        return random.choice(letter) + '00000' + str(randomnum)
    else:
        return random.choice(letter) + '0000' + str(randomnum)

if __name__ == '__main__':
    codepath = os.path.dirname(__file__)
    datapath = codepath + '\data'
    files = os.listdir(datapath)
    #excel_path = 'C:\\Users\\DevinChang\\Desktop\\四家分公司影印件清单_去重匹配版.xlsx'
    #这是笔记本上的路径
    excel_path = 'C:\\Users\\dongd\\Desktop\\四家分公司影印件清单_去重匹配版.xlsx'
    #shopid, name, strength, mfrs  = load_excel(excel_path)
    db = cxOracle()
    job = JobTable() 
    imgpath_root = "F:\IMG"
    #笔记本上的是移动硬盘的路径
    imgpaht_root_desktop = "G:\IMG"
    path_root = "G:\源文件"
    datas = []
    leftdata = []
    rightdata = []
    nums = 0
    flag = 0
    #FIXME:需修改SRC_CO字段
    srcco_dir = os.listdir(datapath)
    for file in os.walk(datapath):
        page = 0
        for file_name in file[2]:
            if '说明书' in file_name:
                imgname = file_name.split('.')[0]
                curpath = file[0].split('data')[1]
                index = imgname.rfind('_')
                id = curpath[curpath.rfind('\\') + 1:]
                #dragname = re.search(r'[\u4e00-\u9fa5]+', file_name).group()
                dragname = re.search(r'[\u4e00-\u9fa5]+', id).group()
                id_code = randomidcode()
                datajson = load_json(file[0] + '\\' + file_name)
                #图片过大或者一些原因，没有识别出来就会有error_code字段
                if 'error_code' in datajson:
                    logmgr.error(file[0] + '\\' + file_name + ':' 'Size Error!')
                    continue
                source_img_path = imgpaht_root_desktop + '\\' + curpath + '\\' + imgname[:index] + '.' + imgname[index:].split('_')[1]
                original_path = path_root + '\\' + curpath + '\\' + imgname[:index - 2] + '.' + 'pdf'
                #FIXME:换工作环境这里也得改！
                try:
                    kindict = hmc.kinds(source_img_path, datajson)
                except Exception as e:
                    logmgr.error(file[0] + '\\' + file_name + ':' + str(e))
                    continue
                print('Current processing: {}'.format(imgpaht_root_desktop + '\\' + curpath + 
                                        '\\' + imgname[:index] + 
                                        '.' + imgname[index:].split('_')[1], 
                                        file[0] + '\\' + file_name))
                
                datatmp = datajson['words_result']
                nums += datajson['words_result_num']
                if kindict['kinds'] == 2:
                    datas += subfiledata(kindict['direction'], kindict['parameter'], kindict['boundary'][0], datatmp)
                elif kindict['kinds'] == 1:
                    datas += datatmp
                flag = 1
                page += 1
                jobdict = {}
                #服务器
                jobdict['SER_IP'] = '10.67.28.8'
                #job id
                jobdict['JOB_ID'] = generatemd5(file[0])
                jobdict['SRC_FILE_NAME'] = imgname[:index - 2] + '.' + 'pdf'
                jobdict['SRC_FILE_PATH'] = original_path
                #原文件
                jobdict['CUT_FILE_NAME'] = imgname[:index] + '.' + imgname[index:].split('_')[1]
                #原路径
                jobdict['CUT_FILE_PATH'] = imgpaht_root_desktop + '\\' + curpath
                #中间文件
                jobdict['MID_FILE_NAME'] = file_name
                #中间文件路径
                jobdict['MID_FILE_PATH'] = file[0]
                #评分
                jobdict['OCR_SCORE'] = int(getscore(datas, nums))
                #时间
                jobdict['HANDLE_TIME'] = time.strftime("%Y-%m-%d %X", time.localtime())
                #药品名
                jobdict['DRUG_NAME'] = dragname
                #影像件类型
                jobdict['FILE_TYPE'] = '说明书全文'
                #影像件内容是否入库
                if len(datas) > 0 and nums > 0:
                    jobdict['IS_TO_DB'] = 'T'
                else:
                    jobdict['IS_TO_DB'] = 'F'
                #同一套影像件识别码
                jobdict['ID_CODE'] = id_code
                #分公司
                jobdict['SRC_CO'] = curpath.split('\\')[1]
                #源文件相对路径
                jobdict['FILE_REL_PATH'] = '\\' + imgname[:index] + '.' + imgname[index:].split('_')[1]
                #文件服务器域名
                jobdict['SYS_URL'] = '10.67.28.8'
                #文件文本内容
                jobdict['FILE_TEXT'] = middict(datas, codepath + '\\middata\\' + curpath, imgname)
                #页数
                jobdict['PAGE_NUM'] = page
                #文件ocr解析识别状态 fk sysparams
                jobdict['OCR_STATE'] = 'T'
                #备注说明
                jobdict['REMARK'] = ''
                #创建用户
                jobdict['ADD_USER'] = 'DevinChang'
                job.job_add(jobdict)
                job.job_todb()
                job.job_del()
        if flag:
            if len(datas) > 0 and nums > 0:
                datadict = inrtroduction(datas, nums)
                print(datadict)
                if not datadict:
                    #db.update('OCRWORKFILE', 'JOB_ID', jobdict['JOB_ID'], 'IS_TO_DB', 'F')
                    nums = cleandata(datadict, datas, nums)
                    continue
                
                if "通用名称" not in datadict:
                    datadict.update({"通用名称" : dragname})
                else:
                    datadict["通用名称"] = dragname

                    
                if datadict['通用名称']:
                    if re.match(r'[\u4e00-\u9fa5]*', datadict['通用名称']):
                        datadict['通用名称'] = re.match(r'[\u4e00-\u9fa5]*', datadict['通用名称']).group()
                    
                datadict = maxdata(datadict)
                datadict.update({"ID_CODE" : id_code})
                if '企业名称' in datadict:
                    if ('生产厂家' not in datadict) or (len(datadict['生产厂家'])== 0):
                        datadict.update({"生产厂家" : datadict['企业名称']})
                        del datadict['企业名称']
                if '生产厂家' in datadict:
                    #用正则 DONE
                    re_comfrs =re.compile(r'企*业名称[:：]*|企业*名称[:：]*')
                    if re_comfrs.match(datadict['生产厂家']):
                        comfrs_index = re_comfrs.match(datadict['生产厂家']).span()[1]
                        datadict['生产厂家'] = datadict['生产厂家'][comfrs_index:]

                #if ("膏" or "贴") in datadict['通用名称'][-1]:
                #    if "外" not in datadict:
                #        datadict.update({"外" : "是"})
                if '批准文号' in datadict:
                    re_guoyao = re.compile(r'国药准?字?|国?药准?字|国药?准字')
                    if re_guoyao.match(datadict['批准文号']):
                        re.sub(re_guoyao, '国药准字', datadict['批准文号'])
                try:
                    addsql, param = db.getsavesql('DRUGPACKAGEINSERT', datadict, 1)
                    db.insert(addsql, param)
                    nums = cleandata(datadict, datas, nums)
                except Exception as e:
                    print('Error: ', e)
                    logmgr.error(file[0] + '\\' + file_name + "insert error!! : " + str(e))
                    nums = cleandata(datadict, datas, nums)
                    continue
            #else:
            #    db.update('OCRWORKFILE','JOB_ID', jobdict['JOB_ID'], 'IS_TO_DB', 'F')

        #print(datas)
    
    

def run_introduction(path, id_code):
    codepath = os.path.dirname(__file__)
    datapath = codepath + '\data'
    files = os.listdir(datapath)
    #excel_path = 'C:\\Users\\DevinChang\\Desktop\\四家分公司影印件清单_去重匹配版.xlsx'
    #这是笔记本上的路径
    #shopid, name, strength, mfrs  = load_excel(excel_path)
    db = cxOracle()
    job = JobTable() 
    imgpath_root = "F:\IMG"
    #笔记本上的是移动硬盘的路径
    imgpaht_root_desktop = "G:\IMG"
    path_root = "G:\源文件"
    datas = []
    leftdata = []
    rightdata = []
    nums = 0
    flag = 0
    #FIXME:需修改SRC_CO字段
    srcco_dir = os.listdir(datapath)
    for file in os.walk(path):
        page = 1
        jobdict = {}
        for file_name in file[2]:
            if '说明书' in file_name:
                imgname = file_name.split('.')[0]
                curpath = file[0].split('data')[1]
                index = imgname.rfind('_')
                id = curpath[curpath.rfind('\\') + 1:]
                dragname = re.search(r'[\u4e00-\u9fa5]+', file_name).group()
                #dragname = re.search(r'[\u4e00-\u9fa5]+', id).group()
                datajson = load_json(file[0] + '\\' + file_name)
                source_img_path = imgpaht_root_desktop + '\\' + curpath + '\\' + imgname[:index] + '.' + imgname[index:].split('_')[1]
                original_path = path_root + '\\' + curpath + '\\' + imgname[:index - 2] + '.' + 'pdf'
                #服务器
                jobdict['SER_IP'] = '10.67.28.8'
                #job id
                job_id = generatemd5(file[0] + imgname)[:20]
                jobdict['JOB_ID'] = job_id
                jobdict['SRC_FILE_NAME'] = imgname[:index - 2] + '.' + 'pdf'
                jobdict['SRC_FILE_PATH'] = original_path
                #原文件
                jobdict['CUT_FILE_NAME'] = imgname[:index] + '.' + imgname[index:].split('_')[1]
                #原路径
                jobdict['CUT_FILE_PATH'] = imgpaht_root_desktop + '\\' + curpath
                #时间
                jobdict['HANDLE_TIME'] = time.strftime("%Y-%m-%d %X", time.localtime())
                #药品名
                jobdict['DRUG_NAME'] = dragname
                #影像件类型
                jobdict['FILE_TYPE'] = '说明书全文'
                #同一套影像件识别码
                jobdict['ID_CODE'] = id_code
                #分公司
                jobdict['SRC_CO'] = curpath.split('\\')[1]
                #源文件相对路径
                jobdict['FILE_REL_PATH'] = '\\' + imgname[:index] + '.' + imgname[index:].split('_')[1]
                #文件服务器域名
                jobdict['SYS_URL'] = '10.67.28.8'
                #页数
                jobdict['PAGE_NUM'] = page
                #文件ocr解析识别状态 fk sysparams
                jobdict['OCR_STATE'] = 'T'
                #备注说明
                jobdict['REMARK'] = ''
                #创建用户
                jobdict['ADD_USER'] = 'DevinChang'
                #图片过大或者一些原因，没有识别出来就会有error_code字段
                if 'error_code' in datajson:
                    jobdict['IS_TO_DB'] = 'F'
                    job.job_add(jobdict)
                    job.job_todb()
                    job.job_del()
                    logmgr.error(file[0] + '\\' + file_name + ':' 'Size Error!')
                    continue
                #FIXME:换工作环境这里也得改！
                try:
                    kindict = hmc.kinds(source_img_path, datajson)
                except Exception as e:
                    logmgr.error(file[0] + '\\' + file_name + ':' + str(e))
                    continue
                print('Current processing: {}'.format(imgpaht_root_desktop + '\\' + curpath + 
                                        '\\' + imgname[:index] + 
                                        '.' + imgname[index:].split('_')[1], 
                                        file[0] + '\\' + file_name))
                
                datatmp = datajson['words_result']
                nums += datajson['words_result_num']
                if kindict['kinds'] == 2:
                    datas += subfiledata(kindict['direction'], kindict['parameter'], kindict['boundary'][0], datatmp)
                elif kindict['kinds'] == 1:
                    datas += datatmp
                flag = 1
                page += 1
                
                #中间文件
                jobdict['MID_FILE_NAME'] = file_name
                #中间文件路径
                jobdict['MID_FILE_PATH'] = file[0]
                #评分
                jobdict['OCR_SCORE'] = int(getscore(datas, nums))
                
                #影像件内容是否入库
                if len(datas) > 0 and nums > 0:
                    jobdict['IS_TO_DB'] = 'T'
                else:
                    jobdict['IS_TO_DB'] = 'F'
                
                #文件文本内容
                jobdict['FILE_TEXT'] = middict(datas, codepath + '\\middata\\' + curpath, imgname)
                ###############
                #jobdict['JOB_ID'] = generatemd5(jobdict['FILE_TEXT'])
                ###############
                
                job.job_add(jobdict)
                job.job_todb()
                job.job_del()
        if flag:
            if len(datas) > 0 and nums > 0:
                datadict = inrtroduction(datas, nums)
                if not datadict:
                    #db.update('OCRWORKFILE', 'JOB_ID', jobdict['JOB_ID'], 'IS_TO_DB', 'F')
                    nums = cleandata(datadict, datas, nums)
                    continue
                
                if "通用名称" not in datadict:
                    datadict.update({"通用名称" : dragname})
                else:
                    datadict["通用名称"] = dragname

                    
                if datadict['通用名称']:
                    if re.match(r'[\u4e00-\u9fa5]*', datadict['通用名称']):
                        datadict['通用名称'] = re.match(r'[\u4e00-\u9fa5]*', datadict['通用名称']).group()
                    
                datadict = maxdata(datadict)
                datadict.update({"ID_CODE" : id_code})
                #datadict.update({"JOB_ID": job_id})
                #datadict.update({"ADD_USER" : 'DevinChang'})
                if '企业名称' in datadict:
                    if ('生产厂家' not in datadict) or (len(datadict['生产厂家'])== 0):
                        datadict.update({"生产厂家" : datadict['企业名称']})
                        del datadict['企业名称']
                if '生产厂家' in datadict:
                    #用正则 DONE
                    re_comfrs =re.compile(r'企*业名称[:：]*|企业*名称[:：]*')
                    if re_comfrs.match(datadict['生产厂家']):
                        comfrs_index = re_comfrs.match(datadict['生产厂家']).span()[1]
                        datadict['生产厂家'] = datadict['生产厂家'][comfrs_index:]

                #if ("膏" or "贴") in datadict['通用名称'][-1]:
                #    if "外" not in datadict:
                #        datadict.update({"外" : "是"})
                if '批准文号' in datadict:
                    re_guoyao = re.compile(r'国药准?字?|国?药准?字|国药?准字')
                    if re_guoyao.match(datadict['批准文号']):
                        re.sub(re_guoyao, '国药准字', datadict['批准文号'])
                print(datadict)
                try:
                    addsql, param = db.getsavesql('DRUGPACKAGEINSERT', datadict, 1)
                    db.insert(addsql, param)
                    nums = cleandata(datadict, datas, nums)
                except Exception as e:
                    print('Error: ', e)
                    logmgr.error(file[0] + '\\' + file_name + "insert error!! : " + str(e))
                    db.update('OCRWORKFILE','JOB_ID', job_id,'IS_TO_DB','F')
                    nums = cleandata(datadict, datas, nums)
                    continue