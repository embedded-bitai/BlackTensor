import sys
import viewController as vc
import dataModel as dm
import dictStock as ds
# import mysqlController as ms

# dbconfig
import dbconfig
import requests
from bs4 import BeautifulSoup
from time import sleep
import re


#pyqt
from PyQt5.QtWidgets import *

class MyAutoTradeApp():
    def __init__(self):
        print("매매 프로그램 클래스")
        self.myDataModel = dm.DataModel()
        self.myViewController = vc.ViewController(self.myDataModel)
        # self.myDictStock = ds.DictStock()
        # self.myPyMySql = ms.MysqlController()


if __name__=="__main__":
    print("Main Run")
    app = QApplication(sys.argv)
    myApp = MyAutoTradeApp()
    myApp.myViewController.show()
    app.exec_()