package com.blacktensor.stockWeb.util;

import com.blacktensor.stockWeb.entity.Member;
import com.blacktensor.stockWeb.entity.MyPage;
import com.blacktensor.stockWeb.entity.TradeHistory;
import com.blacktensor.stockWeb.entity.WishItem;
import com.blacktensor.stockWeb.entity.enterpriseData.StockData;
import com.blacktensor.stockWeb.entity.enterpriseData.StockInfo;

public class ValidateUtil {

    public static boolean validateLoginInfo(String id, String password){
        boolean result = false;

        if(RegexUtil.isEmail(id) && StringUtil.isNotEmptyString(password) && password.length() >= 6){
            result = true;
        }

        return result;
    }

    public static boolean validateSignupInfo(Member member){
        boolean result = false;

        if(member != null && RegexUtil.isEmail(member.getEmail()) && StringUtil.isNotEmptyString(member.getPassword()) && StringUtil.isNotEmptyString(member.getApiId())){
            result = true;
        }

        return result;
    }

    public static boolean validateBuyHistoryInfo(TradeHistory history){
        boolean result = false;

        if(history != null && StringUtil.isNotEmptyString(history.getStockCode()) && StringUtil.isNotEmptyString(history.getStockName())
           && StringUtil.isNotEmptyString(history.getBuyPrice()) && StringUtil.isNotEmptyString(history.getBuyCount())
           && history.getEventDate() != null && StringUtil.isNotEmptyString(history.getEventDate().toString()) && history.getMember() != null
           && StringUtil.isNotEmptyString(history.getMember().getApiId())){
            result = true;
        }

        return result;
    }

    public static boolean validateSellHistoryInfo(TradeHistory history){
        boolean result = false;

        if(history != null && StringUtil.isNotEmptyString(history.getStockCode()) && StringUtil.isNotEmptyString(history.getStockName())
                && StringUtil.isNotEmptyString(history.getSellPrice()) && StringUtil.isNotEmptyString(history.getSellCount())
                && history.getEventDate() != null && StringUtil.isNotEmptyString(history.getEventDate().toString()) && history.getMember() != null
                && StringUtil.isNotEmptyString(history.getMember().getApiId())){
            result = true;
        }

        return result;
    }

    public static boolean validateWishItemInfo(WishItem item){
        boolean result = false;

        if(item != null && StringUtil.isNotEmptyString(item.getStockCode()) && StringUtil.isNotEmptyString(item.getStockName())
           && item.getMember() != null && StringUtil.isNotEmptyString(item.getMember().getApiId())){
            result = true;
        }

        return result;
    }

    public static boolean validateStockDataInfo(StockData data){
        boolean result = false;

        if(data != null && StringUtil.isNotEmptyString(data.getStockCode()) && StringUtil.isNotEmptyString(data.getStockName())
           && StringUtil.isNotEmptyString(data.getCurrentPrice()) && StringUtil.isNotEmptyString(data.getNetChange())
           && StringUtil.isNotEmptyString(data.getFluctuation()) && StringUtil.isNotEmptyString(data.getVolumeValue())
           && StringUtil.isNotEmptyString(data.getTradePrepare()) && StringUtil.isNotEmptyString(data.getStandardPrice())
           && StringUtil.isNotEmptyString(data.getNetChangeSymbol()) && StringUtil.isNotEmptyString(data.getUpperPrice())
           && StringUtil.isNotEmptyString(data.getLowerPrice()) && StringUtil.isNotEmptyString(data.getOpenPrice())
           && StringUtil.isNotEmptyString(data.getHighPrice())){

            result = true;

        }

        return result;
    }

    public static boolean validateStockInfo(StockInfo info){
        boolean result = false;

        if(info != null && StringUtil.isNotEmptyString(info.getStockCode()) && StringUtil.isNotEmptyString(info.getStockName())
           && StringUtil.isNotEmptyString(info.getClosingMonth()) && StringUtil.isNotEmptyString(info.getParValue())
           && StringUtil.isNotEmptyString(info.getCapital()) && StringUtil.isNotEmptyString(info.getListedStock())
           && StringUtil.isNotEmptyString(info.getCreditRatio()) && StringUtil.isNotEmptyString(info.getBestYear())
           && StringUtil.isNotEmptyString(info.getLowYear()) && StringUtil.isNotEmptyString(info.getMarketValue())
           && StringUtil.isNotEmptyString(info.getPerValue()) && StringUtil.isNotEmptyString(info.getEpsValue())
           && StringUtil.isNotEmptyString(info.getRoeValue()) && StringUtil.isNotEmptyString(info.getPbrValue())
           && StringUtil.isNotEmptyString(info.getBpsValue()) && StringUtil.isNotEmptyString(info.getTake())
           && StringUtil.isNotEmptyString(info.getNetIncome())){
            result = true;
        }

        return result;
    }
}
