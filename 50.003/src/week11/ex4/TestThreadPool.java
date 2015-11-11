package week11.ex4;

import java.util.concurrent.*;
import junit.framework.TestCase;

public class TestThreadPool extends TestCase {
	
    public void testPoolExpansion() throws InterruptedException {
        int max_pool_size = 10;
        ExecutorService exec = Executors.newFixedThreadPool(max_pool_size);

       
        //todo: insert your code here to complete the test case
        //hint: you can use the following code to get the number of active threads in a thread pool
        /*int numThreads = 0;
        if (exec instanceof ThreadPoolExecutor) {
        	numThreads = ((ThreadPoolExecutor) exec).getActiveCount();
        }*/
        exec.shutdownNow();
    }
}
