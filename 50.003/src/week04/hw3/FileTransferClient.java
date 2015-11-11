package week04.hw3;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.SocketTimeoutException;
import java.util.ArrayList;


public class FileTransferClient {
	public static void main(String[] args) throws Exception {
        String hostName = "localhost";
        //String hostName = "fe80::7517:c1af:b2bb:da73%4";
        int portNumber = 4321;
        String msg;
 
        Socket echoSocket = new Socket(hostName, portNumber);
        PrintWriter out = new PrintWriter(echoSocket.getOutputStream(), true);
        BufferedReader in =
                new BufferedReader(
                    new InputStreamReader(echoSocket.getInputStream()));
        
        ArrayList<String> data = new ArrayList<String>();
        BufferedReader br = new BufferedReader(new FileReader("src\\data.txt"));
        try { 
        	String line;
            for(; (line = br.readLine()) != null;) {
            	data.add(line);
            }
        } finally {
            br.close();
        }
        
        
        out.println(data.size());
        out.flush();
        msg = in.readLine();
        if(msg.startsWith("OK")) {
        	echoSocket.setSoTimeout(5000);
        	System.out.println(msg);
        	for(int i = 0; i < data.size(); ++i) {
        		do {
        			System.out.println("Sending Line " + i + "...");
        			out.println(i);
            		out.println(data.get(i));
            		out.flush();
            		
            		try {
            			msg = in.readLine();
            		} catch(SocketTimeoutException e) {
            			msg = null;
            			System.out.println("Timeout.");
            		}
            		
        		} while(msg == null || !msg.startsWith("OK"));
        	}
        	
        	do {
        		out.println(-1);
        		out.flush();
        		try {
        			msg = in.readLine();
        		} catch(SocketTimeoutException e) {
        			msg = null;
        			System.out.println("Timeout.");
        		}
        	} while(msg == null || !msg.startsWith("OK"));
        	System.out.println("Done.");
        }
            
        echoSocket.close();
        in.close();
        out.close();       
    }
}
