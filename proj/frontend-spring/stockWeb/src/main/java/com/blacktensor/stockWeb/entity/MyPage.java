package com.blacktensor.stockWeb.entity;

import lombok.*;

import javax.persistence.*;
import java.util.Date;

@Data
@NoArgsConstructor
@Getter
@Setter
@EqualsAndHashCode(of="pageNo")
@ToString
@Entity
public class MyPage {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "pageNo")
    private Long pageNo;

    @Column(nullable = true, length = 20)
    private String name;

    @Column(nullable = true, length = 1)
    private String gender;

    @Column(nullable = true)
    private Date birth;

    @Column(nullable = true, length = 11)
    private String phone;

    @Column(nullable = true, length = 200)
    private String memo;

    @OneToOne
    @JoinColumn(name = "memberNo", nullable = false)
    private Member member;
}
