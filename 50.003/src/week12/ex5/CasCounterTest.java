package week12.ex5;

import java.util.concurrent.atomic.AtomicInteger;

public class CasCounterTest {
	public static final int MAX_ROUND = 1000000000;
	
	public static void main(String[] args) {
		AtomicInteger a = new AtomicInteger(0);
		int i;
		
		long timeStart = System.currentTimeMillis();
		for(i = 1; i <= MAX_ROUND; ++i) {
			a.incrementAndGet();
		}
		long timeEnd = System.currentTimeMillis();
		
		System.out.println("AtomicInteger: " + (timeEnd - timeStart) + "ms");
		
		LockBasedCounter b = new LockBasedCounter(0);
		timeStart = System.currentTimeMillis();
		for(i = 1; i <= MAX_ROUND; ++i) {
			b.increment();
		}
		timeEnd = System.currentTimeMillis();
		
		System.out.println("LockBasedCounter: " + (timeEnd - timeStart) + "ms");
	}
}

class LockBasedCounter {
	private int i;
	
	public LockBasedCounter(int initialValue) {
		this.i = initialValue;
	}
	
	public LockBasedCounter() {
		this.i = 0;
	}
	
	public int increment() {
		synchronized(this) {
			++i;
		}
		return i;
	}
	
	public int get() {
		return i;
	}
}