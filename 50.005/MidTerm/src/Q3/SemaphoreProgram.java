package Q3;

import java.util.ArrayList;
import java.util.Date;
import java.util.concurrent.Semaphore;

public class SemaphoreProgram {
	public static void main(String[] args) {
		Buffer b = new Buffer();
		Producer p1 = new Producer(b, 1);
		Producer p2 = new Producer(b, 2);
		Producer p3 = new Producer(b, 3);
		Producer p4 = new Producer(b, 4);
		Consumer c = new Consumer(b);
		
		p1.start();
		p2.start();
		p3.start();
		p4.start();
		c.start();
	}
}

class Producer extends Thread {
	private Buffer buffer;
	private int index;
	
	public Producer(Buffer b, int index) {
		buffer = b;
		this.index = index;
	}
	
	public void run() {
		for(;;) {
			buffer.produce(new Date(), this.index);
			try {
				Thread.sleep((int)(Math.random() * 10000));
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	}
}

class Consumer extends Thread {
	private Buffer buffer;
	
	public Consumer(Buffer b) {
		buffer = b;
	}
	
	public void run() {
		for(;;) {
			buffer.consume();
			try {
				Thread.sleep((int)(Math.random() * 10000));
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	}
}

class Buffer {
	public static final int BUFFER_SIZE = 3;
	
	private Semaphore p = new Semaphore(BUFFER_SIZE);
	private Semaphore c = new Semaphore(0);
	private ArrayList<Date> buffer = new ArrayList<Date>();
	
	public void produce(Date d, int index) {
		System.out.println("Producer " + index + " thread wishes to insert date and time");
		try {
			p.acquire();
			buffer.add(d);
			c.release();
			System.out.println("Insert item into buffer: " + d.toString());
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	public Date consume() {
		Date result = null;
		try {
			c.acquire();
			result = buffer.remove(0);
			p.release();
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return result;
	}
}