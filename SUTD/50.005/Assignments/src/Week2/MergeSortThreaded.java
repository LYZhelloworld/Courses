package Week2;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Iterator;
import java.util.PriorityQueue;
import java.util.Scanner;
import java.util.Set;

/**
 * @author 1000800
 * code reference: http://karmaandcoding.blogspot.sg/2012/02/merge-n-sorted-listsarrays.html
 */
public class MergeSortThreaded {
	static int NumOfThread = 5000;
	private static int TOTAL = 50;

	public static void main(String[] args) throws InterruptedException, FileNotFoundException {

		// read data from txt
		Scanner fileIn = new Scanner(new File("src//Week2//input_2.txt"));
		ArrayList<Integer> array = new ArrayList<Integer>();
		while(fileIn.hasNextInt()){
			array.add(fileIn.nextInt());
		}
		fileIn.close();
		// TODO: partition the array into N part
		int sizeOfSubArray = (int)Math.ceil(array.size() / (float)NumOfThread);
		ArrayList<MergeThread> threads = new ArrayList<MergeThread>();
		for(int i = 0; i < array.size() ; i += sizeOfSubArray) {
			if(i + sizeOfSubArray > array.size()) {
				threads.add(new MergeThread(new ArrayList<Integer>(array.subList(i, array.size()))));
			} else {
				threads.add(new MergeThread(new ArrayList<Integer>(array.subList(i, i + sizeOfSubArray))));
			}
		}

		// TODO: start recording time
		long startTime = System.currentTimeMillis();

		// TODO: run MergeThread with N threads
		for(MergeThread t: threads) {
			t.start();
		}

		// TODO: merge the N sorted array
		HashMap<String, ArrayList<Integer>> map = new HashMap<String, ArrayList<Integer>>();
		int i = 0;
		for(MergeThread t: threads) {
			t.join();
		}
		for(MergeThread t: threads) {
			map.put(String.valueOf(i), t.getInternal());
			++i;
		}

		// TODO: get the final sorted list
		ArrayList<Integer> result = mergeArrays(map);

		// TODO: end recording time
		long endTime = System.currentTimeMillis();

		// TODO: show the time
		//System.out.println(result);
		System.out.print("Sorted ");
		System.out.print(result.size());
		System.out.println(" element(s) successfully.");
		System.out.print("Execution time: ");
		System.out.print(endTime - startTime);
		System.out.println("ms");

	}

	// function to merge the N sorted arrays
	public static ArrayList<Integer> mergeArrays(HashMap<String, ArrayList<Integer>> arrayMap) {
		ArrayList<Integer> mergedList = new ArrayList<Integer>();
		Set<String> keySet = arrayMap.keySet();
		Comparator<Node> comparator = new NumericComparator();
		PriorityQueue<Node> minHeap = new PriorityQueue<Node>(TOTAL, comparator);

		Iterator<String> iter = keySet.iterator();
		while (iter.hasNext()) {
			String key = iter.next();
			ArrayList<Integer> list = arrayMap.get(key);
			if (list != null) {
				Integer data = list.remove(0);
				Node node = new Node(data, key);
				minHeap.add(node);
			}
		}

		while (minHeap.size() > 0) {
			Node node = minHeap.remove();
			//System.out.print(node.data + " ");
			mergedList.add(node.data);
			String id = node.id;
			ArrayList<Integer> list = arrayMap.get(id);
			if (list != null && list.size() > 0) {
				Integer data = list.remove(0);
				Node newNode = new Node(data, id);
				minHeap.add(newNode);
			}
		}

		return mergedList;

	}

}

// extend thread
class MergeThread extends Thread {
	private ArrayList<Integer> list;

	public ArrayList<Integer> getInternal() {
		return list;
	}

	// TODO: implement merge sort here
	private ArrayList<Integer> MergeSort(ArrayList<Integer> array) {
		if(array.size() == 1) {
			return array;
		} else {
			ArrayList<Integer> a = MergeSort(new ArrayList<Integer>(array.subList(0, array.size() / 2)));
			ArrayList<Integer> b = MergeSort(new ArrayList<Integer>(array.subList(array.size() / 2, array.size())));
			return CombineArrays(a, b);
		}
	}
	
	private ArrayList<Integer> CombineArrays(ArrayList<Integer> a, ArrayList<Integer> b) {
		int i, j;
		ArrayList<Integer> result = new ArrayList<Integer>();
		for(i = 0, j = 0; i < a.size() && j < b.size();) {
			if(a.get(i) < b.get(j)) {
				result.add(a.get(i));
				++i;
			} else {
				result.add(b.get(j));
				++j;
			}
		}
		for(; i < a.size(); ++i) {
			result.add(a.get(i));
		}
		for(; j < b.size(); ++j) {
			result.add(b.get(j));
		}
		return result;
	}

	MergeThread(ArrayList<Integer> array) {
		list = array;
	}

	public void run() {
		// TODO: implement actions here
		list = MergeSort(list);
	}
}

class Node {
	int data;
	String id;
	Node(int data, String key) {
		this.data = data;
		this.id = key;
	}
}

class NumericComparator implements Comparator<Node> {

	public int compare(Node o1, Node o2) {
		if (o1.data < o2.data) {
			return -1;
		} else if (o1.data > o2.data) {
			return 1;
		} 
		return 0;
	}
}