package week08.hw1;

public class Cook {
	private Restaurant restaurant;
	private CookingThread t;
	
	/**
	 * Create a Cook instance
	 * @param r: Restaurant where he/she works
	 */
	public Cook(Restaurant r) {
		this.restaurant = r;
		t = new CookingThread(this.restaurant);
		t.start();
	}
	
	/**
	 * Terminate everything
	 */
	public void close() {
		if(this.t != null) {
			this.t.interrupt();
		}
	}
}

class CookingThread extends Thread {
	private Restaurant restaurant;
	
	public CookingThread(Restaurant r) {
		this.restaurant = r;
	}
	
	public void run() {
		Meal m;
		
		while(!isInterrupted()) {
			//Fetch a meal to be cooked
			if((m = this.restaurant.getOrder()) == null) continue;
			
			//Cook it
			if(!m.cook()) {
				//Failed
				System.out.println("The cooking process of \'" + m.getName() + "\' is interrupted.");
				continue;
			}
			
			//Succeeded
			//Put it into the list
			this.restaurant.addCompletedMeal(m);
		}
	}
}