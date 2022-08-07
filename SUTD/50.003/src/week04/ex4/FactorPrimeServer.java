package week04.ex4;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.math.BigInteger;
import java.net.ServerSocket;
import java.net.Socket;

public class FactorPrimeServer {
	private static BigInteger num = new BigInteger("1127451830576035879");
	//private static BigInteger num = new BigInteger("77");
	public static String result1, result2;
	public static boolean resultFound = false;
	
	public static void main(String[] args) throws Exception {
		Socket clientSocket[] = new Socket[3];
		ServerSocket serverSocket = new ServerSocket(4321);
    	System.out.println("Expecting connection...");
    	for(int i = 0; i < 3; ++i) {
    		clientSocket[i] = serverSocket.accept();
    		System.out.println("Connection " + i + " established.");
    	}
    	System.out.println("Assigning jobs...");
        Thread threads[] = new Thread[3];
        threads[0] = new Thread(new ClientJob(
        		clientSocket[0], BigInteger.valueOf(2), num.divide(BigInteger.valueOf(3)), num));
        threads[1] = new Thread(new ClientJob(
        		clientSocket[1], num.divide(BigInteger.valueOf(3)).add(BigInteger.ONE),
        		num.divide(BigInteger.valueOf(3)).multiply(BigInteger.valueOf(2)), num));
        threads[2] = new Thread(new ClientJob(
        		clientSocket[2], num.divide(BigInteger.valueOf(3)).multiply(BigInteger.valueOf(2)).add(BigInteger.ONE),
        		num.subtract(BigInteger.ONE), num));
        
        threads[0].start();
        threads[1].start();
        threads[2].start();
        
        for(; !resultFound; );
        
        System.out.print(num.toString());
		System.out.print("=");
		System.out.print(result1);
		System.out.print("*");
		System.out.println(result2);
    	
    	serverSocket.close();
	}
}

class ClientJob implements Runnable {
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
		try {
			PrintWriter out =
	                new PrintWriter(client.getOutputStream(), true);                   
	        BufferedReader in = new BufferedReader(
	                new InputStreamReader(client.getInputStream()));
	        
	        out.println(start.toString());
	        out.println(end.toString());
	        out.println(value.toString());
	        out.flush();
	        FactorPrimeServer.result1 = in.readLine();
	        FactorPrimeServer.result2 = in.readLine();
	        FactorPrimeServer.resultFound = true;
	        
	        out.close();
	        in.close();
	        
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
