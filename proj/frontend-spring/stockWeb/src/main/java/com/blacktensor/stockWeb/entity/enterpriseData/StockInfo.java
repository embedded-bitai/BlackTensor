package com.blacktensor.stockWeb.entity.enterpriseData;

import lombok.Getter;
import lombok.Setter;

import java.util.Date;

@Setter
@Getter
public class StockInfo {

    private Long stockNo;

    // 주식 코드
    private String stockCode;

    // 주식 명
    private String stockName;

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

    // 생성 시간
    private Date createDate;
}
