package com.blacktensor.stockWeb.controller;

import com.blacktensor.stockWeb.entity.StockMapping;
import com.blacktensor.stockWeb.entity.enterpriseData.StockAllData;
import com.blacktensor.stockWeb.entity.enterpriseData.StockData;
import com.blacktensor.stockWeb.entity.enterpriseData.StockInfo;
import com.blacktensor.stockWeb.service.StockDataService;
import com.blacktensor.stockWeb.util.StringUtil;
import com.blacktensor.stockWeb.util.ValidateUtil;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/stock")
@CrossOrigin(origins = "http://localhost:8080", allowedHeaders = "*")
public class StockDataController {

    private static final Logger log = LoggerFactory.getLogger(StockDataController.class);

    @Autowired
    private StockDataService service;

    @PostMapping("/add/stockdata")
    public ResponseEntity<String> createStockData(@Validated @RequestBody StockData stock){

        log.debug("information - data : " + stock);

        try {
            if(ValidateUtil.validateStockDataInfo(stock)){
                service.insertStockData(stock);
                return new ResponseEntity<String>("Stock Data create Success", HttpStatus.OK);
            }
        }catch (Exception e){
            log.debug(e.getMessage());
            return new ResponseEntity<String>("Stock Data create Fail", HttpStatus.OK);
        }

        return new ResponseEntity<String>("Check Stock Data Information", HttpStatus.BAD_REQUEST);
    }

    @PostMapping("/add/stockinfo")
    public ResponseEntity<String> createStockInfo(@Validated @RequestBody StockInfo info){

        log.debug("information - data : " + info);

        try {

            if(ValidateUtil.validateStockInfo(info)){
                service.insertStockInfo(info);
                return new ResponseEntity<String>("Stock Info create Success", HttpStatus.OK);
            }

        } catch (Exception e){
            log.debug(e.getMessage());
            return new ResponseEntity<String>("Stock Info create Fail", HttpStatus.OK);
        }


        return new ResponseEntity<String>("Check Stock Info Information", HttpStatus.BAD_REQUEST);
    }

    @GetMapping("/find/data/{stockName}")
    public ResponseEntity<List<StockData>> getStockDatas(@PathVariable String stockName){

        log.debug("information - name : " + stockName);
        List<StockData> result = null;

        try {

            if(StringUtil.isNotEmptyString(stockName)){
                result = service.getStockDatas(stockName);
                return new ResponseEntity<List<StockData>>(result, HttpStatus.OK);
            }

        } catch (Exception e){
            log.debug(e.getMessage());
            return new ResponseEntity<List<StockData>>(result, HttpStatus.OK);
        }

        return new ResponseEntity<List<StockData>>(result, HttpStatus.BAD_REQUEST);
    }

    @GetMapping("/find/info/{stockName}")
    public ResponseEntity<List<StockInfo>> getStockInfo(@PathVariable String stockName){
        log.debug("information - name : " + stockName);
        List<StockInfo> result = null;

        try {

            if(StringUtil.isNotEmptyString(stockName)){
                result = service.getStockInfos(stockName);
                return new ResponseEntity<List<StockInfo>>(result, HttpStatus.OK);
            }

        } catch (Exception e){
            log.debug(e.getMessage());
            return new ResponseEntity<List<StockInfo>>(result, HttpStatus.OK);
        }

        return new ResponseEntity<List<StockInfo>>(result, HttpStatus.BAD_REQUEST);
    }

    @GetMapping("/find/all/{stockName}")
    public ResponseEntity<StockAllData> getStockAllData(@PathVariable String stockName){
        log.debug("information - name : " + stockName);
        StockAllData result = null;

        try {

            if(StringUtil.isNotEmptyString(stockName)){
                result = service.getStockAllData(stockName);
                return new ResponseEntity<StockAllData>(result, HttpStatus.OK);
            }

        } catch (Exception e){
            log.debug(e.getMessage());
            return new ResponseEntity<StockAllData>(result, HttpStatus.OK);
        }

        return new ResponseEntity<StockAllData>(result, HttpStatus.BAD_REQUEST);
    }

    @PostMapping("/add/mapping")
    public ResponseEntity<String> createMappingData (@Validated @RequestBody StockMapping data){
        log.debug("information - data : " + data);

        if(ValidateUtil.validateStockMappingInfo(data)){
            try {
                service.insertStockMapping(data);
                return new ResponseEntity<String>("Stock Mapping Data Create Success", HttpStatus.OK);
            } catch (Exception e){
                log.debug(e.getMessage());
                return new ResponseEntity<String>("Stock Mapping Data Create Fail", HttpStatus.OK);
            }
        }

        return new ResponseEntity<String>("Check Mapping data", HttpStatus.BAD_REQUEST);
    }

}
