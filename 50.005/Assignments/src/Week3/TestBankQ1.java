package Week3;

// test code for Banker's algorithm
public class TestBankQ1 {
	public static void main(String[] args){
		/*--------------Test case for Q1--------------*/
		/* Check one case */
		// initialize a bank
		// set the bank resource
		int[] resource1 = {10, 5, 7};
		// create a bank based on the resource
		Bank theBank1 = new BankImpl(resource1, 5);
		// add customers
		// get customer maximum demand
		int[][] maximum1 = {
				{7, 5, 3}, 
				{3, 2, 2}, 
				{9, 0, 2},
				{2, 2, 2},
				{4, 3, 3},
		};
		// get the number of customers for the bank
		int numberCustomer1 = theBank1.getNumberOfCustomers();
		// add each customer
		for (int i = 0; i < numberCustomer1; i++){
			theBank1.addCustomer(i, maximum1[i]);
		}
		/* Check one safe state */
		// request resource
		int[] request1_0 = {0, 1, 0};
		int[] request1_1 = {2, 0, 0};
		int[] request1_2 = {3, 0, 2};
		int[] request1_3 = {2, 1, 1};
		int[] request1_4 = {0, 0, 2};
		theBank1.requestResources(0, request1_0);
		theBank1.requestResources(1, request1_1);
		theBank1.requestResources(2, request1_2);
		theBank1.requestResources(3, request1_3);
		theBank1.requestResources(4, request1_4);
		// show the bank state
		theBank1.getState();
	}
}
