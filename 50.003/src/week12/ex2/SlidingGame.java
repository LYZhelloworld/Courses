package week12.ex2;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Queue;
import java.util.Set;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

public class SlidingGame {
	//The following models the class sliding game.
	//The following is the board setting.
	// 0 	1 	2 	
	// 3    4 	5 	
	// 6 	7   8 	
    public static void main (String[] args) throws Exception {
    	//int[] initialBoardConfig = new int[] {3,5,6,0,2,7,8,4,1}; 
    	//int[] initialBoardConfig = new int[] {5,0,6,4,7,3,2,8,1}; 
    	//int[] initialBoardConfig = new int[] {2,3,8,4,6,0,1,5,7}; 
       	int[] initialBoardConfig = new int[] {2,1,5,3,6,0,7,8,4}; 
       	List<int[]> trace = BFSSearch(new PuzzleNode(initialBoardConfig, null));
    	
    	if (trace == null) {
    		System.out.println ("No solution");
    	}
    	else {
    		System.out.println ("Solution Found");
    		for (int[] i: trace) {
        		System.out.println (toString(i));    			
    		}
    	}
    }
	
    public static List<int[]> BFSSearch(PuzzleNode init) {
    	Set<String> seen = new HashSet<String>();
    	Queue<PuzzleNode> working = new LinkedList<PuzzleNode>();
    	ExecutorService exec = Executors.newFixedThreadPool(10);
    	Map<Future<List<int[]>>, PuzzleNode> futures = new HashMap<Future<List<int[]>>, PuzzleNode>();
    	
    	working.offer(init);
    	
    	while (working.size() > 0) {
    		futures.clear();
    		
    		while(working.size() > 0) {
    			PuzzleNode current = working.poll();
    			String stringConfig = toString(current.config);
        		//System.out.println("exploring " + stringConfig);
        		if (!seen.contains(stringConfig)) {
                    seen.add(stringConfig);
                    if (isGoal(current.config)) {
                        List<int[]> result = current.getTrace();
                        exec.shutdown();
                        return result;
                    }
                    
                    futures.put(exec.submit(new Callable<List<int[]>>(){
						@Override
						public List<int[]> call() {
							return nextPositions(current.config);
						}
                    }), current);
        		}
    		}
    		
    		for(Future<List<int[]>> f: futures.keySet()) {
    			try {
					for (int[] next : f.get()) {
					    PuzzleNode child = new PuzzleNode(next, futures.get(f));
					    working.offer(child);
					}
				} catch (InterruptedException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				} catch (ExecutionException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
    		}
    	}
    	
    	return null;
    }
	
    private static boolean isGoal (int[] boardConfig) {
    	return boardConfig[0] == 1 && boardConfig[1] == 2 && boardConfig[2] == 3 && boardConfig[3] == 4 &&
    			boardConfig[4] == 5 && boardConfig[5] == 6 && boardConfig[6] == 7 && boardConfig[7] == 8 && boardConfig[8] == 0;
    }

    private static List<int[]> nextPositions (int[] boardConfig) {
    	int emptySlot = -1;
    	
    	for (int i = 0; i < boardConfig.length; i++) {
    		if (boardConfig[i] == 0) {
    			emptySlot = i;
    			break;
    		}
    	}
    	
    	List<int[]> toReturn = new ArrayList<int[]>();
    	
    	//the empty slot goes right
    	if (emptySlot != 2 && emptySlot != 5 && emptySlot != 8) {
    		int[] newConfig = boardConfig.clone(); 
    		newConfig[emptySlot]= newConfig[emptySlot+1];
    		newConfig[emptySlot+1]=0;
    		toReturn.add(newConfig);
    	}
    	//the empty slot goes left    	
    	if (emptySlot != 0 && emptySlot !=3 && emptySlot != 6) {
    		int[] newConfig = boardConfig.clone();     		
    		newConfig[emptySlot]=newConfig[emptySlot-1];
    		newConfig[emptySlot-1]=0;
    		toReturn.add(newConfig);
    	}
    	//the empty slot goes down   
    	if (emptySlot != 6 && emptySlot != 7 && emptySlot != 8) {
    		int[] newConfig = boardConfig.clone();     		    		
    		newConfig[emptySlot]=newConfig[emptySlot+3];
    		newConfig[emptySlot+3]=0;
    		toReturn.add(newConfig);
    	}
    	//the empty slot goes up 
    	if (emptySlot != 0 && emptySlot != 1 && emptySlot != 2) {
    		int[] newConfig = boardConfig.clone();     		    		
    		newConfig[emptySlot] = newConfig[emptySlot-3];
    		newConfig[emptySlot-3] = 0;
    		toReturn.add(newConfig);
    	}
    	
    	return toReturn;
    }
    
    private static String toString(int[] config) {
    	StringBuilder sb = new StringBuilder();
    	for (int i = 0; i < config.length; i++) {
    		sb.append(config[i]);
    	}
    	
    	return sb.toString();
    }
}

class PuzzleNode {
	final int[] config;
	final PuzzleNode prev;
	
	PuzzleNode(int[] config, PuzzleNode prev) {
		this.config = config;
		this.prev = prev;
	}
	
	List<int[]> getTrace() {
		List<int[]> solution = new LinkedList<int[]> ();
		for (PuzzleNode n = this; n.prev != null; n = n.prev) {
			solution.add(0, n.config);
		}
		
		return solution;
	}
}