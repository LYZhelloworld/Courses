package Assignment1.version1;

public class ThreadGroupHierarchy {
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
		System.out.println(getInfo(g));
	}
	
	public static String getInfo(ThreadGroup g) {
		String result;
		result = "Group: " + g.getName() + " Priority: " + g.getMaxPriority() + "\n";
		Thread[] threads = new Thread[g.activeCount()];
		g.enumerate(threads);
		for(Thread i: threads) {
			if(i != null && i.getThreadGroup().equals(g)) result += "\t" + getThreadInfo(i) + "\n";
		}
		
		ThreadGroup[] groups = new ThreadGroup[g.activeGroupCount()];
		g.enumerate(groups, false);
		for(ThreadGroup i: groups) {
			if(i != null && i.getParent().equals(g)) result += getInfo(i);
		}
		
		return result;
	}
	
	public static String getThreadInfo(Thread t) {
		return t.getName() + ":" + t.getId() + ":" + t.getState() + ":" +
				t.isDaemon() + " Priority:" + t.getPriority();
	}
}

class DummyThread implements Runnable {
	public static final long WAITING_TIME = 5000;
	
	public void run() {
		try {
			Thread.sleep(WAITING_TIME);
		} catch (InterruptedException e) {
			//
		}
	}
}
