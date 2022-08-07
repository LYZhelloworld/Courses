package week08.ex6;

public class SafeStack<E> extends java.util.Stack<E> {
	private final int maxSize;
		
	public SafeStack(int maxSize) {
		this.maxSize = maxSize;
	}
	
	public synchronized void pushIfNotFull(E e) {
		if(super.capacity() < maxSize) {
			super.push(e);
		} else {
			//Full
		}
	}
	
	public synchronized E popIfNotEmpty() {
		E result = null;
		try {
			result = super.pop();
		} catch(java.util.EmptyStackException e) {
			//
		}
		return result;
	}
}
