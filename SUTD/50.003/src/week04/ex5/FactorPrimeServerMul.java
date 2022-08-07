package week04.ex5;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.math.BigInteger;
import java.net.ServerSocket;
import java.net.Socket;

public class FactorPrimeServerMul {
	private static final BigInteger REGION_SIZE = BigInteger.valueOf(10000);
	private static BigInteger num = new BigInteger("4294967297");
	public static String result1, result2;
	public static boolean resultFound = false;
	
	public static void main(String[] args) throws Exception {
		Socket clientSocket;
		ServerSocket serverSocket = new ServerSocket(4321);
    	System.out.println("Expecting connection...");
    	for(int i = 0; !resultFound; ++i) {
    		if(getRegionStart(i, num) == null) {
    			for(; !resultFound; );
    			break;
    		}
    		clientSocket = serverSocket.accept();
    		System.out.println("Connection " + i + " established.");
    		System.out.println("Assigning jobs...");
    		new Thread(new ClientJob(
            		clientSocket, getRegionStart(i, num), getRegionEnd(i, num), num)).start();
    	}
    	
        
        for(; !resultFound; );
        
        System.out.print(num.toString());
		System.out.print("=");
		System.out.print(result1);
		System.out.print("*");
		System.out.println(result2);
    	
    	serverSocket.close();
	}
	
	private static BigInteger getRegionStart(int i, BigInteger MaxValue) {
		if(i == 0)
			return BigInteger.valueOf(2);
		else {
			if(REGION_SIZE.multiply(BigInteger.valueOf(i)).compareTo(MaxValue) < 0) {
				return REGION_SIZE.multiply(BigInteger.valueOf(i));
			} else {
				return null;
			}
		}
	}
	
	private static BigInteger getRegionEnd(int i, BigInteger MaxValue) {
		return getRegionStart(i + 1, MaxValue) != null ? getRegionStart(i + 1, MaxValue).subtract(BigInteger.ONE) : MaxValue.subtract(BigInteger.ONE);
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
	        FactorPrimeServerMul.result1 = in.readLine();
	        FactorPrimeServerMul.result2 = in.readLine();
	        FactorPrimeServerMul.resultFound = true;
	        
	        out.close();
	        in.close();
	        
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
