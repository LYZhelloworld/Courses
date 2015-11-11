package week04.ex1;
import java.math.BigInteger;
import java.util.Scanner;


public class FactorPrime {
	public static void main(String[] args) {
		Scanner sc = new Scanner(System.in);
		BigInteger num, i, j = null;
		
		System.out.print("Input a semiprime: ");
		num = new BigInteger(sc.next());
		for(i = BigInteger.valueOf(2); i.compareTo(num) < 0; i = i.add(BigInteger.ONE)) {
			if(num.remainder(i).equals(BigInteger.ZERO)) {
				j = num.divide(i);
				break;
			}
		}
		if(j != null) {
			System.out.print(num.toString());
			System.out.print("=");
			System.out.print(i.toString());
			System.out.print("*");
			System.out.println(j.toString());
		}
	}
}
