package week08.hw1;

public class Main {
	public static void main(String[] args) {
		Restaurant r = new Restaurant();
		
		//Call waiter
		Waiter w = r.callWaiter();
		//Order set 1
		w.order(new Set1());
		//Order set 2
		w.order(new Set2());
		//Send
		w.sendOrder();
		
		//Wait a moment...
		try {
			Thread.sleep(4000);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		//Order set 3
		w.order(new Set3());
		//Send
		w.sendOrder();
		
		//Wait...
		try {
			Thread.sleep(10000);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		//Done
		r.close();
	}
}
