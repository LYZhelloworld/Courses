package com.project.protocol;

public class JsonServerResend extends JsonMsg {
	public final String msg;
	
	public JsonServerResend(String msg) {
		super(JsonCode.SERVER_RESEND);
		this.msg = msg;
	}
}
