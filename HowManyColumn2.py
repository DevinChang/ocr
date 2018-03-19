import json
import numpy as np
import cv2
import re


def loadJson(file):
    with open(file,'r',encoding='utf-8') as f:
        return json.loads(f.read())

# 读取带中文路径的图像
def cv_imread(filePath):
    cv_img = cv2.imdecode(np.fromfile(filePath, dtype=np.uint8), -1)
    return cv_img



#输入为图片的路径，以及json文件的路径
#此程序设计的还是不够完美可能会出现判断出错的情况，以后会慢慢改进
def kinds(imgPath,jsonPath):
    print('进入函数')
    #json文件的读取
    word = loadJson(jsonPath)
    #word = jsonPath

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
    regex = r".+?(?=】)|【.+|.+?(?=])|.+?(?=：)|.+?(?=:)|\[.+"
    if direction == 0:#此时图片为摆正的状态
        width = img.shape[1]
        for d in word['words_result']:
            str = d["words"][0:10]
            if re.match(regex,str):
                numberOfWords = numberOfWords+1
                left.append(d["location"]["left"])

    if direction == 1:#此时图片为逆时针90度
        width = img.shape[0]

        for d in word['words_result']:
            str = d["words"][0:10]
            if re.match(regex,str):
                numberOfWords += 1
                left.append(d["location"]["top"])
        for x in range(numberOfWords):
            left[x] = width - left[x]


    if direction == 2:#此时图片为逆时针180度
        width = img.shape[1]
        for d in word['words_result']:
            str = d["words"][0:10]
            if re.match(regex, str):
                numberOfWords += 1
                left.append(d["location"]["left"])
        for x in range(numberOfWords):
            left[x] = width - left[x]

    if direction == 3:#此时图片为逆时针270度
        width = img.shape[0]
        for d in word['words_result']:
            str = d["words"][0:10]
            if re.match(regex, str):
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
        for j in range(i + 1, numberOfWords):

            if (tempList[i] != 0 and tempList[j] >= (left[i] - 4*width/24)) and (
                    tempList[j] <= (left[i] + 4*width/24) and tempList[j] != 0):
                count += 1
                tempList[j] = 0

        if count >= 1*numberOfWords/4:
            countOfKinds += 1
            if direction == 0 or direction == 3:
                dict.update({countOfKinds: [left[i] - (width/6), left[i] + (width/6)]})
            else:
                dict.update({countOfKinds: [width-left[i] - (width/6), width-left[i] + (width/6)]})


    dict.update({'kinds': countOfKinds})
    if direction == 0 or direction == 2:
        dict.update({'parameter': 'left'})
    else:
        dict.update({'parameter': 'top'})

    boundary = None
    if countOfKinds == 1:
        boundary = None
    elif countOfKinds == 2:
        boundary = [1]
        a1 = dict[1][0]
        a2 = dict[1][1]
        b1 = dict[2][0]
        b2 = dict[2][1]
        if a1 <= b1:
            boundary[0] = a2
        else:
            boundary[0] = b2
    elif  countOfKinds == 3:
        boundary = [-1,-1,-1]
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
                boundary[1] = b2
                # boundary[2] = c2
            else:
                boundary[1] = c2
                # boundary[2] = b2
        elif b1<a1 and b1<c1:
            boundary[0] = b2
            if a1<c1:
                boundary[1] = a2
                # boundary[2] = c2
            else:
                boundary[1] = c2
                # boundary[2] = a2
        elif c1<a1 and c1<b1:
            boundary[0] = c1
            if a1<b1:
                boundary[1] = a1
                # boundary[2] = b1
            else:
                boundary[1] = b1
                # boundary[2] = a1
    elif countOfKinds >= 4:
        print(imgPath + '情况特殊，请人工处理')

    dict.update({'boundary': boundary})
    #输出为字典
    #例子： {1: [1735.0, 2549.0], 2: [1167.0, 1981.0], 'kinds': 2, 'parameter': 'top', 'boundary': [1981.0]}
    #kinds是指 栏数，parameter是指应该根据该位置信息对内容 进行分栏 boundary是指内容的划分界限
    return dict



#jsonPath = "data/说明书1_jpg.json"
#imgPath = "IMG/图片/test2.jpg"
#
#n = kinds(imgPath,jsonPath)
#print(n)

if __name__ == '__main__':
    jsonPath = "F:\\DevinChang\\Code\\Python\\ocr\\data\\国药海南去重\\11A0019\\说明书_jpg.json"
    imgPath = "C:\\Users\\dongd\\Desktop\\11A0019\\说明书.jpg"
    n = kinds(imgPath,jsonPath)
    print(n)







