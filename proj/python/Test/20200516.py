# import sys
# from PyQt5.QtWidgets import *
# from PyQt5.QAxContainer import *
# from PyQt5.QtCore import *
#
#
# class Mainwindow(QMainWindow):
#
# ##### 메인화면 영역
# ##########################################################################
#     def __init__(self, parent=None):
#         super(Mainwindow,self).__init__(parent)
#
#         self.kiwoom()
#
#         ##### 위젯 창 연결
#         self.mywidget = MyWindow(self)
#         self.setCentralWidget(self.mywidget)
#
#         ##### 메인창 이름설정 및 크기설정
#         self.setWindowTitle("auto-trader")
#         self.setGeometry(300,300,1000,600)
#
#         ##### 메인창을 중앙에 위치 == 아래에 함수로 정의 되어있음
#         self.center()
#
#         ##### 상태표시줄 생성
#         self.statusbar = QStatusBar(self)
#         self.setStatusBar(self.statusbar)
#
#         ##### 타이머 설정 1 - 상태표시줄 현재시간
#         self.timer = QTimer(self)
#         self.timer.start(1000)
#         self.timer.timeout.connect(self.timeout)
#
#         ##### 타이머 설정 2 - 실시간 조회
#         self.timer2 = QTimer(self)
#         self.timer2.start(1000*10)
#         self.timer2.timeout.connect(self.timeout2)
#
#         ##### 종목명 또는 종목코드로 검색
#         self.mywidget.name_edit_1.returnPressed.connect(self.total_changed)  # textChanged 텍스트 변경옵션
#
#         ##### 종목명으로 종목코드검색
#         #self.mywidget.name_edit_1.textChanged.connect(self.name_changed)
#
#         ##### 종목코드로 종목검색
#         #self.mywidget.name_edit_1.textChanged.connect(self.code_changed)
#
#         ##### 현금주문 실행
#         self.mywidget.active_buy.clicked.connect(self.send_order)
#
#     ##### 기본창 화면 중앙으로 배치시키는 함수
#     def center(self):
#         qr = self.frameGeometry()
#         cp = QDesktopWidget().availableGeometry().center()
#         qr.moveCenter(cp)
#         self.move(qr.topLeft())
#
#     ##### 종료이벤트 발생시 메세지박스로 종료 확인 함수
#     def closeEvent(self, QCloseEvent):
#         re = QMessageBox.question(self, "종료 확인", "종료 하시겠습니까?",
#                     QMessageBox.Yes|QMessageBox.No)
#
#         if re == QMessageBox.Yes:
#             QCloseEvent.accept()
#         else:
#             QCloseEvent.ignore()
#
#     ##### 상태표시줄에 들어갈 현재시간
#     def timeout(self):
#         current_time = QTime.currentTime()
#         text_time = current_time.toString("hh:mm:ss")
#         time_msg = "현재시간 : " + text_time
#
#         self.statusbar.showMessage("서버 연결 중 | " + time_msg)
#
#     ##### 잔고 및 보유종목현황 실시간 조회
#     def timeout2(self):
#         self.kiwoom.OnEventConnect.connect(self.detail_account_info1)     #예수금 정보 요청
#         self.kiwoom.OnEventConnect.connect(self.detail_account_info2)     #잔고정보 요청
#         self.kiwoom.OnReceiveTrData.connect(self.trdata_slot)             #예수금 및잔고 정보 수신
#         self.mywidget.text_edit.append("잔고현황 업데이트")
# ##########################################################################
#
# ##### openAPI구동 영역
# ##########################################################################
#     def kiwoom(self):
#         ##### 로그인 영역
#         self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
#         self.kiwoom.dynamicCall("CommConnect()")
#         self.stocks
#         ##### 이벤트실행 실행
#         self.kiwoom.OnEventConnect.connect(self.event_connect)            #로그인
#         self.kiwoom.OnEventConnect.connect(self.account)                  #계좌정보
#         self.kiwoom.OnEventConnect.connect(self.stocks)                   #종목코드
#         self.kiwoom.OnEventConnect.connect(self.detail_account_info1)     #예수금 정보 요청
#         self.kiwoom.OnEventConnect.connect(self.detail_account_info2)     #잔고정보 요청
#         self.kiwoom.OnReceiveTrData.connect(self.trdata_slot)             #예수금 및잔고 정보 수신
#
#     ##### CommConnect()호출 후 반환값이 리턴 되면 UI에 text_edit 표출
#     def event_connect(self, err_code):
#         if err_code == 0:
#             self.mywidget.text_edit.append("로그인 성공")
#         else:
#             self.mywidget.text_edit.append("로그인 실패")
#
#     ##### 계좌정보 가저오는 함수
#     def account(self):
#         num = int(self.kiwoom.dynamicCall("GetLoginInfo(QString)", ["ACCOUNT_CNT"]))
#         account_list = self.kiwoom.dynamicCall("GetLoginInfo(QString)", ["ACCNO"])
#         #self.mywidget.text_edit.append("계좌번호: " + account_list.rstrip(';'))
#         self.mywidget.account_combo.addItems(account_list.split(';')[0:num])
#         #self.account_num = account_list.split(';')[0]
#
#     ##### 예수금 정보 요청 함수
#     def detail_account_info1(self, sPrevNext="0"):
#         account_num = self.mywidget.account_combo.currentText()
#         self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "계좌번호", account_num)
#         self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "비밀번호", "0000")
#         self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "비밀번호입력매체구분", "00")
#         self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "조회구분", "1")
#         self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", "예수금상세현황요청", "opw00001", sPrevNext, "0362")
#
#     ##### 계좌평가잔고 정보 요청 함수
#     def detail_account_info2(self, sPrevNext="0"):
#         account_num = self.mywidget.account_combo.currentText()
#         self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "계좌번호", account_num)
#         self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "비밀번호", "0000")
#         self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "비밀번호입력매체구분", "00")
#         self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "조회구분", "1")
#         self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", "계좌평가잔고내역요청", "opw00018", sPrevNext, "0362")
#
#         ### 루프 생성
#         self.detail_account_info_event_loop = QEventLoop()
#         self.detail_account_info_event_loop.exec_()
#
#     ##### 계좌 정보 수신 함수
#     def trdata_slot(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):
#         ##### 예수금 및 출금가능금액
#         if sRQName == "예수금상세현황요청":
#             ##### 예수금 데이터 반환
#             deposit = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "예수금")
#
#             ##### 출금가능 데이터 반환
#             output_deposit = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "출금가능금액")
#
#             ##### 예수금에 필요없는 숫자 삭제하고 원화 표출양식으로 변환
#             deposit = self.change_format(deposit)
#             output_deposit = self.change_format(output_deposit)
#
#             ##### 결과값 표출
#             deposit = QTableWidgetItem(deposit)
#             deposit.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
#             self.mywidget.tableWidget_balance.setItem(0,0,deposit)
#
#             output_deposit = QTableWidgetItem(output_deposit)
#             output_deposit.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
#             self.mywidget.tableWidget_balance.setItem(0,1,output_deposit)
#
#         ##### 매입금액 등 현황 수신
#         elif sRQName == "계좌평가잔고내역요청":
#             ##### 잔고현황 반환
#             total_purchsase = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "총매입금액")
#             total_eval_price = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "총평가금액")
#             total_eval_profit_loss = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "총평가손익금액")
#             total_earning_rate = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "총수익률(%)")
#             estimated_deposit = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "추정예탁자산")
#
#             ##### 잔고현황 결과값 숫자형태 변환
#             total_purchsase = self.change_format(total_purchsase)
#             total_eval_price = self.change_format(total_eval_price)
#             total_eval_profit_loss = self.change_format(total_eval_profit_loss)
#             total_earning_rate = self.change_format(total_earning_rate)
#             estimated_deposit = self.change_format(estimated_deposit)
#
#             ##### 테이블위젯에 결과값 넣기
#             total_purchsase = QTableWidgetItem(total_purchsase)
#             total_purchsase.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
#             self.mywidget.tableWidget_balance.setItem(0,2,total_purchsase)
#
#             total_eval_price = QTableWidgetItem(total_eval_price)
#             total_eval_price.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
#             self.mywidget.tableWidget_balance.setItem(0,3,total_eval_price)
#
#             total_eval_profit_loss = QTableWidgetItem(total_eval_profit_loss)
#             total_eval_profit_loss.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
#             self.mywidget.tableWidget_balance.setItem(0,4,total_eval_profit_loss)
#
#             total_earning_rate = QTableWidgetItem(total_earning_rate)
#             total_earning_rate.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
#             self.mywidget.tableWidget_balance.setItem(0,5,total_earning_rate)
#
#             estimated_deposit = QTableWidgetItem(estimated_deposit)
#             estimated_deposit.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
#             self.mywidget.tableWidget_balance.setItem(0,6,estimated_deposit)
#             ###############################################################
#
#             ##### 종목현황 반환
#             rows = self.kiwoom.dynamicCall("GetRepeatCnt(QString, QString)", sTrCode, sRQName)
#
#             item_output = []
#             ##### 종목현황 반환된 값에서 원하는 값 추출
#             for i in range(rows):
#                 name = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "종목명")
#                 name = name.strip()
#
#                 quantity = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "보유수량")
#                 purchase_price = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "매입가")
#                 current_price = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "현재가")
#                 eval_profit_loss = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "평가손익")
#                 eraning_rate = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "수익률(%)")
#
#                 ##### 결과값 숫자형태 변환
#                 quantity = self.change_format(quantity)
#                 purchase_price = self.change_format(purchase_price)
#                 current_price = self.change_format(current_price)
#                 eval_profit_loss = self.change_format(eval_profit_loss)
#                 eraning_rate = self.change_format2(eraning_rate)
#
#                 ##### 리스트에 저장
#                 item_output.append([name,quantity,purchase_price,current_price,eval_profit_loss,eraning_rate])
#
#             ##### item의 갯수세고 띄워줄 테이블에 로우를 만듬
#             item_count = len(item_output)
#             self.mywidget.tableWidget_item.setRowCount(item_count)
#
#             ##### 종목을 UI에 띄우기
#             for j in range(item_count):
#                 item_output[j]
#                 for i,k in enumerate(item_output[j]):
#                     item = QTableWidgetItem(k)
#                     if i == 0:
#                         item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
#                         self.mywidget.tableWidget_item.setItem(j,i,item)
#                     else:
#                         item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
#                         self.mywidget.tableWidget_item.setItem(j,i,item)
#             ###############################################################
#
#             ##### 로그현황에 결과 띄우기
#             self.mywidget.text_edit.append("잔고현황 실시간조회 실행")
#
#             ##### 슬롯연결 끊기
#             self.stop_screen_cancel("0362")
#
#             ##### 루프 종료
#             self.detail_account_info_event_loop.exit()
#
#     ##### 슬롯연결 끊기 함수
#     def stop_screen_cancel(self, sScrNo=None):
#         self.kiwoom.dynamicCall("DisconnectRealData(QString)", sScrNo) # 스크린 번호 연결 끊기
#
#     ##### 숫자 표출형식 변환 1
#     def change_format(self, data):
#         strip_data = data.lstrip('-0')
#         if strip_data == '' or strip_data == '.00':
#             strip_data = '0'
#         try:
#             format_data = format(int(strip_data), ',d')
#         except:
#             format_data = format(float(strip_data))
#         if data.startswith('-'):
#             format_data = '-' + format_data
#
#         return format_data
#
#     ##### 수익률 표출형식 변환 2
#     def change_format2(self, data):
#         strip_data = data.lstrip('-0')
#
#         if strip_data == '':
#             strip_data = '0'
#
#         if strip_data.startswith('.'):
#             strip_data = '0' + strip_data
#
#         if data.startswith('-'):
#             strip_data = '-' + strip_data
#
#         return strip_data
#
#     ##### 종목코드 가저오는 함수
#     def stocks(self,input_name):
#         ret = self.kiwoom.dynamicCall("GetCodeListByMarket(QString)", ["0"])
#         kospi_code_list = ret.split(';')
#         kospi_code_name_list = []
#
#         for x in kospi_code_list:
#             name = self.kiwoom.dynamicCall("GetMasterCodeName(QString)", [x])
#             kospi_code_name_list.append(x + " : " + name)
#
#     ##### 종목 UI에 종목명 입력시 종목코드 출력실행 함수
#     def total_changed(self):
#         input_text = self.mywidget.name_edit_1.text()
#         if input_text.isdigit() == True:
#             code = self.mywidget.name_edit_1.text()
#             name = self.get_master_code(code)
#             self.mywidget.name_edit_2.setText(name)
#         else:
#             name = self.mywidget.name_edit_1.text()
#             code = self.get_master_name(name)
#             self.mywidget.name_edit_2.setText(code)
#
#     ##### 종목 UI에 종목명 입력시 종목코드 출력실행 함수
#     def name_changed(self):
#         name = self.mywidget.name_edit_1.text()
#         code = self.get_master_name(name)
#         self.mywidget.name_edit_2.setText(code)
#
#     ##### 종목 UI에 코드 입력시 종목명 출력실행 함수
#     def code_changed(self):
#         code = self.mywidget.name_edit_1.text()
#         name = self.get_master_code(code)
#         self.mywidget.name_edit_2.setText(name)
#
#
#     ##### 하나의 종목명 입력시 종목코드 출력
#     def get_master_name(self,input_name):
#         ret = self.kiwoom.dynamicCall("GetCodeListByMarket(QString)", ["0"])
#         kospi_code_list = ret.split(';')
#
#         kospi_code_name_lists = []
#         for x in kospi_code_list:
#             name = self.kiwoom.dynamicCall("GetMasterCodeName(QString)", [x])
#             kospi_code_name_lists.append(["{}".format(name),"{}".format(x)])
#
#         kospi_code_name_lists = dict(kospi_code_name_lists)
#
#         try:
#             code = kospi_code_name_lists["{}".format(input_name)]
#         except KeyError:
#             code = ""
#         return code
#
#     ##### 종목명 출력
#     def get_master_code(self, input_code):
#         name = self.kiwoom.dynamicCall("GetMasterCodeName(QString)", input_code)
#         return name
#
#     ##### 수동주문
#     def send_order(self):
#         order_type_lookup = {"신규매수":1 , "신규매도":2, "매수취소":3, "매도취소":4}
#         hoga_lookup = {"시장가":"03","지정가":"00"}
#
#         account = self.mywidget.account_combo.currentText()           ### UI에서 현재 선택되어있는 계좌정보를 받아옴
#         order_type = self.mywidget.order_combo.currentText()          ### UI에서 현재 선택되어있는 주문형태정보를 받아옴
#         code = self.mywidget.name_edit_2.text()                       ### UI에서 현재 선택되어있는 주문하고자 하는 종목의 코드를 받아옴
#         hoga = self.mywidget.type_spin.currentText()                  ### UI에서 현재 선택되어있는 시장가,지정가 선택
#         num = self.mywidget.num_spin.value()                          ### UI에서 현재 선택되어있는 수량정보를 받아옴
#         price = self.mywidget.price_spin.value()                      ### UI에서 현재 선택되어있는 지정가일 경우 가격정보를 받아옴
#
#         self.kiwoom.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
#                          ["send_order_req", "0101", account, order_type_lookup[order_type], code, num, price, hoga_lookup[hoga], ""])
# ##########################################################################
#
# class MyWindow(QWidget):
#     def __init__(self, parent):
#         super(MyWindow,self).__init__(parent)
#
#         self.initUI()
#
# ##### UI 영역
# ##########################################################################
#     def initUI(self):
#         ##### 수동매수 영역
#         #####################################################################
#
#         ##### 계좌번호 선택 라벨
#         self.account_label = QLabel("계좌")
#         self.account_label.setMaximumWidth(40)
#         self.account_label.setMinimumWidth(40)
#         ##### 계좌번호 선택 콤보
#         self.account_combo = QComboBox(self)
#         self.account_combo.setMaximumWidth(160)
#         self.account_combo.setMinimumWidth(160)
#
#         ##### 주문방식 선택 라벨
#         self.order_label = QLabel("주문")
#         self.order_label.setMaximumWidth(40)
#         self.order_label.setMinimumWidth(40)
#         ##### 계좌번호 선택 콤보
#         self.order_combo = QComboBox(self)
#         self.order_combo.setMaximumWidth(160)
#         self.order_combo.setMinimumWidth(160)
#         self.order_combo.addItem("신규매수")
#         self.order_combo.addItem("신규매도")
#         self.order_combo.addItem("매수취소")
#         self.order_combo.addItem("매도취소")
#
#         ##### 종목선택 라벨1
#         self.name_labe_1 = QLabel("종목")
#         self.name_labe_1.setMaximumWidth(40)
#         self.name_labe_1.setMinimumWidth(40)
#         ##### 종목선택 에디트1
#         self.name_edit_1 = QLineEdit(self)
#         self.name_edit_1.setMaximumWidth(160)
#         self.name_edit_1.setMinimumWidth(160)
#
#         ##### 종목선택 라벨2
#         self.name_labe_2 = QLabel("")
#         self.name_labe_2.setMaximumWidth(40)
#         self.name_labe_2.setMinimumWidth(40)
#         ##### 종목선택 에디트2
#         self.name_edit_2 = QLineEdit(self)
#         self.name_edit_2.setEnabled(False)
#         self.name_edit_2.setMaximumWidth(160)
#         self.name_edit_2.setMinimumWidth(160)
#
#         ##### 종류 선택 라벨
#         self.type_label = QLabel("종류")
#         self.type_label.setMaximumWidth(40)
#         self.type_label.setMinimumWidth(40)
#         ##### 종류 선택 콤보
#         self.type_spin = QComboBox(self)
#         self.type_spin.setMaximumWidth(160)
#         self.type_spin.setMinimumWidth(160)
#         self.type_spin.addItem("시장가")
#         self.type_spin.addItem("지정가")
#
#         ##### 수량 선택 라벨
#         self.num_label = QLabel("수량")
#         self.num_label.setMaximumWidth(40)
#         self.num_label.setMinimumWidth(40)
#         ##### 수량 선택 스핀
#         self.num_spin = QSpinBox(self)
#         self.num_spin.setMaximumWidth(160)
#         self.num_spin.setMinimumWidth(160)
#
#         ##### 가격 선택 라벨
#         self.price_label = QLabel("가격")
#         self.price_label.setMaximumWidth(40)
#         self.price_label.setMinimumWidth(40)
#         ##### 가격 선택 스핀
#         self.price_spin = QSpinBox(self)
#         self.price_spin.setMaximumWidth(160)
#         self.price_spin.setMinimumWidth(160)
#
#         ##### 현금매수 클릭 푸쉬
#         self.active_buy = QPushButton("현금매수",self)
#         self.active_buy.setMaximumWidth(230)
#         self.active_buy.setMinimumWidth(230)
#         #####################################################################
#
#         ##### 종목코드를 표출할 위젯 생성
#         #self.listWidget = QListWidget(self)
#
#         ##### openAPI에서 발생하는 이벤트를 표출할 영역 생성
#         self.text_edit = QTextEdit(self)
#         self.text_edit.setEnabled(False)
#         self.text_edit.setFixedHeight(100)
#
#         ##### 잔고표출 영역생성
#         #####################################################################
#         self.tableWidget_balance = QTableWidget(self)
#         balance = ['예수금(d+2)','출금가능금액', '총매입금', '총평가', '총손익', '총수익률', '추정예탁자산']
#         self.tableWidget_balance.setRowCount(1)                            # 행의 갯수
#         self.tableWidget_balance.setColumnCount(len(balance))              # 컬럼의 갯수
#         self.tableWidget_balance.setHorizontalHeaderLabels(balance)        # 컬럼명 설정
#         #self.tableWidget_balance.resizeColumnsToContents()                # 컬럼 사이즈를 내용에 맞추어설정
#         self.tableWidget_balance.resizeRowsToContents()                    # 행의 사이즈를 내용에 맞추어설정
#         self.tableWidget_balance.setFixedHeight(100)                       # 위젯크기 고정
#         self.tableWidget_balance.setColumnWidth(0,100)                     # 0에 위치한것 크기조정(원하는사이즈로 수정가능)
#         self.tableWidget_balance.setColumnWidth(1,100)
#         self.tableWidget_balance.setColumnWidth(2,100)
#         self.tableWidget_balance.setColumnWidth(3,100)
#         self.tableWidget_balance.setColumnWidth(4,100)
#         self.tableWidget_balance.setColumnWidth(5,100)
#         self.tableWidget_balance.setColumnWidth(6,100)
#
#         ##### 보유종목현황 영역생성
#         self.tableWidget_item = QTableWidget(self)
#         item = ['종목명', '보유량', '매입가', '현재가', '평가손익','수익률']
#         #self.tableWidget_item.setRowCount(100)
#         self.tableWidget_item.setColumnCount(len(item))
#         self.tableWidget_item.setHorizontalHeaderLabels(item)
#         #self.tableWidget_item.resizeColumnsToContents()
#         self.tableWidget_item.resizeRowsToContents()
#
#         ##### 주문대기현황(선정종목 리스트)
#         self.tableWidget_buy_lists = QTableWidget(self)
#         buy_lists = ['주문유형', '종목명', '호가구분', '수량', '가격','상태']
#         self.tableWidget_buy_lists.setColumnCount(len(buy_lists))
#         self.tableWidget_buy_lists.setHorizontalHeaderLabels(buy_lists)
#         self.tableWidget_buy_lists.resizeRowsToContents()
#         # 행갯수는 나중에 주문형태가 구성되면 지정
#         #####################################################################
#
#         ##### layout 영역
#         #####################################################################
#         groupbox1_1 = QGroupBox('수동주문')
#         sub_groupbox1_1 = QVBoxLayout()
#         condition1_1 = QHBoxLayout()
#         condition1_1.addWidget(self.account_label)
#         condition1_1.addWidget(self.account_combo)
#         condition1_2 = QHBoxLayout()
#         condition1_2.addWidget(self.order_label)
#         condition1_2.addWidget(self.order_combo)
#         condition1_3 = QHBoxLayout()
#         condition1_3.addWidget(self.name_labe_1)
#         condition1_3.addWidget(self.name_edit_1)
#         condition1_4 = QHBoxLayout()
#         condition1_4.addWidget(self.name_labe_2)  # QHBoxLayout() or QVBoxLayout()안에 기능을 넣을때는addWidget()
#         condition1_4.addWidget(self.name_edit_2)
#         condition1_5 = QHBoxLayout()
#         condition1_5.addWidget(self.type_label)
#         condition1_5.addWidget(self.type_spin)
#         condition1_6 = QHBoxLayout()
#         condition1_6.addWidget(self.num_label)
#         condition1_6.addWidget(self.num_spin)
#         condition1_7 = QHBoxLayout()
#         condition1_7.addWidget(self.price_label)
#         condition1_7.addWidget(self.price_spin)
#         condition1_8 = QHBoxLayout()
#         condition1_8.addWidget(self.active_buy)
#         sub_groupbox1_1.addLayout(condition1_1)   # QHBoxLayout() or QVBoxLayout() 끼리는 addLayout 사용
#         sub_groupbox1_1.addLayout(condition1_2)
#         sub_groupbox1_1.addLayout(condition1_3)
#         sub_groupbox1_1.addLayout(condition1_4)
#         sub_groupbox1_1.addLayout(condition1_5)
#         sub_groupbox1_1.addLayout(condition1_6)
#         sub_groupbox1_1.addLayout(condition1_7)
#         sub_groupbox1_1.addLayout(condition1_8)
#         groupbox1_1.setLayout(sub_groupbox1_1)    # QGroupBox()에는 setLayout() 사용
#         groupbox1_1.setFixedHeight(350)
#
#         groupbox1_2 = QGroupBox('로그현황')
#         condition1_2 = QVBoxLayout()
#         condition1_2.addWidget(self.text_edit)
#         groupbox1_2.setLayout(condition1_2)
#         groupbox1_2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
#
#         groupbox1 = QVBoxLayout()
#         groupbox1.addWidget(groupbox1_1)
#         groupbox1.addWidget(groupbox1_2)
#
#         groupbox2 = QGroupBox('잔고 및 보유종목현황')
#         condition2 = QVBoxLayout()
#         condition2.addWidget(self.tableWidget_balance)
#         condition2.addWidget(self.tableWidget_item)
#         groupbox2.setLayout(condition2)
#
#         groupbox3 = QGroupBox('주문대기현황(선정종목 리스트)')
#         condition3 = QVBoxLayout()
#         condition3.addWidget(self.tableWidget_buy_lists)
#         groupbox3.setLayout(condition3)
#
#         sub_layout1 = QVBoxLayout()
#         sub_layout1.addLayout(groupbox1)
#         sub_layout1.addStretch(1)
#
#         sub_layout2 = QVBoxLayout()
#         sub_layout2.addWidget(groupbox2)
#         sub_layout2.addWidget(groupbox3)
#
#         main_layout = QHBoxLayout()
#         main_layout.addLayout(sub_layout1)
#         main_layout.addLayout(sub_layout2)
#         main_layout.setStretchFactor(sub_layout1, 0)
#         main_layout.setStretchFactor(sub_layout2, 1)
#
#         self.setLayout(main_layout)
#
#
# ##########################################################################
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     mywindow = Mainwindow()
#     mywindow.show()
#     app.exec_()
