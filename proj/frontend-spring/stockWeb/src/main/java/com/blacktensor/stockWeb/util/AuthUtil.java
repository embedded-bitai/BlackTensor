package com.blacktensor.stockWeb.util;

import com.blacktensor.stockWeb.constants.KeyConstants;

import java.security.MessageDigest;

public class AuthUtil {
    public static String getSignUpAuthKey(String mail, String apiId) throws Exception{

        String authKey = null;

        if(RegexUtil.isEmail(mail) && StringUtil.isNotEmptyString(apiId)){
            String msg = mail+apiId+ KeyConstants.key;
            MessageDigest md = MessageDigest.getInstance("SHA-256");

            md.update(msg.getBytes());
            byte[] bytes = md.digest();
            StringBuilder sb = new StringBuilder();

            for(byte b : bytes){
                sb.append(String.format("%02x", b));
            }

            authKey = sb.toString();
        }

        return authKey;
    }

    public static String getAuthUrl(String mail, String authKey){
        return "http://localhost:8000/member/auth/" + mail + "/" +authKey;
    }
}
