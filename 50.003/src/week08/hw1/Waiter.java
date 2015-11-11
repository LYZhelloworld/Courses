package week08.hw1;

import java.util.ArrayList;

public class Waiter {
	private ArrayList<Meal> orderList;
	private Restaurant restaurant;
	private ArrayList<WaiterThread> threads;
	
	/**
	 * Create a Waiter instance
	 * @param r: Restaurant where he/she works
	 */
	public Waiter(Restaurant r) {
		this.orderList = null;
		this.restaurant = r;
		this.threads = new ArrayList<WaiterThread>();
		this.orderList = new ArrayList<Meal>();
	}
	
	/**
	 * Customer orders a meal
	 * @param m: meal
	 */
	public void order(Meal m) {
		orderList.add(m);
	}
	
	/**
	 * Send the order to the restaurant (asynchronously)
	 */
	public void sendOrder() {
		String result = "Ordered:\n";
		for(Meal i: this.orderList) {
			result += "\t" + i.getName();
		}
		System.out.println(result);
		
		WaiterThread t = new WaiterThread(this.restaurant, this.orderList);
		threads.add(t);
		t.start();
		
		this.orderList = new ArrayList<Meal>();
	}
	
	/**
	 * Terminate everything
	 */
	public void close() {
		for(WaiterThread i: threads) {
			if(i != null) {
				if(i.getState() != Thread.State.TERMINATED) {
					i.interrupt();
				}
			}
		}
	}
}

class WaiterThread extends Thread {
	private Restaurant restaurant;
	private ArrayList<Meal> list;
	
	public WaiterThread(Restaurant r, ArrayList<Meal> list) {
		this.restaurant = r;
		this.list = list;
	}
	
	public void run() {
		this.restaurant.addOrder(list);
	}
}
