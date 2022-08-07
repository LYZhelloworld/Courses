package week05.ex6;
import java.math.BigInteger;
import java.util.LinkedList;


public class FactorThread {
	private static final BigInteger REGION_SIZE = new BigInteger("1000000000000");
	private static BigInteger num = new BigInteger("1127451830576035879");
	public static SearchThread found = null;
	
	public static void main(String[] args) {
		long timeStart, timeEnd;
		LinkedList<SearchThread> threads = new LinkedList<SearchThread>();
		BigInteger start, end;
		int i = 0;
		start = getRegionStart(i, num);
		end = getRegionEnd(i, num);
		for(; start != null; ) {
			threads.add(new SearchThread(num, start, end));
			++i;
			start = getRegionStart(i, num);
			end = getRegionEnd(i, num);
		}
		
		timeStart = System.currentTimeMillis();
		
		for(SearchThread t: threads) {
			t.start();
		}
		
		for(; found == null; ) {
			Boolean allThreadsFinished = true;
			for(SearchThread t: threads) {
				if(t.isAlive()) {
					allThreadsFinished = false;
					break;
				}
			}
			if(!allThreadsFinished)
				continue;
			else
				break;
		}
		timeEnd = System.currentTimeMillis();
		
		for(SearchThread t: threads) {
			t.interrupt();
		}
		
		if(found != null) {
			BigInteger[] result = found.getResult();
			System.out.print(num.toString());
			System.out.print("=");
			System.out.print(result[0].toString());
			System.out.print("*");
			System.out.println(result[1].toString());
		}

		System.out.println("Time taken: " + (timeEnd - timeStart) + "ms");
	}
	
	private static BigInteger getRegionStart(int i, BigInteger MaxValue) {
		if(i == 0)
			return BigInteger.valueOf(2);
		else {
			if(REGION_SIZE.multiply(BigInteger.valueOf(i)).compareTo(MaxValue) < 0) {
				return REGION_SIZE.multiply(BigInteger.valueOf(i));
			} else {
				return null;
			}
		}
	}
	
	private static BigInteger getRegionEnd(int i, BigInteger MaxValue) {
		return getRegionStart(i + 1, MaxValue) != null ? getRegionStart(i + 1, MaxValue).subtract(BigInteger.ONE) : MaxValue.subtract(BigInteger.ONE);
	}
}

class SearchThread extends Thread {
	private BigInteger target, start, end;
	private BigInteger result1, result2;
	
	public SearchThread(BigInteger target, BigInteger start, BigInteger end) {
		this.target = target;
		this.start = start;
		this.end = end;
		this.result1 = null;
		this.result2 = null;
	}
	
	public void run() {
		//System.out.println("Thread(" + target.toString() + "," + start.toString() + "," + end.toString() + ") has been started.");
		for(BigInteger i = this.start; i.compareTo(this.end) < 0; i = i.add(BigInteger.ONE)) {
			if(this.isInterrupted()) return;
			if(this.target.remainder(i).equals(BigInteger.ZERO)) {
				FactorThread.found = this;
				this.result1 = i;
				this.result2 = this.target.divide(i);
				break;
			}
		}
		//System.out.println("Thread(" + target.toString() + "," + start.toString() + "," + end.toString() + ") has finished.");
	}
	
	public BigInteger[] getResult() {
		return new BigInteger[] {this.result1, this.result2};
	}
}
