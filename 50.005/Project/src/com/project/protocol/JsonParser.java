package com.project.protocol;

import java.util.HashMap;
import java.util.Map;

import org.json.JSONObject;

public class JsonParser {
	private static JsonParser instance = null;
	
	//Client-side request code
	protected static final int CLIENT_DONE = 0;
	protected static final int CLIENT_GET_IDENTITY = 1;
	protected static final int CLIENT_GET_CERTIFICATE = 2;
	protected static final int CLIENT_SET_MODE = 3;
	protected static final int CLIENT_PUT_FILE = 4;
	protected static final int CLIENT_END = 99;

	//Server-side response code
	protected static final int SERVER_OK = 100;
	protected static final int SERVER_RESEND = 101;
	protected static final int SERVER_UNKNOWN_ERROR = 999;
	
	//Singleton
	public static JsonParser getInstance() {
		if(JsonParser.instance == null) {
			JsonParser.instance = new JsonParser();
		}
		return JsonParser.instance;
	}
	
	private JsonParser() {}
	
	public Map<String, Object> parse(JSONObject json) {
		int type = json.getInt("code");
		switch(type) {
		case CLIENT_DONE:
			return parse_ClientDone();
		case CLIENT_GET_IDENTITY:
			return parse_ClientGetIdentity();
		case CLIENT_GET_CERTIFICATE:
			return parse_ClientGetCertificate();
		case CLIENT_SET_MODE:
			return parse_ClientSetMode(json.getString("mode"));
		case CLIENT_PUT_FILE:
			return parse_ClientPutFile(json.getInt("part"), json.getString("data"));
		case CLIENT_END:
			return parse_ClientEnd();
		case SERVER_OK:
			return parse_ServerOK(json.getString("msg"));
		case SERVER_RESEND:
			return parse_ServerResend(json.getString("msg"));
		case SERVER_UNKNOWN_ERROR:
			return parse_ServerUnknownError(json.getString("msg"));
		default:
			return null;				
		}
	}
	
	private Map<String, Object> parse_ClientDone() {
		Map<String, Object> result = new HashMap<String, Object>();
		result.put("code", CLIENT_DONE);
		return result;
	}
	
	private Map<String, Object> parse_ClientGetIdentity() {
		Map<String, Object> result = new HashMap<String, Object>();
		result.put("code", CLIENT_GET_IDENTITY);
		return result;
	}
	
	private Map<String, Object> parse_ClientGetCertificate() {
		Map<String, Object> result = new HashMap<String, Object>();
		result.put("code", CLIENT_GET_CERTIFICATE);
		return result;
	}
	
	private Map<String, Object> parse_ClientSetMode(String mode) {
		Map<String, Object> result = new HashMap<String, Object>();
		result.put("code", CLIENT_SET_MODE);
		result.put("mode", mode);
		return result;
	}
	
	private Map<String, Object> parse_ClientPutFile(int part, String data) {
		Map<String, Object> result = new HashMap<String, Object>();
		result.put("code", CLIENT_SET_MODE);
		result.put("part", part);
		result.put("data", data);
		return result;
	}
	
	private Map<String, Object> parse_ClientEnd() {
		Map<String, Object> result = new HashMap<String, Object>();
		result.put("code", CLIENT_END);
		return result;
	}
	
	private Map<String, Object> parse_ServerOK(String msg) {
		Map<String, Object> result = new HashMap<String, Object>();
		result.put("code", SERVER_OK);
		return result;
	}
	
	private Map<String, Object> parse_ServerResend(String msg) {
		Map<String, Object> result = new HashMap<String, Object>();
		result.put("code", SERVER_RESEND);
		return result;
	}
	
	private Map<String, Object> parse_ServerUnknownError(String msg) {
		Map<String, Object> result = new HashMap<String, Object>();
		result.put("code", SERVER_UNKNOWN_ERROR);
		return result;
	}
	
