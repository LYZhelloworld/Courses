package Q1;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

public class ClientSendReceive {
	public static void main(String[] args) {
		try {
			Socket socket = new Socket("127.0.0.1", 1027);
			PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
	        BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
	        
	        out.println("59");
	        out.flush();
	        System.out.println("Message sent to the server: 59");
	        
	        System.out.print("Message received from server: ");
	        System.out.print(in.readLine());
	        in.close();
	        out.close();
	        socket.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}
