import json
import cx_Oracle
from config import *

"""
__application__: 数据入库
__author__: 肖帅
__date__: 2018/1/31
"""


class cxOracle:
    #connectstr = 'scott/123456@localhost:1521/orcl'

    def __init__(self,username = USER_NAME, password = PASSWORD, port = 1521, database = 'orcl'):
        self.connectstr = '{}/{}@localhost:{}/{}'.format(username, password, port, database)


    #获取连接
    def getconnect(self):
        conn = cx_Oracle.connect(self.connectstr)
        return conn
    #插入数据
    def insert(self,sql):
        conn=self.getconnect()
        cr = conn.cursor()  # 获取cursor
        cr.execute(sql)
        # 关闭连接
        cr.close()
        conn.commit()
        conn.close()
        print('存入成功')

    def _convert_key(self, key):
        """将识别后的数据的key转换为可以插入到数据库的key"""
        if key == '通用名称':
            return 'GENERIC_NAME'
        elif key == '汉语拼音':
            return 'CHN_PINYIN'
        elif key == 'OTC':
            return 'OTC_SIGN'
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
        elif key == '生产企业':
            return 'MFRS'
        elif key == '企业名称':
            return 'CO_NAME'
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

        

    def getsavesql(self,tablename,jsonstrs):
        """获取插入sql"""
        keys = ''
        values = ''
        #text = json.loads(jsonstrs)
        text = jsonstrs
        print(text)
        if isinstance(text,dict):
            i = 0
            for key in text:
                print(key)
                convert_key = self._convert_key(key) 
                i = i+1
                if i == len(text):
                    keys = keys+str(convert_key)
                    values = values+"'"+str(text[key])+"'"
                else:
                    keys = keys + str(convert_key) + ','
                    values = values+"'"+str(text[key])+"'"+','
        else:
            print('json类型不正确')
        sql = 'INSERT INTO '+tablename+'('+keys+') VALUES('+values+')'
        print(sql)
        return sql