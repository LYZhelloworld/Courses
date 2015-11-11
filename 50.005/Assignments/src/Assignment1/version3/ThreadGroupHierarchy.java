package Assignment1.version3;

import java.util.Scanner;

public class ThreadGroupHierarchy {
	public static volatile Boolean signal_stopAllDummyThreads = false;
	
	public static void main(String[] args) {
		ThreadGroup alpha = new ThreadGroup("alpha");
		ThreadGroup beta = new ThreadGroup("beta");
		ThreadGroup theta = new ThreadGroup(alpha, "theta");
		ThreadGroup lambda = new ThreadGroup(alpha, "lambda");
		ThreadGroup sigma = new ThreadGroup(beta, "sigma");
		
		new Thread(alpha, new DummyThread(), "Thread-0").start();
		new Thread(alpha, new DummyThread(), "Thread-1").start();
		new Thread(alpha, new DummyThread(), "Thread-2").start();
		
		new Thread(beta, new DummyThread(), "Thread-3").start();
		
		new Thread(theta, new DummyThread(), "Thread-4").start();
		new Thread(theta, new DummyThread(), "Thread-5").start();
		
		new Thread(lambda, new DummyThread(), "Thread-6").start();
		
		new Thread(sigma, new DummyThread(), "Thread-7").start();
		
		Thread t = Thread.currentThread();
		ThreadGroup g = t.getThreadGroup();
		g = g.getParent(); //System
		
		String threadName;
		Scanner sc = new Scanner(System.in);
		System.out.print("Enter the name of the thread: ");
		threadName = sc.next();
		sc.close();
		
		String result = searchThread(threadName, g);
		if(result == null)
			System.out.println("The specified thread cannot be found.");
		else
			System.out.println(result);
		
		signal_stopAllDummyThreads = true;
	}
	
	public static String searchThread(String name, ThreadGroup g) {
		Thread[] threads = new Thread[g.activeCount()];
		g.enumerate(threads);
		for(Thread i: threads) {
			if(i != null) {
				if(i.getName().equals(name)) {
					return getThreadTrace(i);
				}
			}
		}
		
		ThreadGroup[] groups = new ThreadGroup[g.activeGroupCount()];
		g.enumerate(groups);
		for(ThreadGroup i: groups) {
			if(i != null) {
				return searchThread(name, i);
			}
		}
		
		return null;
	}
	
	public static String getThreadTrace(Thread t) {
		String result = "";
		ThreadGroup g = t.getThreadGroup();
		result = g.getName();
		g = g.getParent();
		
		for(; g != null; ) {
			result = g.getName() + "->" + result;
			g = g.getParent();
		}
		
		return result;
	}
}

class DummyThread implements Runnable {
	
	public void run() {
		for(; !ThreadGroupHierarchy.signal_stopAllDummyThreads; ){} //Infinite loop
	}
}
