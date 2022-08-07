package week05.hw3;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;


public class FileTransfer {
	public static void main(String[] args) throws Exception {
    	ServerSocket serverSocket = new ServerSocket(4321);
    	
    	System.out.println("Expecting connection ...");
    	
    	for(;;) {
    		new ClientThread(serverSocket.accept()).start();     
    		System.out.println("Connection established ...");
    	}
    	
    	//serverSocket.close();
    	
    }
}

class ClientThread extends Thread {
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
            
            int lines = Integer.parseInt(in.readLine());
            String data[] = new String[lines];
            out.println("OK. " + lines + " line(s) in total.");
            out.flush();
            System.out.println("OK. " + lines + " line(s) in total.");
            for(;;) {
            	int i = Integer.parseInt(in.readLine());
            	if(i == -1) break;
            	data[i] = in.readLine();
            	out.println("OK. Line " + i + " received.");
            	out.flush();
            	System.out.println("OK. Line " + i + " received.");
            }
            out.println("OK.");
            out.flush();
            
            System.out.println("Done.");
            System.out.println();
            
            //Here we just write the data of file to console
            for(String i: data) {
            	System.out.println(i);
            }
                    
            
    	} catch (IOException e) {
    		
    	} finally {
    		try {
    			if(clientSocket != null) clientSocket.close();
        		if(out != null) out.close();
            	if(in != null) in.close();
    		} catch (IOException e) {
    			//
    		}
    		
    	}
		
	}
}
