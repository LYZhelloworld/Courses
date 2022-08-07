package week04.ex4;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.math.BigInteger;
import java.net.Socket;


public class FactorPrimeClient {
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
        BigInteger start, end, value, i, j = null;
        start = new BigInteger(in.readLine());
        end = new BigInteger(in.readLine());
        value = new BigInteger(in.readLine());
        System.out.println("Message received: start=" + start.toString() + "; end=" + end.toString() + "; value=" + value.toString());
        
        for(i = start; i.compareTo(end) <= 0; i = i.add(BigInteger.ONE)) {
			if(value.remainder(i).equals(BigInteger.ZERO)) {
				j = value.divide(i);
				break;
			}
		}
        if(j != null) {
        	out.println(i.toString());
            out.println(j.toString());
            out.flush();
        }
        System.out.println("Done.");
        
        echoSocket.close();
        in.close();
        out.close();          
    }
}
