package com.blacktensor.stockWeb.entity.enterpriseData;

import lombok.Getter;
import lombok.Setter;

import java.util.Date;

@Getter
@Setter
public class StockData {

    private Long stockNo;

    // 주식 코드
    private String stockCode;

    // 주식 명
    private String stockName;

    // 현재가
    private String currentPrice;

    // 전일 대비
    private String netChange;

    // 등락율
    private String fluctuation;

    // 거래량
    private String volumeValue;

    // 거래대비
    private String tradePrepare;

    // 기준가
    private String standardPrice;

    // 전일대비기호
    private String netChangeSymbol;

    // 상한가
    private String upperPrice;

    // 하한가
    private String lowerPrice;

    // 시가
    private String openPrice;

    // 고가
    private String highPrice;

    // 생성 시간
    private Date createDate;

}