	/*
	public JsonMsg parse(JSONObject json) {
		int type = json.getInt("code");
		switch(type) {
		case JsonCode.CLIENT_DONE:
			return new JsonClientDone();
		case JsonCode.CLIENT_GET_IDENTITY:
			return new JsonClientGetIdentity();
		case JsonCode.CLIENT_GET_CERTIFICATE:
			return new JsonClientGetCertificate();
		case JsonCode.CLIENT_SET_MODE:
			return new JsonClientSetMode(json.getString("mode"));
		case JsonCode.CLIENT_PUT_FILE:
			return new JsonClientPutFile(json.getInt("part"), json.getString("data"));
		case JsonCode.CLIENT_END:
			return new JsonClientEnd();
		case JsonCode.SERVER_OK:
			return new JsonServerOK(json.getString("msg"));
		case JsonCode.SERVER_RESEND:
			return new JsonServerResend(json.getString("msg"));
		case JsonCode.SERVER_UNKNOWN_ERROR:
			return new JsonServerUnknownError(json.getString("msg"));
		default:
			return null;
		}
	}*/
	
	public JSONObject build(Map<String, Object> msg) {
		int type = (int) msg.get("code");
		switch(type) {
		case CLIENT_DONE:
			return new JSONObject().put("code", CLIENT_DONE);
		case CLIENT_GET_IDENTITY:
			return new JSONObject().put("code", CLIENT_GET_IDENTITY);
		case CLIENT_GET_CERTIFICATE:
			return new JSONObject().put("code", CLIENT_GET_CERTIFICATE);
		case CLIENT_SET_MODE:
			return new JSONObject().put("code", CLIENT_SET_MODE)
					.put("mode", (String) msg.get("mode"));
		case CLIENT_PUT_FILE:
			return new JSONObject().put("code", CLIENT_SET_MODE)
					.put("part", (int) msg.get("part"))
					.put("data", (String) msg.get("data"));
		case CLIENT_END:
			return new JSONObject().put("code", CLIENT_END);
		case SERVER_OK:
			return new JSONObject().put("code", SERVER_OK)
					.put("msg", (String) msg.get("msg"));
		case SERVER_RESEND:
			return new JSONObject().put("code", SERVER_RESEND)
					.put("msg", (String) msg.get("msg"));
		case SERVER_UNKNOWN_ERROR:
			return new JSONObject().put("code", SERVER_UNKNOWN_ERROR)
					.put("msg", (String) msg.get("msg"));
		default:
			return null;
		}
	}
	
	/*
	public JSONObject build(JsonMsg msg) {
		int type = msg.code;
		switch(type) {
		case JsonCode.CLIENT_DONE:
			return new JSONObject().put("code", JsonCode.CLIENT_DONE);
		case JsonCode.CLIENT_GET_IDENTITY:
			return new JSONObject().put("code", JsonCode.CLIENT_GET_IDENTITY);
		case JsonCode.CLIENT_GET_CERTIFICATE:
			return new JSONObject().put("code", JsonCode.CLIENT_GET_CERTIFICATE);
		case JsonCode.CLIENT_SET_MODE:
			return new JSONObject().put("code", JsonCode.CLIENT_SET_MODE)
					.put("mode", ((JsonClientSetMode) msg).mode);
		case JsonCode.CLIENT_PUT_FILE:
			return new JSONObject().put("code", JsonCode.CLIENT_SET_MODE)
					.put("part", ((JsonClientPutFile) msg).part)
					.put("data", ((JsonClientPutFile) msg).data);
		case JsonCode.CLIENT_END:
			return new JSONObject().put("code", JsonCode.CLIENT_END);
		case JsonCode.SERVER_OK:
			return new JSONObject().put("code", JsonCode.SERVER_OK)
					.put("msg", ((JsonServerOK) msg).msg);
		case JsonCode.SERVER_RESEND:
			return new JSONObject().put("code", JsonCode.SERVER_RESEND)
					.put("msg", ((JsonServerResend) msg).msg);
		case JsonCode.SERVER_UNKNOWN_ERROR:
			return new JSONObject().put("code", JsonCode.SERVER_UNKNOWN_ERROR)
					.put("msg", ((JsonServerUnknownError) msg).msg);
		default:
			return null;
		}
	}*/
}
