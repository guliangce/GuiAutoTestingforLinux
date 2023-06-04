#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
这是一个测试用例模板

测试用例:测试文档编辑器LibreOffice,创建word文档，输入文字并能正常保存。

执行步骤：
1.打开文档编辑器 LibreOffice
2.新建一个word文件。
3.输入 www.baidu.com。
4.保存文件。
5.关闭LibreOffice。

预期结果:
1.可以正常打开LibreOfficed,打开的是 LibreOffice 创建文档的首页。（通过图片对比）
2.word编辑器被打开
3.能够正常输入.(通过图片对比)
4.保存成功。（检查保存目录下是否有存档文件。）
5.关闭成功。

'''
#加载系统模块
import os
import subprocess
import logging
#加载unittest
import unittest
#加载dogtail
from dogtail.tree import *
from dogtail.utils import *
from dogtail import rawinput
#导入图片文字识别模块
import textfromimage as tfi
#导入图片比对模块
import Imagecomparison as ic

#全局变量
TEXT = "linux GUI autotesting"
IMG1 = "demoimage1"
IMG2 = "demoimage2"

#测试用例类
class TestCase_Demo(unittest.TestCase):
    """测试用例 demo"""
    #初始化函数
    def setUp(self):
        logging.info('开始测试')
        #启动应用程序
        run('soffice')
        #获取应用程序对象
        self.app = root.application(appName="soffice")
        logging.info('应用启动成功')

    # 设置焦点，确保操作的是被测程序
    def setfocus(self):
        #等待GUI的加载
        LibreOffice = self.app.child('LibreOffice', 'frame')
        LibreOffice.click()
        #打开word编辑器
        wordedit = self.app.child('Writer 文本文档', 'push button')
        wordedit.click()
        logging.info('编辑器打开成功')

    # 输入文字
    def inputtext(self):
        #获得输入控件的父对象
        input_father = self.app.child('未命名 1 - LibreOffice 文档', 'document text')
        #获得输入对象
        input_text = input_father.child('','paragraph')
        #输入文字
        input_text.typeText(TEXT)
        logging.info('文字输入成功')

    # 保存文件
    def savetext(self):
        #sleep(1)
        #使用快捷键盘保存
        rawinput.keyCombo('<Ctrl>s')
        #获取保存窗口的父控件
        save_father = self.app.child('保存', 'file chooser')
        save_text = save_father.child('','text')
        #输入保存文件名称
        save_text.typeText('demo_dogtail')
        #点击保存按钮
        save_father.child('保存(S)','push button').click()
        logging.info('文件保存成功')

    #关闭应用
    def closeapp(self):
        rawinput.keyCombo('<Ctrl>q')

    # 用例运行逻辑
    def test_go(self):
        #运行用例
        self.setfocus()
        self.inputtext()
        self.savetext()
        #获取屏幕截图 - 示例
        screenshot('liunx_gui_test')
        #检查目录下的保存文件 是否生成
        p = subprocess.Popen(["ls", "/home/guliangce/"],stdout=subprocess.PIPE)
        out,err = p.communicate()
        #获取两个需要对比的截图 - 示例
        ima1 = ic.getImageFile(IMG1)
        ima2 = ic.getImageFile(IMG2)
        #断言检查文件是否保存？截图是否一致？输入的文字是否和预期一致？
        if ('dogtail' in str(out)) and (TEXT in tfi.textfromimage(IMG1+'.png')) and ic.CompareImage(ima1,ima2):
            self.assertEqual('True', 'True')
        else:
            self.assertEqual('False', 'True')

    def tearDown(self):
        self.closeapp()
        os.system('rm -fr /home/guliangce/demo_dogtail.odt')
        logging.info('测试已完成')
    
