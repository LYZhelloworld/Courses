package Week3;

public class BankImpl implements Bank {
	private int numberOfCustomers;	// the number of customers
	private int numberOfResources;	// the number of resources

	private int[] available; 	// the available amount of each resource
	private int[][] maximum; 	// the maximum demand of each customer
	private int[][] allocation;	// the amount currently allocated
	private int[][] need;		// the remaining needs of each customer
	
	public BankImpl (int[] resources, int numberOfCustomers) {
		// TODO: set the number of resources
		this.numberOfResources = resources.length;

		// TODO: set the number of customers
		this.numberOfCustomers = numberOfCustomers;

		// TODO: set the value of bank resources to available
		this.available = resources.clone();

		// TODO: set the array size for maximum, allocation, and need
		this.maximum = new int[this.numberOfCustomers][this.numberOfResources];
		this.allocation = new int[this.numberOfCustomers][this.numberOfResources];
		this.need = new int[this.numberOfCustomers][this.numberOfResources];

	}
	
	public int getNumberOfCustomers() {
		// TODO: return numberOfCustomers
		return this.numberOfCustomers;
	}

	public void addCustomer(int customerNumber, int[] maximumDemand) {
		// TODO: initialize the maximum, allocation, need for this customer
		if(customerNumber < 0 || customerNumber >= this.numberOfCustomers) {
			throw new IllegalArgumentException("Invalid customer number.");
		}
		
		// TODO: check if the customer's maximum demand exceeds bank's available resource
		for(int i = 0; i < maximumDemand.length; ++i) {
			if(maximumDemand[i] > this.available[i]) {
				throw new IllegalArgumentException("Demand exceeds bank's avaliable resource.");
			}
		}

		// TODO: set value for maximum and need
		this.maximum[customerNumber] = maximumDemand.clone();
		this.need[customerNumber] = maximumDemand.clone();
	}

	public void getState() {
		// TODO: print available
		System.out.print("Avaliable: ");
		for(int i: this.available) {
			System.out.print(i);
			System.out.print(" ");
		}
		System.out.println();

		// TODO: print allocation
		System.out.println("Allocation:");
		for(int[] i: this.allocation) {
			for(int j: i) {
				System.out.print(j);
				System.out.print(" ");
			}
			System.out.println();
		}
		System.out.println();

		// TODO: print max
		System.out.println("Maximum:");
		for(int[] i: this.maximum) {
			for(int j: i) {
				System.out.print(j);
				System.out.print(" ");
			}
			System.out.println();
		}
		System.out.println();

		// TODO: print need
		System.out.println("Need:");
		for(int[] i: this.need) {
			for(int j: i) {
				System.out.print(j);
				System.out.print(" ");
			}
			System.out.println();
		}
		System.out.println();

	}

	public synchronized boolean requestResources(int customerNumber, int[] request) {
		if(customerNumber < 0 || customerNumber >= this.numberOfCustomers) {
			throw new IllegalArgumentException("Invalid customer number.");
		}
		// TODO: check if the state is safe or not
		if(!this.checkSafe(customerNumber, request))
			return false;

		// TODO: if it is safe, allocate the resources to customer customerNumber 
		for(int i = 0; i < request.length; ++i) {
			this.allocation[customerNumber][i] += request[i];
			this.need[customerNumber][i] -= request[i];
			this.available[i] -= request[i];
		}
		
		// TODO: return state
		return true;

	}

	public synchronized void releaseResources(int customerNumber, int[] release) {
		if(customerNumber < 0 || customerNumber >= this.numberOfCustomers) {
			throw new IllegalArgumentException("Invalid customer number.");
		}
		// TODO: release the resources from customer customerNumber 
		for(int i = 0; i < release.length; ++i) {
			this.allocation[customerNumber][i] -= release[i];
			this.available[i] += release[i];
		}

	}

	private synchronized boolean checkSafe(int customerNumber, int[] request) {
		// TODO: check if the state is safe
		if(customerNumber < 0 || customerNumber >= this.numberOfCustomers) {
			throw new IllegalArgumentException("Invalid customer number.");
		}
		
		// TODO: initialize a finish vector
		boolean[] finish = new boolean[this.numberOfCustomers];
		boolean possible = true;

		// TODO: copy the available matrix to temp_available
		int[] temp_avail = this.available.clone();
		
		// TODO: subtract request from temp_available
		for(int i = 0; i < this.numberOfResources; ++i) {
			temp_avail[i] -= request[i];
		}
		
		// TODO: temporarily subtract request from need
		// TODO: temporarily add request to allocation
		for(int i = 0; i < this.numberOfResources; ++i) {
			this.need[customerNumber][i] -= request[i];
		}
		for(int i = 0; i < this.numberOfResources; ++i) {
			this.allocation[customerNumber][i] += request[i];
		}
		
		// TODO: if customer request exceed maximum, return false
		while(possible) {
			possible = false;
			for(int ci = 0; ci < this.numberOfCustomers; ++ci) {
				if(!finish[ci]) {
					boolean temp_compare = true;
					for(int i = 0; i < this.numberOfResources; ++i) {
						if(this.need[ci][i] > temp_avail[i]) {
							temp_compare = false;
							break;
						}
					}
					if(temp_compare) {
						possible = true;
						for(int i = 0; i < this.numberOfResources; ++i) {
							temp_avail[i] += this.allocation[ci][i];
						}
						finish[ci] = true;
					}
				}
			}
		}

		// TODO: check if the Bank's algorithm can finish based on safety algorithm
		// (see P332, Section 7.5.3.1, Operating System Concepts with Java, Eighth Edition)
		// TODO: restore the value of need and allocation for the customer
		for(int i = 0; i < this.numberOfResources; ++i) {
			this.need[customerNumber][i] += request[i];
		}
		for(int i = 0; i < this.numberOfResources; ++i) {
			this.allocation[customerNumber][i] -= request[i];
		}
		
		// TODO: go through the finish to see if all value is true
		for(boolean i: finish) {
			if(!i) {
				return false;
			}
		}
		// TODO: return state
		return true;
	}
}