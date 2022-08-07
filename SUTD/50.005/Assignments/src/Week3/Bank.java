package Week3;

public interface Bank {
	/**
	 * Add a customer
	 * @param customerNumber - the number of the customer
	 * @param maximumDemand - the maximum demand for this customer
	 */
	public void addCustomer(int customerNumber, int[] maximumDemand);
	
	/**
	 * Output the value of available, maximum,
	 * allocation, and need
	 */
	public void getState();
	
	/**
	 * Request resources
	 * If the request is not granted, this method should print the error message
	 * @param customerNumber - the customer requesting resources
	 * @param request - the resources being requested
	 * @return grant state - whether granting the request leaves the system in safe or unsafe state
	 */
	public boolean requestResources(int customerNumber, int[] request);
	
	/**
	 * Release resources
	 * @param customerNumber - the customer releasing resources
	 * @param release - the resources being released
	 */
	public void releaseResources(int customerNumber, int[] release);
	
	/**
	 * Get number of customers
	 * @return numberCustomer - number of customers
	 */
	public int getNumberOfCustomers();
}
