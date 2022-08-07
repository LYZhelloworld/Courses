package week08.ex1;

public class MyStackThreadSafe {
	private final int maxSize;
	private long[] stackArray;
	private int top; //invariant: top < stackArray.length && top >= -1	
	
	//pre-condition: s > 0
	//post-condition: maxSize == s && top == -1 && stackArray != null
	public MyStackThreadSafe(int s) { //Do we need "synchronized" for the constructor?
		maxSize = s;
	    stackArray = new long[maxSize];
	    top = -1;
	}
	
	//pre-condition: top+1 < maxSize
	//post-condition: top++, stackArray[top] == j
	public synchronized void push(long j) {
		while(isFull()) {
			try {
				wait();
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		
		stackArray[++top] = j;
		notifyAll();
	}

	//pre-condition: top >= 0
	//post-condition: stackArray[top] is removed, top--
	public synchronized long pop() {
		long toReturn; 
		
		while (isEmpty()) {
			try {
				wait();
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		
		toReturn = stackArray[top--];
		notifyAll();			
	    return toReturn;
	}
	
	//pre-condition: top > -1
	//post-condition: N/A
	public long peek() {
	    return stackArray[top];
	}

	//pre-condition: N/A
	//post-condition: N/A
	public boolean isEmpty() {
		return (top == -1);
	}
	
	//pre-condition: N/A
	//post-condition: N/A
	public boolean isFull() {
		return (top == maxSize - 1);
	}
}