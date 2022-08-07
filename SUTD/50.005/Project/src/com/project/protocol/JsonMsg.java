package com.project.protocol;

public abstract class JsonMsg {
	public final int code;
	
	protected JsonMsg(int code) {
		this.code = code;
	}
}
