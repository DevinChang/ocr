import os
import json
import re
import hashlib
from DatabaseToolsNew import cxOracle
class ProcessForRGA:
    # def __init__(self):
    #     self.start()

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

    def generatemd5(self,strid):
        md5 = hashlib.md5()
        md5.update(strid.encode('utf-8'))
        return md5.hexdigest()

    def _fenlan(self,fullpath):#F:\测试\json\test'
        # for root,dirs,files in os.walk(filepath):
        #     for file in files:
        #         if '进口药品注册证' in file and file[-4:]=='json':
        #             # jobdict['JOB_ID'] = generatemd5(file[0])
        #             fullpath = os.path.join(root,file)
                    if os.path.isfile(fullpath):
                        print('--------------------------'+fullpath+'-------------------------------')
                        jsondict = self._ReadJsonFile(fullpath)#读取json 返回json字典
                        words_result = jsondict['data']['words_result']#获取内容字典
                        words_result_num = jsondict['data']['words_result_num']
                        maxwidth = words_result[0]['location']['width']
                        leftlist = []
                        rightlist = []
                        rightlocation = 10000
                        beginflag = 0
                        endflag  = 10000
                        for i in words_result:
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
                            else:
                                pass
                        for i in words_result:
                            if endflag-10 > i['location']['top'] >= beginflag-20 :
                                if i['location']['left'] >  rightlocation - maxwidth/6:
                                    rightlist.append(i)
                                else:
                                    leftlist.append(i)
                        print("left----------------------------")
                        firstkey,jianju = self._getjianju(leftlist)
                        finaldic = {'药品名称':'','主要成份':'','剂型':'','包装规格':'','生产厂':'','国家':'','商品名':'','药品有效期':'','规格':'','日期':''}
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
                        dbdict['DRUG_NAME'] = finaldic['药品名称']
                        dbdict['TRADE_NAME'] = finaldic['商品名']
                        dbdict['DRUG_FORM'] = finaldic['剂型']
                        dbdict['STRENGTH'] = finaldic['规格']
                        dbdict['MFRS'] = finaldic['生产厂']
                        dbdict['APRV_DATE'] = finaldic['日期']
                        dbdict['COUNTRY'] = finaldic['国家']
                        print(dbdict)
                        # return dbdict
                    else:
                        print(fullpath+'-----文件错误')

    def _getjianju(self,leftlist):
        a = [ '药品名称', '主要成份', '剂型', '包装规格', '生产厂']
        jianju1 = 0
        jianju2 = 0
        list =[]
        for i in range(len(leftlist)):
            if self._judge_keywords(leftlist[i]['words']) != None and self._judge_keywords(leftlist[i]['words'])[0] in a:
                for j in range(i, len(leftlist), 1):
                    if self._judge_keywords(leftlist[j]['words']) != None and self._judge_keywords(leftlist[j]['words'])[0] in a:
                        if a.index(self._judge_keywords(leftlist[i]['words'])[0]) + 1 == a.index(
                                self._judge_keywords(leftlist[j]['words'])[0]):
                            jianju1 = leftlist[j]['location']['top'] - leftlist[i]['location']['top'] - \
                                     leftlist[i]['location']['height']
                            # print(leftlist[i]['words'],leftlist[j]['words'])
                            return i,jianju1


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


    def start(self,filepath):
        # pfrga = ProcessForRGA()
        for root,dirs,files in os.walk(filepath):
            for file in files:
                if '进口药品注册证' in file and file[-4:]=='json':
                    # jobdict['JOB_ID'] = generatemd5(file[0])
                    fullpath = os.path.join(root,file)

                    #这是最终的数据库需要的字典
                    dbdict =  self._fenlan(fullpath)#{'DRUG_NAME': '氯米龙滴眼液', 'TRADE_NAME': '关童', 'DRUG_FORM': '滴眼', 'STRENGTH': '5ml: Ing', 'MFRS': '等天制药株式会社滋贺工', 'APRV_DATE': '', 'COUNTRY': '日本'}

                    #这里需要在dbdict基础上插入job_id 同一套识别码 备注 创建用户  创建时间
                    dbdict['JOB_ID']=''
                    dbdict['ID_CODE'] = ''
                    dbdict['REMARK'] = ''
                    dbdict['ADD_USER'] = ''
                    dbdict['ADD_TIME'] = ''
                    # 这里调用数据库存储
                    dbtool = cxOracle()

                    # 用getsavesql()得到插入sql然后insert(tablename,sql,pram)插入
                    dbtool.insert(dbtool.getsavesql('DRUGREGAPPROVAL',dbdict,0))



pga = ProcessForRGA()
pga.start('F;/test')
