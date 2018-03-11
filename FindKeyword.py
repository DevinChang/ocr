import re
def findImportWords(str):

    #case a:当'】'能够被提取的时候
    if re.match(r".+?(?=】)", str):
        leftvalue = str.split('】')[0]
        rightvalue = str.split('】')[1]
        flag = 1
    elif re.match(r".+?(?=])", str):
        leftvalue = str.split(']')[0]
        rightvalue = str.split(']')[1]
        flag = 1
    elif re.match(r".+?(?=：)", str):
        leftvalue = str.split('：')[0]
        rightvalue = str.split('：')[1]
        flag = 1
    elif re.match(r".+?(?=:)", str):
        leftvalue = str.split(':')[0]
        rightvalue = str.split(':')[1]
        flag = 1
    else:
        flag = 0
    if flag == 1:#当有】或者]的时候
        # 第16个字段：孕妇及哺乳期妇女用药
        pA16 = r"孕妇及*哺*乳*期*妇*女*用*药|孕*妇及*哺乳期*妇女*用药*"
        patternA16 = re.compile(pA16)
        matcherA16 = re.search(patternA16, leftvalue)  # 在源文本中搜索符合正则表达式的部分
        if matcherA16!=None:
            return ["孕妇及哺乳期妇女用药", rightvalue, matcherA16.group()]
        # 第17个字段：儿童用药
        pA17 = r"儿童*用药*|儿*童用*药" 
        patternA17 = re.compile(pA17)
        matcherA17 = re.search(patternA17, leftvalue)  # 在源文本中搜索符合正则表达式的部分
        if matcherA17!=None:
            return ["儿童用药", rightvalue, matcherA17.group()]

        # 第18个字段：老年用药
        pA18 = r"老年*用药*|老*年用*药"
        patternA18 = re.compile(pA18)
        matcherA18 = re.search(patternA18, leftvalue)  # 在源文本中搜索符合正则表达式的部分
        if matcherA18!=None:
            return ["老年用药", rightvalue, matcherA18.group()]

        # 第19个字段：药物相互作用
        pA19 = r"药*物*相互作用*|药*物相互作用"
        patternA19 = re.compile(pA19)
        matcherA19 = re.search(patternA19, leftvalue)  # 在源文本中搜索符合正则表达式的部分
        if matcherA19!=None:
            return ["药物相互作用", rightvalue, matcherA19.group()]

        # 第20个字段：药物过量
        pA20 = r"药*物过量*|药物*过量*"
        patternA20 = re.compile(pA20)
        matcherA20 = re.search(patternA20, leftvalue)  # 在源文本中搜索符合正则表达式的部分
        if matcherA20!=None:
            return ["药物过量", rightvalue, matcherA20.group()] 

        # 第21个字段：临床试验
        pA21 = r"临*床试验*|临床*试*验"
        patternA21 = re.compile(pA21)
        matcherA21 = re.search(patternA21, leftvalue)  # 在源文本中搜索符合正则表达式的部分
        if matcherA21 != None:
            return ["临床试验",  rightvalue, matcherA21.group()]

        # 第22个字段：药理毒理
        pA22 = r"药理毒*理*|药理*毒理*|药*理毒*理"
        patternA22 = re.compile(pA22)
        matcherA22 = re.search(patternA22, leftvalue)  # 在源文本中搜索符合正则表达式的部分
        if matcherA22 != None:
            return ["药理毒理", rightvalue, matcherA22.group()]

        # 第23个字段：药代动力学
        pA23 = r"药代*动力*学|药代*动*力学"
        patternA23 = re.compile(pA23)
        matcherA23 = re.search(patternA23, leftvalue)  # 在源文本中搜索符合正则表达式的部分
        if matcherA23 != None:
            return ["药代动力学", rightvalue, matcherA23.group()]

        # 第24个字段：贮藏
        pA24 = r"贮藏*|贮*藏"
        patternA24 = re.compile(pA24)
        matcherA24 = re.search(patternA24, leftvalue)  # 在源文本中搜索符合正则表达式的部分
        if matcherA24 != None:
            return ["贮藏", rightvalue, matcherA24.group()]

        # 第25个字段：包装
        pA25 = r"包装*|包*装"
        patternA25 = re.compile(pA25)
        matcherA25 = re.search(patternA25, leftvalue)  # 在源文本中搜索符合正则表达式的部分
        if matcherA25 != None:
            return ["包装", rightvalue, matcherA25.group()]

        # 第26个字段：有效期
        pA26 = r"有*效期|有效*期"
        patternA26 = re.compile(pA26)
        matcherA26 = re.search(patternA26, leftvalue)  # 在源文本中搜索符合正则表达式的部分
        if matcherA26 != None:
            return ["有效期", rightvalue, matcherA26.group()]

        # 第27个字段：执行标准
        pA27 = r"执行*标*准|执*行标*准|执行*标准*"
        patternA27 = re.compile(pA27)
        matcherA27 = re.search(patternA27, leftvalue)  # 在源文本中搜索符合正则表达式的部分
        if matcherA27 != None:
            return ["执行标准", rightvalue, matcherA27.group()]

        # 第28个字段：批准文号
        pA28 = r"批准*文*号|批*准文*号|批*准文号*"
        patternA28 = re.compile(pA28)
        matcherA28 = re.search(patternA28, leftvalue)  # 在源文本中搜索符合正则表达式的部分
        if matcherA28 != None:
            return ["批准文号", rightvalue, matcherA28.group()]

        # 第29个字段：企业名称
        pA29 = r"企业*名称*|企*业名*称"
        patternA29 = re.compile(pA29)
        matcherA29 = re.search(patternA29, leftvalue)  # 在源文本中搜索符合正则表达式的部分
        if matcherA29 != None:
            return ["企业名称", rightvalue, matcherA29.group()]

        # 第30个字段：企业地址
        pA30 = r"企业*地址|企*业地址*|企*业地*址"
        patternA30 = re.compile(pA30)
        matcherA30 = re.search(patternA30, leftvalue)  # 在源文本中搜索符合正则表达式的部分
        if matcherA30 != None:
            return ["企业地址", rightvalue, matcherA30.group()]

        # 第31个字段： 生产厂家
        pA31 = r"生*产厂家*：*|生产*厂家*：*|生*产厂*家：*|生产*厂*家：*|生*产企业*：*|生产*企业*：*|生*产企*业：*|生产*企*业：*"
        patternA31 = re.compile(pA31)
        matcherA31 = re.search(patternA31, str)  # 在源文本中搜索符合正则表达式的部分
        if matcherA31!=None:
            indexA31 = matcherA31.span()[1] + 1
            return ["生产厂家", str[indexA31:], matcherA31.group()]

        # 第32个字段： 生产地址
        pA32 = r"生*产地址*|生*产地*址|生产*地*址|生产*地址*"
        patternA32 = re.compile(pA32)
        matcherA32 = re.search(patternA32, str)  # 在源文本中搜索符合正则表达式的部分
        if matcherA32 != None:
            indexA32 = matcherA32.span()[1] + 1
            return ["生产地址", str[indexA32:], matcherA32.group()]


        #第33个字段： 邮政编码
        pA33 = r"邮*政*编码*"
        patternA33 = re.compile(pA33)
        matcherA33 = re.search(patternA33, str)  # 在源文本中搜索符合正则表达式的部分
        if matcherA33 != None:
            indexA33 = matcherA33.span()[1] + 1
            return ["邮政编码", str[indexA33:], matcherA33.group()]

        #第34个字段： 电话号码
        pA34 = r"电*话号码*"
        patternA34 = re.compile(pA34)
        matcherA34 = re.search(patternA34, str)  # 在源文本中搜索符合正则表达式的部分
        if matcherA34 != None:
            indexA34 = matcherA34.span()[1] + 1
            return ["电话号码", str[indexA34:], matcherA34.group()]

        ##第35个字段： 传真号码
        pA35 = r"传*真号码*"
        patternA35 = re.compile(pA35)
        matcherA35 = re.search(patternA35, str)  # 在源文本中搜索符合正则表达式的部分
        if matcherA35 != None:
            indexA35 = matcherA35.span()[1] + 1
            return ["传真号码", str[indexA35:], matcherA35.group()]

        #第36个字段： 网址
        pA36 = r"网址*：*"
        patternA36 = re.compile(pA36)
        matcherA36 = re.search(patternA36, str)  # 在源文本中搜索符合正则表达式的部分
        if matcherA36 != None:
            indexA36 = matcherA36.span()[1] + 1
            return ["网址", str[indexA36:], matcherA36.group()]

        #第37个字段： 核准日期
        pA37 = r"核*准日期*：*"
        patternA37 = re.compile(pA37)
        matcherA37 = re.search(patternA37, str)  # 在源文本中搜索符合正则表达式的部分
        if matcherA37 != None:
            indexA37 = matcherA37.span()[1] + 1
            return ["核准日期", str[indexA37:], matcherA37.group()]

        #第38个字段： 修改日期
        pA38 = r"修*改日期*：*"
        patternA38 = re.compile(pA38)
        matcherA38 = re.search(patternA38, str)  # 在源文本中搜索符合正则表达式的部分
        if matcherA38 != None:
            indexA38 = matcherA38.span()[1] + 1
            return ["修改日期", str[indexA38:], matcherA38.group()]

    # case b:当'】'不能够被提取的时候
    else:
        # 第16个字段：孕妇及哺乳期妇女用药
        p = r"孕妇及*哺*乳*期*妇*女*用*药|孕*妇及*哺乳期*妇女*用药*"
        keystr = str[0:10]
        pattern = re.compile(p)
        matcher = re.search(pattern, keystr)  # 限制在源文本前4个词中搜索符合正则表达式的部分
        if matcher != None:
            rightvalue = matcher.span()[1]
            return ["孕妇及哺乳期妇女用药", rightvalue, matcher.group()]

        # 第17个字段：儿童用药
        p = r"儿童*用药*|儿*童用*药"
        keystr = str[0:4]
        pattern = re.compile(p)
        matcher = re.search(pattern, keystr)  # 限制在源文本前4个词中搜索符合正则表达式的部分
        if matcher != None:
            rightvalue = matcher.span()[1]
            return ["儿童用药", rightvalue, matcher.group()]

        # 第18个字段：老年用药
        p = r"老年*用药*|老*年用*药"
        keystr = str[0:4]
        pattern = re.compile(p)
        matcher = re.search(pattern, keystr)  # 限制在源文本前4个词中搜索符合正则表达式的部分
        if matcher != None:
            rightvalue = matcher.span()[1]
            return ["老年用药", rightvalue, matcher.group()]

        # 第19个字段：药物相互作用
        pA19 = r"药*物*相互作用*|药*物相互作用"
        keystr = str[0:4]
        pattern = re.compile(p)
        matcher = re.search(pattern, keystr)  # 限制在源文本前4个词中搜索符合正则表达式的部分
        if matcher != None:
            rightvalue = matcher.span()[1]
            return ["药物相互作用", rightvalue, matcher.group()]

        # 第20个字段：药物过量
        p = r"药*物过量*|药物*过量*"
        keystr = str[0:4]
        pattern = re.compile(p)
        matcher = re.search(pattern, keystr)  # 限制在源文本前4个词中搜索符合正则表达式的部分
        if matcher != None:
            rightvalue = matcher.span()[1]
            return ["药物过量", rightvalue, matcher.group()]

        # 第21个字段：临床试验
        p = r"临*床试验*|临床*试*验"
        keystr = str[0:4]
        pattern = re.compile(p)
        matcher = re.search(pattern, keystr)  # 限制在源文本前4个词中搜索符合正则表达式的部分
        if matcher != None:
            rightvalue = matcher.span()[1]
            return ["临床试验", rightvalue, matcher.group()]

        # 第22个字段：药理毒理
        p = r"药理毒*理*|药理*毒理*|药*理毒*理"
        keystr = str[0:4]
        pattern = re.compile(p)
        matcher = re.search(pattern, keystr)  # 限制在源文本前4个词中搜索符合正则表达式的部分
        if matcher != None:
            rightvalue = matcher.span()[1]
            return ["药理毒理", rightvalue, matcher.group()]

        # 第23个字段：药代动力学
        p = r"药代*动力*学|药代*动*力学"
        keystr = str[0:5]
        pattern = re.compile(p)
        matcher = re.search(pattern, keystr)  # 限制在源文本前4个词中搜索符合正则表达式的部分
        if matcher != None:
            rightvalue = matcher.span()[1]
            return ["药代动力学", rightvalue, matcher.group()]

        # 第24个字段：贮藏
        p = r"贮藏*|贮*藏"
        keystr = str[0:2]
        pattern = re.compile(p)
        matcher = re.search(pattern, keystr)  # 限制在源文本前4个词中搜索符合正则表达式的部分
        if matcher != None:
            rightvalue = matcher.span()[1]
            return ["贮藏", rightvalue, matcher.group()]

        # 第25个字段：包装
        p = r"包装*|包*装"
        keystr = str[0:2]
        pattern = re.compile(p)
        matcher = re.search(pattern, keystr)  # 限制在源文本前4个词中搜索符合正则表达式的部分
        if matcher != None:
            rightvalue = matcher.span()[1]
            return ["包装", rightvalue, matcher.group()]

        # 第26个字段：有效期
        p = r"有*效期|有效*期"
        keystr = str[0:3]
        pattern = re.compile(p)
        matcher = re.search(pattern, keystr)  # 限制在源文本前4个词中搜索符合正则表达式的部分
        if matcher != None:
            rightvalue = matcher.span()[1]
            return ["有效期", rightvalue, matcher.group()]

        # 第27个字段：执行标准
        p = r"执行*标*准|执*行标*准|执行*标准*"
        keystr = str[0:4]
        pattern = re.compile(p)
        matcher = re.search(pattern, keystr)  # 限制在源文本前4个词中搜索符合正则表达式的部分
        if matcher != None:
            rightvalue = matcher.span()[1]
            return ["执行标准", rightvalue, matcher.group()]

        # 第28个字段：批准文号
        p = r"批准*文*号|批*准文*号|批*准文号*"
        keystr = str[0:4]
        pattern = re.compile(p)
        matcher = re.search(pattern, keystr)  # 限制在源文本前4个词中搜索符合正则表达式的部分
        if matcher != None:
            rightvalue = matcher.span()[1]
            return ["批准文号", rightvalue, matcher.group()]

        # 第29个字段：企业名称
        p = r"企业*名称*|企*业名*称"
        keystr = str[0:4]
        pattern = re.compile(p)
        matcher = re.search(pattern, keystr)  # 限制在源文本前4个词中搜索符合正则表达式的部分
        if matcher != None:
            rightvalue = matcher.span()[1]
            return ["企业名称", rightvalue, matcher.group()]

        # 第30个字段：企业地址
        p = r"企业*地址|企*业地址*|企*业地*址"
        keystr = str[0:4]
        pattern = re.compile(p)
        matcher = re.search(pattern, keystr)  # 限制在源文本前4个词中搜索符合正则表达式的部分
        if matcher != None:
            rightvalue = matcher.span()[1]
            return ["企业地址", rightvalue, matcher.group()]

        # 第31个字段： 生产厂家
        str31 = str[0:6] #在前六个字符中去判断，无括号，则应该以更加严格的方式检查
        pB31 = r"生*产厂家*：*|生产*厂家*：*|生*产厂*家：*|生产*厂*家：*|生*产企业*：*|生产*企业*：*|生*产企*业：*|生产*企*业：*"
        patternB31 = re.compile(pB31)
        matcherB31 = re.search(patternB31, str31)  # 在源文本中搜索符合正则表达式的部分
        if matcherB31 != None:
            indexB31 = matcherB31.span()[1]
            return ["生产厂家", str[indexB31:], matcherB31.group()]
        #第32个字段： 生产地址
        str32 = str[0:6]
        pB32 = r"生*产地址*：*|生*产地*址：*|生产*地*址：*|生产*地址*：*"
        patternB32 = re.compile(pB32)
        matcherB32 = re.search(patternB32, str32)  # 在源文本中搜索符合正则表达式的部分
        if matcherB32 != None:
            indexB32 = matcherB32.span()[1]
            return ["生产地址", str[indexB32:], matcherB32.group()]
        # 第33个字段： 邮政编码
        str33 = str[0:6]
        pB33 = r"邮*政编码*|邮政*编码*"
        patternB33 = re.compile(pB33)
        matcherB33 = re.search(patternB33, str33)  # 在源文本中搜索符合正则表达式的部分
        if matcherB33 != None:
            indexB33 = matcherB33.span()[1]
            return ["邮政编码", str[indexB33:], matcherB33.group()]
        ## 第34个字段： 电话号码
        str34 = str[0:6]
        pB34 = r"电*话号码*"
        patternB34 = re.compile(pB34)
        matcherB34 = re.search(patternB34, str34)  # 在源文本中搜索符合正则表达式的部分
        if matcherB34 != None:
            indexB34 = matcherB34.span()[1]
            return ["电话号码", str[indexB34:], matcherB34.group()]
        ##第35个字段： 传真号码
        str35 = str[0:6]
        pB35 = r"传*真号码*"
        patternB35 = re.compile(pB35)
        matcherB35 = re.search(patternB35, str35)  # 在源文本中搜索符合正则表达式的部分
        if matcherB35 != None:
            indexB35 = matcherB35.span()[1]
            return ["传真号码", str[indexB35:], matcherB35.group()]
        ##第36个字段： 网址
        str36 = str[0:4]
        pB36 = r"网址*：*"
        patternB36 = re.compile(pB36)
        matcherB36 = re.search(patternB36, str36)  # 在源文本中搜索符合正则表达式的部分
        if matcherB36 != None:
            indexB36 = matcherB36.span()[1]
            return ["网址", str[indexB36:], matcherB36.group()]
        ##第37个字段： 核准日期
        str37 = str[0:6]
        pB37 = r"核*准日期*：*"
        patternB37 = re.compile(pB37)
        matcherB37 = re.search(patternB37, str37)  # 在源文本中搜索符合正则表达式的部分
        if matcherB37 != None:
            indexB37 = matcherB37.span()[1]
            return ["网址", str[indexB37:], matcherB37.group()]
        ##第38个字段： 修改日期
        str38 = str[0:6]
        pB38 = r"修*改日期*：*"
        patternB38 = re.compile(pB38)
        matcherB38 = re.search(patternB38, str38)  # 在源文本中搜索符合正则表达式的部分
        if matcherB38 != None:
            indexB38 = matcherB38.span()[1]
            return ["修改日期", str[indexB38:], matcherB38.group()]








#print(findImportWords("有期】就是123修改日期"))