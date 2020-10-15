import dataModel as dm
import sys
import datetime
import time
import os
import json
import requests
# import dictStock as ds

#pyqt
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QAxContainer import *
from PyQt5.QtGui import *

import csv
form_class = uic.loadUiType("main_windows.ui")[0]

class ViewController(QMainWindow, form_class):
    def __init__(self, my_model):
        super().__init__()
        # kiwoom Open API 초기화
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.login()
        self.setUI()
        self.myModel = my_model
        print("View Controller")

        # # kiwoom Open API event Trigger
        # self.kiwoom.OnEventConnect.connect(self.event_connect)
        #
        # # UI event Trigger
        # self.searchItemButton.clicked.connect(self.searchItem)

        # 키움 Open API Trigger

###
        # 변수선언
        self.repeatNum = 0
        self.input_data = []
        self.dicStock = {}

        # 저장할 폴더 없으면 생성
        dirname = './Data'
        if not os.path.isdir(dirname):
            os.mkdir(dirname)

###

    def login(self):
        self.kiwoom.dynamicCall("CommConnect()")

    def setUI(self):
        self.setupUi(self)

        # 키움 Open API Trigger
        self.kiwoom.OnReceiveTrData.connect(self.receive_trdata)
        self.kiwoom.OnEventConnect.connect(self.event_connect)

        # UI event Trigger
        self.searchItemButton.clicked.connect(self.searchItem)

        # Qt Trigger
        self.kiwoom.OnReceiveTrData.connect(self.get_stock_trdata)
        self.pushButton.clicked.connect(self.getDatas)
        #
        self.searchButton.clicked.connect(self.btn1_clicked)
        #
