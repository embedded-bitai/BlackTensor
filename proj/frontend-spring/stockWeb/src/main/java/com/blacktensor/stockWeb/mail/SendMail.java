package com.blacktensor.stockWeb.mail;

import javax.mail.*;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeMessage;
import java.util.Properties;

public class SendMail {

    private static SendMail instance = new SendMail();

    public static SendMail getInstance(){
        return instance;
    }

    private SendMail() {
        this.init();
    }

    private String user = null;
    private String password = null;

    private Properties props = null;

    private boolean isInit = false;

    private void init(){
        this.user = "sendmailtestid@gmail.com";
        this.password = "sendMailTest123!";

        props = new Properties();
        props.put("mail.smtp.host", "smtp.gmail.com");
        props.put("mail.smtp.port", 465);
        props.put("mail.smtp.auth", "true");
        props.put("mail.smtp.ssl.enable", "true");
        props.put("mail.smtp.ssl.trust", "smtp.gmail.com");

        this.isInit = true;
    }

    public boolean send(String title, String to, String url) throws Exception{

        boolean result = false;

        if(this.isInit){
            Session session = Session.getDefaultInstance(props, new Authenticator() {
                @Override
                protected PasswordAuthentication getPasswordAuthentication() {
                    return new PasswordAuthentication(user, password);
                }
            });

            MimeMessage message = new MimeMessage(session);
            message.setFrom(new InternetAddress("admin@stockWeb.com"));
            message.addRecipient(Message.RecipientType.TO, new InternetAddress(to));

            message.setSubject(title);

            message.setText("Stock Web 인증 메일 입니다.\n인증 Url : " + url);

            Transport.send(message);
            result = true;
        }

        return result;
    }

}
