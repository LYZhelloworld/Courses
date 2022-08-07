package week04.hw4;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

public class TictactoeViewSocket extends TictactoeView {
	
	private PrintWriter outX;
	private BufferedReader inX;
	private PrintWriter outO;
	private BufferedReader inO;
	
	public TictactoeViewSocket(Socket clientX, Socket clientO) {
		super();
		
		try {
			this.outX =
	                new PrintWriter(clientX.getOutputStream(), true);                   
	        this.inX = new BufferedReader(
	                new InputStreamReader(clientX.getInputStream()));
	        this.outO =
	                new PrintWriter(clientO.getOutputStream(), true);                   
	        this.inO = new BufferedReader(
	                new InputStreamReader(clientO.getInputStream()));
		} catch(IOException e) {
			e.printStackTrace();
		}
		
	}
	
	public int putX() {
		outX.println("Put X at (0-8): ");
		outX.flush();
		try {
			return Integer.parseInt(inX.readLine());
		} catch (NumberFormatException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return -1;
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return -1;
		}
	}
	
	public int putO() {
		outO.println("Put O at (0-8): ");
		outO.flush();
		try {
			return Integer.parseInt(inO.readLine());
		} catch (NumberFormatException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return -1;
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return -1;
		}
	}
	
	public void printState(char[] states) {
		outX.println("State:");
		for(int i = 0; i < 9; ++i) {
			outX.print(states[i]);
			if((i + 1) % 3 == 0) { //2, 5, 8
				outX.println();
			} else {
				outX.print(" ");
			}
		}
		outX.flush();
		
		outO.println("State:");
		for(int i = 0; i < 9; ++i) {
			outO.print(states[i]);
			if((i + 1) % 3 == 0) { //2, 5, 8
				outO.println();
			} else {
				outO.print(" ");
			}
		}
		outO.flush();
	}
	
	public void printWinner(char winner) {
		switch(winner) {
		case 'X':
			outX.println("Winner:");
			outX.println("X wins.");
			outX.flush();
			outO.println("Winner:");
			outO.println("X wins.");
			outO.flush();
			break;
		case 'O':
			outX.println("Winner:");
			outX.println("O wins.");
			outX.flush();
			outO.println("Winner:");
			outO.println("O wins.");
			outO.flush();
			break;
		case ' ':
			outX.println("Winner:");
			outX.println("Draw.");
			outX.flush();
			outO.println("Winner:");
			outO.println("Draw.");
			outO.flush();
			break;
		}
	}
}
