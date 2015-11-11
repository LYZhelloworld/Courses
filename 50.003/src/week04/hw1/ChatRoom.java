package week04.hw1;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;


public class ChatRoom {
	public static void main(String[] args) {
		ServerSocket serverSocket = null;
		try {
			serverSocket = new ServerSocket(4321);
	    	System.out.println("[SERVER] Expecting connection...");
	    	
	    	
	    	//Infinite loop
	    	for(;;) {
	    		Socket clientSocket = serverSocket.accept();     
	        	System.out.println("[SERVER] Connection established...");
	            new Thread(new ClientThread(clientSocket)).start();
	    	}
		} catch(Exception e) {
			//
		} finally {
			try {
				if(serverSocket != null) serverSocket.close();
			} catch(Exception e) {
				
			}
		}
    }
}

class ClientThread implements Runnable {
	private Socket clientSocket;
	
	public ClientThread(Socket client) {
		this.clientSocket = client;
	}
	
	public void run() {
		PrintWriter out = null;
    	BufferedReader in = null;
    	try {
    		out = new PrintWriter(clientSocket.getOutputStream(), true);                   
            in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
            
            String input;
            for(; !(input = in.readLine()).equals("bye"); ) {
            	System.out.println(input);
            }
            System.out.println(input);
            this.clientSocket.close();
    	} catch(IOException e) {
    		//
    	} finally {
    		if(out != null) out.close();
    		if(in != null) {
    			try {
    				in.close();
    			} catch(IOException e) {
    				//
    			}
    		}
    	}
	}
}
