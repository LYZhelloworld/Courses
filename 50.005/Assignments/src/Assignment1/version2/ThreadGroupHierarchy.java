package Assignment1.version2;

import java.awt.Desktop;
import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;

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
		//System.out.println(getInfo(g));
		
		File file = new File("report.htm");
		try {
			file.createNewFile();
			System.out.println("See:\n\t" + file.getAbsolutePath() + "\nfor detailed information.");
			PrintWriter out = new PrintWriter(file);
			out.println("<html>");
			out.println("<head>");
			out.println("<title>Report of thread group</title>");
			out.println("<style>");
			out.println("table {width: 100%; border: 1px solid #000; border-collapse: collapse;}");
			out.println("td, th {border: 1px solid #000;}");
			out.println("</style>");
			out.println("</head>");
			out.println("<body>");
			
			out.println("<table style=\"width: 100%; border: 1px solid #000;\">");
			out.println("<tr><th>Thread Group</th><th>Threads</th><th>ID</th><th>State</th><th>Is Daemon</th><th>Priority</th></tr>");
			out.println(getInfo(g));
			out.println("</table>");
			
			out.println("</body>");
			out.println("</html>");
			
			out.close();
			
			Desktop.getDesktop().browse(file.toURI());
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		
	}
	
	public static String getInfo(ThreadGroup g) {
		String result = "";
		
		Thread[] threads = new Thread[g.activeCount()];
		g.enumerate(threads);
		int n = 0;
		for(Thread i: threads) {
			if(i != null && i.getThreadGroup().equals(g)) {
				result += (n == 0 ? "" : "<tr>") + getThreadInfo(i) + "</tr>";
				++n;
			}
		}
		result = "<tr><td rowspan=\"" + n + "\"><strong>" + g.getName() + "</strong><br/>Priority: " + g.getMaxPriority() + "</td>" + result;
		
		ThreadGroup[] groups = new ThreadGroup[g.activeGroupCount()];
		g.enumerate(groups, false);
		for(ThreadGroup i: groups) {
			if(i != null && i.getParent().equals(g)) result += getInfo(i);
		}
		
		return result;
	}
	
	public static String getThreadInfo(Thread t) {
		return "<td>" + t.getName() + "</td><td>" + t.getId() + "</td><td>" + t.getState() + "</td><td>" +
				t.isDaemon() + "</td><td>" + t.getPriority();
	}
}

class DummyThread implements Runnable {
	public static final long WAITING_TIME = 1000;
	
	public void run() {
		try {
			Thread.sleep(WAITING_TIME);
		} catch (InterruptedException e) {
			//
		}
	}
}
