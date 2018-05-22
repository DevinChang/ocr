# -*- coding: utf-8 -*-


import os
import re
import time
from tool import Tools
from log import LogMgr




class Regisration(Tools):
    """
    识别药品再注册批件
    """
    def __init__(self, imgpath):
        Tools.__init__(self)
        self.imgpath = imgpath
        self.logmgr = LogMgr()

    def _recognize(self,datas, nums):
        """
        程序的主逻辑
        """
        keylist = []
        datadict = dict()
      
        for (word, i) in zip(datas, range(0, nums)):
            '''
            循环读识别出的数据，然后根据judge_keywords函数是否提取到了关键信息；
            若提取到了，则保存到datadict中。
            若未提取到，list_result为空。有两种情况，
                1.这段信息不是我们所需要的。
                2.这段信息是上个关键字的值。
                然后执行else，进行更精确的判别。若是需归到上个字段，则循环递减，根据
                keylist[1],也就是list_reault[2]是否出现再上面的某个字段。若有则追加。
            '''
            list_result = self._judge_keywords(word['words'])
            if list_result != None:
                if list_result[0] in datadict and keylist[-1][0] != list_result[0]:
                    datadict[list_result[0]] += list_result[1]
                    flag = 1
                else:
                    datadict[list_result[0]] = list_result[1]
                    flag = 1
                #保存关键字段的信息，以及这段信息原本关键字段的信息
                keylist.append([list_result[0],list_result[2]])
            else:
                j = i
                while j > 0:
                    if not keylist:
                        break
                    if keylist[-1][0] == '批准文号':
                        if re.search(r'.?[a-zA-z][0-9]+', word['words']):
                            break
                    if keylist[-1][0] == '规格':
                        if not re.search(r'.*m*g|.*m*l', word['words']):
                            break
                    if flag:
                        if keylist[-1][1] in datas[j]['words']:
                            datadict[keylist[-1][0]] += word['words']
                            break
                    j -= 1  
        return datadict
    
    def _judge_keywords(self, strword):
        '''
        判断关键字,若识别到关键字，返回一个包含关键字的list。
        $resultlist[0] -----要入库的关键字
        $resultlist[1] -----提取到内容
        $resultlist[2] -----需判断的信息中本来的关键字
        如:'证书编号:H12345',resultlist = ['证书编号', 'H12345', '证书编号']
           '证书号:H123', resultlist = ['证书编号', 'H123', '证书号']
        '''
        re_coname = re.compile(r"名称")
        re_num_orig = re.compile(r"原始*编号*|原*始编*号")
        re_drug_standord = re.compile(r"药品*标准*|药*品标*准")
        re_drug_valid = re.compile(r"药品*有效期*|药*品有*效期")
        re_drug_class = re.compile(r"药品*分类*|药*品分*类")
        re_common_name = re.compile(r'药品*通?用名称?|药*品通?用名?称')
        re_product_name = re.compile(r'商?品名称?|商?品名?称')
        re_english = re.compile(r'英文?名称?|英文名?称')
        re_pinyin = re.compile(r'汉语?拼音?|汉?语拼?音')    
        re_coaddr = re.compile(r"生产*地址*|生*产地*址")
        re_conclution = re.compile(r"审批*结论*|审*批结*论")
        re_drug_approval = re.compile(r"药品*批准文*号|药*品批*准文号")
        re_drug_approval_valid = re.compile(r"药*品批准文号有*效期|药品*批准文号*有效*期")
        #TODO:有些注册批件的生产厂家
        re_annex = re.compile(r"附件")
        re_zhusong = re.compile(r"主送")
        re_chaobao = re.compile(r"抄报")
        re_regisnum = re.compile(r"注册*证号*|注*册证*号")
        re_regisnum_valid = re.compile(r"注册*证号有效期*|注*册证号有效*期")
        re_specification = re.compile(r'规格')
        re_jixing = re.compile(r'剂型')
        

        if len(strword) >= 8: 
            index = 6
        else:
            index = len(strword)

        if(re.match(r'.+?(?:\:)', strword[:index])):
            if re_common_name.search(strword[:8]):
                return ['药品名称', strword[re_common_name.search(strword).span()[1]:], re_common_name.search(strword).group()]
            elif re_pinyin.search(strword[:index]):
                return ['汉语拼音' , strword[re_pinyin.search(strword).span()[1] + 1:], re_pinyin.search(strword).group()]
            elif re_coname.search(strword[:4]):
                return ['名称', strword[re_coname.search(strword).span()[1] + 1:], re_coname.search(strword).group()]
            elif re_coaddr.search(strword[:index]):
                return ['生产地址', strword[re_coaddr.search(strword).span()[1] + 1:], re_coaddr.search(strword).group()]
            else:
                return None
        else: 
            if re_common_name.search(strword[:8]):
                return ['药品名称', strword[re_common_name.search(strword).span()[1]:], re_common_name.search(strword).group()]
            elif re_pinyin.search(strword[:index]):
                return ['汉语拼音', strword[re_pinyin.search(strword).span()[1]:], re_pinyin.search(strword).group()]
            elif re_coname.search(strword[:4]):
                return ['名称', strword[re_coname.search(strword).span()[1]:], re_coname.search(strword).group()]
            elif re_coaddr.search(strword[:index]):
                return ['生产地址', strword[re_coaddr.search(strword).span()[1]:], re_coaddr.search(strword).group()]
            elif re_conclution.search(strword[:index]):
                return ['审批结论', strword[re_conclution.search(strword).span()[1]:], re_conclution.search(strword).group()]
            elif re_drug_approval.search(strword[:index]):
                return ['再注册证批准文号', strword[re_drug_approval.search(strword).span()[1]:], re_drug_approval.search(strword).group()]
            elif re_drug_approval_valid.search(strword[:index]):
                return ['药品批准文号有效期', strword[re_drug_approval_valid.search(strword).span()[1]:], re_drug_approval_valid.search(strword).group()]
            elif re_regisnum.search(strword[:index]):
                return ['注册证号', strword[re_regisnum.search(strword).span()[1]:], re_regisnum.search(strword).group()]
            elif re_regisnum_valid.search(strword[:8]):
                return ['批准文号有效期', strword[re_regisnum_valid.search(strword).span()[1]:], re_regisnum_valid.search(strword).group()]
            elif re_zhusong.search(strword[:index]):
                return ['主送', strword[re_zhusong.search(strword).span()[1]:], re_zhusong.search(strword).group()]
            elif re_specification.search(strword[:self._short_index(strword)]):
                return ['规格', strword[re_specification.search(strword).span()[1]:], re_specification.search(strword).group()]
            elif re_jixing.search(strword[:self._short_index(strword):]):
                return ['剂型', strword[re_jixing.search(strword).span()[1]:], re_jixing.search(strword).group()]
            elif re_drug_class.search(strword[:index]):
                return ['药品分类', strword[re_drug_class.search(strword).span()[1]:], re_drug_class.search(strword).group()]
            else:
                return None


    def regisration(self, path, id_code):
        flag = 0
        temp = ''
        for file in os.walk(path):
            page = 1
            jobdict = {}
            for file_name in file[2]:
                if '药品再注册批件' in file_name:
                    imgname = file_name.split('.')[0]
                    curpath = file[0].split('data')[1]
                    index = imgname.rfind('_')
                    id = curpath[curpath.rfind('\\') + 1:]
                    if re.search(r'[\u4e00-\u9fa5]+', id):
                        dragname = re.search(r'[\u4e00-\u9fa5]+', id).group()
                    else:
                        dragname = re.search(r'[\u4e00-\u9fa5]+', file_name).group()
                    if dragname.find('(') > 0:
                        dragname = dragname[:dragname.find('(')]
                    datajson = self._load_json(file[0] + '\\' + file_name)
                    original_path = self.imgpath + '\\' + curpath + '\\' + imgname[:index - 2] + '.' + 'pdf'
                    #服务器
                    jobdict['SER_IP'] = '10.67.28.8'
                    #job id
                    jobdict['JOB_ID'] = self._generatemd5(file[0] + imgname)
                    jobid = jobdict['JOB_ID']
                    jobdict['SRC_FILE_NAME'] = imgname[:index - 2] + '.' + 'pdf'
                    jobdict['SRC_FILE_PATH'] = original_path
                    #原文件
                    jobdict['CUT_FILE_NAME'] = imgname[:index] + '.' + imgname[index:].split('_')[1]
                    #原路径
                    jobdict['CUT_FILE_PATH'] = 'G:\\IMG' + '\\' + curpath
                    #时间
                    jobdict['HANDLE_TIME'] = time.strftime("%Y-%m-%d %X", time.localtime())
                    #药品名
                    jobdict['DRUG_NAME'] = dragname
                    #影像件类型
                    jobdict['FILE_TYPE'] = '药品再注册批件'
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
                        self.job.job_add(jobdict)
                        self.job.job_todb()
                        self.job.job_del()
                        self.logmgr.error(file[0] + '\\' + file_name + ": img size error!")
                        continue
                    datas = datajson['words_result']
                    nums = datajson['words_result_num']
                    flag = 1

                    
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
                    jobdict['FILE_TEXT'] = self._middict(datas, self.codepath + '\\middata\\' + curpath, imgname)
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
                    datadicttmp = self._recognize(datas, nums)
                    datadict = dict()
                    if '药品名称' in datadicttmp:
                        if re.match('[:：]',datadicttmp['药品名称']):
                            datadict['药品名称'] = datadicttmp['药品名称'][1:]
                        else:
                            datadict['药品名称'] = datadicttmp['药品名称']

                    if '剂型' in datadicttmp:
                        if re.match('[:：]',datadicttmp['剂型']):
                            datadict['剂型'] = datadicttmp['剂型'][1:]
                        else:
                            datadict['剂型'] = datadicttmp['剂型']

                    if '规格' in datadicttmp:
                        if re.match('[:：]',datadicttmp['规格']):
                            datadict['规格'] = datadicttmp['规格'][1:]
                        else:
                            datadict['规格'] = datadicttmp['规格']

                    if '生产厂家' in datadicttmp:
                        if re.match('[:：]',datadicttmp['生产厂家']):
                            datadict['生产厂家'] = datadicttmp['生产厂家'][1:]
                        else:
                            datadict['生产厂家'] = datadicttmp['生产厂家']

                    if '日期' in datadicttmp:
                        if re.match('[:：]',datadicttmp['日期']):
                            datadict['日期'] = datadicttmp['日期'][1:]
                        else:
                            datadict['日期'] = datadicttmp['日期']


                    ######################################增加部分###########################################
                    datadict['ID_CODE']=id_code
                    datadict['REMARK']=''
                    datadict['ADD_USER']='shuai'
                    datadict['JOB_ID'] = self._generatemd5(temp)
                    ######################################增加部分###########################################
                    print(datadict)
                    ###########################

                    ###########################
                    if not datadict:
                        nums = self._cleandata(datadict, datas, nums)
                        continue
                    try:
                        self._data_to_db('DRUGREGAPPROVAL', datadict)
                        nums = self._cleandata(datadict, datas, nums)
                    except Exception as e:
                        print('Error: ', e)
                        self.logmgr.error(file[0] + '\\' + file_name + "insert error!! : " + str(e))
                        self._update_item('OCRWORKFILE','JOB_ID', jobid,'IS_TO_DB','F')
                        nums = self._cleandata(datadict, datas, nums)
                        continue  




if __name__ == '__main__':
    codepath = os.path.dirname(__file__)
    regisration = Regisration('F:\DevinChang\Code\Python\ocr\data\重庆泰民\银杏叶提取物注射液A000047545')
    regisration.regisration('F:\DevinChang\Code\Python\ocr\data\重庆泰民\银杏叶提取物注射液A000047545','1111')