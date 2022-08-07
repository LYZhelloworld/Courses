package week04.hw4;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;

public class Server {
	public static void main(String[] args) throws Exception {
    	ServerSocket serverSocket = new ServerSocket(4321);
    	System.out.println("Expecting connection...");
        Socket clientX = serverSocket.accept();     
    	System.out.println("Connection established: X player");
    	Socket clientO = serverSocket.accept();     
    	System.out.println("Connection established: O player");
    	serverSocket.close();
    	
    	TictactoeGame game = new TictactoeGame(new TictactoeViewSocket(clientX, clientO));
    	game.start();
        
        clientX.close();
        clientO.close();
    }
}
