package Week2;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Scanner;

public class MultiThread {
	static int NumOfThread = 10;
	public static void main(String[] args) throws InterruptedException {
		// read data from txt
		Scanner fileIn;
		try {
			fileIn = new Scanner(new File("src//Week2//input_2.txt"));
			ArrayList<Integer> array = new ArrayList<Integer>();
			while(fileIn.hasNextInt()){
				array.add(fileIn.nextInt());
			}
			fileIn.close();
			// TODO: partition the array list into N part
			int sizeOfSubArray = (int)Math.ceil(array.size() / (float)NumOfThread);
			ArrayList<SimpleThread> threads = new ArrayList<SimpleThread>();
			for(int i = 0; i < array.size() ; i += sizeOfSubArray) {
				if(i + sizeOfSubArray > array.size()) {
					threads.add(new SimpleThread(new ArrayList<Integer>(array.subList(i, array.size()))));
				} else {
					threads.add(new SimpleThread(new ArrayList<Integer>(array.subList(i, i + sizeOfSubArray))));
				}
			}

			// TODO: run SimpleThread with N threads
			for(SimpleThread t: threads) {
				t.start();
			}

			// TODO: get the N max value
			for(SimpleThread t: threads) {
				t.join();
			}
			ArrayList<Integer> maxValues = new ArrayList<Integer>();
			for(SimpleThread t: threads) {
				maxValues.add(t.getMax());
			}

			// TODO: show the N max value
			for(int i: maxValues) {
				System.out.print(i);
				System.out.print(" ");
			}
			System.out.println();

			// TODO: get the max value from N max values
			SimpleThread finalThread = new SimpleThread(maxValues);
			finalThread.run();
			finalThread.join();

			// TODO: show the max value
			System.out.println(finalThread.getMax());
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}
}

//extend thread
class SimpleThread extends Thread {
	private ArrayList<Integer> list;
	private int max;

	public int getMax() {
		return max;
	}

	SimpleThread(ArrayList<Integer> array) {
		list = array;
	}

	public void run() {
		// TODO: implement actions here
		max = Integer.MIN_VALUE;
		for(int i: list) {
			if(i > max) max = i;
		}
	}
}