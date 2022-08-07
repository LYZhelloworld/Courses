package week05.ex5;

public class MultiThreadSearch {
	public static boolean found = false;
	public static final int ARRAYSIZE = 5000;
	public static final int VALUETOBEFOUND = 4000;
	
	public static void main(String[] args) {
		int[] array = new int[ARRAYSIZE];
		for(int i = 0; i < ARRAYSIZE; ++i) {
			array[i] = i; //Initialization
		}
		
		Thread thread1 = new SearchThread(array, 0, ARRAYSIZE / 2, VALUETOBEFOUND, 1);
		Thread thread2 = new SearchThread(array, ARRAYSIZE / 2, ARRAYSIZE, VALUETOBEFOUND, 2);
		
		thread1.start();
		thread2.start();
		
		for(; found == false && (thread1.isAlive() && thread2.isAlive()); );
		
		thread1.interrupt();
		thread2.interrupt();
		
		System.out.println(found ? "The result has been found." : "The result cannot be found.");
	}
}

class SearchThread extends Thread {
	private int[] array;
	private int start, end, value, id;
	
	public SearchThread(int[] array, int start, int end, int value, int id) {
		this.array = array;
		this.start = start;
		this.end = end;
		this.value = value;
		this.id = id;
	}
	
	public void run() {
		System.out.println("Thread " + this.id + " started.");
		for(int i = start; i < end; ++i) {
			if(isInterrupted()) {
				System.out.println("Thread " + this.id + " is interrupted.");
				break;
			}
			if(this.array[i] == this.value) {
				System.out.println("Thread " + this.id + " has found the result.");
				MultiThreadSearch.found = true;
				break;
			}
		}
		System.out.println("Thread " + this.id + " finished successfully.");
	}
}