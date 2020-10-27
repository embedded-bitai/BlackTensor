package com.blacktensor.stockWeb.controller;

import com.blacktensor.stockWeb.entity.TradeHistory;
import com.blacktensor.stockWeb.service.TradeHistoryService;
import com.blacktensor.stockWeb.util.StringUtil;
import com.blacktensor.stockWeb.util.ValidateUtil;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;

@RestController
@RequestMapping("/history")
@CrossOrigin(origins = "http://localhost:8080", allowedHeaders = "*")
public class TradeHistoryController {

    private static final Logger log = LoggerFactory.getLogger(TradeHistoryController.class);

    @Autowired
    TradeHistoryService service;

    @PostMapping("/buy")
    public ResponseEntity<String> insertBuyHistory(@Validated @RequestBody TradeHistory history){
        log.debug("information - history : " + history);

        try{

            if(ValidateUtil.validateBuyHistoryInfo(history)){
                service.insertBuyHistory(history);
                return new ResponseEntity<String>("Buy History create Success", HttpStatus.OK);
            }

        }catch (Exception e){
            log.info(e.getMessage());
            return new ResponseEntity<String>("Buy History create Fail", HttpStatus.OK);
        }

        return new ResponseEntity<String>("Check Buy History Information", HttpStatus.BAD_REQUEST);
    }

    @PostMapping("/sell")
    public ResponseEntity<String> insertSellHistory(@Validated @RequestBody TradeHistory history){
        log.debug("information - history : " + history);

        try{

            if(ValidateUtil.validateSellHistoryInfo(history)){
                service.insertSellHistory(history);
                return new ResponseEntity<String>("Sell History create Success", HttpStatus.OK);
            }

        }catch (Exception e){
            log.info(e.getMessage());
            return new ResponseEntity<String>("Sell History create Fail", HttpStatus.OK);
        }

        return new ResponseEntity<String>("Check Sell History Information", HttpStatus.BAD_REQUEST);
    }

    @GetMapping("/total/{apiId}")
    public ResponseEntity<List<TradeHistory>> getTotalHistory(@PathVariable String apiId){
        log.debug("information - apiId : " + apiId);
        List<TradeHistory> list = null;

        try {

            if(StringUtil.isNotEmptyString(apiId)){
                list = service.getTotalHistory(apiId);
                return new ResponseEntity<List<TradeHistory>>(list, HttpStatus.OK);
            }

        }catch (Exception e){
            log.info(e.getMessage());
            return new ResponseEntity<List<TradeHistory>>(list, HttpStatus.OK);
        }

        return new ResponseEntity<List<TradeHistory>>(list, HttpStatus.BAD_REQUEST);
    }

    @GetMapping("/find/{apiId}/{stockName}")
    public ResponseEntity<List<TradeHistory>> getHistoryByStockName(@PathVariable String apiId, @PathVariable String stockName){
        log.debug("information - apiId : " + apiId + ", stockName : " + stockName);
        List<TradeHistory> list = null;

        try{
            if(StringUtil.isNotEmptyString(apiId) && StringUtil.isNotEmptyString(stockName)){
                list = service.getHistoryByStockName(apiId, stockName);
                return new ResponseEntity<List<TradeHistory>>(list, HttpStatus.OK);
            }
        }catch (Exception e){
            log.info(e.getMessage());
            return new ResponseEntity<List<TradeHistory>>(list, HttpStatus.OK);
        }

        return new ResponseEntity<List<TradeHistory>>(list, HttpStatus.BAD_REQUEST);
    }

    @GetMapping("/total/type/{apiId}")
    public ResponseEntity<List<TradeHistory>> getTotalHistoryByType(@PathVariable String apiId, @Validated @RequestBody HashMap<String, String> values){
        String type = values.get("type");
        log.debug("information - apiId : " + apiId + ", type : " + type);
        List<TradeHistory> list = null;

        try {
            if(StringUtil.isNotEmptyString(apiId) && StringUtil.isNotEmptyString(type)){
                list = service.getTotalHistoryByType(apiId, type);
                return new ResponseEntity<List<TradeHistory>>(list, HttpStatus.OK);
            }
        }catch (Exception e){
            log.info(e.getMessage());
            return new ResponseEntity<List<TradeHistory>>(list, HttpStatus.OK);
        }

        return new ResponseEntity<List<TradeHistory>>(list, HttpStatus.BAD_REQUEST);
    }

