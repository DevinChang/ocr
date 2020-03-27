# -*- coding: utf-8 -*-
import os
import re
import json
import time
from log import LogMgr
from tool import Tools
import howManyColumnsOfCertificate as hmc
import hashlib


class ProductionCertificate(Tools):
    def __init__(self, jsonpath, imgpath):
        Tools.__init__(self)
        self.jsonpath = jsonpath
        self.imgpath = imgpath
        self.logmgr = LogMgr()
        

    def generatemd5(strid):
        md5 = hashlib.md5()
        md5.update(strid.encode('utf-8'))
        return md5.hexdigest()

    def subfiledata(self,direction, parameter, boundary, datas):
        leftdata = []
        rightdata = []
        for data in datas:
            if direction == 1 or direction == 2:
                if data['location'][parameter] >= boundary:
                    # 此处有bug
                    leftdata.append(data)
                else:
                    rightdata.append(data)
            else:
                if data['location'][parameter] <= boundary:
                    leftdata.append(data)
                else:
                    rightdata.append(data)
        return leftdata+(rightdata)

    def _productionCertificate(self, datas, nums):
        """
        识别生产许可证
        """
        keylist = []
        datadict = {}#这里做了一点小改动！！！！！！！！！！！！！！！！！！！1
        i = 0
        flag = 0
        for (word, i) in zip(datas, range(0, nums)):
            list_result = self._judge_keywords(word['words'])
            if list_result != None:
                if list_result[0] in datadict and keylist[-1][0] != list_result[0]:
                    datadict[list_result[0]] += list_result[1]
                    flag = 1
                else:
                    datadict[list_result[0]] = list_result[1]
                    flag = 1
                keylist.append([list_result[0], list_result[2]])
            else:
                flag = 1
                j = i
                while j >= 0:
                    if not keylist:
                        break
                    if ("分类码" in keylist[-1][0]):
                        if re.match(r'[a-zA-z]+', word['words']):
                            flag = 1
                        else:
                            break
                    elif "有效期至" in keylist[-1][0]:
                        if re.match(r'[0-9]+年?[0-9]+月?[0-9]+日?', word['words']):
                            flag = 1
                        else:
                            break

                    # # 字段追加问题
                    # if re.match(r'.?[:：]', word['words'][:10]) and not re.match(r'质*量受*权人*',word['words']):
                    #     if  not re.match(r'质*量受*权人*', word['words']):
                    #         flag = 0
                    #         break
                    if flag:
                        if keylist[-1][1] in datas[j]['words']:
                            datadict[keylist[-1][0]] += word['words']
                            break
                    j -= 1
                # datadict[list_result[0]] = list_result[1]
                # flag = 1

        return datadict


    def _judge_keywords(self, strword):
        '''判断关键字'''
        # re_coname = re.compile(r"企业*名称*|企*业名*称")
        # re_cernum = re.compile(r"证书*编号*|证*书编*号")
        # re_addr = re.compile(r"地址")
        # re_cerscope = re.compile(r"认证*范围*|认*证范*围")
        # re_valid = re.compile(r"有效期至*|有效*期至")
        # re_liceauth = re.compile(r"发证*机关*|发*证机*关")
        # re_licedate = re.compile(r"发证*日期*|发*证日*期")

        re_entname = re.compile(r"企业*名称*|企*业名*称")
        re_regAddr = re.compile(r"注册*地址|注册地*址")
        re_uscc = re.compile(r"社会*信用社*代*码|社*会信用*社*代码*")
        re_legalReps = re.compile(r"法定*代表*人|法*定代表人*")
        re_entPrincipal = re.compile(r"企.负责人|.业负*责人|企.负.人")
        re_qcPrincipal = re.compile(r"质*量负责*人|质*量负责人*|.量负.人*")
        re_vld = re.compile(r"有*效期*至|有效*期至")
        re_supervisionDEP = re.compile(r"日常*监管*机构*|日*常监*管机*构")
        re_supervisor = re.compile(r"日常*监管*人员*|日*常监*管人*员")
        re_supervisorCT = re.compile(r"监督*举报*电话*|监*督举*报电*话")
        re_licNO = re.compile(r"编号|編号|号：|号:|号")
        re_licNO2 = re.compile(r"号")
        re_cateCode = re.compile(r"分*类码")
        re_prodAddrScope = re.compile(r"生*产地*址和生产*范*围|生*产*地址和*生*产范*围|.产.址和.产.围|生产地址.生产范.")
        re_issueOrg = re.compile(r"发证机.|发证.关")
        re_issuer = re.compile(r"签发*人")
        re_issueDate = re.compile(r"发证*日*期")
        re_kindsOfEnterprise = re.compile(r"企业*类型*")
        re_useLimit = re.compile(r"此*复印件*仅*限用*于*")
        re_qcLegal = re.compile(r"质*量受*权人*")
        re_NO = re.compile(r"NO|N0")
        re_authorizedDEPT = re.compile(r"国*家*食品*药品*监督*管*理局制*|.家*食.药.监督*.理局.")
        re_country = re.compile(r"中华人民共和国")
        re_kindsOfDocument = re.compile(r"药品生产许可证")






        #这里将提取关键字段的长度延长到了12个,尽可能的将由于印章等造成的干扰降低
        if len(strword) >= 4:
            index = 6
        else:
            index = len(strword)

        if (re.match(r'.+?(?:\:)', strword[:index])):
            if re_entname.search(strword[:index]):
                return ['企业名称_许可证', strword[re_entname.search(strword).span()[1]+1:], re_entname.search(strword).group()]
            elif re_regAddr.search(strword[:index]):
                return ['注册地址', strword[re_regAddr.search(strword).span()[1] + 1:], re_regAddr.search(strword).group()]
            elif re_uscc.search(strword[:9]):
                return ['社会信用社代码', strword[re_uscc.search(strword).span()[1] + 1:], re_uscc.search(strword).group()]
            elif re_legalReps.search(strword[:7]):
                return ['法定代表人', strword[re_legalReps.search(strword).span()[1] + 1:], re_legalReps.search(strword).group()]
            elif re_entPrincipal.search(strword[:7]):
                return ['企业负责人', strword[re_entPrincipal.search(strword).span()[1] + 1:], re_entPrincipal.search(strword).group()]
            elif re_qcPrincipal.search(strword[:7]):
                return ['质量负责人', strword[re_qcPrincipal.search(strword).span()[1] + 1:], re_qcPrincipal.search(strword).group()]
            elif re_vld.search(strword[:index]):
                return ['有效期至', strword[re_vld.search(strword).span()[1] + 1:], re_vld.search(strword).group()]
            elif re_supervisionDEP.search(strword[:8]):
                return ['日常监管机构', strword[re_supervisionDEP.search(strword).span()[1] + 1:], re_supervisionDEP.search(strword).group()]
            elif re_supervisionDEP.search(strword[:8]):
                return ['日常监管机构', strword[re_supervisionDEP.search(strword).span()[1] + 1:], re_supervisionDEP.search(strword).group()]
            elif re_supervisor.search(strword[:8]):
                return ['日常监管人员', strword[re_supervisor.search(strword).span()[1] + 1:], re_supervisor.search(strword).group()]
            elif re_supervisorCT.search(strword[:8]):
                return ['监督举报电话', strword[re_supervisorCT.search(strword).span()[1] + 1:], re_supervisorCT.search(strword).group()]
            elif re_licNO.search(strword[:3]):
                return ['许可证编号', strword[re_licNO.search(strword).span()[1] + 1:], re_licNO.search(strword).group()]
            elif re_licNO2.search(strword[:1]):
                return ['许可证编号', strword[re_licNO2.search(strword).span()[1] + 1:], re_licNO2.search(strword).group()]
            elif re_cateCode.search(strword[:5]):
                return ['分类码', strword[re_cateCode.search(strword).span()[1] + 1:], re_cateCode.search(strword).group()]
            elif re_prodAddrScope.search(strword[:11]):
                return ['生产地址和生产范围', strword[re_prodAddrScope.search(strword).span()[1] + 1:], re_prodAddrScope.search(strword).group()]
            elif re_issueOrg.search(strword[:index]):
                return ['发证机关', strword[re_issueOrg.search(strword).span()[1] + 1:], re_issueOrg.search(strword).group()]
            elif re_issuer.search(strword[:5]):
                return ['签发人', strword[re_issuer.search(strword).span()[1] + 1:], re_issuer.search(strword).group()]
            elif re_issueDate.search(strword[:index]):
                return ['发证日期', strword[re_issueDate.search(strword).span()[1] + 1:],re_issueDate.search(strword).group()]
            elif re_kindsOfEnterprise.search(strword[:index]):
                return ['企业类型', strword[re_kindsOfEnterprise.search(strword).span()[1] + 1:],re_kindsOfEnterprise.search(strword).group()]
            elif re_useLimit.search(strword[:10]):
                return ['此复印件仅限用于', strword[re_useLimit.search(strword).span()[1] + 1:],re_useLimit.search(strword).group()]
            # elif re_qcLegal.search(strword[:index]):
            #     return ['质量受权人', strword[re_qcLegal.search(strword).span()[1] + 1:],re_qcLegal.search(strword).group()]
            elif re_NO.search(strword[:3]):
                return ['NO', strword[re_NO.search(strword).span()[1] + 1:],re_NO.search(strword).group()]
            elif re_authorizedDEPT.search(strword[:13]):
                return ['国家食品药品监督管理局制', strword[re_authorizedDEPT.search(strword).span()[1]:],re_authorizedDEPT.search(strword).group()]
            elif re_country.search(strword[:8]):
                return ['中华人民共和国', strword[re_country.search(strword).span()[1]:],re_country.search(strword).group()]
            elif re_kindsOfDocument.search(strword[:8]):
                return ['药品生产许可证', strword[re_kindsOfDocument.search(strword).span()[1]:],re_kindsOfDocument.search(strword).group()]
            else:
                return None
        else:
            if re_entname.search(strword[:index]):
                return ['企业名称_许可证', strword[re_entname.search(strword).span()[1]+1:], re_entname.search(strword).group()]
            elif re_regAddr.search(strword[:index]):
                return ['注册地址', strword[re_regAddr.search(strword).span()[1] + 1:], re_regAddr.search(strword).group()]
            elif re_uscc.search(strword[:9]):
                return ['社会信用社代码', strword[re_uscc.search(strword).span()[1] + 1:], re_uscc.search(strword).group()]
            elif re_legalReps.search(strword[:7]):
                return ['法定代表人', strword[re_legalReps.search(strword).span()[1] + 1:], re_legalReps.search(strword).group()]
            elif re_entPrincipal.search(strword[:7]):
                return ['企业负责人', strword[re_entPrincipal.search(strword).span()[1] + 1:], re_entPrincipal.search(strword).group()]
            elif re_qcPrincipal.search(strword[:7]):
                return ['质量负责人', strword[re_qcPrincipal.search(strword).span()[1] + 1:], re_qcPrincipal.search(strword).group()]
            elif re_vld.search(strword[:index]):
                return ['有效期至', strword[re_vld.search(strword).span()[1] + 1:], re_vld.search(strword).group()]
            elif re_supervisionDEP.search(strword[:8]):
                return ['日常监管机构', strword[re_supervisionDEP.search(strword).span()[1] + 1:], re_supervisionDEP.search(strword).group()]
            elif re_supervisionDEP.search(strword[:8]):
                return ['日常监管机构', strword[re_supervisionDEP.search(strword).span()[1] + 1:], re_supervisionDEP.search(strword).group()]
            elif re_supervisor.search(strword[:8]):
                return ['日常监管人员', strword[re_supervisor.search(strword).span()[1] + 1:], re_supervisor.search(strword).group()]
            elif re_supervisorCT.search(strword[:8]):
                return ['监督举报电话', strword[re_supervisorCT.search(strword).span()[1] + 1:], re_supervisorCT.search(strword).group()]
            elif re_licNO.search(strword[:3]):
                return ['许可证编号', strword[re_licNO.search(strword).span()[1] + 1:], re_licNO.search(strword).group()]
            elif re_cateCode.search(strword[:5]):
                return ['分类码', strword[re_cateCode.search(strword).span()[1] + 1:], re_cateCode.search(strword).group()]
            elif re_prodAddrScope.search(strword[:11]):
                return ['生产地址和生产范围', strword[re_prodAddrScope.search(strword).span()[1] + 1:], re_prodAddrScope.search(strword).group()]
            elif re_issueOrg.search(strword[:index]):
                return ['发证机关', strword[re_issueOrg.search(strword).span()[1] + 1:], re_issueOrg.search(strword).group()]
            elif re_issuer.search(strword[:5]):
                return ['签发人', strword[re_issuer.search(strword).span()[1] + 1:], re_issuer.search(strword).group()]
            elif re_issueDate.search(strword[:index]):
                return ['发证日期', strword[re_issueDate.search(strword).span()[1] + 1:],re_issueDate.search(strword).group()]
            elif re_kindsOfEnterprise.search(strword[:index]):
                return ['企业类型', strword[re_kindsOfEnterprise.search(strword).span()[1] + 1:],re_kindsOfEnterprise.search(strword).group()]
            elif re_useLimit.search(strword[:10]):
                return ['此复印件仅限用于', strword[re_useLimit.search(strword).span()[1] + 1:],re_useLimit.search(strword).group()]
            # elif re_qcLegal.search(strword[:index]):
            #     return ['质量受权人', strword[re_qcLegal.search(strword).span()[1] + 1:], re_qcLegal.search(strword).group()]
            elif re_NO.search(strword[:3]):
                return ['NO', strword[re_NO.search(strword).span()[1]+1:], re_NO.search(strword).group()]
            elif re_authorizedDEPT.search(strword[:13]):
                return ['国家食品药品监督管理局制', strword[re_authorizedDEPT.search(strword).span()[1]:],re_authorizedDEPT.search(strword).group()]
            elif re_country.search(strword[:8]):
                return ['中华人民共和国', strword[re_country.search(strword).span()[1]:], re_country.search(strword).group()]
            elif re_kindsOfDocument.search(strword[:8]):
                return ['药品生产许可证', strword[re_kindsOfDocument.search(strword).span()[1]:],re_kindsOfDocument.search(strword).group()]
            else:
                return None

    def recognize_deploy(self, imgs, id_code):
        nums = 0
        flag = 0
        temp = ''
        datas = []
        for file in imgs:
            #提取药品名称
            id = file['imgpath'].split('/')[-2]
            file_name = file['imgpath'].split('/')[-1]
            if re.search(r'[\u4e00-\u9fa5]+', id):
                dragname = re.search(r'[\u4e00-\u9fa5]+', id).group()
            else:
                dragname = re.search(r'[\u4e00-\u9fa5]+', file_name).group() 

            if 'error_code' in file['imgjson']:
                self.logmgr.error(file['imgpath'] + ' : ' + 'Size Error!')
            #判别是否是多栏
            try:
                kindict = hmc.kinds(file['imgpath'], file['imgjson'])
            except Exception as e:
                self.logmgr.error(file['imgpath'] + ' : ' + 'Size Error!')
                continue
            print('Current processing: {}'.format(file['imgpath']))
            #提取关键信息
            datatmp = file['imgjson']['words_result']
            nums += file['imgjson']['words_result_num']
            if kindict['kinds'] == 2:
                datas += subfiledata(kindict['direction'], kindict['parameter'], kindict['boundary'][0], datatmp)
            elif kindict['kinds'] == 1:
                datas += datatmp
        if len(datas) > 0 and nums > 0:
            datadict = self._productionCertificate(datas, nums)
            if '企业类型' in datadict:
                del datadict['企业类型']
            if '此复印件仅限于' in datadict:
                del datadict['次复印件仅限于']
            if 'NO' in datadict:
                del datadict['NO']
            if '国家食品药品监督管理局制' in datadict:
                del datadict['国家食品药品监督管理局制']
            if '中华人民共和国' in datadict:
                del datadict['中华人民共和国']
            if '药品许可证' in datadict:
                del datadict['药品许可证']

            ######################################增加部分###########################################
            datadict['ID_CODE'] = id_code
            datadict['REMARK'] = ''
            datadict['ADD_USER'] = 'shuai'
            datadict['JOB_ID'] = self._generatemd5(temp)
            ######################################增加部分###########################################
            if not datadict:
                nums = self._cleandata(datadict, datas, nums)
                return datadict
            return datadict
            #try:
            #    #self._data_to_db('DRUGMFRSCERT', datadict)
            #    nums = self._cleandata(datadict, datas, nums)
            #except Exception as e:
            #    #self.logmgr.error(file[0] + '\\' + file_name + "insert error!! : " + str(e))
            #    #self._update_item('OCRWORKFILE','JOB_ID', jobid,'IS_TO_DB','F')
            #    nums = self._cleandata(datadict, datas, nums)
            #    continue

    def recognize(self, path, id_code):
        flag = 0
        page = 0
        temp  =''
        jobdict = {}
        for file in os.walk(path):#这里将原来imgpath换成了 jsonpath
            for file_name in file[2]:
                if '生产许可证' in file_name:
                    jsonname = file_name.split('.')[0]
                    curpath = file[0].split('data')[1]
                    index = jsonname.rfind('_')
                    id = curpath[curpath.rfind('\\') + 1:]
                    if re.search(r'[\u4e00-\u9fa5]+', id):
                        dragname = re.search(r'[\u4e00-\u9fa5]+', id).group()
                    else:
                        dragname = re.search(r'[\u4e00-\u9fa5]+', file_name).group()
                    if dragname.find('(') > 0:
                        dragname = dragname[:dragname.find('(')]
                    jsonPath = file[0] + '\\' + file_name
                    datajson = self._load_json(file[0] + '\\' + file_name)
                    source_img_path = self.imgpath + curpath + '\\' + jsonname[:index] + '.' + jsonname[index:].split('_')[1]
                    original_path = self.imgpath + '\\' + curpath + '\\' + jsonname[:index - 2] + '.' + 'pdf'

                    #服务器
                    jobdict['SER_IP'] = '10.67.28.8'
                    #job id
                    jobdict['JOB_ID'] = self._generatemd5(file[0] + jsonname)
                    jobid = jobdict['JOB_ID']
                    jobdict['SRC_FILE_NAME'] = jsonname[:index - 2] + '.' + 'pdf'
                    jobdict['SRC_FILE_PATH'] = original_path
                    #原文件
                    jobdict['CUT_FILE_NAME'] = jsonname[:index] + '.' + jsonname[index:].split('_')[1]
                    #原路径
                    jobdict['CUT_FILE_PATH'] = 'G:\\IMG' + '\\' + curpath
                    #时间
                    jobdict['HANDLE_TIME'] = time.strftime("%Y-%m-%d %X", time.localtime())
                    #药品名
                    jobdict['DRUG_NAME'] = dragname
                    #影像件类型
                    jobdict['FILE_TYPE'] = '药品生产许可证'
                    #同一套影像件识别码
                    jobdict['ID_CODE'] = id_code
                    #分公司
                    jobdict['SRC_CO'] = curpath.split('\\')[1]
                    #源文件相对路径
                    jobdict['FILE_REL_PATH'] = '\\' + jsonname[:index] + '.' + jsonname[index:].split('_')[1]
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
                    # 图片过大或者一些原因，没有识别出来就会有error_code字段
                    if 'error_code' in datajson:
                        jobdict['IS_TO_DB'] = 'F'
                        self.job.job_add(jobdict)
                        self.job.job_todb()
                        self.job.job_del() 
                        self.logmgr.error(file[0] + '\\' + file_name + ": img size error!")
                        continue

                    #source_img_path = 'img\\'+jsonname+'.jpg' #由于需要增加分栏的程序所以，需要图片的路径，但是目前这里面的路径存在一定的问题
                    # source_img_path = file[0] + '\\' + file_name
                    # original_path = path_root + '\\' + curpath + '\\' + imgname[:index - 2] + '.' + 'pdf'
                    # FIXME:换工作环境这里也得改！
                    try:
                       kindict = hmc.kinds(source_img_path, jsonPath)
                    except Exception as e:
                        self.logmgr.error(file[0] + '\\' + file_name + ':' + str(e))
                        continue
                    #index = jsonname.rfind('.')
                    # print('Current processing: {}'.format(source_img_path + '\\' +
                    #                        '\\' + imgname[:index] +
                    #                        '.' + imgname[index:].split('.')[1],
                    #                        file[0] + '\\' + file_name))

                    datas = datajson['words_result']
                    nums = datajson['words_result_num']
                    if kindict['kinds'] == 2:
                        datas = self.subfiledata(kindict['direction'], kindict['parameter'], kindict['boundary'][0],datas)
                    elif kindict['kinds'] == 1 or kindict['kinds'] == 0:
                        datas = datas
                    flag = 1
                    page += 1
                    
                    #中间文件
                    jobdict['MID_FILE_NAME'] = file_name
                    #中间文件路径
                    jobdict['MID_FILE_PATH'] = file[0]
                    #评分
                    jobdict['OCR_SCORE'] = int(self._getscore(datas, nums))
                    
                    #影像件内容是否入库
                    if len(datas) > 0 and nums > 0:
                        jobdict['IS_TO_DB'] = 'T'
                    else:
                        jobdict['IS_TO_DB'] = 'F'
                    
                    #文件文本内容
                    jobdict['FILE_TEXT'] = self._middict(datas, self.codepath + '\\middata\\' + curpath, jsonname)
                    ###############
                    temp = jobdict['FILE_TEXT']
                    #jobdict['JOB_ID'] = self._generatemd5(jobdict['FILE_TEXT'])
                    ###############
                    
                    page += 1 
                    self.job.job_add(jobdict)
                    self.job.job_todb()
                    self.job.job_del() 
                if flag:
                    if len(datas) > 0 and nums > 0:
                        datadict = self._productionCertificate(datas, nums)
                        if '企业类型' in datadict:
                            del datadict['企业类型']
                        if '此复印件仅限于' in datadict:
                            del datadict['次复印件仅限于']
                        if 'NO' in datadict:
                            del datadict['NO']
                        if '国家食品药品监督管理局制' in datadict:
                            del datadict['国家食品药品监督管理局制']
                        if '中华人民共和国' in datadict:
                            del datadict['中华人民共和国']
                        if '药品许可证' in datadict:
                            del datadict['药品许可证']

                        print(source_img_path)
                        ######################################增加部分###########################################
                        datadict['ID_CODE'] = id_code
                        datadict['REMARK'] = ''
                        datadict['ADD_USER'] = 'shuai'
                        datadict['JOB_ID'] = self._generatemd5(temp)
                        ######################################增加部分###########################################
                        print(datadict)
                        if not datadict:
                            nums = self._cleandata(datadict, datas, nums)
                            continue
                        try:
                            self._data_to_db('DRUGMFRSCERT', datadict)
                            nums = self._cleandata(datadict, datas, nums)
                        except Exception as e:
                            print('Error: ', e)
                            self.logmgr.error(file[0] + '\\' + file_name + "insert error!! : " + str(e))
                            self._update_item('OCRWORKFILE','JOB_ID', jobid,'IS_TO_DB','F')
                            nums = self._cleandata(datadict, datas, nums)
                            continue





if __name__ == '__main__':
    codepath = os.path.dirname(__file__)
    gmptest = ProductionCertificate('F:\DevinChang\Code\Python\ocr\data\重庆泰民\银杏叶提取物注射液A000047545', r'D:\\IMG')

    gmptest.recognize('F:\DevinChang\Code\Python\ocr\data\重庆泰民\银杏叶提取物注射液A000047545','1111')