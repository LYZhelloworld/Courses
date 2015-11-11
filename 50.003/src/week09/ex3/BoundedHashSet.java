package week09.ex3;

import java.util.Collections;
import java.util.HashSet;
import java.util.Set;
import java.util.concurrent.Semaphore;

public class BoundedHashSet<T> {	
	private final Set<T> set;
	private Semaphore addingSemaphore;
	private Semaphore removingSemaphore;
	
	public BoundedHashSet (int bound) {
		this.set = Collections.synchronizedSet(new HashSet<T>());
		this.addingSemaphore = new Semaphore(bound);
		this.removingSemaphore = new Semaphore(0);
	}
	
	public boolean add(T o) throws InterruptedException {
		this.addingSemaphore.acquire();
		boolean result = set.add(o);
		this.removingSemaphore.release();
		return result;
	}
	
	public boolean remove (Object o) throws InterruptedException {
		this.removingSemaphore.acquire();
		boolean result = set.remove(o);
		this.addingSemaphore.release();
		return result;
	}
}