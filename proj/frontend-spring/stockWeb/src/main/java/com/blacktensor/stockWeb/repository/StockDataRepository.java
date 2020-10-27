package com.blacktensor.stockWeb.repository;

import com.blacktensor.stockWeb.entity.enterpriseData.StockAllData;
import com.blacktensor.stockWeb.entity.enterpriseData.StockData;
import com.blacktensor.stockWeb.entity.enterpriseData.StockInfo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.stereotype.Repository;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.List;

@Repository
public class StockDataRepository {

    @Autowired
    private JdbcTemplate jdbc;

    public boolean isExistTable(String tableName){
        String query = "select count(*) as count from information_schema.tables where table_name = ?";
        List<Integer> list = jdbc.query(query, new RowMapper<Integer>() {

            @Override
            public Integer mapRow(ResultSet rs, int rowNum) throws SQLException {

                if(rs.getInt("count") == 1){
                    return 1;
                }

                return 0;
            }
        }, tableName);

        return list.get(0) == 1;
    }

    public void createStockTable(String tableName){
        String query = "create table " + tableName +" (";
        query += " stockNo BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,";
        query += " stockCode VARCHAR(255) not null,";
        query += " stockName VARCHAR(255) not null,";
        query += " currentPrice VARCHAR(255) not null,";
        query += " netChange VARCHAR(255) not null,";
        query += " fluctuation VARCHAR(255) not null,";
        query += " volumeValue VARCHAR(255) not null,";
        query += " tradePrepare VARCHAR(255) not null,";
        query += " standardPrice VARCHAR(255) not null,";
        query += " netChangeSymbol VARCHAR(1) not null,";
        query += " upperPrice VARCHAR(255) not null,";
        query += " lowerPrice VARCHAR(255) not null,";
        query += " openPrice VARCHAR(255) not null,";
        query += " highPrice VARCHAR(255) not null,";
        query += " createDate TIMESTAMP not null default now()";
        query += ")";

        jdbc.update(query);
    }

    public void insertStockData(String tableName, StockData data){
        String query = "insert into " + tableName + " (stockCode, stockName, currentPrice,";
        query += " netChange, fluctuation, volumeValue, tradePrepare, standardPrice, netChangeSymbol, upperPrice, lowerPrice, openPrice, highPrice)";
        query += " values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";

        jdbc.update(query, data.getStockCode(), data.getStockName(), data.getCurrentPrice(), data.getNetChange(), data.getFluctuation(),
                    data.getVolumeValue(), data.getTradePrepare(), data.getStandardPrice(), data.getNetChangeSymbol(), data.getUpperPrice(),
                    data.getLowerPrice(), data.getOpenPrice(), data.getHighPrice());
    }

    public void createInfoTable(String tableName){
        String query = "create table " + tableName + " (";
        query += " stockNo BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,";
        query += " stockCode varchar(255) not null,";
        query += " stockName varchar(255) not null,";
        query += " closingMonth varchar(255) not null,";
        query += " parValue varchar(255) not null,";
        query += " capital varchar(255) not null,";
        query += " listedStock varchar(255) not null,";
        query += " creditRatio varchar(255) not null,";
        query += " bestYear varchar(255) not null,";
        query += " lowYear varchar(255) not null,";
        query += " marketValue varchar(255) not null,";
        query += " perValue varchar(255) not null,";
        query += " epsValue varchar(255) not null,";
        query += " roeValue varchar(255) not null,";
        query += " pbrValue varchar(255) not null,";
        query += " bpsValue varchar(255) not null,";
        query += " take varchar(255) not null,";
        query += " operationProfit varchar(255) not null,";
        query += " netIncome varchar(255) not null,";
        query += " createDate TIMESTAMP not null default now()";
        query += ")";

        jdbc.update(query);
    }

    public void insertInfoData(String tableName, StockInfo data){
        String query = "insert into " + tableName + " (stockCode, stockName, closingMonth,";
        query += " parValue, capital, listedStock, creditRatio, bestYear, lowYear, marketValue,";
        query += " perValue, epsValue, roeValue, pbrValue, bpsValue, take, operationProfit,";
        query += " netIncome) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";

        jdbc.update(query, data.getStockCode(), data.getStockName(), data.getClosingMonth(), data.getParValue(), data.getCapital(), data.getListedStock(),
                    data.getCreditRatio(), data.getBestYear(), data.getLowYear(), data.getMarketValue(), data.getPerValue(), data.getEpsValue(),
                    data.getRoeValue(), data.getPbrValue(), data.getBpsValue(), data.getTake(), data.getOperationProfit(), data.getNetIncome());

    }

