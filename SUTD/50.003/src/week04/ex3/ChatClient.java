package week04.ex3;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.Date;


public class ChatClient {
	public static void main(String[] args) throws Exception {
        String hostName = "localhost";
        //String hostName = "fe80::7517:c1af:b2bb:da73%4";
        int portNumber = 4321;
 
        Socket echoSocket = new Socket(hostName, portNumber);
        PrintWriter out = new PrintWriter(echoSocket.getOutputStream(), true);
        BufferedReader in =
                new BufferedReader(
                    new InputStreamReader(echoSocket.getInputStream()));
        
        System.out.println(in.readLine());
        out.println("[" + new Date().toString() + "] Message received.");
        out.flush();
            
        echoSocket.close();
        in.close();
        out.close();       
    }
}
