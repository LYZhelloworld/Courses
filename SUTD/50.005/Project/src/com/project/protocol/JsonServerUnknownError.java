package com.project.protocol;

public class JsonServerUnknownError extends JsonMsg {
	public final String msg;
	
	public JsonServerUnknownError(String msg) {
		super(JsonCode.SERVER_UNKNOWN_ERROR);
		this.msg = msg;
	}
}
