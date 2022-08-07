package week11.ex3;

import junit.framework.TestCase;

//this class is thread safe
public class BoundedBufferTest<E> extends TestCase {	
	private static final long LOCKUP_DETECT_TIMEOUT = 1000;

	public void testIsEmptyWhenConstructued () {
		BoundedBuffer<Integer> bb = new BoundedBuffer<Integer>(10);
		assertTrue(bb.isEmpty());
		assertFalse(bb.isFull());
	}
	
	public void testIsFullAfterPuts () throws InterruptedException {
		BoundedBuffer<Integer> bb = new BoundedBuffer<Integer>(10);
		for (int i = 0; i < 10; i++) {
			bb.put(i);
		}
		
		assertTrue(bb.isFull());
		assertFalse(bb.isEmpty());
	}
	
	public void testTakeBlocksWhenEmpty () {
		final BoundedBuffer<Integer> bb = new BoundedBuffer<Integer>(10);
		Thread taker = new Thread() {
			public void run() {
				try {
					int unused = bb.take();
					fail();
				} catch (InterruptedException success) {} //if interrupted, the exception is caught here
			}
		};
		
		try {
			taker.start();
			Thread.sleep(LOCKUP_DETECT_TIMEOUT);
			taker.interrupt();
			taker.join(LOCKUP_DETECT_TIMEOUT);
			assertFalse(taker.isAlive()); //the taker should not be alive for some time
		} catch (Exception unexpected) {
			fail(); //it fails for other exceptions
		}
	}
	
	public static void main(String[] args) {
		new BoundedBufferTest<Integer>().testIsEmptyWhenConstructued();
		try {
			new BoundedBufferTest<Integer>().testIsFullAfterPuts();
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		new BoundedBufferTest<Integer>().testTakeBlocksWhenEmpty();
	}
}
