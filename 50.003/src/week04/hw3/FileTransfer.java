package week04.hw3;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;


public class FileTransfer {
	public static void main(String[] args) throws Exception {
    	ServerSocket serverSocket = new ServerSocket(4321);
    	PrintWriter out = null;
    	BufferedReader in = null;
    	System.out.println("Expecting connection ...");
    	
    	
		Socket clientSocket = serverSocket.accept();     
    	System.out.println("Connection established ...");
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
                
        clientSocket.close();
    	serverSocket.close();
    	if(out != null) out.close();
    	if(in != null) in.close();
    }
}
