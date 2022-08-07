package com.project.protocol;

public class JsonClientSetMode extends JsonMsg {
	public final String mode;
	
	public JsonClientSetMode(String mode) {
		super(JsonCode.CLIENT_SET_MODE);
		this.mode = mode;
	}
}
