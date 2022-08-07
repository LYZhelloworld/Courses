package week04.hw4;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;


public class Client {
	public static void main(String[] args) throws Exception {
        String hostName = "localhost";
        //String hostName = "fe80::7517:c1af:b2bb:da73%4";
        int portNumber = 4321;
 
        Socket echoSocket = new Socket(hostName, portNumber);
        PrintWriter out = new PrintWriter(echoSocket.getOutputStream(), true);
        BufferedReader in =
                new BufferedReader(
                    new InputStreamReader(echoSocket.getInputStream()));
        BufferedReader stdIn =
                new BufferedReader(
                    new InputStreamReader(System.in));
        String msg;
        
        for(;;) {
            msg = in.readLine();
            if(msg.equals("Put X at (0-8): ") || msg.equals("Put O at (0-8): ")) {
            	System.out.print(msg);
            	out.println(stdIn.readLine());
            	out.flush();
            } else if(msg.equals("State:")) {
            	System.out.println(msg);
            	System.out.println(in.readLine());
            	System.out.println(in.readLine());
            	System.out.println(in.readLine());
            } else if(msg.equals("Winner:")) {
            	System.out.print(msg);
            	System.out.println(in.readLine());
            	break;
            }
        }
            
        echoSocket.close();
        in.close();
        out.close();
        stdIn.close();           
    }
}
