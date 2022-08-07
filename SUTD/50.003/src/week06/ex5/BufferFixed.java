package week06.ex5;

import java.util.Random;

public class BufferFixed {
	public static void main (String[] args) throws Exception {
		Buffer buffer = new Buffer (10);
		MyProducer prod = new MyProducer(buffer);
		prod.start();
		MyConsumer cons = new MyConsumer(buffer);
		cons.start();
	}
}

class MyProducer extends Thread {
	private Buffer buffer;
	
	public MyProducer (Buffer buffer) {
		this.buffer = buffer;
	}
	
	public void run () {
		Random random = new Random();
		try {
			Thread.sleep(random.nextInt(1000));
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		
		buffer.addItem(new Object());
	}
}

class MyConsumer extends Thread {
	private Buffer buffer;
	
	public MyConsumer (Buffer buffer) {
		this.buffer = buffer;
	}
	
	public void run () {
		Random random = new Random();
		try {
			Thread.sleep(random.nextInt(1000));
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		
		buffer.removeItem();
	}
}

class Buffer {
	public int SIZE;	
	private Object[] objects;
	private int count = 0;

	public Buffer (int size) {
		SIZE = size;
		objects = new Object[SIZE];
	}
	
	public void addItem (Object object) {
		while (count >= SIZE) Thread.yield();
		synchronized (this) {
			objects[count] = object;
			count++;
		}		
	}
	
	public Object removeItem() {
		if (count > 0) {
			count--;
			return objects[count];
		}
		else {
			return null; 
		}		
	}
}