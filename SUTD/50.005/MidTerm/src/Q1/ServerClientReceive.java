package Q1;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;

public class ServerClientReceive {
	public static void main(String[] args) {
		try {
			ServerSocket server = new ServerSocket(1027);
			Socket socket = server.accept();
			PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
	        BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
	        
	        System.out.print("Message received from client is ");
	        System.out.print(in.readLine());
	        out.println("Successful connection");
	        out.flush();
	        
	        server.close();
	        in.close();
	        out.close();
	        socket.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}
