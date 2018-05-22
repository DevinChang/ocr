import os
import json
import re
import hashlib
import time
from log import LogMgr
from tool import Tools
from DatabaseToolsNew import cxOracle
class Improtdrug(Tools):
    def __init__(self,imgpath):
        Tools.__init__(self)
        self.imgpath = imgpath
        self.logmgr = LogMgr()

    def _ReadJsonFile( self,jsonfilepath):
        try:
            with open(jsonfilepath, 'r') as f:
                temp = json.loads(f.read())  # 将 JSON 对象转换为 Python 字典
        except UnicodeDecodeError as e:
            with open(jsonfilepath, 'r', encoding='utf-8') as f:
                temp = json.loads(f.read())  # 将 JSON 对象转换为 Python 字典
        except Exception as e:
            print(str(e))
        finally:
            return temp

    def _generatemd5(self,strid):
        md5 = hashlib.md5()
        md5.update(strid.encode('utf-8'))
        return md5.hexdigest()[:20]

    def _fenlan(self,fullpath):#F:\测试\json\test'
        # for root,dirs,files in os.walk(filepath):
        #     for file in files:
        #         if '进口药品注册证' in file and file[-4:]=='json':
        #             # jobdict['JOB_ID'] = generatemd5(file[0])
        #             fullpath = os.path.join(root,file)
        if os.path.isfile(fullpath):
            print('--------------------------'+fullpath+'-------------------------------')
            jsondict1 = self._ReadJsonFile(fullpath)#读取json 返回json字典
            jsondict = {'data':jsondict1}
            words_result = jsondict['data']['words_result']#获取内容字典
            words_result_num = jsondict['data']['words_result_num']
            maxwidth = words_result[0]['location']['width']
            leftlist = []
            rightlist = []
            rightlocation = 10000
            beginflag = 0
            endflag  = 10000
            ISSUE_DATE = ''
            zhucezhenghaonum=0#注册证号遍历计数
            LICENSENO = ''#注册证号
            #第一次遍历 获取提取范围
            for i in words_result:
                zhucezhenghaonum = zhucezhenghaonum +1
                if zhucezhenghaonum <10:#注册证号应该在前10行进行寻找
                    if re.search(r'[A-Z]*\d{8}\Z',i['words']):
                        LICENSENO = re.search(r'[A-Z]*\d{8}\Z',i['words']).group()#得到注册证号
                if i['location']['width'] > maxwidth:
                    maxwidth = i['location']['width']
                if re.match(r'公司*名称*|公*司名*称',i['words']):
                    beginflag = i['location']['top']
                elif re.match(r'备*注|备注*',i['words']):
                    endflag = i['location']['top']
                elif re.match(r'规格', i['words']):
                    if i['location']['left']< rightlocation:
                        rightlocation = i['location']['left']
                elif re.match(r'商品名', i['words']):
                    if i['location']['left']< rightlocation:
                        rightlocation = i['location']['left']
                elif re.match(r'药品有*效期*|药*品有效*期|药品*有*效期', i['words']):
                    if i['location']['left']< rightlocation:
                        rightlocation = i['location']['left']
                elif re.match(r'[0-9]+[年月日]+',i['words']):
                    ISSUE_DATE = i['words']
                else:
                    pass
            for i in words_result:
                if endflag-10 > i['location']['top'] >= beginflag-20 :
                    if i['location']['left'] >  rightlocation - maxwidth/6:
                        rightlist.append(i)
                    else:
                        leftlist.append(i)
            print("left----------------------------")
            jianju = self._getjianju(leftlist)
            finaldic = {'药品名称':'','主要成份':'','剂型':'','包装规格':'','生产厂':'','地址':'','国家':'','商品名':'','药品有效期':'','规格':'','日期':'','ID_CODE':'','JOB_ID':'','REMARK':'','ADDUSER':''}
            # print(firstkey,jianju)
            for i in leftlist:
                i_word_judge = self._judge_keywords(i['words'])
                if i_word_judge!=None:
                    finaldic[i_word_judge[0]] = i_word_judge[1]
                    for j in leftlist:
                        j_word_judge = self._judge_keywords(j['words'])
                        if j_word_judge==None and (i['location']['top']-jianju/3*2)<j['location']['top']<(i['location']['top']+jianju/3):
                            if i['location']['top']-jianju/3<j['location']['top']:
                                finaldic[i_word_judge[0]]=j['words']+finaldic[i_word_judge[0]]
                            else:
                                finaldic[i_word_judge[0]]=finaldic[i_word_judge[0]]+j['words']
            # print(finaldic)
            print("right-------------------------------------------------------------------------")
            for i in rightlist:
                i_word_judge = self._judge_keywords(i['words'])
                if i_word_judge!=None:
                    finaldic[i_word_judge[0]] = i_word_judge[1]
                    for j in rightlist:
                        j_word_judge = self._judge_keywords(j['words'])
                        if j_word_judge==None and (i['location']['top']-jianju/3*2)<j['location']['top']<(i['location']['top']+jianju/3):
                            if i['location']['top']-jianju/3<j['location']['top']:
                                finaldic[i_word_judge[0]]=j['words']+finaldic[i_word_judge[0]]
                            else:
                                finaldic[i_word_judge[0]]=finaldic[i_word_judge[0]]+j['words']
            print(finaldic)
            print("end------------------------------------------------------------------------------------")
            print()
            print()
            # self._savetoDB(finaldic)
            dbdict = {}
            # dbdict['DRUG_NAME'] = finaldic['药品名称']#这是获取的直接OCR的药品名称

            dbdict['TRADE_NAME'] = finaldic['商品名']
            dbdict['DRUG_FORM'] = finaldic['剂型']
            dbdict['STRENGTH'] = finaldic['规格']
            dbdict['MFRS'] = finaldic['生产厂']
            dbdict['LICENSENO'] = LICENSENO#注册证号
            dbdict['ADDRESS'] = finaldic['地址']
            dbdict['ISSUE_DATE'] = ISSUE_DATE
            dbdict['COUNTRY'] = finaldic['国家']
            # print('dict = ' )
            # print(dbdict)
            return dbdict
        else:
            print(fullpath+'-----文件错误')

    def _getjianju(self,leftlist):
        a = [ '药品名称', '主要成份', '剂型', '包装规格', '生产厂','地址']
        jianju1 = 0
        jianju2 = 0
        list =[]
        try:
            for i in range(len(leftlist)):
                if self._judge_keywords(leftlist[i]['words']) != None and self._judge_keywords(leftlist[i]['words'])[0] in a:
                    for j in range(i, len(leftlist), 1):
                        if self._judge_keywords(leftlist[j]['words']) != None and self._judge_keywords(leftlist[j]['words'])[0] in a:
                            if a.index(self._judge_keywords(leftlist[i]['words'])[0]) + 1 == a.index(
                                    self._judge_keywords(leftlist[j]['words'])[0]):
                                jianju1 = leftlist[j]['location']['top'] - leftlist[i]['location']['top'] - \
                                         leftlist[i]['location']['height']
                                # print(leftlist[i]['words'],leftlist[j]['words'])
                                return jianju1
        except Exception as e:
            print(str(e))
            return 47


                            # print(leftlist[i]['words'],leftlist[i]['location']['top'],leftlist[i]['location']['height'])
                            # print(leftlist[j]['words'],leftlist[j]['location']['top'])
                            # return jianju1
                            # try:
                            #     return (getjianju(leftlist[i+1:])+jianju1)/2
                            # except:

    def _judge_keywords(self,strword):
        '''判断关键字'''
        re_company = re.compile(r'公司*名称*|公*司名*称')
        re_companyaddr = re.compile(r'地址')
        re_drugname = re.compile(r"药品*名称*|药*品名*称")
        re_tradename = re.compile(r"商*品名|商品*名|商")
        re_active = re.compile(r"主要*成份*|主要成份")
        re_dosage = re.compile(r'剂型')
        re_stength = re.compile(r"规格")
        re_manufacturer = re.compile(r"生产厂*|生产*厂")
        re_country = re.compile(r"国家")
        re_package = re.compile(r'包装*规格*|包*装规*格')
        re_addr = re.compile(r'地址')
        re_shelfdate = re.compile(r'药品有*效期*|药*品有效*期|药品*有*效期')
        #这里将提取关键字段的长度延长到了12个,尽可能的将由于印章等造成的干扰降低
        if len(strword) >= 4:
            index = 6
        else:
            index = len(strword)

        if (re.match(r'.+?(?:\:)', strword[:index])):
            # if re_company.search(strword[:index]):
            #     return ['公司名称', strword[re_company.search(strword).span()[1]+1:], re_company.search(strword).group()]

            if re_drugname.search(strword[:index]):
                return ['药品名称', strword[re_drugname.search(strword).span()[1]+1:], re_drugname.search(strword).group()]
            elif re_tradename.search(strword[:index]):
                return ['商品名', strword[re_tradename.search(strword).span()[1] + 1:], re_tradename.search(strword).group()]
            elif re_active.search(strword[:index]):
                return ['主要成份', strword[re_active.search(strword).span()[1] + 1:], re_active.search(strword).group()]
            elif re_dosage.search(strword[:index]):
                return ['剂型', strword[re_dosage.search(strword).span()[1] + 1:], re_dosage.search(strword).group()]
            elif re_stength.match(strword[:index]):
                return ['规格', strword[re_stength.match(strword).span()[1] + 1:], re_stength.match(strword).group()]
            elif re_manufacturer.search(strword[:index]):
                return ['生产厂', strword[re_manufacturer.search(strword).span()[1] + 1:], re_manufacturer.search(strword).group()]
            elif re_country.search(strword[:index]):
                return ['国家', strword[re_country.search(strword).span()[1] + 1:], re_country.search(strword).group()]
            elif re_package.match(strword[:index]):
                return ['包装规格', strword[re_package.match(strword).span()[1] + 1:], re_package.match(strword).group()]
            elif re_addr.search(strword[:index]):
                return ['地址', strword[re_addr.search(strword).span()[1] + 1:], re_addr.search(strword).group()]
            elif re_shelfdate.search(strword[:index]):
                return ['药品有效期', strword[re_shelfdate.search(strword).span()[1] + 1:], re_shelfdate.search(strword).group()]

            else:
                return None




        else:
            # if re_company.search(strword[:index]):
            #     return ['公司名称', strword[re_company.search(strword).span()[1] :], re_company.search(strword).group()]

            if re_drugname.search(strword[:index]):
                return ['药品名称', strword[re_drugname.search(strword).span()[1]:], re_drugname.search(strword).group()]
            elif re_tradename.search(strword[:index]):
                return ['商品名', strword[re_tradename.search(strword).span()[1] :], re_tradename.search(strword).group()]
            elif re_active.search(strword[:index]):
                return ['主要成份', strword[re_active.search(strword).span()[1] :], re_active.search(strword).group()]
            elif re_dosage.search(strword[:index]):
                return ['剂型', strword[re_dosage.search(strword).span()[1] :], re_dosage.search(strword).group()]
            elif re_stength.match(strword[:index]):
                return ['规格', strword[re_stength.match(strword).span()[1] :], re_stength.match(strword).group()]
            elif re_manufacturer.search(strword[:index]):
                return ['生产厂', strword[re_manufacturer.search(strword).span()[1] :], re_manufacturer.search(strword).group()]
            elif re_country.search(strword[:index]):
                return ['国家', strword[re_country.search(strword).span()[1] :], re_country.search(strword).group()]
            elif re_package.match(strword[:index]):
                return ['包装规格', strword[re_package.match(strword).span()[1] :], re_package.match(strword).group()]
            elif re_addr.search(strword[:index]):
                return ['地址', strword[re_addr.search(strword).span()[1] :], re_addr.search(strword).group()]
            elif re_shelfdate.search(strword[:index]):
                return ['药品有效期', strword[re_shelfdate.search(strword).span()[1] :], re_shelfdate.search(strword).group()]
            else:
                return None

    # def _savetoDB(self,finaldic):
    def _job(self,path,id_code):
        flag = 0
        for file in os.walk(path):
            for file_name in file[2]:
                page = 1
                if '进口药品注册证' in file_name:
                    imgname = file_name.split('.')[0]
                    curpath = file[0].split('data')[1]
                    index = imgname.rfind('_')
                    id = curpath[curpath.rfind('\\') + 1:]
                    dragname = re.search(r'[\u4e00-\u9fa5]+', id).group()
                    if dragname.find('(') > 0:
                        dragname = dragname[:dragname.find('(')]
                    #id_code = id[name_index_e - 1:]
                    datajson = self._load_json(file[0] + '\\' + file_name)
                    #图片过大或者一些原因，没有识别出来就会有error_code字段
                    if 'error_code' in datajson:
                        self.logmgr.error(file[0] + '\\' + file_name + ": img size error!")
                        continue
                    #source_img_path = imgpaht_root_desktop + '\\' + curpath + '\\' + imgname[:index] + '.' + imgname[index:].split('_')[1]
                    original_path = self.imgpath + '\\' + curpath + '\\' + imgname[:index - 2] + '.' + 'pdf'
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

                    jobdict = {}
                    #服务器
                    jobdict['SER_IP'] = '10.67.28.8'
                    #job id
                    jobdict['JOB_ID'] = self._generatemd5(file[0] + dragname)
                    jobdict['SRC_FILE_NAME'] = imgname[:index - 2] + '.' + 'pdf'
                    jobdict['SRC_FILE_PATH'] = original_path
                    #原文件
                    jobdict['CUT_FILE_NAME'] = imgname[:index] + '.' + imgname[index:].split('_')[1]
                    #原路径
                    jobdict['CUT_FILE_PATH'] = 'G:\\IMG' + '\\' + curpath
                    #中间文件
                    jobdict['MID_FILE_NAME'] = file_name
                    #中间文件路径
                    jobdict['MID_FILE_PATH'] = file[0]
                    #评分
                    jobdict['OCR_SCORE'] = int(self._getscore(datas, nums))
                    #时间
                    jobdict['HANDLE_TIME'] = time.strftime("%Y-%m-%d %X", time.localtime())
                    #药品名
                    jobdict['DRUG_NAME'] = dragname
                    #影像件类型
                    jobdict['FILE_TYPE'] = '进口药品注册证'
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
                    jobdict['FILE_TEXT'] = self._middict(datas, self.codepath + '\\middata\\' + curpath, imgname)
                    #页数
                    jobdict['PAGE_NUM'] = page
                    #文件ocr解析识别状态 fk sysparams
                    jobdict['OCR_STATE'] = 'T'
                    #备注说明
                    jobdict['REMARK'] = ''
                    #创建用户
                    jobdict['ADD_USER'] = 'DevinChang'
                    print('jobdict:',jobdict)
                    self.job.job_add(jobdict)
                    self.job.job_todb()
                    self.job.job_del()
                    page+=1


    def start(self,filepath,ID_CODE,ADD_USER,REMARK):
        # pfrga = ProcessForRGA()
        # print('begin job')
        # self._job(filepath,ID_CODE)
        # print('end job')
        temp = ''
        for file in os.walk(filepath):
            for file_name in file[2]:
                dbdict2 = {}
                ##################
                page = 1
                ####################
                if (('进口药品注册证' in file_name) or ('进口注册证' in file_name)) and file_name[-4:]=='json':
                    ##################
                    imgname = file_name.split('.')[0]
                    curpath = file[0].split('data')[1]
                    index = imgname.rfind('_')
                    id = curpath[curpath.rfind('\\') + 1:]
                    dragname = re.search(r'[\u4e00-\u9fa5]+', id).group()
                    if dragname.find('(') > 0:
                        dragname = dragname[:dragname.find('(')]
                    # id_code = id[name_index_e - 1:]
                    datajson = self._load_json(file[0] + '\\' + file_name)
                    # 图片过大或者一些原因，没有识别出来就会有error_code字段
                    if 'error_code' in datajson:
                        self.logmgr.error(file[0] + '\\' + file_name + ": img size error!")
                        continue
                    # source_img_path = imgpaht_root_desktop + '\\' + curpath + '\\' + imgname[:index] + '.' + imgname[index:].split('_')[1]
                    original_path = 'G:\\IMG' + '\\' + curpath + '\\' + imgname[:index - 2] + '.' + 'pdf'
                    # try:
                    #    kindict = hmc.kinds(source_img_path, datajson)
                    # except Exception as e:
                    #    logmgr.error(file[0] + '\\' + file_name + ':' + str(e))
                    #    continue
                    # print('Current processing: {}'.format(imgpaht_root_desktop + '\\' + curpath +
                    #                        '\\' + imgname[:index] +
                    #                        '.' + imgname[index:].split('_')[1],
                    #                        file[0] + '\\' + file_name))
                    datas = datajson['words_result']
                    nums = datajson['words_result_num']
                    flag = 1

                    jobdict = {}
                    # 服务器
                    jobdict['SER_IP'] = '10.67.28.8'
                    # job id
                    jobdict['JOB_ID'] = self._generatemd5(file[0] + imgname)
                    jobdict['SRC_FILE_NAME'] = imgname[:index - 2] + '.' + 'pdf'
                    jobdict['SRC_FILE_PATH'] = original_path
                    # 原文件
                    jobdict['CUT_FILE_NAME'] = imgname[:index] + '.' + imgname[index:].split('_')[1]
                    # 原路径
                    jobdict['CUT_FILE_PATH'] = 'G:\\IMG' + '\\' + curpath
                    # 中间文件
                    jobdict['MID_FILE_NAME'] = file_name
                    # 中间文件路径
                    jobdict['MID_FILE_PATH'] = file[0]
                    # 评分
                    jobdict['OCR_SCORE'] = int(self._getscore(datas, nums))
                    # 时间
                    jobdict['HANDLE_TIME'] = time.strftime("%Y-%m-%d %X", time.localtime())
                    # 药品名
                    jobdict['DRUG_NAME'] = dragname
                    # 影像件类型
                    jobdict['FILE_TYPE'] = '进口药品注册证'
                    # 影像件内容是否入库
                    if len(datas) > 0 and nums > 0:
                        jobdict['IS_TO_DB'] = 'T'
                    else:
                        jobdict['IS_TO_DB'] = 'F'
                    # 同一套影像件识别码
                    jobdict['ID_CODE'] = ID_CODE
                    # 分公司
                    jobdict['SRC_CO'] = curpath.split('\\')[1]
                    # 源文件相对路径
                    jobdict['FILE_REL_PATH'] = '\\' + imgname[:index] + '.' + imgname[index:].split('_')[1]
                    # 文件服务器域名
                    jobdict['SYS_URL'] = '10.67.28.8'
                    # 文件文本内容
                    jobdict['FILE_TEXT'] = self._middict(datas, self.codepath + '\\middata\\' + curpath, imgname)
                    ###############
                    jobdict['JOB_ID'] = self._generatemd5(jobdict['FILE_TEXT'])
                    temp = jobdict['FILE_TEXT']
                    ###############
                    # 页数
                    jobdict['PAGE_NUM'] = page
                    # 文件ocr解析识别状态 fk sysparams
                    jobdict['OCR_STATE'] = 'T'
                    # 备注说明
                    jobdict['REMARK'] = ''
                    # 创建用户
                    jobdict['ADD_USER'] = 'DevinChang'
                    print('jobdict:', jobdict)
                    self.job.job_add(jobdict)
                    self.job.job_todb()
                    self.job.job_del()
                    page += 1
                    ##################


                    fullpath = os.path.join(file[0],file_name)

                    #这是最终的数据库需要的字典
                    dbdict2 =  self._fenlan(fullpath)#{'DRUG_NAME': '氯米龙滴眼液', 'TRADE_NAME': '关童', 'DRUG_FORM': '滴眼', 'STRENGTH': '5ml: Ing', 'MFRS': '等天制药株式会社滋贺工', 'ISUUE_DATE': '', 'COUNTRY': '日本'}
                    print('dbdict2 =')
                    # print(dbdict2)
                    #这里需要在dbdict基础上插入job_id 同一套识别码 备注 创建用户  创建时间

                    # dbdict['JOB_ID']=self.generatemd5(os.path.join(root,file))
                    # print('1')
                    dbdict2['DRUG_NAME'] = dragname
                    dbdict2['ID_CODE'] = ID_CODE
                    # print('2')
                    dbdict2['REMARK'] = REMARK
                    dbdict2['ADD_USER'] = ADD_USER
                    dbdict2['JOB_ID'] = self._generatemd5(temp)
                    # dbdict2['ADD_TIME'] = ADD_TIME
                    print(dbdict2)

                    # cxoracle = cxOracle('scott', '123456')
                    cxoracle = cxOracle()
                    sql,pram=cxoracle.getsavesql('ImportedDrugLicense',dbdict2,2)

                    cxoracle.insert(sql,pram)


#
# pga = Improtdrug(r'F:\data\test')
# ID_CODE ='ss'
# pga.start(r'F:\data\test',ID_CODE,'shuai','')
