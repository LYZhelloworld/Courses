package week08.hw1;

import java.util.ArrayList;

//Restaurant class
public class Restaurant {
	private ArrayList<Meal> orderList;
	private ArrayList<Meal> completedList;
	
	private Waiter waiter;
	private ServingWaiter serving;
	private Cook cook;
	
	public Restaurant() {
		this.orderList = new ArrayList<Meal>();
		this.completedList = new ArrayList<Meal>();
		
		this.waiter = new Waiter(this);
		this.serving = new ServingWaiter(this);
		this.cook = new Cook(this);
	}
	
	/**
	 * Get the instance of a Waiter class
	 * @return instance of Waiter
	 */
	public Waiter callWaiter() {
		return this.waiter;
	}
	
	/**
	 * Add an order (meals) to the list
	 * @param order
	 */
	public void addOrder(ArrayList<Meal> order) {
		synchronized(orderList) {
			orderList.addAll(order);
		}
	}
	
	/**
	 * Get a meal from the list
	 * @return meal
	 */
	public Meal getOrder() {
		synchronized(orderList) {
			if(orderList.isEmpty()) return null;
			return orderList.remove(0);
		}
	}
	
	/**
	 * Add a cooked meal to the list
	 * @param m: meal to be added
	 */
	public void addCompletedMeal(Meal m) {
		synchronized(completedList) {
			completedList.add(m);
		}
	}
	
	/**
	 * Get a meal to be served
	 * @return meal
	 */
	public Meal serveOrder() {
		synchronized(completedList) {
			if(completedList.isEmpty()) return null;
			return completedList.remove(0);
		}
	}
	
	/**
	 * Close the restaurant
	 */
	public void close() {
		this.waiter.close();
		this.cook.close();
		this.serving.close();
		
		System.out.println("Done.");
	}
}