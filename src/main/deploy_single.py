# -*- coding： utf-8 -*-


import json
import os
from introduction import Inrtroduction
from GMP import GMP
from license import License
from regisration import Regisration
from Improtdrug import Improtdrug
from productionCertificate import ProductionCertificate

def storage(json_file):
    datapath = os.path.dirname(__file__) + '\data'
    imgpath = r'D:\\IMG'
    introduction = Inrtroduction(imgpath)
    gmp = GMP(imgpath)
    regisration = Regisration(imgpath)
    license = License(imgpath)
    certificate = ProductionCertificate(datapath, imgpath)
    pga = Improtdrug(imgpath)
    files = json_file['files']
    for file in files:
        if '说明书' in file['type']:
            introduction_dict = introduction.introduction_deploy(file['imgs'], '12345')
        elif 'GMP' in file['type']:
            gmp_dict = gmp.gmp_delploy(file['imgs'], '12345')
        elif '注册批件' in file['type']:
            regisration_dict = regisration.regisration_deploy(file['imgs'], '12345')
        elif '营业执照' in file['type']:
            license_dict = license.license_deploy(file['imgs'], '12345')
        elif '许可证' in file['type']:
            certificate_dict = certificate.recognize_deploy(file['imgs'], '12345')

    #for file in os.walk(datapath):
    #    id_code = randomidcode()
    #    for file_name in file[2]:
    #    # if 'GMP证书' in file_name:
    #        gmp.gmp(file[0], id_code)
    #    # elif "营业执照" in file_name:
    #        license.license(file[0], id_code)
    #    # elif "药品再注册批件" in file_name:
    #        regisration.regisration(file[0], id_code)
    #    # elif '药品生产许可证' in file_name:
    #        certificate.recognize(file[0], id_code)
    #    # elif '说明书' in file_name:
    #        introduction.run_introduction(file[0], id_code)
    #    # elif '进口药品注册证' in file_name:
    #        try:
    #            pga.start(file[0], id_code, 'shuai', '')
    #        except Exception as e:
    #            logmgr = LogMgr()
    #            logmgr.error(file[0]+ ":" + str(e))
    #            continue
    #        break

if __name__ == '__main__':
    with open(r'F:\IMG\11A0015\testnet.json', 'rb') as f:
        json_data = json.loads(f.read())
    storage(json_data)