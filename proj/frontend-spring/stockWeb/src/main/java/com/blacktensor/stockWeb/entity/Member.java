package com.blacktensor.stockWeb.entity;

import lombok.*;

import javax.persistence.*;

@Data
@NoArgsConstructor
@Getter
@Setter
@EqualsAndHashCode(of="memberNo")
@ToString
@Entity
public class Member {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "memberNo")
    private Long memberNo;

    @Column(nullable = false)
    private String email;

    @Column(nullable = false)
    private String password;

    @Column(nullable = false)
    private String apiId;

    @Column(nullable = false, length = 256)
    private String authKey;

    @Column(nullable = false, columnDefinition = "TINYINT(1) default 0")
    private boolean isConfirm;
}
