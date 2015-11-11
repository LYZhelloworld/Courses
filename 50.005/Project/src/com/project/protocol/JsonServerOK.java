package com.project.protocol;

public class JsonServerOK extends JsonMsg {
	public final String msg;
	
	public JsonServerOK(String msg) {
		super(JsonCode.SERVER_OK);
		this.msg = msg;
	}
}
