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
        def __init__(self, stockName, stockCode, closingMonth, parValue,
                  capital, ListedStock, creditRatio, bestYear, lowstYear, marketValue, PER, EPS, ROE, PBR, BPS, take,
                  operatProfit, netIncome, currentPrice, netChange, fluctuation, volume, TradePrepare):
            self.stockName = stockName
            self.stockCode = stockCode
            self.closingMonth = closingMonth
            self.parValue = parValue
            self.currentPrice = currentPrice
            self.capital = capital
            self.ListedStock = ListedStock
            self.creditRatio = creditRatio
            self.bestYear = bestYear
            self.lowstYear = lowstYear
            self.marketValue = marketValue
            self.PER = PER
            self.EPS = EPS
            self.ROE = ROE
            self.PBR = PBR
            self.BPS = BPS
            self.take = take
            self.operatProfit = operatProfit
            self.netIncome = netIncome
            self.currentPrice = currentPrice
            self.netChange = netChange
            self.fluctuation = fluctuation
            self.volume = volume
            self.TradePrepare = TradePrepare

