package week09.ex1;

import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

public class HashMapExp {
	public static final int THREAD_COUNT = 16;
	
	public static void main(String[] args) throws Exception {
		Thread threads[] = new Thread[THREAD_COUNT];
		long startTime, endTime;
		
		startTime = System.currentTimeMillis();
		for(int i = 0; i < THREAD_COUNT; ++i) {
			threads[i] = new WorkerThread(new HashMap<String, Integer>());
		}
		for(int i = 0; i < THREAD_COUNT; ++i) {
			threads[i].start();
		}
		for(int i = 0; i < THREAD_COUNT; ++i) {
			threads[i].join();
		}
		endTime = System.currentTimeMillis();
		System.out.println("Normal: " + (endTime - startTime) + "ms");
		

		startTime = System.currentTimeMillis();
		for(int i = 0; i < THREAD_COUNT; ++i) {
			threads[i] = new SynchronizedWorkerThread(new HashMap<String, Integer>());
		}
		for(int i = 0; i < THREAD_COUNT; ++i) {
			threads[i].start();
		}
		for(int i = 0; i < THREAD_COUNT; ++i) {
			threads[i].join();
		}
		endTime = System.currentTimeMillis();
		System.out.println("Synchronized Map: " + (endTime - startTime) + "ms");
		

		startTime = System.currentTimeMillis();
		for(int i = 0; i < THREAD_COUNT; ++i) {
			threads[i] = new ConcurrentWorkerThread(new HashMap<String, Integer>());
		}
		for(int i = 0; i < THREAD_COUNT; ++i) {
			threads[i].start();
		}
		for(int i = 0; i < THREAD_COUNT; ++i) {
			threads[i].join();
		}
		endTime = System.currentTimeMillis();
		System.out.println("Concurrent Map: " + (endTime - startTime) + "ms");
	}
}

class WorkerThread extends Thread {    	      
    private Map<String, Integer> map = null;

    public WorkerThread(Map<String, Integer> map) {
          this.map = map;     
    }

    public void run() {                
          for (int i=0; i<500000; i++) {
                 // Return 2 integers between 1-1000000 inclusive
                 Integer newInteger1 = (int) Math.ceil(Math.random() * 1000000);
                 Integer newInteger2 = (int) Math.ceil(Math.random() * 1000000);                                           
                 // 1. Attempt to retrieve a random Integer element
                 map.get(String.valueOf(newInteger1));                       
                 // 2. Attempt to insert a random Integer element
                 map.put(String.valueOf(newInteger2), newInteger2);                
          }
    }
}

class SynchronizedWorkerThread extends Thread {    	      
    private Map<String, Integer> map = null;

    public SynchronizedWorkerThread(Map<String, Integer> map) {
          this.map = Collections.synchronizedMap(map);     
    }

    public void run() {                
          for (int i=0; i<500000; i++) {
                 // Return 2 integers between 1-1000000 inclusive
                 Integer newInteger1 = (int) Math.ceil(Math.random() * 1000000);
                 Integer newInteger2 = (int) Math.ceil(Math.random() * 1000000);                                           
                 // 1. Attempt to retrieve a random Integer element
                 map.get(String.valueOf(newInteger1));                       
                 // 2. Attempt to insert a random Integer element
                 map.put(String.valueOf(newInteger2), newInteger2);                
          }
    }
}

class ConcurrentWorkerThread extends Thread {    	      
    private ConcurrentHashMap<String, Integer> map = null;

    public ConcurrentWorkerThread(Map<String, Integer> map) {
          this.map = new ConcurrentHashMap<String, Integer>(map);     
    }

    public void run() {                
          for (int i=0; i<500000; i++) {
                 // Return 2 integers between 1-1000000 inclusive
                 Integer newInteger1 = (int) Math.ceil(Math.random() * 1000000);
                 Integer newInteger2 = (int) Math.ceil(Math.random() * 1000000);                                           
                 // 1. Attempt to retrieve a random Integer element
                 map.get(String.valueOf(newInteger1));                       
                 // 2. Attempt to insert a random Integer element
                 map.put(String.valueOf(newInteger2), newInteger2);                
          }
    }
}