package week05.ex7;

public class Increment {
	public static final int NUMBEROFTHREADS = 10000;
	public static long value = 0;
	
	public static void main(String[] args) {
		IncrementerThread[] threads = new IncrementerThread[NUMBEROFTHREADS];
		for(int i = 0; i < threads.length; ++i) {
			threads[i] = new IncrementerThread();
		}
		for(int i = 0; i < threads.length; ++i) {
			threads[i].start();
		}
		for(int i = 0; i < threads.length; ++i) {
			try {
				threads[i].join();
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		System.out.println(value);
	}
}

class IncrementerThread extends Thread {
	public void run() {
		++Increment.value;
	}
}