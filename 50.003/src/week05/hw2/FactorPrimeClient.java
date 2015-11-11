package week05.hw2;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.math.BigInteger;
import java.net.Socket;


public class FactorPrimeClient {
	public static Boolean done = false;
	public static BigInteger result1 = null, result2 = null;
	
	public static void main(String[] args) throws Exception {
        String hostName = "localhost";
        //String hostName = "fe80::7517:c1af:b2bb:da73%4";
        int portNumber = 4321;
 
        Socket echoSocket = new Socket(hostName, portNumber);
        PrintWriter out = new PrintWriter(echoSocket.getOutputStream(), true);
        BufferedReader in =
                new BufferedReader(
                    new InputStreamReader(echoSocket.getInputStream()));
        
        System.out.println("Initializing...");
        BigInteger start, end, value;
        start = new BigInteger(in.readLine());
        end = new BigInteger(in.readLine());
        value = new BigInteger(in.readLine());
        System.out.println("Message received: start=" + start.toString() + "; end=" + end.toString() + "; value=" + value.toString());
        
        SearchingThread thread1 = new SearchingThread(start, end.divide(BigInteger.valueOf(2)), value);
        SearchingThread thread2 = new SearchingThread(end.divide(BigInteger.valueOf(2)).add(BigInteger.ONE), end, value);
        
        thread1.start();
        thread2.start();
        
        for(; !done && !echoSocket.isClosed() && !echoSocket.isInputShutdown() && !echoSocket.isOutputShutdown(); ) {
        	if(thread1.isFinished() && thread2.isFinished()) break;
        }
        thread1.interrupt();
        thread2.interrupt();

        if(result1 != null && result2 != null) {
        	out.println(result1.toString());
            out.println(result2.toString());
            out.flush();
            
            System.out.println(result1.toString());
            System.out.println(result2.toString());
        }
        System.out.println("Done.");
        
        echoSocket.close();
        in.close();
        out.close();          
    }
}

class SearchingThread extends Thread {
	private BigInteger start, end, target;
	private Boolean finished;
	
	public SearchingThread(BigInteger start, BigInteger end, BigInteger target) {
		this.start = start;
		this.end = end;
		this.target = target;
		this.finished = false;
	}
	
	public void run() {
		for(BigInteger i = start; i.compareTo(end) <= 0; i = i.add(BigInteger.ONE)) {
			if(isInterrupted()) break;
			if(target.remainder(i).equals(BigInteger.ZERO)) {
				FactorPrimeClient.result1 = i;
				FactorPrimeClient.result2 = target.divide(i);
				FactorPrimeClient.done = true;
				break;
			}
		}
		this.finished = true;
	}
	
	public Boolean isFinished() {
		return this.finished;
	}
}
