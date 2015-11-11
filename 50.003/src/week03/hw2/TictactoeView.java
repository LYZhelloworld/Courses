package week03.hw2;
import java.util.Scanner;


public class TictactoeView {
	
	public TictactoeView() {
		
	}
	
	public int putX() {
		Scanner sc = new Scanner(System.in);
		System.out.print("Put X at (0-8): ");
		return sc.nextInt();
	}
	
	public int putO() {
		Scanner sc = new Scanner(System.in);
		System.out.print("Put O at (0-8): ");
		return sc.nextInt();
	}
	
	public void printState(char[] states) {
		for(int i = 0; i < 9; ++i) {
			System.out.print(states[i]);
			if((i + 1) % 3 == 0) { //2, 5, 8
				System.out.println();
			} else {
				System.out.print(" ");
			}
		}
	}
	
	public void printWinner(char winner) {
		switch(winner) {
		case 'X':
			System.out.println("X wins.");
			break;
		case 'O':
			System.out.println("O wins.");
			break;
		case ' ':
			System.out.println("Draw.");
			break;
		}
	}
}
