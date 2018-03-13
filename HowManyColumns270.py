import json
import numpy as np
import cv2

a = {"name":"lenna","sex":"woman","age":"22"}
#print(a)

def loadJson(file):
    with open(file,'r',encoding='utf-8') as f:
        return json.loads(f.read())



    #寻找类别：
    #判别准则
    #1.范式+- width/8（或者其他的数值）之间的都属于同一类
    #2. 如果一类的数目大于总行数的1/5(或者其他的一个数值)
def kinds270(listOfLeft,numberOfWords,width):
    tempList = []
    for n in range(numberOfWords):
        tempList.insert(n, listOfLeft[n])
    countOfKinds = 0
    dict={}
    for i in range(numberOfWords):
        count = 0
        for j in range(i+1,numberOfWords):
           if (tempList[i]!=0 and tempList[j]>=(listOfLeft[i] - 4*width/24)) and (tempList[j]<=(listOfLeft[i] + 4*width/24) and tempList[j]!=0):
               count+=1
               tempList[j] = 0
        if count >= 6*numberOfWords/24:
            countOfKinds += 1
            dict.update({countOfKinds:[listOfLeft[i]-width/6,listOfLeft[i]+width/6]})
    dict.update({'kinds':countOfKinds})
    dict.update({'parameter': 'top'})
    return dict

#读取带中文路径的图像
def cv_imread(filePath):
    cv_img=cv2.imdecode(np.fromfile(filePath,dtype=np.uint8),-1)
    ## imdecode读取的是rgb，如果后续需要opencv处理的话，需要转换成bgr，转换后图片颜色会变化
    ##cv_img=cv2.cvtColor(cv_img,cv2.COLOR_RGB2BGR)
    return cv_img

left=[]
jsonPath = "data/270双栏说明书10.json"
word = loadJson(jsonPath)
number = word['words_result_num']
direction = word['direction']

for d in word['words_result']:
    left.append(d["location"]["top"])

imgPath = "IMG/图片/270双栏说明书10.jpg"
img = cv_imread(imgPath)
#这一行代码一定要注意
width = img.shape[0]
#n = kinds(left,number,width).get('kinds')
n = kinds270(left,number,width)



print(n)