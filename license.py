import os
import re
import time
from tool import Tools
from log import LogMgr




class License(Tools):
    """
    识别营业执照
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
            if '名' == word['words'] and datas[i + 1]['words'][0] == '称':
                datadict['ENT_NAME'] = datas[i + 1]['words'][1:]
                continue
            elif '类' == word['words'] and '型' == datas[i + 1]['words'][0]:
                datadict['ENT_TYPE'] = datas[i + 1]['words'][1:]
                continue
            elif '住' == word['words'] and '所' == datas[i + 1]['words'][0]:
                datadict['住所'] = datas[i + 1]['words'][1:]
                continue
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
                    if keylist[-1][0] == '统一社会信用代码':
                        if re.search(r'[\u4e00-\u9fa5]+', word['words']):
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
        re_name = re.compile(r"名称")
        re_social_code = re.compile(r"统*一社*会信用代码|统一*社会*信用*代码")
        re_type = re.compile(r"类型")
        re_residence = re.compile(r"住所")
        re_legal_representative = re.compile(r"法定*代表*人|法*定代表人*")
        re_capital = re.compile(r'注册*资本*|注*册资*本')
        re_establish = re.compile(r'成立*日期*|成*立日*期')
        re_period = re.compile(r'营业*期限*|营*业期*限')    
        re_scope = re.compile(r"经营*范围*|经*营范*围")
        re_authority = re.compile(r"登记*机关*|登*记机*关")

        if len(strword) >= 10: 
            index = 8
        elif len(strword) >=8:
            index = 6
        else:
            index = len(strword)

        if re_social_code.search(strword[:index]):
            return ['统一社会信用代码', strword[re_social_code.search(strword).span()[1]:], re_social_code.search(strword).group()]
        elif re_legal_representative.search(strword[:index]):
            return ['法定代表人', strword[re_legal_representative.search(strword).span()[1]:], re_legal_representative.search(strword).group()]
        elif re_capital.search(strword[:index]):
            return ['注册资本', strword[re_capital.search(strword).span()[1]:], re_capital.search(strword).group()]
        elif re_establish.search(strword[:index]):
            return ['成立日期', strword[re_establish.search(strword).span()[1]:], re_establish.search(strword).group()]
        elif re_period.search(strword[:index]):
            return ['营业期限', strword[re_period.search(strword).span()[1]:], re_period.search(strword).group()]
        elif re_scope.search(strword[:index]):
            return ['经营范围', strword[re_scope.search(strword).span()[1]:], re_scope.search(strword).group()]
        elif re_authority.search(strword[:index]):
            return ['登记机关', strword[re_authority.search(strword).span()[1]:], re_authority.search(strword).group()]
        else:
            return None


    def license(self, path, id_code):
        flag = 0
        temp = ''
        jobdict = {}
        for file in os.walk(path):
            page = 1
            for file_name in file[2]:
                if '营业执照' in file_name:
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
                    jobdict['FILE_TYPE'] = '营业执照'
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
                    ###########################
                    temp = jobdict['FILE_TEXT']
                    ###########################
                    #jobdict['JOB_ID'] = self._generatemd5(jobdict['FILE_TEXT'])
                    ###############
                    
                    page += 1
                    self.job.job_add(jobdict)
                    self.job.job_todb()
                    self.job.job_del()
            if flag:
                if len(datas) > 0 and nums > 0:
                    datadict = self._recognize(datas, nums)
                    ######################################增加部分###########################################
                    datadict['ID_CODE']=id_code
                    datadict['REMARK']=''
                    datadict['ADD_USER']='shuai'
                    datadict['JOB_ID'] = self._generatemd5(temp)
                    ######################################增加部分###########################################
                    print(datadict)
                    if not datadict:
                        nums = self._cleandata(datadict, datas, nums)
                        continue
                    if '登记机关' in datadict:
                        del datadict['登记机关']
                    try:
                        self._data_to_db('BUSINESSLICENCE', datadict)
                        nums = self._cleandata(datadict, datas, nums)
                    except Exception as e:
                        print('Error: ', e)
                        self.logmgr.error(file[0] + '\\' + file_name + "insert error!! : " + str(e))
                        self._update_item('OCRWORKFILE','JOB_ID', jobid,'IS_TO_DB','F')
                        nums = self._cleandata(datadict, datas, nums)
                        continue 

if __name__ == '__main__':
    datapath = os.path.dirname(__file__) + '\data'
    testpath = 'f:\DevinChang\Code\Python\ocr\data\国控盐城\西药\酮康唑乳膏A000060628'
    license = License(datapath)
    license.license(testpath, '12345')