package com.project.protocol;

public class JsonCode {
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
}
