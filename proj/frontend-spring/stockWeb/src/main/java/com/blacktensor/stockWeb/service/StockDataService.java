package com.blacktensor.stockWeb.service;

import com.blacktensor.stockWeb.entity.enterpriseData.StockAllData;
import com.blacktensor.stockWeb.entity.enterpriseData.StockData;
import com.blacktensor.stockWeb.entity.enterpriseData.StockInfo;

import java.util.List;

public interface StockDataService {
    public void insertStockData(StockData data);
    public void insertStockInfo(StockInfo data);
    public List<StockData> getStockDatas(String stockCode);
    public List<StockInfo> getStockInfos(String stockCode);
    public StockAllData getStockAllData(String stockCode);
}
