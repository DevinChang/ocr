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
    def insertsql(self,sql):
        conn = self.getconnect()
        cr = conn.cursor()
        # col 是clob字段
        cr.execute(sql)
        # rs=cr.fetchall()
        # for r in rs:
        #     print(r[0])
        #     #text = r[0][0].read()
        #     #pram.appen(text)
        cr.close()
        conn.commit()
        conn.close()

        # print('执行成功')

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
        elif key == '剂型':
            return 'DRUG_FORM'
        elif key == '证书编号':
            return 'GMP_NO'
        elif key == '地址':
            return 'ADDR'
        elif key == '认证范围':
            return 'INSP_SCOPE'
        elif key == '有效期至':
            return 'VLD'
        elif key == '发证机关':
            return 'ISSUE_ORG'
        elif key == '发证日期':
            return 'ISSUE_DATE'
        elif key == 'ENT_NAME':
            return 'ENT_NAME'
        elif key == 'ENT_TYPE':
            return 'ENT_TYPE'
        elif key == '住所':
            return 'ADDR'
        elif key == '法定代表人':
            return 'LEGAL_REPS'
        elif key == '注册资本':
            return 'REG_CAPITAL'
        elif key == '成立日期':
            return 'EST_DATE'
        elif key == '营业期限':
            return 'OPT_TERM'
        elif key == '经营范围':
            return 'BIZ_SCOPE'
        elif key == '统一社会信用代码':
            return 'USCC'
        elif key == '药品名称':
            return 'DRUG_NAME'
        elif key == '企业名称_许可证':
            return 'ENT_NAME'
        elif key == '注册地址':
            return 'REG_ADDR'
        elif key == '企业负责人':
            return 'ENT_PRINCIPAL'
        elif key == '质量负责人':
            return 'QC_PRINCIPAL'
        elif key == '日常监管机构':
            return 'SUPERVISION_DEPT'
        elif key == '日常监管人员':
            return 'SUPERVISOR'
        elif key == '监督举报电话':
            return 'SUPERVISOR_CT'
        elif key == '许可证编号':
            return 'LIC_NO'
        elif key == '分类码':
            return 'CATE_CODE'
        elif key == '许可证编号':
            return 'LIC_NO'
        elif key == '生产地址和生产范围':
            return 'PROD_ADDR_SCOPE'
        elif key == '签发人':
            return 'ISSUER'
            

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

    def update(self,tablename,uniqueid,uniqueidvalue,update_pram,update_value):#依次为：表名 唯一性标识如JOB_ID JOB_ID的内容 要更新的字段  要更新为的内容
        insertsql = 'UPDATE '+tablename+' SET '+update_pram+' = '+"'"+update_value+"'"+' WHERE '+uniqueid+" = '"+uniqueidvalue+"'"
        print('insert语句为：'+insertsql)
        try:
            self.insertsql(insertsql)
        except Exception as e:
            print(e)
            print('更新失败')

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
                elif flag ==2:
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



# cxoracle = cxOracle('scott','123456')
# cxoracle.update('OCRWORKFILE','JOB_ID','9c4298c9eacdd342f9d224b425b07c62','IS_TO_DB','T')
