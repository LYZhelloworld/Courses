package week06.hw5;

import java.util.ArrayList;
import java.util.concurrent.Semaphore;

public class FruitMarket {
	private ArrayList<FruitQueue> queues;
	
	public FruitMarket() {
		queues = new ArrayList<FruitQueue>();
	}
	
	/**
	 * Farmer produce a kind of fruit.
	 * @param fruit
	 */
	public void produce(Fruit fruit) {
		for(FruitQueue q: queues) {
			if(q.getType().equals(fruit.getType())) {
				q.append(fruit);
				return;
			}
		}
		//No such queue
		throw new IllegalArgumentException("No such type of queue.");
	}
	
	/**
	 * Consumer consumes a kind of fruit.
	 * @param type
	 * @return the fruit consumed
	 */
	public Fruit consume(String type) {
		for(FruitQueue q: queues) {
			if(q.getType().equals(type)) {
				return q.pop();
			}
		}
		//No such queue
		throw new IllegalArgumentException("No such type of queue.");
	}
	
	/**
	 * Add a queue of a specific kind of fruit.
	 * If the specific kind of queue exists, no changes will be made.
	 * @param type
	 * @param capacity
	 */
	public void addQueue(String type, int capacity) {
		for(FruitQueue q: queues) {
			if(q.getType().equals(type)) {
				//Existed queue
				return;
			}
		}
		synchronized (queues) {
			queues.add(new FruitQueue(type, capacity));
		}
	}
	
	//A private class for fruit queue
	private class FruitQueue {
		private ArrayList<Fruit> queue;
		private Semaphore s_append, s_pop;
		private String type;
		
		public FruitQueue(String type, int capacity) {
			this.queue = new ArrayList<Fruit>();
			this.type = type;
			this.s_append = new Semaphore(capacity);
			this.s_pop = new Semaphore(0);
		}
		
		/**
		 * Add a new fruit to the queue
		 * @param item
		 */
		public void append(Fruit item) {
			if(!item.getType().equals(type)) throw new IllegalArgumentException("Wrong type of fruit.");
			
			try {
				s_append.acquire();
				queue.add(item);
				s_pop.release();
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		
		/**
		 * Remove a fruit from the queue
		 * @return
		 */
		public Fruit pop() {
			Fruit result = null;
			try {
				s_pop.acquire();
				result = queue.remove(0);
				s_append.release();
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			return result;
		}
		
		/**
		 * Get the type of the queue
		 * @return
		 */
		public String getType() {
			return type;
		}
	}
}

//Fruit class
abstract class Fruit {
	private String type;
	
	public Fruit(String type) {
		this.type = type;
	}
	
	public String getType() {
		return type;
	}
	
	public String toString() {
		return type;
	}
}

//Fruits
class AppleFruit extends Fruit {
	public AppleFruit() {
		super("Apple");
	}
}

class OrangeFruit extends Fruit {
	public OrangeFruit() {
		super("Orange");
	}
}

class GrapeFruit extends Fruit {
	public GrapeFruit() {
		super("Grape");
	}
}

class WatermelonFruit extends Fruit {
	public WatermelonFruit() {
		super("Watermelon");
	}
}