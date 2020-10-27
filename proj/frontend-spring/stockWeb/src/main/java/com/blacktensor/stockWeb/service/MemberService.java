package com.blacktensor.stockWeb.service;

import com.blacktensor.stockWeb.entity.Member;
import com.blacktensor.stockWeb.entity.MyPage;

public interface MemberService {
    public boolean login(String id, String password) throws Exception;
    public void signup(Member member) throws Exception;
    public boolean findMail(String email) throws Exception;
    public void updateAppId(String email, String appId) throws Exception;
    public boolean findApiId(String appid) throws Exception;
    public Member getMemberInfo(String mail) throws Exception;
    public MyPage getMyPage(String mail) throws Exception;
    public void updateMyPageInfo(String mail, MyPage mypage) throws Exception;
    public boolean confirmUser(String mail, String authKey) throws Exception;
}
