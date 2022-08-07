package week08.ex1;

public class MyStack {
	private final int maxSize;
	private long[] stackArray;
	private int top; 
	private Object lock;
	
	public MyStack(int s) { //Do we need "synchronized" for the constructor?
		maxSize = s;
	    stackArray = new long[maxSize];
	    top = -1;
	    lock = new Object();
	}
	
	public void push(long j) {
		if(isFull()) {
			try {
				wait();
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		synchronized(lock) {
			stackArray[++top] = j;
		}
	}

	public long pop() {	
		if(isEmpty()) {
			try {
				wait();
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		synchronized(lock) {
			return stackArray[top--];
		}
	}
	
	public long peek() {
	    return stackArray[top];
	}

	public boolean isEmpty() {
		return (top == -1);
	}
	
	public boolean isFull() {
		return (top == maxSize - 1);
	}
}