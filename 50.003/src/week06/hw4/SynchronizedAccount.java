package week06.hw4;

import java.util.concurrent.atomic.AtomicInteger;

public class SynchronizedAccount {
	private AtomicInteger balance;
	
	/**
	 * Constructor with initial balance = 0
	 */
	public SynchronizedAccount() {
		this.balance = new AtomicInteger(0);
	}
	
	/**
	 * Constructor with initial balance given
	 * @param initialBalance
	 */
	public SynchronizedAccount(int initialBalance) {
		this.balance = new AtomicInteger(initialBalance);
	}
	
	/**
	 * Deposit a specific amount
	 * @param amount
	 */
	public synchronized void deposit(int amount) {
		if(amount < 0) throw new IllegalArgumentException("Amount must be positive integer.");
		
		synchronized(balance) {
			balance.addAndGet(amount);
		}
	}
	
	/**
	 * Withdraw a specific amount
	 * @param amount
	 * @return true if success; false if failure
	 */
	public synchronized boolean withdraw(int amount) {
		if(amount < 0) throw new IllegalArgumentException("Amount must be positive integer.");
		
		synchronized(balance) {
			if(balance.get() < amount)
				return false;
			else {
				balance.addAndGet(-amount);
				return true;
			}
		}
	}
	
	/**
	 * Check the balance
	 * @return balance
	 */
	public int checkBalance() {
		return balance.get();
	}
}