##
    def event_connect(self, nErrCode):
        if nErrCode == 0:
            self.label.setText("로그인 성공")
            self.get_login_info()
            self.getItemList()
            # ---
            self.getCodeListByMarket()
            self.listWidget.addItem(QListWidgetItem("로그인 성공"))
            # ---

        elif nErrCode == 100:

            print("사용자 정보 교환 실패")
        elif nErrCode == 101:
            print("서버 접속 실패")
        elif nErrCode == 102:
            print("버전 처리 실패")


    def get_login_info(self):
        accCnt = self.kiwoom.dynamicCall("GetLoginInfo(QString)", "ACCOUNT_CNT")
        accList = self.kiwoom.dynamicCall("GetLoginInfo(QString)", "ACCLIST")
        userId = self.kiwoom.dynamicCall("GetLoginInfo(QString)", "USER_ID")
        userName = self.kiwoom.dynamicCall("GetLoginInfo(QString)", "USER_NAME")
        keyBSEC = self.kiwoom.dynamicCall("GetLoginInfo(QString)", "KEY_BSECGB")
        firew = self.kiwoom.dynamicCall("GetLoginInfo(QString)", "FIREW_SECGB")
        serverGubun = self.kiwoom.dynamicCall("GetLoginInfo(QString)", "GetServerGubun")

        self.myModel.myLoginInfo = dm.DataModel.LoginInfo(accCnt, accList, userId, userName, keyBSEC, firew, serverGubun)

        self.statusbar.showMessage(self.myModel.myLoginInfo.getServerGubun())

        print("나의 이름: " + str(self.myModel.myLoginInfo.userName))
        print("나의 ID: " + str(self.myModel.myLoginInfo.userId))
        print("나의 계좌: " + str(self.myModel.myLoginInfo.accList.rstrip(';')))

        ### Test Python Dictionary
        # appid = { 'id' : userId }
        # jsonString = json.dumps(appid)
        # print(jsonString)
        # print(type(jsonString))

        ### 인자 전달 --------------------------------------------------------------
        # # Api id 변경
        # url = "http://127.0.0.1:8080/member/changeAppId"
        # payload = {'appid' : userId}
        # r = requests.put(url, params=payload)
        # print(r.status_code)
        # print(r.text)
        #
        # print('status code: ', r.status_code, "// 200은 정상, 400 Data 누락")
        # print('encoding: ', r.encoding)
        #
        # Api id 조회
        url = "http://localhost:8000/member/find/"
        payload = userId
        r = requests.get(url, params=payload)
        print(r.status_code)
        print(r.text)
        #
        # print('status code: ', r.status_code, "// 200은 정상, 400 Data 누락")
        # print('encoding: ', r.encoding)
        ####################################################################
        ##Create a dictionary to be sent.
        # json_data = { 'id' : userId }
        # ## Send the data.
        # response = requests.get(url='http://127.0.0.1:8000/member/find/', json=json_data)
        # print("Server responded with %s" % response.status_code)

        #
        # # Api id 중복 검색
        # url = "http://127.0.0.1:8080/check/"
        # payload = {userId}
        # r = requests.get(url, params=payload)
        # print(r.status_code)
        # print(r.text)
        #
        # print('status code: ', r.status_code, "// 200은 정상, 400 Data 누락")
        # print('encoding: ', r.encoding)

        ###----------------------------------------------------------------------------

        # # GET
        # res = requests.get('http://127.0.0.1:8080/member/changeAppId')
        # print(str(res.status_code) + " | " + res.text)
        #
        # # POST (JSON)
        # headers = {'Content-Type': 'application/json; chearset=utf-8'}
        # payload = {'UserId': 'userId'}
        # res = requests.post('http://localhost:8080/member/changeAppId', payload=json.dumps(payload), headers=headers)
        # print(str(res.status_code) + " | " + res.text)

    ### 종목리스트 가져와서 저장
    def getCodeListByMarket(self):
        codeList = self.kiwoom.dynamicCall("GetCodeListByMarket(QString)", "0").split(";")
        codeList.pop()

        for code in codeList:
            itemName = self.kiwoom.dynamicCall("GetMasterCodeName(QString)", code)
            self.dicStock[code] = itemName
        print(self.dicStock)

    # 주식일봉차트 조회를 위한 관리
    def getDatas(self):
        scrNo = 0  # 키움 OpenAPI의 경우에 200개의 스크린 번호를 사용할수 있고, 해당 스크린 번호가 겹치면 이상한 데이터가 섞여서 올수 있음
        checkPoint = -1  # 전에 수집한 데이터 수집은 건너뛰고 데이터 수집을 하기 위해 변수 사용
        startStock = self.textEdit.toPlainText()  # 데이터 수집을 시작할 종목이름

        for key in self.dicStock.keys():
            if self.dicStock[key] == startStock:
                checkPoint = 0

                scrNo += 1
                scrNo = scrNo % 199
                print(key, "수집 시작")
                for i in range(20):
                    self.getData(key, scrNo)
                    time.sleep(0.4)  # 데이터 수집후 0.4초만큼 딜레이를 줌, 키움 Open API의 경우 1초당 5회 요청할수 있다고 하는데 실제로 제약사항이 더 있음
                    if self.repeatNum == -1:  # 데이터의 마지막까지 불렀다면 그만 요청함
                        break
                self.saveData(self.dicStock[key])  # 데이터 수집후 저장 (은근 딜레이 먹음)
                time.sleep(0.8)  # 딜레이 또 주는 중, 그래도 실질적인 제약사항 충족이 안됨

    # 주식일봉차트 조회 요청
    def getData(self, code, scrNo):
        if self.repeatNum != -1:
            now = datetime.datetime.now()
            nowdate = now.strftime('%Y%m%d')  # 오늘 날짜를 기준으로 데이터를 받아옴

            self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "종목코드", str(code))
            self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "조회일자", nowdate)
            self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "표시구분", "0")

            # repeatNum는 반복번호인데 처음에는 0, 반복해서 다음 데이터를 불러올라면 trData수신시 prev_next번호를 주는데 그 값으로 다시 요청하면 됨
            self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", '주식일봉차트조회요청', "opt10081",
                                    self.repeatNum, str(scrNo + 6000))
        else:
            print("요청 안함", self.repeatNum)

    # 데이터 저장
    # 데이터가 중복되는 것이 있는데 수집할때 제대로 수집이 안되고 있긴함
    # 따라서 중복제거랑 정렬을 해줘야 하는데
    # 데이터 수집후 배치처리로 하는게 좋다고 판단
    # 따라서 여기서는 일단 데이터 저장

    def saveData(self, itemName):
        f = open('./Data/' + itemName + '.csv', 'w', encoding='utf-8', newline='')
        wr = csv.writer(f)
        for line in self.input_data:
            wr.writerow(line)
        f.close()

        print(itemName, " 저장")

        # self.input_data.clear()
        # self.repeatNum = 0
        #
        # json_object = {
        #     line
        # }
        # json_string = json.dumps(json_object)
        # print(json_string)

    # 데이터 수신 후 저장
    def receive_trdata(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):
        if trcode == "opt10081":
            if rqname == "주식일봉차트조회요청":
                count = int(self.kiwoom.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname))
                if count != 0:
                    for index in range(count):
                        m_date = self.kiwoom.dynamicCall("GetCommData(Qstring, QString, int, QString)", trcode,
                                                         rqname, index, "일자").strip(" ")
                        openPrice = int(
                            self.kiwoom.dynamicCall("GetCommData(Qstring, QString, int, QString)", trcode, rqname,
                                                    index, "시가"))
                        highPrice = int(
                            self.kiwoom.dynamicCall("GetCommData(Qstring, QString, int, QString)", trcode, rqname,
                                                    index, "고가"))
                        lowPrice = int(
                            self.kiwoom.dynamicCall("GetCommData(Qstring, QString, int, QString)", trcode, rqname,
                                                    index, "저가"))
                        currentPrice = int(
                            self.kiwoom.dynamicCall("GetCommData(Qstring, QString, int, QString)", trcode, rqname,
                                                    index, "현재가"))
                        volumn = int(
                            self.kiwoom.dynamicCall("GetCommData(Qstring, QString, int, QString)", trcode, rqname,
                                                    index, "거래량"))
                        tradingValue = int(
                            self.kiwoom.dynamicCall("GetCommData(Qstring, QString, int, QString)", trcode, rqname,
                                                    index, "거래대금"))

                        # data = {
                        #     # 'itemName' : itemName,
                        #     'date' : m_date,
                        #     'openPrice' : openPrice
                        # }
                        # json_data = json.dumps(data)
                        # print(json_data)

                        self.input_data.append(
                            (m_date, openPrice, highPrice, lowPrice, currentPrice, volumn, tradingValue))

                    if count < 600:
                        self.repeatNum = -1
                    else:
                        self.repeatNum = prev_next

    # def setItemList(self, itemName, m_date, openPrice):
    #
    #     data = {
    #         'itemName' : itemName,
    #         'date' : m_date,
    #         'openPrice' : openPrice
    #     }
    #     json_data = json.dumps(data)
    #     print(json_data)
    ###