    public List<StockData> getStockDatas(String tableName){
        String query = "select * from " + tableName + " where createDate >= (select DATE_SUB(MAX(createDate), INTERVAL 1095 DAY) from " + tableName + ")";

        List<StockData> result = jdbc.query(query, new RowMapper<StockData>() {

            @Override
            public StockData mapRow(ResultSet rs, int rowNum) throws SQLException {

                StockData data = new StockData();

                data.setStockNo(rs.getLong("stockNo"));
                data.setStockCode(rs.getString("stockCode"));
                data.setStockName(rs.getString("stockName"));
                data.setCurrentPrice(rs.getString("currentPrice"));
                data.setNetChange(rs.getString("netChange"));
                data.setFluctuation(rs.getString("fluctuation"));
                data.setVolumeValue(rs.getString("volumeValue"));
                data.setTradePrepare(rs.getString("tradePrepare"));
                data.setStandardPrice(rs.getString("standardPrice"));
                data.setNetChangeSymbol(rs.getString("netChangeSymbol"));
                data.setUpperPrice(rs.getString("upperPrice"));
                data.setLowerPrice(rs.getString("lowerPrice"));
                data.setOpenPrice(rs.getString("openPrice"));
                data.setHighPrice(rs.getString("highPrice"));
                data.setCreateDate(rs.getDate("createDate"));

                return data;
            }
        });

        return result;
    }

    public List<StockInfo> getStockInfos(String tableName){
        String query = "select * from " + tableName + " where createDate = (select MAX(createDate) from " + tableName + ")";

        List<StockInfo> result = jdbc.query(query, new RowMapper<StockInfo>() {

            @Override
            public StockInfo mapRow(ResultSet rs, int rowNum) throws SQLException {

                StockInfo data = new StockInfo();

                data.setStockNo(rs.getLong("stockNo"));
                data.setStockCode(rs.getString("stockCode"));
                data.setStockName(rs.getString("stockName"));
                data.setClosingMonth(rs.getString("closingMonth"));
                data.setParValue(rs.getString("parValue"));
                data.setCapital(rs.getString("capital"));
                data.setListedStock(rs.getString("listedStock"));
                data.setCreditRatio(rs.getString("creditRatio"));
                data.setBestYear(rs.getString("bestYear"));
                data.setLowYear(rs.getString("lowYear"));
                data.setMarketValue(rs.getString("marketValue"));
                data.setPerValue(rs.getString("perValue"));
                data.setEpsValue(rs.getString("epsValue"));
                data.setRoeValue(rs.getString("roeValue"));
                data.setPbrValue(rs.getString("pbrValue"));
                data.setBpsValue(rs.getString("bpsValue"));
                data.setTake(rs.getString("take"));
                data.setOperationProfit(rs.getString("operationProfit"));
                data.setNetIncome(rs.getString("netIncome"));
                data.setCreateDate(rs.getDate("createDate"));

                return data;
            }
        });

        return result;
    }

    public StockAllData getStockAllData(String stockTableName, String infoTableName){
        String query = "select stock.stockCode, stock.stockName, stock.currentPrice, stock.netChange, stock.fluctuation, stock.volumeValue, stock.tradePrepare, stock.standardPrice,";
        query += " stock.netChangeSymbol, stock.upperPrice, stock.lowerPrice, stock.openPrice, stock.highPrice,";
        query += " info.closingMonth, info.parValue, info.capital, info.listedStock, info.creditRatio, info.bestYear, info.lowYear,";
        query += " info.marketValue, info.perValue, info.epsValue, info.roeValue, info.pbrValue, info.bpsValue, info.take,";
        query += " info.operationProfit, info.netIncome";
        query += " from " + stockTableName + " stock, " + infoTableName + " info";
        query += " where stock.createDate = (select MAX(createDate) from " + stockTableName + ")";
        query += " and info.createDate = (select MAX(createDate) from " + infoTableName + ")";
        query += " and info.stockCode = stock.stockCode";

        List<StockAllData> result = jdbc.query(query, new RowMapper<StockAllData>() {
            @Override
            public StockAllData mapRow(ResultSet rs, int rowNum) throws SQLException {

                StockAllData data = new StockAllData();

                data.setStockCode(rs.getString("stockCode"));
                data.setStockName(rs.getString("stockName"));
                data.setCurrentPrice(rs.getString("currentPrice"));
                data.setNetChange(rs.getString("netChange"));
                data.setFluctuation(rs.getString("fluctuation"));
                data.setVolumeValue(rs.getString("volumeValue"));
                data.setTradePrepare(rs.getString("tradePrepare"));
                data.setStandardPrice(rs.getString("standardPrice"));
                data.setNetChangeSymbol(rs.getString("netChangeSymbol"));
                data.setUpperPrice(rs.getString("upperPrice"));
                data.setLowerPrice(rs.getString("lowerPrice"));
                data.setOpenPrice(rs.getString("openPrice"));
                data.setHighPrice(rs.getString("highPrice"));

                data.setClosingMonth(rs.getString("closingMonth"));
                data.setParValue(rs.getString("parValue"));
                data.setCapital(rs.getString("capital"));
                data.setListedStock(rs.getString("listedStock"));
                data.setCreditRatio(rs.getString("creditRatio"));
                data.setBestYear(rs.getString("bestYear"));
                data.setLowYear(rs.getString("lowYear"));
                data.setMarketValue(rs.getString("marketValue"));
                data.setPerValue(rs.getString("perValue"));
                data.setEpsValue(rs.getString("epsValue"));
                data.setRoeValue(rs.getString("roeValue"));
                data.setPbrValue(rs.getString("pbrValue"));
                data.setBpsValue(rs.getString("bpsValue"));
                data.setTake(rs.getString("take"));
                data.setOperationProfit(rs.getString("operationProfit"));
                data.setNetIncome(rs.getString("netIncome"));

                return data;
            }
        });

        return result.size() == 1 ? result.get(0) : null;
    }
}
