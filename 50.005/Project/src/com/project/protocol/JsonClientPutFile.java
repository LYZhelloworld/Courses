package com.project.protocol;

public class JsonClientPutFile extends JsonMsg {
	public final int part;
	public final String data;
	
	public JsonClientPutFile(int part, String data) {
		super(JsonCode.CLIENT_PUT_FILE);
		this.part = part;
		this.data = data;
	}
}
