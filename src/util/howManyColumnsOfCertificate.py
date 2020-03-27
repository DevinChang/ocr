#encoding:utf-8
import json
import numpy as np
import cv2
import re
import os


def loadJson(file):
    with open(file,'r',encoding='utf-8') as f:
        return json.loads(f.read())

# 读取带中文路径的图像
def cv_imread(filePath):
    cv_img = cv2.imdecode(np.fromfile(filePath, dtype=np.uint8), -1)
    return cv_img

def _judge_keywordsOfCerficate( strword):
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
    re_licNO = re.compile(r"编号|编.|.号")
    re_cateCode = re.compile(r"分*类码")
    re_prodAddrScope = re.compile(r"生*产地*址和生产*范*围|生*产*地址和*生*产范*围|.产.址和.产.围")
    re_issueOrg = re.compile(r"发证*机*关")
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
    if len(strword) >= 12:
        index = 12
    else:
        index = len(strword)

    if (re.match(r'.+?(?:\:)', strword[:index])):
        if re_entname.search(strword[:index]):
            return ['企业名称', strword[re_entname.search(strword).span()[1]+1:], re_entname.search(strword).group()]
        elif re_regAddr.search(strword[:index]):
            return ['注册地址', strword[re_regAddr.search(strword).span()[1] + 1:], re_regAddr.search(strword).group()]
        elif re_uscc.search(strword[:index]):
            return ['社会信用社代码', strword[re_uscc.search(strword).span()[1] + 1:], re_uscc.search(strword).group()]
        elif re_legalReps.search(strword[:index]):
            return ['法定代表人', strword[re_legalReps.search(strword).span()[1] + 1:], re_legalReps.search(strword).group()]
        elif re_entPrincipal.search(strword[:index]):
            return ['企业负责人', strword[re_entPrincipal.search(strword).span()[1] + 1:], re_entPrincipal.search(strword).group()]
        elif re_qcPrincipal.search(strword[:index]):
            return ['质量负责人', strword[re_qcPrincipal.search(strword).span()[1] + 1:], re_qcPrincipal.search(strword).group()]
        elif re_vld.search(strword[:index]):
            return ['有效期至', strword[re_vld.search(strword).span()[1] + 1:], re_vld.search(strword).group()]
        elif re_supervisionDEP.search(strword[:index]):
            return ['日常监管机构', strword[re_supervisionDEP.search(strword).span()[1] + 1:], re_supervisionDEP.search(strword).group()]
        elif re_supervisionDEP.search(strword[:index]):
            return ['日常监管机构', strword[re_supervisionDEP.search(strword).span()[1] + 1:], re_supervisionDEP.search(strword).group()]
        elif re_supervisor.search(strword[:index]):
            return ['日常监管人员', strword[re_supervisor.search(strword).span()[1] + 1:], re_supervisor.search(strword).group()]
        elif re_supervisorCT.search(strword[:index]):
            return ['监督举报电话', strword[re_supervisorCT.search(strword).span()[1] + 1:], re_supervisorCT.search(strword).group()]
        # elif re_licNO.search(strword[:index]):
        #     return ['编号', strword[re_licNO.search(strword).span()[1] + 1:], re_licNO.search(strword).group()]
        elif re_cateCode.search(strword[:index]):
            return ['分类码', strword[re_cateCode.search(strword).span()[1] + 1:], re_cateCode.search(strword).group()]
        elif re_prodAddrScope.search(strword[:index]):
            return ['生产地址和生产范围', strword[re_prodAddrScope.search(strword).span()[1] + 1:], re_prodAddrScope.search(strword).group()]
        elif re_issueOrg.search(strword[:index]):
            return ['发证机关', strword[re_issueOrg.search(strword).span()[1] + 1:], re_issueOrg.search(strword).group()]
        elif re_issuer.search(strword[:index]):
            return ['签发人', strword[re_issuer.search(strword).span()[1] + 1:], re_issuer.search(strword).group()]
        elif re_issueDate.search(strword[:index]):
            return ['发证日期', strword[re_issueDate.search(strword).span()[1] + 1:],re_issueDate.search(strword).group()]
        elif re_kindsOfEnterprise.search(strword[:index]):
            return ['企业类型', strword[re_kindsOfEnterprise.search(strword).span()[1] + 1:],re_kindsOfEnterprise.search(strword).group()]
        # elif re_useLimit.search(strword[:index]):
        #     return ['此复印件仅限用于', strword[re_useLimit.search(strword).span()[1] + 1:],re_useLimit.search(strword).group()]
        # elif re_qcLegal.search(strword[:index]):
        #     return ['质量受权人', strword[re_qcLegal.search(strword).span()[1] + 1:],re_qcLegal.search(strword).group()]
        # elif re_NO.search(strword[:index]):
        #     return ['NO', strword[re_NO.search(strword).span()[1] + 1:],re_NO.search(strword).group()]
        # elif re_authorizedDEPT.search(strword[:index]):
        #     return ['国家食品药品监督管理局制', strword[re_authorizedDEPT.search(strword).span()[1]:],re_authorizedDEPT.search(strword).group()]
        # elif re_country.search(strword[:index]):
        #     return ['中华人民共和国', strword[re_country.search(strword).span()[1]:],re_country.search(strword).group()]
        # elif re_kindsOfDocument.search(strword[:index]):
        #     return ['药品生产许可证', strword[re_kindsOfDocument.search(strword).span()[1]:],re_kindsOfDocument.search(strword).group()]
        else:
            return None




    else:
        if re_entname.search(strword[:index]):
            return ['企业名称', strword[re_entname.search(strword).span()[1]+1:], re_entname.search(strword).group()]
        elif re_regAddr.search(strword[:index]):
            return ['注册地址', strword[re_regAddr.search(strword).span()[1] + 1:], re_regAddr.search(strword).group()]
        elif re_uscc.search(strword[:index]):
            return ['社会信用社代码', strword[re_uscc.search(strword).span()[1] + 1:], re_uscc.search(strword).group()]
        elif re_legalReps.search(strword[:index]):
            return ['法定代表人', strword[re_legalReps.search(strword).span()[1] + 1:], re_legalReps.search(strword).group()]
        elif re_entPrincipal.search(strword[:index]):
            return ['企业负责人', strword[re_entPrincipal.search(strword).span()[1] + 1:], re_entPrincipal.search(strword).group()]
        elif re_qcPrincipal.search(strword[:index]):
            return ['质量负责人', strword[re_qcPrincipal.search(strword).span()[1] + 1:], re_qcPrincipal.search(strword).group()]
        elif re_vld.search(strword[:index]):
            return ['有效期至', strword[re_vld.search(strword).span()[1] + 1:], re_vld.search(strword).group()]
        elif re_supervisionDEP.search(strword[:index]):
            return ['日常监管机构', strword[re_supervisionDEP.search(strword).span()[1] + 1:], re_supervisionDEP.search(strword).group()]
        elif re_supervisionDEP.search(strword[:index]):
            return ['日常监管机构', strword[re_supervisionDEP.search(strword).span()[1] + 1:], re_supervisionDEP.search(strword).group()]
        elif re_supervisor.search(strword[:index]):
            return ['日常监管人员', strword[re_supervisor.search(strword).span()[1] + 1:], re_supervisor.search(strword).group()]
        elif re_supervisorCT.search(strword[:index]):
            return ['监督举报电话', strword[re_supervisorCT.search(strword).span()[1] + 1:], re_supervisorCT.search(strword).group()]
        # elif re_licNO.search(strword[:index]):
        #     return ['编号', strword[re_licNO.search(strword).span()[1] + 1:], re_licNO.search(strword).group()]
        elif re_cateCode.search(strword[:index]):
            return ['分类码', strword[re_cateCode.search(strword).span()[1] + 1:], re_cateCode.search(strword).group()]
        elif re_prodAddrScope.search(strword[:index]):
            return ['生产地址和生产范围', strword[re_prodAddrScope.search(strword).span()[1] + 1:], re_prodAddrScope.search(strword).group()]
        elif re_issueOrg.search(strword[:index]):
            return ['发证机关', strword[re_issueOrg.search(strword).span()[1] + 1:], re_issueOrg.search(strword).group()]
        elif re_issuer.search(strword[:index]):
            return ['签发人', strword[re_issuer.search(strword).span()[1] + 1:], re_issuer.search(strword).group()]
        elif re_issueDate.search(strword[:index]):
            return ['发证日期', strword[re_issueDate.search(strword).span()[1] + 1:],re_issueDate.search(strword).group()]
        elif re_kindsOfEnterprise.search(strword[:index]):
            return ['企业类型', strword[re_kindsOfEnterprise.search(strword).span()[1] + 1:],re_kindsOfEnterprise.search(strword).group()]
        # elif re_useLimit.search(strword[:index]):
        #     return ['此复印件仅限用于', strword[re_useLimit.search(strword).span()[1] + 1:],re_useLimit.search(strword).group()]
        # # elif re_qcLegal.search(strword[:index]):
        # #     return ['质量受权人', strword[re_qcLegal.search(strword).span()[1] + 1:], re_qcLegal.search(strword).group()]
        # elif re_NO.search(strword[:index]):
        #     return ['NO', strword[re_NO.search(strword).span()[1]+1:], re_NO.search(strword).group()]
        # elif re_authorizedDEPT.search(strword[:index]):
        #     return ['国家食品药品监督管理局制', strword[re_authorizedDEPT.search(strword).span()[1]:],re_authorizedDEPT.search(strword).group()]
        # elif re_country.search(strword[:index]):
        #     return ['中华人民共和国', strword[re_country.search(strword).span()[1]:], re_country.search(strword).group()]
        # elif re_kindsOfDocument.search(strword[:index]):
        #     return ['药品生产许可证', strword[re_kindsOfDocument.search(strword).span()[1]:],re_kindsOfDocument.search(strword).group()]
        else:
            return None
