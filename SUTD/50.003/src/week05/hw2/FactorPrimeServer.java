package week05.hw2;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.math.BigInteger;
import java.net.ServerSocket;
import java.net.Socket;

public class FactorPrimeServer {
	//private static BigInteger num = new BigInteger("4294967297");
	private static BigInteger num = new BigInteger("77");
	public static String result1, result2;
	public static volatile boolean resultFound = false;
	
	public static void main(String[] args) throws Exception {
		Socket clientSocket[] = new Socket[3];
		ServerSocket serverSocket = new ServerSocket(4321);
    	System.out.println("Expecting connection...");
    	for(int i = 0; i < 3; ++i) {
    		clientSocket[i] = serverSocket.accept();
    		System.out.println("Connection " + i + " established.");
    	}
    	System.out.println("Assigning jobs...");
        ClientJob threads[] = new ClientJob[3];
        threads[0] = new ClientJob(
        		clientSocket[0], BigInteger.valueOf(2), num.divide(BigInteger.valueOf(3)), num);
        threads[1] = new ClientJob(
        		clientSocket[1], num.divide(BigInteger.valueOf(3)).add(BigInteger.ONE),
        		num.divide(BigInteger.valueOf(3)).multiply(BigInteger.valueOf(2)), num);
        threads[2] = new ClientJob(
        		clientSocket[2], num.divide(BigInteger.valueOf(3)).multiply(BigInteger.valueOf(2)).add(BigInteger.ONE),
        		num.subtract(BigInteger.ONE), num);
        
        threads[0].start();
        threads[1].start();
        threads[2].start();
        
        for(; !resultFound; );
        
        threads[0].interrupt();
        clientSocket[0].close();
        threads[1].interrupt();
        clientSocket[1].close();
        threads[2].interrupt();
        clientSocket[2].close();
        
        System.out.print(num.toString());
		System.out.print("=");
		System.out.print(result1);
		System.out.print("*");
		System.out.println(result2);
    	
    	serverSocket.close();
	}
}

class ClientJob extends Thread {
	private Socket client;
	private BigInteger start, end, value;
	
	public ClientJob(Socket client, BigInteger start, BigInteger end, BigInteger value) {
		this.client = client;
		this.start = start;
		this.end = end;
		this.value = value;
	}
	
	public void run() {
		System.out.println("Thread has been started. start=" + start.toString() + "; end=" + end.toString() + "; value=" + value.toString());
		PrintWriter out = null;
		BufferedReader in = null;
		try {
			out = new PrintWriter(client.getOutputStream(), true);                   
	        in = new BufferedReader(new InputStreamReader(client.getInputStream()));
	        
	        out.println(start.toString());
	        out.println(end.toString());
	        out.println(value.toString());
	        out.flush();
	        
	        FactorPrimeServer.result1 = in.readLine();
	        FactorPrimeServer.result2 = in.readLine();
	        FactorPrimeServer.resultFound = true;
	        
	        
	        
		} catch (Exception e) {
			//
		} finally {
			try {
				out.close();
				in.close();
				client.close();
			} catch (Exception e) {
				//
			}
		}
	}
}
