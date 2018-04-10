# -*- coding: utf-8 -*-
import os
import re
import json
from log import LogMgr
import howManyColumnsOfCertificate as hmc
import hashlib


class ProductionCertificate(object):
    def __init__(self, jsonpath):
        self.jsonpath = jsonpath
        # self.imgpath = imgpath
        self.log = LogMgr()

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
                    # if ("分类码" in keylist[-1][0]):
                    #     if re.match(r'[a-zA-z]+', word['words']):
                    #         flag = 1
                    #     else:
                    #         break
                    # elif "有效期至" in keylist[-1][0]:
                    #     if re.match(r'[0-9]{4}年?[0-9]{2}月?[0-9]{2}日?', word['words']):
                    #         flag = 1
                    #     else:
                    #         break

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
        re_prodAddrScope = re.compile(r"生*产地*址和生产*范*围|生*产*地址和*生*产范*围|.产.址和.产.围")
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
                return ['企业名称', strword[re_entname.search(strword).span()[1]+1:], re_entname.search(strword).group()]
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
                return ['编号', strword[re_licNO.search(strword).span()[1] + 1:], re_licNO.search(strword).group()]
            elif re_licNO2.search(strword[:1]):
                return ['编号', strword[re_licNO2.search(strword).span()[1] + 1:], re_licNO2.search(strword).group()]
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
                return ['企业名称', strword[re_entname.search(strword).span()[1]+1:], re_entname.search(strword).group()]
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
                return ['编号', strword[re_licNO.search(strword).span()[1] + 1:], re_licNO.search(strword).group()]
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
        page = 0
        for file in os.walk(self.jsonpath):#这里将原来imgpath换成了 jsonpath
            for file_name in file[2]:
                if '药品生产许可证' in file_name:
                    jsonname = file_name.split('.')[0]
                    # curpath = file[0].split('data')[1]
                    # index = imgname.rfind('_')
                    # id = curpath[curpath.rfind('\\') + 1:]
                    # name_index_e = re.match(r'.*[A-Z]', id).span()[1]
                    # dragname = id[:name_index_e - 1]
                    # if dragname.find('(') > 0:
                    #    dragname = dragname[:dragname.find('(')]
                    # id_code = id[name_index_e - 1:]
                    jsonPath = file[0] + '\\' + file_name
                    datajson = self._load_json(file[0] + '\\' + file_name)
                    # 图片过大或者一些原因，没有识别出来就会有error_code字段
                    if 'error_code' in datajson:
                        self.log.error(file[0] + '\\' + file_name + ": img size error!")
                        continue

                    # source_img_path = imgpaht_root_desktop + '\\' + curpath + '\\' + imgname[:index] + '.' + imgname[index:].split('_')[1]
                    source_img_path = 'img\\'+jsonname+'.jpg' #由于需要增加分栏的程序所以，需要图片的路径，但是目前这里面的路径存在一定的问题
                    # source_img_path = file[0] + '\\' + file_name
                    # original_path = path_root + '\\' + curpath + '\\' + imgname[:index - 2] + '.' + 'pdf'
                    # FIXME:换工作环境这里也得改！
                    try:
                       kindict = hmc.kinds(source_img_path, jsonPath)
                    except Exception as e:
                        LogMgr.error(file[0] + '\\' + file_name + ':' + str(e))
                        continue
                    index = jsonname.rfind('.')
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
                if flag:
                    if len(datas) > 0 and nums > 0:
                        datadict = self._productionCertificate(datas, nums)
                        print(source_img_path)
                        print(datadict)
                        if not datadict:
                            nums = self._cleandata(datadict, datas, nums)
                            continue





if __name__ == '__main__':
    codepath = os.path.dirname(__file__)
    gmptest = ProductionCertificate(codepath + '/data/')

    gmptest.recognize()