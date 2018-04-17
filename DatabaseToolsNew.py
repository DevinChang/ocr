# -!- coding: utf-8 -!-
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
# # cxoracle.update('OCRWORKFILE','JOB_ID','9c4298c9eacdd342f9d224b425b07c62','IS_TO_DB','T')
# sql = "INSERT INTO DRUGPACKAGEINSERT VALUES(1,'阿托伐他汀钙片',NULL,NULL,' Atuofatatinggai Pi',NULL,NULL,'本品主要成份为阿托他汀钙化学名称:(3R,5R)-7-[2-(4基)-5-异丙基3-基4苯基)吡咯-1]35-二羟基庆酸钙盐(2:1其化学结构式分子式:(= 3II4FN2CC分子量:1155.38','本品为片,云膜衣后显白色',NULL,'高胆固醇血症R原发性高胆醚血症患者,包活家旅性高胆出醇症杂合平型)或合高脂《抗受当于F分类法la和1)患者,如饮食治疗和其他非药物跨疗疗效入满意,安应用本品可治疗其总照醇升、低密度脂蛋白固升高,载脂蛋商和油三命升高标赢凡M在纯合子家族性高胆醇血症者,阿托伐他汀钙可与其他陷脂疗法(平法合或单独使用〔当无其他治疗手时),以低总胆醇和低密后蛋白胆固醇','育限司(jCH3N2O5计)','病人在开始本品治疗前,应进行标准的低胆周醇控:在整个治疗期间也应维持合理膳食。应根低密度脑白胆醇基线水平、治疗国标和患者的治疗效果进行剂量的个体化调整常月的始剂为10mg每日一次。剂量调整时间间隔为4周成更长。本品大剂量为8ung每日一次:阿托伐他汀每日用量可在一天内的任时间一次股用,并不受餐影响原发性高晅固醇血症和混合型高脂血症的治疗大多数者服用阿托伐他汀钙10mng每日一次,其血水平可得到控制。治疗2周内可见明显疗效,治疗4尚内可见最大疗效。长期治疗可维持疗效杂子型家族性高胆固醇血症的治疗总者初始剂量应为10mg/日应遵循剂量的个达化原则以每4周为间隔逐步调整量至40mgi日。如果仍然未达到满意疗效,习选择将剂调整至最大剂量80mg日或以4mg每日一次本品配用胆酸盔剂治疗纯合子型家族性高胆固醇血症的治疗在一项由6例者参加的慈善性用药蛋究中,其中46例患者有确认的LDL受体信息这46患者的LDL-C平均下降21%。本品的剂量可增g/日对于纯合子型家族性高胆固醇立症患者,本品的推荐剂量是10-80mg/日。阿托伐他汀钙应作为其他降脂治疗措施(如LDI血浆透析法)的辅助治疗,或当无这些条件时,品可益独使用肾功能不全忠省肾脏疾病不会对本品的血浆浓度或降指效果产生影响,所以无需调整剂量',	'品最常见的不良反应为便秘、胃肠胀气、消化不良和痛,通常生背尼解临木研究中低于2%的患因与本品有关的不良反应中治疗(国)根临研究的数据和上市后广泛经验,本药的不良事件如下按照惯例,不良事件的估训频率排序为:常见(≥1/100,/10 ttha:, 458710001/100):罕见1/10000,<1/100星号非常罕见(<10000胃肠道功能异常常见:使秘:肖肠胀气,消化不良,心腹泻签少见:厌食,呕止血液和淋巴系统功能异常少见:血小板减少症免疫系统功能异常常见:变东反应非常罕见:过敏反应内分泌系统功能异常少见;发,高血症,低血糖:胰腺炎精神常见:失眠少见:健忘症神经系统功能异常常见:头痛,头晕,觉异常,感觉迟少见;外周神经病非常罕见:味觉阜碍眼异常:斗常见:梨觉磁肝胆功能紊乱气见:肝炎,胆汁淤积性黄疽非信罕:肝班衰竭皮肤及共附物常见:皮疹,瘙痒少见:风疹APKA品上CEU非常罕见;血管坤经水浒,大性皮废(包括多形性红斑, Steers Johnse综合征和毒性表皮松解症)耳迷路异常存匿公时少见:耳鸣非常罕见:听方受损骨骼肌肉异常常见:肌痛,关节痛少见:就病上罕见:肌炎,横纹肌溶解症,肌肉痉挛非常罕:肌腱断裂生殖系统和乳房异常按少见:阳痿非常罕见:男子乳腺发育全身异常常见:衰弱:胸痛,青痛,外周水肿,疲劳少见:不适,体重增加客检查中)粉三有限公司与其它 himg-cua还原醇冲制剂同:普报道服用本品的患者出现机游无街。这些改变通常是轻微、一过性的并不需要中断治疗。在接受本品治疗的患者中具有临床意义的血清转氨酶升高(正常上限3倍)的发生率为0.8%、所有者发生的这改变均与剂量相关并且都是可逆性的',NULL,:1,NULL,'大品应只白专科医生在儿童中使用:本品在儿的治疗经验仅限于少数(4至17岁患有严重脂质紊乳如纯合子家族高胆固醇血症的思本品在这一急者人群的推荐起始剂量为10mg日。根据思者的反应和耐受性,齐量可增加至80mg/日。尚无本品对该人群生长发育的安全性资冲','在年龄70岁以上的老年人使用推荐剂盘的阿托伐他汀钙,其疗效及安全性与普通人群没有区别〖药物相互作用在应用 hmg-coa还原酶制剂治疗期间,与下列药物合用可增加发生肌病的危险',NULL,'尚无特殊治疗措施一旦出现药物过敏,病人应根据需要采取对症治疗及支持性措旅以供要器官的功能。应检查患者的功能和监测血清肌酸磷酸激酶水平。由于阿托伐他汀与血浆蛋白广泛结合,液透析不能明显加速本品从体内清除','验中的 hmg-coa还原酶抑制剂相似,服用本品的患者中有2.5%的病人山现血清磁酸肌酸激酶(CPK升高大于正常上限3倍服月本品的患者中有0.4%的病人共磷酸肌酸激升高大于正上限10倍他汀类药品的上市后监测中有高血糖反应,量异常、糖化它红蛋白水平升高、新发慧尿病、血糖控制恶化的报:部分他汀类药品亦有低血糖反应的报告上市后经验:他汀类药品的国外上市后监测中有罕见的认知障碍的报道,表魂为记忆力丧失、记忆力卜降、思维淮孔等:多为非严重、可逆性反应,一般停药后即可复','药效学阿托伐汀属于 hmg-coa还原酶排制剂 P HARMNACEUT阿托伐他汀是 hmg-coa还原醇的选择性、竞争制剂 hmg-coa还怎为限】令','吸收:阿托伐他汀口服后吸收迅速:1-2小时内药浓度达峰Cmx)。吸收程度阿托伐他汀剂量成正比例增加。与口服溶液剂比,阿托伐他汀片的兰物利月度为95~99对生物利用度约为12%,HM(-CA还原酶扣制活性的全身生物利用度约为30%,全身生物利用度较低的原因在一进入体循环前胃肠粘膜消除和成脏首过效应分布:阿托他汀的平均分布容积约为381升。98%以上的阿托伐他汀与血浆蛋白结合代谢:阿托伐名由细胞色素P45034代谢成邻位和对位羟基衍生物及多种B氧化产物。除其他途径外,这些产物还经过葡萄糖醛酸化过程代谢。体外实验中,邹位和对位羟基化代谢物对 hmg-coa还原酶的制作用与阿托伐他汀相当。对 hmg-coa还原酶的抑制活性约70%是主活性代谢产生的消除t阿托伐他汀主要经脏和或肝外代谢后经胆汁消除。但阿托伐他汀无明显的肝肠再循环,阿托伐他汀的平均血浆消除半衰期约为14小时四其活性代流产物的作月,阿托伐汀对 hmg-cua还原酶排制活性的半哀期约为20-30小时特殊人群老年人:健康老年受试者托伐他汀及其活性代谢产物的血浆浓度高于年轻成受试丸彳者,但降脂效果与年轻患者相当儿童:尚无儿童人群的药代动力学资料性别:女性的阿托伐他汀及其活性代谢产物的止浆浓度与男性的不同〔在女性增如约20%AL降低10%,这些差异无临床显著性,因性和女性的路脂效临 LACEU显性差肾功能不全思者:肾腺疾病对阿托伐他汀及共活性代产幼的血浆浓度及效果无仁公何影响 PHA8MACEUTIO日尚无不良事件报行本品灯患者的驾驶能力和操作机器的能力产生任何影响肝功能不全者:慢性酒精性升病患老( childs-''u分级B)中阿括伐他及性制产物的血浆浓度显著升高(Cmax约16倍,AC约11倍)',NULL,'铝铝泡包装,10片/盒,30片/盒国药准字J2013017','35个月','进口药品注册标准JX20130027',NULL,NULL,NULL,' Lek Pha 3 d,d','a57.SI-1526 Ljubljana,斯洛文尼广东省中山火炬开发区国家健基中图',NULL,'0038615861366U760.8531934','0386156813660760-85310695',NULL,NULL,NULL,NULL,NULL,'A000027466',NULL,NULL,TO_DATE( '2018-04-08 20:53:04', 'SYYYY-MM-DD HH24:MI:SS' ),NULL,NULL,NULL,NULL,NULL,NULL)"
# pram = ['肝脏影响开始治疗前应做肝功检查并定期复查患者出现何提示有肝脏的症状或件征时应检查肝功能。转复酶水平升高的患者应加以监测直至恢复正常。如果转氨酶持续升高超过正常3倍以上,建议减量或用本品(见【不良反应过量饮和/或有脏病史患者慎用品强化降低胆固醇水平预防卒中发生( SPARCL研究在一项事后分析中,在无冠心病(CHD>的近期有卒中或短暂缺血发作联20卒中亚型进行了分析,与安慰剂较,阿托他汀80m吃治疗组患者出血性率中发生率较备修在研究入选时有出直卒中或腔隙性梗塞史的患考中危险性的增加显著,于江消出虚性邓中的患者,阿托伐他汀80mg治疗的风与获益的平衡尚不确定,在开始治疗前,应细考忘出血性卒中的潜在危险骨骼肌影响 A9HARMACEUTICAZ(中国)与其他 hmg-coa矫原抑制剂一样:在罕见情况下,阿托伐他汀可能影响骨L,引非痛、肌炎和肌病,可能进为威励兰命的横纹溶解症,现为CPK明显计高超公司正常上限10倍以上)、球蛋白血症和肌球蛋白尿,导致肾治疗前孕妇和哺乳期妇女禁用阿打伐他汀钙片。育龄妇女应采适当的避孕措施、阿托他汀对孕妇和哺乳期女的安全性简未得到证实(见【禁忌】〉动物试验记实,HMG-CnA还原酶抑制剂对胚和婴儿的生长发育可能产生影响当服用阿托伐他汀剂量在过20mg/kgiE(相当于临床人体给药剂量)时,大鼠后代发育迟缓出生后存活率降大鼠血浆中的阿托伐汀及其活性代谢产物的浓度与共乳汁中的浓度同。该药及其活性代谢产物是否在人乳中分泌八清楚)有限公司3细胞色黄4503A4抑刷剂:阿托他经细胞色索P4503A4代射,木品细胞费3及P4503A4的扣制剂环孢素、大环内醛类抗生如红霉素,泰利霉素或克拉每和唑类C抗真菌药如伊曲京唑及HIV蛋白酶抑制剂)合用时可能发生药物相互作用,并用药导致阿托伐他汀力浆浓度加,所以,当阿气汀与上迟药物合用时尤应注意《见注意事项公司载体排制剂:阿托伐他汀及其代谢产物是OATP1B1载体的底物阿托伐他汀10mg号环孢菌素5.2mgkg联合应用使阿托伐他汀的暴落增加77倍。在阿托伐他汀与环孢菌素必须合用的情况下,阿托伐他汀的剂量不应该超过1C红霉素、克拉霉素:红霉和克霉素是已知的红色P4503A4的抑制剂。阿托伐他汀80mg每日一次与红霉素500mgQI1合用使网托他汀的全部活性路335阿托伐他汀10mg/与红霉素(500 mg QID)合用可使阿扎伐低汀的暴多增方3.4倍:在阿托伐他汀与克拉霉素必须合用的情况下,建议服用较低的阿托伐他汀维刊量a对于服用解过4:剂量的患者:建议进行适当的临床检测伊曲康:阿托伐他汀20mg至40mg与伊曲康唑200g日合月可使阿托伐他汀的暴露增加1.5-2.3倍。在阿托伐他汀与伊曲康唑必须合用的情况下,建议求用较低的阿他汀维持剂量对于服用超过40mg剂量的患者,建议进行适当的临庆监测蛋白酶抑制判:蛋白扣制剂为已知的细胞色素P453A4抑制剂,与阿伐他汀合月时,增其血装浓度盐酸地尔卓:阿托伐他汀40ng与地尔硫卓240mg合用可使阿托伐他汀的暴露增加51,在开始地尔硫卓治疗或其剂量调整后,建议对这些患进行适当的临床监测依折姿布:单独使用依折麦布治疗与肌病的发生相关。因此依折麦布与阿伐他汀联会使用时可能增加病的危险性柚子汁:包含抑制细胞色素P4503A4的一种或更多成分,可增加经过该酶谢的药物浆浓度。入240ml轴子汁使阿托发他汀AIC增加37%,活性对羟基代谢物ATC降低2.4%:但是,入大量柚子汁(每天饮用超过1.2L,连续5天)增加阿托化他汀和活性(阿托伐他汀和代谢物) IMG. COA还原酶排制剂AC分别为2.5倍和1.3倍。所以,建议服用阿托伐他汀者不应同时摄入大三柚子汁细胞色素P4503A4导剂:阿托他汀与细泡色索P45034导剂文:依非韦伦利福平、贯叶连翘联合应用可以使阿托伐他汀血浆浓度产生不同水平的降低。由于利福平的双作用机制导肝细胞细胞色素P4503A4和制细胞微取载体 OATPIBL)因为在利福平给药后延迟阿托战他汀的药与阿托伐池汀血浆浓度的显著降低有关,因解配托伐他汀与利福平同时给药维拉帕米和懒酮:尚末进行与维拉的米和供的药物相互作用研究拉帕米和酮已知均可抑制CYPA4活性,与阿托伐们汀合用丁使托伐他汀的暴露增青限其他联治疗24吉非贝齐纤维衍生物:单独应用贝特类药物(如青非贝齐、孝扎贝特>有时房CEU的发生有关到托伐他汀与纤维酸衍生物用,发生病的化险栏可能增(注意项史国潮与吉非以齐300g3合用可使阿托他汀的暴露增加24有限公司地高辛:本品10ng与多个剂量的高辛联合用药时,地高辛的稳态血浆浓度不受影响本品80mg日与地高辛联合用药时,地高辛浓度增加约205这是由于细泡膜转运蛋白P糖蛋白受到抑制。同对服用地高辛的患者应子以适当临未监测口眼避孕药:本品与口服孕药合用时,烘诺酮和乙炔二醇的血浆液度增高。选用口服避孕药时应注意其浓度增高考来拍(胆):本品与考来替泊合用,打伐他汀及其活栏代谢产物的血浆浓度F降约25%,但二药台用的降脂效大于单一药物使用的降指效果抗酸剂:本品与含有氢氧化镁和氢氧化铝的口服抗酸药混悬这合用时,阿托伐他江的血液度下降约35%,但其降低低密度脂蛋白胆醉的作用未受影响华法林:本品与华法林合,凝血酶原时间在最初几天内轻度下降,15天后恢复正需即便如此,服用华头林的患者加服本品时应严密监测氨替比林:木品多个剂星与氨替比林联合用约时未发现对氨替比林清除的影响西咪替丁:有关本马与西珠丁相互作用的研究未发现二之间存相工作用氮氯地平:在健受试者中进行的药物相互作用研究中,阿托伐他汀80mg和氨氯地平0mng合用可使阿伐他汀的暴露增加18%夫西地酸:目前尚未开展阿伐他汀与夫西地酸的相互作用究。与其他他汀类药物样,在合井使用阿托伐他汀和夫西地酸的二市后经验中,已有肌肉相关事件的报道:和纹肌济解症,这一相互作用的制不明确、必须对患者进行密切监测,适当可暂停使用阿托伐他汀其它:本品与降压药物或降糖药物合的床试验中,未发现有临床意义的药物相互作用']
# cxoracle.insert(sql,pram)