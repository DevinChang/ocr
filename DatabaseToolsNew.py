import json
import cx_Oracle
from config import *


class cxOracle:
    #connectstr = 'scott/123456@localhost:1521/orcl'

    def __init__(self,username = USER_NAME, password = PASSWORD, port = 1521, database = 'orcl'):
        self.connectstr = '{}/{}@localhost:{}/{}'.format(username, password, port, database)
#获取数据库连接
    def getconnect(self):
        conn = cx_Oracle.connect(self.connectstr)
        return conn


#执行sql
    def insert(self,sql):
        conn = self.getconnect()
        cr = conn.cursor()
        # col 是clob字段
        cr.execute(sql)
        rs=cr.fetchall()
        for r in rs:
            print(r[0])
            #text = r[0][0].read()
            #pram.appen(text)
        cr.close()

    def _convert_key(self, key):
        """将识别后的数据的key转换为可以插入到数据库的key"""
        if key == '通用名称':
            return 'GENERIC_NAME'
        elif key == '汉语拼音':
            return 'CHN_PINYIN'
        elif key == '英文名称':
            return 'EN_NAME'
        elif key == '成份':
            return 'INGREDIENTS'
        elif key == '性状':
            return 'DRUG_DESCRIPTION'
        elif key == '功能主治':
            return 'INDICATION'
        elif key == '规格':
            return 'STRENGTH'
        elif key == '用法用量':
            return 'DOSAGE_ADMIN'
        elif key == '不良反应':
            return 'ADR_REACTION'
        elif key == '禁忌':
            return 'CONTRAINDICATION'
        elif key == '注意事项':
            return 'PRECAUTION'
        elif key == '贮藏':
            return 'DRUG_STORAGE'
        elif key == '包装':
            return 'DRUG_PACKAGE'
        elif key == '有效期':
            return 'SHELF_LIFE'
        elif key == '执行标准':
            return 'SPEC_NO'
        elif key == '批准文号':
            return 'APRV_NO'
        elif key == '生产厂家':
            return 'MFRS'
        elif key == '企业名称':
            return 'CO_NAME'
        elif key == '企业地址':
            return 'CO_ADDR'
        elif key == '生产地址':
            return 'PROD_ADDR'
        elif key == '邮政编码':
            return 'ZIP_CODE'
        elif key == '电话号码':
            return 'TEL'
        elif key == '传真号码':
            return 'FAX'
        elif key == '核准日期':
            return 'ISSUE_DATE'
        elif key == '修改日期':
            return 'MOD_DATE'
        elif key == '药物相互作用':
            return 'INTERACTION_DRUG'
        elif key == '网址':
            return 'WEB_SITE'
        elif key == '药代动力学':
            return 'PHARMACOKINETICS'
        elif key == '孕妇及哺乳期妇女用药':
            return 'PREGNANCY_LACTATION'
        elif key == '儿童用药':
            return 'USE_IN_CHD'
        elif key == '老年用药':
            return 'USE_IN_ELDR'
        elif key == '药物过量':
            return 'OVER_DOSAGE'
        elif key == '药理毒理':
            return 'PHARMACOLOGY'
        elif key == '生产厂家':
            return 'MFRS'
        elif key == '商品名称':
            return 'TRADE_NAME'
        elif key == '临床试验':
            return 'CLINICAL_TRIAL'
        elif key == 'OTC':
            return 'OTC_SIGN'
        elif key == '外':
            return 'IS_EXT_MEDICINE'
        elif key == '作用类别':
            return 'ACTION_CATE'
        elif key == '委托方企业名称':
            return 'CL_NAME'
        elif key == '委托方企业地址':
            return 'CL_ADDR'
        elif key == '受托方企业名称':
            return 'TR_NAME'
        elif key == '受托方企业名称':
            return 'TR_ADDR'
        elif key == '分装企业名称':
            return 'SU_NAME'
        elif key == '分装企业地址':
            return 'SU_ADDR'
        elif key == 'ID_CODE':
            return 'ID_CODE'

    #根据sql语句（带参数）执行插入数据
    def insert(self,sql,pram):
        conn = self.getconnect()
        cr = conn.cursor()  # 获取cursor
        cr.execute(sql,pram)
        # 关闭连接
        cr.close()
        conn.commit()
        conn.close()
        print('存入成功')

#根据json字典返回
    def getsavesql(self,tablename,jsonstrs, flag):
        keys = ''
        values = ''
        pram=[]
        #text = json.loads(jsonstrs)
        text = jsonstrs
        if isinstance(text,dict):
            i = 0
            for key in text:
                i = i+1
                #if (key == '质量电话') or (key == '销售电话'):
                #    continue
                if flag == 1:
                    convert_key = self._convert_key(key)
                else:
                    convert_key = key
                if not convert_key:
                    continue
                if i == len(text):

                    keys = keys+str(convert_key)
                    pram.append(str(text[key]))
                    values = values + ':' + str(i)
                else:
                    keys = keys + str(convert_key) + ','
                    pram.append(str(text[key]))
                    values = values + ':' + str(i) + ','
        else:
            print('json类型不正确')
        sql = 'INSERT INTO '+tablename+'('+keys+') VALUES('+values+')'
        print(sql)
        
        return sql,pram


