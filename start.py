# -*- coding: utf-8 -*-

import os
import random
from ocr import MyOcr
from config import *
from GMP import GMP
from regisration import Regisration
from license import License
from productionCertificate import ProductionCertificate
import introduction
from Improtdrug import Improtdrug

def randomidcode():
    letter = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    randomnum = random.randint(1000, 99999)
    if randomnum < 10000:
        return random.choice(letter) + '00000' + str(randomnum)
    else:
        return random.choice(letter) + '0000' + str(randomnum)

def storage():
    datapath = os.path.dirname(__file__) + '\data'
    gmp = GMP(datapath)
    regisration = Regisration(datapath)
    license = License(datapath)
    certificate = ProductionCertificate(datapath)
    pga = Improtdrug(datapath)
    for file in os.walk(datapath):
        id_code = randomidcode()
        for file_name in file[2]:
        # if 'GMP证书' in file_name:
            gmp.gmp(file[0], id_code)
        # elif "营业执照" in file_name:
            license.license(file[0], id_code)
        # elif "药品再注册批件" in file_name:
            regisration.regisration(file[0], id_code)
        # elif '药品生产许可证' in file_name:
            certificate.recognize(file[0], id_code)
        # elif '说明书' in file_name:
            introduction.run_introduction(file[0], id_code)
        # elif '进口药品注册证' in file_name:
            pga.start(file[0], id_code, 'shuai', '')

            break



if __name__ == '__main__':
    ocr = MyOcr(APP_ID, API_KEY, SECRET_KEY, 4)
    ##ocr.pdf2img()
    # ocr.run()
    storage()