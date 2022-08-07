package week08.hw1;

public class ServingWaiter {
	private Restaurant restaurant;
	private ServingThread t;
	
	/**
	 * Create a ServingWaiter instance
	 * @param r: Restaurant where he/she works
	 */
	public ServingWaiter(Restaurant r) {
		this.restaurant = r;
		this.t = new ServingThread(this.restaurant);
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

class ServingThread extends Thread {
	private Restaurant restaurant;
	
	public ServingThread(Restaurant r) {
		this.restaurant = r;
	}
	
	public void run() {
		Meal m;
		
		while(!isInterrupted()) {
			//Fetch a meal to be served
			if((m = this.restaurant.serveOrder()) == null) continue;
			System.out.println("\'" + m.getName() + "\' is served.");
		}
	}
}
