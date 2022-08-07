package Q2;

public class WaitThread {
	public static void main(String[] args) {
		PrintZ thread1 = new PrintZ();
		PrintNumber thread2 = new PrintNumber(thread1);
		
		thread2.start();
		thread1.start();
	}
}

class PrintNumber extends Thread {
	private Thread zThread;
	
	public PrintNumber(Thread zThread) {
		this.zThread = zThread;
	}
	
	public void run() {
		for(int i = 1; i <= 3; ++i) {
			if(i == 3)
				try {
					zThread.join();
				} catch (InterruptedException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			System.out.print(i);
		}
	}
}

class PrintZ extends Thread {
	public void run() {
		for(int i = 0; i < 3; ++i) {
			System.out.print("z");
		}
	}
}