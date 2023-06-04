#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

"""
#加载模块
from cnocr import CnOcr
import logging

def textfromimage(image,index=0,key='text'):

    ocr = CnOcr()
    try:
        res = ocr.ocr(image)
        print(res[index][key])
        return res[index][key]
    except:
        logging.error("图片识别文件错误！")
