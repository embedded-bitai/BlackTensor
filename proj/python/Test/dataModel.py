class DataModel:
    def __init__(self):
        print("Data Model")
        self.myLoginInfo = None
        self.itemList = []

    class LoginInfo:
        def __init__(self, accCnt, accList, userId, userName, keyBSEC, firew, serverGubun):
           self.accCnt = accCnt
           self.accList = accList
           self.userId = userId
           self.userName = userName
           self.keyBSEC = keyBSEC
           self.firew = firew
           self.serverGubun = serverGubun

        def getServerGubun(self):
            if self.serverGubun == "1":
                return "모의 투자"
            else:
                return "실 서버"

    class ItemInfo:
        def __init__(self, itemCode, itemName):
            self.itemCode = itemCode
            self.itemName = itemName

           # print("userName: " + str(userName))
##

    class StockTrdata:
        def __init__(self, stockName, stockCode, cTransactionVolume, openingPrice, currentPrice, stockPer, stockPbr):
            self.stockName = stockName
            self.stockCode = stockCode
            self.cTransactionVolume = cTransactionVolume
            self.openingPrice = openingPrice
            self.currentPrice = currentPrice
            self.stockPer = stockPer
            self.stockPbr = stockPbr
