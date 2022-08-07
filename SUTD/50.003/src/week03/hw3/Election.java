package week03.hw3;
import java.util.Scanner;

public class Election {
	public static void main(String[] args) {
		Scanner sc = new Scanner(System.in);
		String input;
		int candA = 0, candB = 0;
		
		for(int i = 1; i <= 5; ++i) {
			for(;;) {
				System.out.print("Electorate ");
				System.out.print(i);
				System.out.print(", choose (A or B): ");
				input = sc.next();
				if(input.equals("A")) {
					++candA;
					break;
				} else if(input.equals("B")) {
					++candB;
					break;
				}
			}
		}
		
		if(candA > candB) {
			System.out.println("Candidate A wins.");
		} else {
			System.out.println("Candidate B wins.");
		}
	}
}
