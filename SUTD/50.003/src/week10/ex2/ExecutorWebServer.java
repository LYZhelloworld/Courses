package week10.ex2;

import java.io.*;
import java.math.BigInteger;
import java.net.*;
import java.util.concurrent.Executor;
import java.util.concurrent.Executors;
 
public class ExecutorWebServer {
	private static final int NTHREADS = 100;
	private static final Executor exec = Executors.newFixedThreadPool(NTHREADS);
	
    public static void main(String[] args) throws Exception {
		ServerSocket socket = new ServerSocket(4321, 1000);

		while (true) {
			final Socket connection = socket.accept();
			Runnable task = new Runnable () {
				public void run() {
					try {
						handleRequest(connection);
					} catch (Exception e) {
						//
					}
				}
			};
			
			exec.execute(task);
		}
    }

	protected static void handleRequest(Socket connection) throws Exception {
		PrintWriter out = new PrintWriter(connection.getOutputStream(), true);
    	BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
    	out.println(factor(new BigInteger(in.readLine())).toString());
    	out.flush();
    	out.close();
    	in.close();
	}
	
	private static BigInteger factor(BigInteger n) {
		BigInteger i = new BigInteger("2");
		BigInteger zero = new BigInteger("0");
		
		while (i.compareTo(n) < 0) {			
			if (n.remainder(i).compareTo(zero) == 0) {
				return i;
			}
			
			i = i.add(new BigInteger("1"));
		}
		
		assert(false);
		return null;
	}
}