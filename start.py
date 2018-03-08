# -*- coding: utf-8 -*-

from ocr import MyOcr
from config import *




if __name__ == '__main__':
    ocr = MyOcr(APP_ID, API_KEY, SECRET_KEY, 3)
    #ocr.pdf2img()
    ocr.run()