#输入为图片的路径，以及json文件的路径
#此程序设计的还是不够完美可能会出现判断出错的情况，以后会慢慢改进
def kinds(imgPath,jsonPath):
    print('进入函数')
    #json文件的读取
    word = loadJson(jsonPath)
    # word = jsonPath

    # 图片文件的读取
    img = cv_imread(imgPath)

    numberOfAimWords = word['words_result_num']#json中句子的数量
    numberOfWords = 0

    # - 0: 正向，
    # - 1: 逆时针90度，
    # - 2: 逆时针180度，
    # - 3: 逆时针270度
    direction = word['direction']#方向信息的提取

    left = []#此列表为左边距的集合
    # regex = r".+】"
    # regex = r".+]"
    # regex = r".*]| .*】"
    regex = r".+?(?=】)|【.+|.+?(?=])|\[.+|.+:|.+："
    if direction == 0:#此时图片为摆正的状态
        width = img.shape[1]
        for d in word['words_result']:
            str = d["words"][0:12]
            if _judge_keywordsOfCerficate(str) or re.match(regex,str):
                numberOfWords = numberOfWords + 1
                left.append(d["location"]["left"])



    if direction == 1:#此时图片为逆时针90度
        width = img.shape[0]

        for d in word['words_result']:
            str = d["words"][0:12]
            if _judge_keywordsOfCerficate(str) or re.match(regex,str):
            # if re.match(regex,str):
                numberOfWords += 1
                left.append(d["location"]["top"])
        for x in range(numberOfWords):
            left[x] = width - left[x]


    if direction == 2:#此时图片为逆时针180度
        width = img.shape[1]
        for d in word['words_result']:
            str = d["words"][0:12]
            # if re.match(regex, str):
            if _judge_keywordsOfCerficate(str) or re.match(regex,str):
                numberOfWords += 1
                left.append(d["location"]["left"])
        for x in range(numberOfWords):
            left[x] = width - left[x]

    if direction == 3:#此时图片为逆时针270度
        width = img.shape[0]
        for d in word['words_result']:
            str = d["words"][0:12]
            # if re.match(regex, str):
            if _judge_keywordsOfCerficate(str) or re.match(regex,str):
                numberOfWords += 1
                left.append(d["location"]["top"])

    tempList = []
    for n in range(numberOfWords):
        tempList.append(left[n])

    countOfKinds = 0
    dict = {}

    for i in range(numberOfWords):
        count = 0
        # tempFlag = []
        for j in range(i+1 , numberOfWords):
            fenmu = 4

            if (tempList[i] != 0 and tempList[j] != 0 and tempList[j] >= (left[i] - width/fenmu)) \
                    and (tempList[j] <= (left[i] + width/fenmu) ):
                count += 1
                tempList[j] = 0
            if count != 0:
                count += 1
        tempList[i] = 0

        if count >= 1*numberOfWords/5:
            countOfKinds += 1
            # tempList[i] = 0
            if direction == 0 or direction == 3:
                dict.update({countOfKinds: [left[i] - (width/(fenmu)), left[i] + (width/(fenmu))]})
            else:
                dict.update({countOfKinds: [width-left[i] - (width/(fenmu)), width-left[i] + (width/(fenmu))]})


    dict.update({'kinds': countOfKinds})
    if direction == 0 or direction == 2:
        dict.update({'parameter': 'left'})
    else:
        dict.update({'parameter': 'top'})

    boundary = None
    if countOfKinds == 1:
        boundary = None
    elif countOfKinds == 2:
        # boundary = [width/2]
        boundary = [1]
        a1 = dict[1][0]
        a2 = dict[1][1]
        b1 = dict[2][0]
        b2 = dict[2][1]
        if a1 <= b1:
            if a2<b1:
                boundary[0] = a2
            else:
                boundary[0] = b1
            # boundary[0] = b1
        else:
            if b2<a1:
                boundary[0] = b2
            else:
                boundary[0] = a1
            # boundary[0] = b1
            # boundary[0] = a1
    elif  countOfKinds == 3:
        boundary = [-1,-1]
        a1 = dict[1][0]
        a2 = dict[1][1]
        b1 = dict[2][0]
        b2 = dict[2][1]
        c1 = dict[3][0]
        c2 = dict[3][1]
        #将三种情况排好序
        if a1<b1 and a1<c1:
            boundary[0] = a2
            if b1<c1:
                # boundary[1] = c1
                boundary[2] = c2
            else:
                # boundary[1] = b1
                boundary[2] = b2
        elif b1<a1 and b1<c1:
            boundary[0] = b2
            if a1<c1:
                boundary[1] = c1
                # boundary[2] = c2
            else:
                # boundary[1] = a1
                boundary[2] = a2
        elif c1<a1 and c1<b1:
            boundary[0] = c1
            if a1<b1:
                boundary[1] = b1
                # boundary[2] = b1
            else:
                # boundary[1] = a1
                boundary[2] = a1
    elif countOfKinds >= 4:
        print(imgPath + '情况特殊，请人工处理')

    dict.update({'boundary': boundary})
    dict.update({'direction':direction})
    #输出为字典
    #例子： {1: [1735.0, 2549.0], 2: [1167.0, 1981.0], 'kinds': 2, 'parameter': 'top', 'boundary': [1981.0]}
    #kinds是指 栏数，parameter是指应该根据该位置信息对内容 进行分栏 boundary是指内容的划分界限
    print(dict)
    return dict

# codepath = os.path.dirname(__file__)
# jsonpath = codepath+'/data/'
# for file in os.walk(jsonpath):  # 这里将原来imgpath换成了 jsonpath
#     for file_name in file[2]:
#         if '药品生产许可证' in file_name:
#             jsonname = file_name.split('.')[0]
#             tempPathOfJson = file[0] + '\\' + file_name
#             datajson = loadJson(file[0] + '\\' + file_name)
#             if 'error_code' in datajson:
#                 print(file[0] + '\\' + file_name + ": img size error!")
#                 continue
#             source_img_path = 'img\\' + jsonname + '.jpg'
#             print(jsonname)
#             n = kinds(source_img_path, tempPathOfJson)

            # print(n)


# jsonPath = "data/39207_122055-药品生产许可证0.json"
# imgPath = "img/39207_122055-药品生产许可证0.jpg"
# n = kinds(imgPath, jsonPath)
# print(n)
# print(n)






