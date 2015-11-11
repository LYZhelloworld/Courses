package week04.ex3;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Date;


public class ChatServer {
	public static void main(String[] args) throws Exception {
    	ServerSocket serverSocket = new ServerSocket(4321);
    	PrintWriter out = null;
    	BufferedReader in = null;
    	System.out.println("(... expecting connection ...)");
    	
    	//Assume that the server only accept 3 times
    	for(int i = 0; i < 3; ++i) {
    		Socket clientSocket = serverSocket.accept();     
        	System.out.println("(... connection established ...)");
            out = new PrintWriter(clientSocket.getOutputStream(), true);                   
            in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
            
            out.println("[" + new Date().toString() + "] Connection " + i + " established.");
            out.flush();
            System.out.println(in.readLine());
                        
            clientSocket.close();
    	}
    	
    	serverSocket.close();
    	if(out != null) out.close();
    	if(in != null) in.close();
    }
}