    @GetMapping("/total/date/{apiId}")
    public ResponseEntity<List<TradeHistory>> getTotalHistoryByDate(@PathVariable String apiId, @Validated @RequestBody HashMap<String, String> values){
        String date = values.get("date");
        List<TradeHistory> list = null;
        log.debug("information - apiId : " + apiId + ", date str : " + date);

        try {
            if(StringUtil.isNotEmptyString(apiId) && StringUtil.isNotEmptyString(date)){
                list = service.getTotalHistoryByDate(apiId, date);
                return new ResponseEntity<List<TradeHistory>>(list, HttpStatus.OK);
            }
        }catch (Exception e){
            log.info(e.getMessage());
            return new ResponseEntity<List<TradeHistory>>(list, HttpStatus.OK);
        }

        return new ResponseEntity<List<TradeHistory>>(list, HttpStatus.BAD_REQUEST);
    }

    @GetMapping("/total/period/{apiId}")
    public ResponseEntity<List<TradeHistory>> getTotalHistoryByPeriod(@PathVariable String apiId, @Validated @RequestBody HashMap<String, String> values){
        String startstr = values.get("startdate");
        String endstr = values.get("enddate");
        List<TradeHistory> list = null;

        log.debug("information - apiId : " + apiId + ", start_date : " + startstr + ", end_date : " + endstr);

        try{
            if(StringUtil.isNotEmptyString(apiId) && StringUtil.isNotEmptyString(startstr) && StringUtil.isNotEmptyString(endstr)){
                list = service.getTotalHistoryByPeriod(apiId, startstr, endstr);
                return new ResponseEntity<List<TradeHistory>>(list, HttpStatus.OK);
            }
        }catch (Exception e) {
            log.info(e.getMessage());
            return new ResponseEntity<List<TradeHistory>>(list, HttpStatus.OK);
        }

        return new ResponseEntity<List<TradeHistory>>(list, HttpStatus.BAD_REQUEST);
    }

    @GetMapping("/find/type/{apiId}/{stockName}")
    public ResponseEntity<List<TradeHistory>> getHistoryByStockNameAndType(@PathVariable String apiId, @PathVariable String stockName, @Validated @RequestBody HashMap<String, String> values){
        String type = values.get("type");
        List<TradeHistory> list = null;

        log.debug("information - apiId : " + apiId + ", stockName : " + stockName + ", type : " + type);

        try {

            if(StringUtil.isNotEmptyString(apiId) && StringUtil.isNotEmptyString(stockName) && StringUtil.isNotEmptyString(type)){
                list = service.getHistoryByStockNameAndType(apiId, stockName, type);
                return new ResponseEntity<List<TradeHistory>>(list, HttpStatus.OK);
            }

        } catch (Exception e){
            log.info(e.getMessage());
            return new ResponseEntity<List<TradeHistory>>(list, HttpStatus.OK);
        }

        return new ResponseEntity<List<TradeHistory>>(list, HttpStatus.BAD_REQUEST);
    }

    @GetMapping("/find/date/{apiId}/{stockName}")
    public ResponseEntity<List<TradeHistory>> getHistoryByStockNameAndDate(@PathVariable String apiId, @PathVariable String stockName ,@Validated @RequestBody HashMap<String, String> values){
        String date = values.get("date");
        List<TradeHistory> list = null;

        log.debug("information - apiId : " + apiId + ", stockName : " + stockName + ", date str : " + date);

        try {

            if(StringUtil.isNotEmptyString(apiId) && StringUtil.isNotEmptyString(stockName) && StringUtil.isNotEmptyString(date)){
                list = service.getHistoryByStockNameAndDate(apiId, stockName, date);
                return new ResponseEntity<List<TradeHistory>>(list, HttpStatus.OK);
            }

        }catch (Exception e){
            log.info(e.getMessage());
            return new ResponseEntity<List<TradeHistory>>(list, HttpStatus.OK);
        }

        return new ResponseEntity<List<TradeHistory>>(list, HttpStatus.BAD_REQUEST);
    }

    @GetMapping("/find/period/{apiId}/{stockName}")
    public ResponseEntity<List<TradeHistory>> getHistoryByStockNameAndPeriod(@PathVariable String apiId, @PathVariable String stockName, @Validated @RequestBody HashMap<String, String> values){
        String startstr = values.get("startdate");
        String endstr = values.get("enddate");
        List<TradeHistory> list = null;

        try{
            if(StringUtil.isNotEmptyString(apiId) && StringUtil.isNotEmptyString(startstr) && StringUtil.isNotEmptyString(endstr)){
                list = service.getHistoryByStockNameAndPriod(apiId, stockName, startstr, endstr);
                return new ResponseEntity<List<TradeHistory>>(list, HttpStatus.OK);
            }
        }catch (Exception e){
            log.info(e.getMessage());
            return new ResponseEntity<List<TradeHistory>>(list, HttpStatus.OK);
        }

        return new ResponseEntity<List<TradeHistory>>(list, HttpStatus.BAD_REQUEST);
    }
}
