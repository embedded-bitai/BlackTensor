package com.blacktensor.stockWeb.entity;

import lombok.*;

import javax.persistence.*;

@Data
@NoArgsConstructor
@Getter
@Setter
@EqualsAndHashCode(of="stockNo")
@ToString
@Entity
public class StockMapping {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "stockNo")
    private Long stockNo;

    @Column
    private String stockName;

    @Column
    private String stockCode;
}
