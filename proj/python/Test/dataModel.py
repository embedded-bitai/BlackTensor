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
                  capital, listedStock, creditRatio, bestYear, lowstYear, marketValue, per, eps, roe, pbr, bps, take,
                  operatProfit, netIncome, openPrice, highPrice, upperPrice, lowerPrice, standardPrice, exClosingPrice,
                  exStockAmount, currentPrice, changeSymbol, netChange, fluctuation, volume, tradePrepare):
            self.stockName = stockName
            self.stockCode = stockCode
            self.closingMonth = closingMonth
            self.parValue = parValue
            self.currentPrice = currentPrice
            self.capital = capital
            self.listedStock = listedStock
            self.creditRatio = creditRatio
            self.bestYear = bestYear
            self.lowstYear = lowstYear
            self.marketValue = marketValue
            self.per = per
            self.eps = eps
            self.roe = roe
            self.pbr = pbr
            self.bps = bps
            self.take = take
            self.operatProfit = operatProfit
            self.netIncome = netIncome

            self.openPrice = openPrice
            self.highPrice = highPrice
            self.upperPrice = upperPrice
            self.lowerPrice = lowerPrice
            self.standardPrice = standardPrice
            self.exClosingPrice = exClosingPrice
            self.exStockAmount = exStockAmount
            self.currentPrice = currentPrice
            self.changeSymbol = changeSymbol
            self.netChange = netChange
            self.fluctuation = fluctuation
            self.volume = volume
            self.tradePrepare = tradePrepare