#     종목 리스트 요청
    def getItemList(self):
        marketList = ["0", "10"]
        for market in marketList:
            codeList = self.kiwoom.dynamicCall("GetCodeListByMarket(QString)", market).split(";")
            for code in codeList:
                name = self.kiwoom.dynamicCall("GetMasterCodeName(QString)", code)
                item = dm.DataModel.ItemInfo(code, name)
                self.myModel.itemList.append(item)

            print(self.myModel.itemList[0].itemName)

    def searchItem(self):
        itemName = self.searchItemText.toPlainText()
        print("입력 종목 명: " + itemName)
        self.listWidget.addItem(QListWidgetItem("입력 종목 명: " + itemName))
        for item in self.myModel.itemList:
            if item.itemName == itemName:
                print("종목코드: " + item.itemCode)
                print("종목 명: " + item.itemName)
                self.listWidget.addItem(QListWidgetItem("종목코드: " + item.itemCode))
                self.listWidget.addItem(QListWidgetItem("종목 명: " + item.itemName))
                break
    #
    def btn1_clicked(self):
        stockCode = self.textEdit2.toPlainText()
        # self.text_edit.append("종목코드: " + code)
        self.listWidget.addItem(QListWidgetItem("입력 종목 명: " + stockCode))

        # SetInputValue
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "종목코드", str(stockCode))

        # CommRqData
        self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", "opt10001_req", "opt10001", 0, "0101")

    def get_stock_trdata(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):
        if trcode == "opt10001":
            if rqname == "opt10001_req":

                stockName = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode,
                                                    recordname, 0, "종목명")
                stockCode = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode,
                                                    recordname, 0, "종목코드")
                cTransactionVolume = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode,
                                                    recordname, 0, "거래량")
                openingPrice = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode,
                                                    recordname, 0, "시가")
                currentPrice = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode,
                                                    recordname, 0, "현재가").replace("-","")
                stockPer = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode,
                                                    recordname, 0, "PER")
                stockPbr = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode,
                                                    recordname, 0, "PBR")

                self.myModel.myStockTrdata = dm.DataModel.StockTrdata(stockName, stockCode, cTransactionVolume,
                                                                      openingPrice, currentPrice, stockPer, stockPbr)

                print("주식 종목명: " + str(self.myModel.myStockTrdata.stockName))
                print("주식 종목코드: " + str(self.myModel.myStockTrdata.stockCode))
                print("거래량: " + str(self.myModel.myStockTrdata.cTransactionVolume))
                print("시가: " + str(self.myModel.myStockTrdata.openingPrice))
                print("현재가: " + str(self.myModel.myStockTrdata.currentPrice))
                print("PER: " + str(self.myModel.myStockTrdata.stockPer))
                print("PBR: " + str(self.myModel.myStockTrdata.stockPbr))

                self.listWidget.addItem(QListWidgetItem("주식 종목명:" + stockName))
                self.listWidget.addItem(QListWidgetItem("주식 종목코드:" + stockCode))
                self.listWidget.addItem(QListWidgetItem("주식 거래량:" + cTransactionVolume))
                self.listWidget.addItem(QListWidgetItem("주식 시가:" + openingPrice))
                self.listWidget.addItem(QListWidgetItem("주식 현재가:" + currentPrice))
                self.listWidget.addItem(QListWidgetItem("주식 PER:" + stockPer))
                self.listWidget.addItem(QListWidgetItem("주식 PBR:" + stockPbr))

                url = "http://localhost:8000/wish/add"
                payload = {'stockCode' : stockName, 'stockName' : stockName, 'cTransactionVolume' : cTransactionVolume,
                           'openingPrice' : openingPrice, 'currentPrice' : currentPrice,
                           'stockPer' : stockPer, 'stockPbr' : stockPbr}
                r = requests.post(url, data=json.dumps(payload))
                print(r.status_code)
                print(r.text)




