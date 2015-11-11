package week06.hw1;

public class PrintLetters {
	public static void main(String[] args) {
		StringBuffer buffer = new StringBuffer();
		LetterThread thread1 = new LetterThread('A', buffer);
		LetterThread thread2 = new LetterThread('B', buffer);
		LetterThread thread3 = new LetterThread('C', buffer);
		
		thread1.start();
		thread2.start();
		thread3.start();
		
		try {
			thread1.join();
			thread2.join();
			thread3.join();
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		System.out.println(buffer.toString());
	}
}

class LetterThread extends Thread {
	private char letter;
	private StringBuffer buffer;
	
	@Override
	public void run() {
		for(int i = 0; i < 100; ++i) {
			synchronized(buffer) {
				buffer.append(letter);
			}
		}
	}
	
	public LetterThread(char letter, StringBuffer buffer) {
		this.letter = letter;
		this.buffer = buffer;
	}
}