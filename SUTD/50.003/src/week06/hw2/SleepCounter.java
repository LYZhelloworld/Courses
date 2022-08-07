package week06.hw2;

import java.util.Scanner;

public class SleepCounter {
	public static void main(String[] args) {
		CounterThread t = new CounterThread();
		t.start();
		
		Scanner sc = new Scanner(System.in);
		int i;
		do {
			i = sc.nextInt();
		}while(i != 0);
		
		t.interrupt();
		sc.close();
	}
}

class CounterThread extends Thread {
	private int n = 0;
	
	public void run() {
		while(!isInterrupted()) {
			++n;
			System.out.println(n);
			try {
				Thread.sleep(1000);
			} catch (InterruptedException e) {
				break;
			}
		}
		
		System.out.println("Counter stops at: " + n);
	}
}