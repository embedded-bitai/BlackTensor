package com.blacktensor.stockWeb.serviceImpl;

import com.blacktensor.stockWeb.entity.enterpriseData.StockAllData;
import com.blacktensor.stockWeb.entity.enterpriseData.StockData;
import com.blacktensor.stockWeb.entity.enterpriseData.StockInfo;
import com.blacktensor.stockWeb.repository.StockDataRepository;
import com.blacktensor.stockWeb.service.StockDataService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class StockDataServiceImpl implements StockDataService {

    @Autowired
    private StockDataRepository repo;

    @Override
    public void insertStockData(StockData data) {
        String tableName = "stock_" + data.getStockCode();
        if(!repo.isExistTable(tableName)){
            repo.createStockTable(tableName);
        }

        repo.insertStockData(tableName, data);
    }

    @Override
    public void insertStockInfo(StockInfo data) {
        String tableName = "info_" + data.getStockCode();
        if(!repo.isExistTable(tableName)){
            repo.createInfoTable(tableName);
        }

        repo.insertInfoData(tableName, data);
    }

    @Override
    public List<StockData> getStockDatas(String stockCode) {
        String tableName = "stock_" + stockCode;
        if(repo.isExistTable(tableName)){
            return repo.getStockDatas(tableName);
        }else{
            return null;
        }
    }

    @Override
    public List<StockInfo> getStockInfos(String stockCode) {
        String tableName = "info_" + stockCode;
        if(repo.isExistTable(tableName)){
            return repo.getStockInfos(tableName);
        }else{
            return null;
        }
    }

    @Override
    public StockAllData getStockAllData(String stockCode) {
        String stockTableName = "stock_" + stockCode;
        String infoTableName = "info_" + stockCode;

        if(repo.isExistTable(stockTableName) && repo.isExistTable(infoTableName)){
            return repo.getStockAllData(stockTableName, infoTableName);
        }else{
            return null;
        }
    }
}
