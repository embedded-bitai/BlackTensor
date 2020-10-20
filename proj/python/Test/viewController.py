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

        self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", "OPTKWFID", "OPTKWFID_req", 0, "0101")

    def get_stock_trdata(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):
        if trcode == "opt10001":
            if rqname == "opt10001_req":

                stockCode = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode,
                                                    recordname, 0, "종목코드")
                stockName = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode,
                                                    recordname, 0, "종목명")
                closingMonth = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode,
                                                    recordname, 0, "결산월")
                parValue = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode,
                                                    recordname, 0, "액면가")
                capital = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode,
                                                             recordname, 0, "자본금")
                listedStock = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode,
                                                             recordname, 0, "상장주식")
                creditRatio = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode,
                                                             recordname, 0, "신용비율")
                bestYear = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode,
                                                             recordname, 0, "연중최고")
                lowstYear = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode,
                                                             recordname, 0, "연중최저")
                marketValue = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode,
                                                             recordname, 0, "시가총액")
                per = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode,
                                                             recordname, 0, "PER")
                eps = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode,
                                                             recordname, 0, "EPS")
                roe = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode,
                                                             recordname, 0, "ROE")
                pbr = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode,
                                                             recordname, 0, "PBR")
                bps = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode,
                                                             recordname, 0, "BPS")
                take = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode,
                                                    recordname, 0, "매출액")
                operatProfit = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode,
                                               recordname, 0, "영업이익")
                netIncome = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode,
                                               recordname, 0, "당기순이익")
                openPrice = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode,
                                                    recordname, 0, "시가")
                highPrice = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode,
                                                    recordname, 0, "고가")
                upperPrice = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode,
                                                    recordname, 0, "상한가")
                lowerPrice = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode,
                                                    recordname, 0, "하한가")
                standardPrice = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode,
                                                    recordname, 0, "기준가")
                exClosingPrice = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode,
                                                    recordname, 0, "예상체결가")
                exStockAmount = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode,
                                                         recordname, 0, "예상체결수량")
                currentPrice = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode,
                                               recordname, 0, "현재가")
                changeSymbol = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode,
                                                    recordname, 0, "대비기호")
                netChange = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode,
                                                    recordname, 0, "전일대비")
                fluctuation = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode,
                                               recordname, 0, "등락율")
                volume = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode,
                                                      recordname, 0, "거래량")
                tradePrepare = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString", trcode,
                                                      recordname, 0, "거래대비")

                # .replace("-", "").replace("+", "")

                #
                userId = self.kiwoom.dynamicCall("GetLoginInfo(QString)", "USER_ID")
                #

                self.myModel.myStockTrdata = dm.DataModel.StockTrdata(stockName, stockCode, closingMonth, parValue,
                  capital, listedStock, creditRatio, bestYear, lowstYear, marketValue, per, eps, roe, pbr, bps, take,
                  operatProfit, netIncome, openPrice, highPrice, upperPrice, lowerPrice, standardPrice, exClosingPrice,
                  exStockAmount, currentPrice, changeSymbol, netChange, fluctuation, volume, tradePrepare)

                print("주식 종목명: " + str(self.myModel.myStockTrdata.stockName))
                print("주식 종목코드: " + str(self.myModel.myStockTrdata.stockCode))
                print("결산월: " + str(self.myModel.myStockTrdata.closingMonth))
                print("액면가: " + str(self.myModel.myStockTrdata.parValue))
                print("자본금: " + str(self.myModel.myStockTrdata.capital))
                print("상장주식: " + str(self.myModel.myStockTrdata.listedStock))
                print("신용비율: " + str(self.myModel.myStockTrdata.creditRatio))
                print("연중최고: " + str(self.myModel.myStockTrdata.bestYear))
                print("연중최저: " + str(self.myModel.myStockTrdata.lowstYear))
                print("시가총액: " + str(self.myModel.myStockTrdata.marketValue))
                print("PER: " + str(self.myModel.myStockTrdata.per))
                print("EPS: " + str(self.myModel.myStockTrdata.eps))
                print("ROE: " + str(self.myModel.myStockTrdata.roe))
                print("PBR: " + str(self.myModel.myStockTrdata.pbr))
                print("BPS: " + str(self.myModel.myStockTrdata.bps))
                print("매출액: " + str(self.myModel.myStockTrdata.take))
                print("영업이익: " + str(self.myModel.myStockTrdata.operatProfit))
                print("당기순이익: " + str(self.myModel.myStockTrdata.netIncome))
                print("시가: " + str(self.myModel.myStockTrdata.openPrice))
                print("고가: " + str(self.myModel.myStockTrdata.highPrice))
                print("상한가: " + str(self.myModel.myStockTrdata.upperPrice))
                print("하한가: " + str(self.myModel.myStockTrdata.lowerPrice))
                print("기준가: " + str(self.myModel.myStockTrdata.standardPrice))
                print("예상체결가: " + str(self.myModel.myStockTrdata.exClosingPrice))
                print("예상체결수량: " + str(self.myModel.myStockTrdata.exStockAmount))
                print("현재가: " + str(self.myModel.myStockTrdata.currentPrice))
                print("대비기호: " + str(self.myModel.myStockTrdata.changeSymbol)) # 2 상승, 5 하락
                print("전일대비: " + str(self.myModel.myStockTrdata.netChange))
                print("등락율: " + str(self.myModel.myStockTrdata.fluctuation))
                print("거래량: " + str(self.myModel.myStockTrdata.volume))
                print("거래대비: " + str(self.myModel.myStockTrdata.tradePrepare))


                #
                print("나의 ID: " + userId)
                #
                #
                self.listWidget.addItem(QListWidgetItem("주식 종목명:" + stockName))
                self.listWidget.addItem(QListWidgetItem("주식 종목코드:" + stockCode))
                self.listWidget.addItem(QListWidgetItem("결산월:" + closingMonth))
                self.listWidget.addItem(QListWidgetItem("액면가:" + parValue))
                self.listWidget.addItem(QListWidgetItem("자본금:" + capital))
                self.listWidget.addItem(QListWidgetItem("상장주식:" + listedStock))
                self.listWidget.addItem(QListWidgetItem("신용비율:" + creditRatio))
                self.listWidget.addItem(QListWidgetItem("연중최고:" + bestYear))
                self.listWidget.addItem(QListWidgetItem("연중최저:" + lowstYear))
                self.listWidget.addItem(QListWidgetItem("시가총액:" + marketValue))
                self.listWidget.addItem(QListWidgetItem("PER:" + per))
                self.listWidget.addItem(QListWidgetItem("EPS:" + eps))
                self.listWidget.addItem(QListWidgetItem("ROE:" + roe))
                self.listWidget.addItem(QListWidgetItem("PBR:" + pbr))
                self.listWidget.addItem(QListWidgetItem("BPS:" + bps))
                self.listWidget.addItem(QListWidgetItem("매출액:" + take))
                self.listWidget.addItem(QListWidgetItem("영업이익:" + operatProfit))
                self.listWidget.addItem(QListWidgetItem("당기순이익:" + netIncome))
                self.listWidget.addItem(QListWidgetItem("시가:" + openPrice))
                self.listWidget.addItem(QListWidgetItem("고가:" + highPrice))
                self.listWidget.addItem(QListWidgetItem("상한가:" + upperPrice))
                self.listWidget.addItem(QListWidgetItem("하한가:" + lowerPrice))
                self.listWidget.addItem(QListWidgetItem("기준가:" + standardPrice))
                self.listWidget.addItem(QListWidgetItem("예상체결가:" + exClosingPrice))
                self.listWidget.addItem(QListWidgetItem("예상체결량:" + exStockAmount))
                self.listWidget.addItem(QListWidgetItem("현재가:" + currentPrice))
                self.listWidget.addItem(QListWidgetItem("대비기호:" + changeSymbol))
                self.listWidget.addItem(QListWidgetItem("전일대비:" + netChange))
                self.listWidget.addItem(QListWidgetItem("등락율:" + fluctuation))
                self.listWidget.addItem(QListWidgetItem("거래량:" + volume))
                self.listWidget.addItem(QListWidgetItem("거래대비:" + tradePrepare))
                #
                #

                url = "http://localhost:8000/wish/add"
                headers = {'Content-Type': 'application/json; charset=utf-8'}
                payload = {'stockCode' : stockCode, 'stockName' : stockName, 'member' : {'apiId' : userId},
                           'closingMonth' : closingMonth, 'parValue' : parValue, 'capital' : capital,
                           'listedStock' : listedStock, 'creditRatio' : creditRatio, 'bestYear' : bestYear,
                           'lowstYear' : lowstYear, 'marketValue' : marketValue, 'per' : per, 'eps' : eps, 'roe' : roe,
                           'pbr' : pbr, 'bps' : bps, 'take' : take, 'operatProfit' : operatProfit,
                           'netIncome' : netIncome, 'openPrice' : openPrice, 'highPrice' : highPrice,
                           'upperPrice' : upperPrice, 'lowerPrice' : lowerPrice, 'standardPrice' : standardPrice,
                           'exClosingPrice' : exClosingPrice, 'exStockAmount' : exStockAmount,
                           'currentPrice': currentPrice, 'netChange': netChange, 'fluctuation': fluctuation,
                           'volume' : volume, 'tradePrepare' : tradePrepare}
                # payload = {'stockCode' : stockCode, 'stockName' : stockName, 'member' : {'apiId' : userId}}
                data_tr = json.dumps(payload)
                res = requests.post(url, headers=headers, data=data_tr)
                print(res.status_code)
                print(res.text)

