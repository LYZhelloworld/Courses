package week04.hw2;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketTimeoutException;
import java.util.ArrayList;


public class ChatRoom2 {
	public static void main(String[] args) {
		ServerSocket serverSocket = null;
		ArrayList<Socket> clients = new ArrayList<Socket>();
		try {
			serverSocket = new ServerSocket(4321);
			serverSocket.setSoTimeout(10000);
	    	System.out.println("[SERVER] Expecting connection...");
	    	
	    	try {
	    		for(;;) {
	    			Socket clientSocket = serverSocket.accept();   
		    		clients.add(clientSocket);
		    		System.out.println("[SERVER] Connection " + (clients.size() - 1) + " established...");
	    		}
	    	} catch(SocketTimeoutException e) {
	    		//
	    	}
	    	
	    	for(Socket i: clients) {
    			i.setSoTimeout(5000);
    		}
	    	System.out.println("[SERVER] Chat starts.");
	    		    	
	    	for(; clients.size() != 0;) {
	    		for(int i = 0; i < clients.size(); ++i) {
	    			clientProcess(clients.get(i), i);
	    		}
	    		for(int i = clients.size() - 1; i >= 0; --i) {
	    			if(clients.get(i).isClosed()) clients.remove(i);
	    		}
	    	}
	    	
	    	System.out.println("[SERVER] Chat ends.");
	    	
		} catch(IOException e) {
			//
		} finally {
			try {
				if(serverSocket != null) serverSocket.close();
			} catch(Exception e) {
				
			}
		}
    }
	
	public static void clientProcess(Socket client, int id) {
		PrintWriter out = null;
    	BufferedReader in = null;
    	try {
    		out = new PrintWriter(client.getOutputStream(), true);                   
            in = new BufferedReader(new InputStreamReader(client.getInputStream()));
            
            String input;
            for(; !(input = in.readLine()).equals("bye"); ) {
            	System.out.println("[" + id + "] " + input);
            }
            System.out.println("[" + id + "] " + input);
            if(out != null) out.close();
    		if(in != null) {
    			try {
    				in.close();
    			} catch(IOException e) {
    				//
    			}
    		}
            client.close();
    	} catch(SocketTimeoutException timeout) {
    		//
    	} catch(IOException io) {
    		try {
    			client.close();
    		} catch(Exception ex) {
    			//
    		}
    	}
	}
}