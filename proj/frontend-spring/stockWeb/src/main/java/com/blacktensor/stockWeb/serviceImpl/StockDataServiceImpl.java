package com.blacktensor.stockWeb.serviceImpl;

import com.blacktensor.stockWeb.entity.StockMapping;
import com.blacktensor.stockWeb.entity.enterpriseData.StockAllData;
import com.blacktensor.stockWeb.entity.enterpriseData.StockData;
import com.blacktensor.stockWeb.entity.enterpriseData.StockInfo;
import com.blacktensor.stockWeb.repository.StockDataRepository;
import com.blacktensor.stockWeb.repository.StockMappingRepository;
import com.blacktensor.stockWeb.service.StockDataService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class StockDataServiceImpl implements StockDataService {

    @Autowired
    private StockDataRepository repo;

    @Autowired
    private StockMappingRepository mappingRepo;

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
    public List<StockData> getStockDatas(String stockName) {

        List<StockMapping> list = mappingRepo.findByStockName(stockName);

        if(list.size() == 1){
            String stockCode = list.get(0).getStockCode();

            String tableName = "stock_" + stockCode;
            if(repo.isExistTable(tableName)){
                return repo.getStockDatas(tableName);
            }
        }

        return null;
    }

    @Override
    public List<StockInfo> getStockInfos(String stockName) {

        List<StockMapping> list = mappingRepo.findByStockName(stockName);

        if(list.size() == 1){
            String stockCode = list.get(0).getStockCode();
            String tableName = "info_" + stockCode;

            if(repo.isExistTable(tableName)){
                return repo.getStockInfos(tableName);
            }
        }

        return null;
    }

    @Override
    public StockAllData getStockAllData(String stockName) {

        List<StockMapping> list = mappingRepo.findByStockName(stockName);

        if(list.size() == 1){

            String stockCode = list.get(0).getStockCode();

            String stockTableName = "stock_" + stockCode;
            String infoTableName = "info_" + stockCode;

            if(repo.isExistTable(stockTableName) && repo.isExistTable(infoTableName)){
                return repo.getStockAllData(stockTableName, infoTableName);
            }
        }

        return null;
    }

    @Override
    public void insertStockMapping(StockMapping data) {
        mappingRepo.save(data);
    }
}
