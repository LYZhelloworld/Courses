package week09.ex4;

import java.util.concurrent.CountDownLatch;

public class CountDownLatchExercise {
	public static void main(String[] args) {
		java.util.Random r = new java.util.Random();
		String str = "";
		System.out.print("Initializing string...");
		for(int i = 0; i < 100000; ++i) {
			str += Character.toString((char) (65 + r.nextInt(6)));
		}
		System.out.println("Done.");
		
		SearchingThread threads[] = new SearchingThread[10];
		CountDownLatch latch = new CountDownLatch(7);
		
		for(int i = 0; i < 10; ++i) {
			threads[i] = new SearchingThread(10000 * i, 10000 * (i + 1), str, latch, i);
		}
		for(int i = 0; i < 10; ++i) {
			threads[i].start();
		}
		try {
			latch.await();
			System.out.println("Interrupting all threads...");
			for(int i = 0; i < 10; ++i) {
				threads[i].interrupt();
			}
			System.out.println("Seven Fs have been found.");
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}

class SearchingThread extends Thread {
	private CountDownLatch latch;
	private int start, stop;
	private int id;
	private String str;
	
	public SearchingThread(int start, int stop, String str, CountDownLatch latch, int ID) {
		this.start = start;
		this.stop = stop;
		this.latch = latch;
		this.str = str;
		this.id = ID;
		System.out.println("Thread " + this.id + " has been created.");
	}
	
	public void run() {
		System.out.println("Thread " + this.id + " is running. (" + this.start + "-" + this.stop + ")");
		for(int i = this.start; i < this.stop; ++i) {
			if(isInterrupted()) {
				System.out.println("Thread " + this.id + " has been interrupted.");
			}
			
			if(str.charAt(i) == 'F') {
				latch.countDown();
				System.out.println("Thread " + this.id + " has found an F.");
				return;
			}
		}
	}
}