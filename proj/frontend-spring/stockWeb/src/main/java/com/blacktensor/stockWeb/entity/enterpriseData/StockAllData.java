package com.blacktensor.stockWeb.entity.enterpriseData;

import lombok.Getter;
import lombok.Setter;

import java.util.Date;

@Setter
@Getter
public class StockAllData {

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

    // 결산일
    private String closingMonth;

    // 액면가
    private String parValue;

    // 자본금
    private String capital;

    // 상장주식
    private String listedStock;

    // 신용비율
    private String creditRatio;

    // 연중최고
    private String bestYear;

    // 연중최저
    private String lowYear;

    // 시가 총액
    private String marketValue;

    // PER
    private String perValue;

    // EPS
    private String epsValue;

    // ROE
    private String roeValue;

    // PBR
    private String pbrValue;

    // BPS
    private String bpsValue;

    // 매출액
    private String take;

    // 영업 이익
    private String operationProfit;

    // 당기 순이익
    private String netIncome;
    
}
