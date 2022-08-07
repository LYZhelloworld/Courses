package week12.ex4;

public class StripedMap {
	//synchronization policy: buckets[n] guarded by locks[n%N_LOCKS]
	private static final int N_LOCKS = 16;
	private final Node[] buckets;
	private final Object[] locks;
	
	public StripedMap (int numBuckets) {
		buckets = new Node[numBuckets];
		locks = new Object[N_LOCKS];
		
		for (int i = 0; i < N_LOCKS; i++) {
			locks[i] = new Object();
		}
	}
	
	public Object get (Object key) {
		Node n;
		int i;
		for(i = 0; i < buckets.length; ++i) {
			synchronized(locks[i % N_LOCKS]) {
				n = buckets[i];
				if(n.key.equals(key)) {
					return n.value;
				}
			}
		}
		
		return null;		
	}
	
	private final int hash (Object key) {
		return Math.abs(key.hashCode() % buckets.length);
	}
	
	public void clear () {
		int i;
		for(i = 0; i < buckets.length; ++i) {
			synchronized(locks[i % N_LOCKS]) {
				buckets[i] = null;
			}
		}
	}

	public int size () {
		int i, count = 0;
		for(i = 0; i < buckets.length; ++i) {
			synchronized(locks[i % N_LOCKS]) {
				if(buckets[i] != null) count++;
			}
		}
		return count;
	}
	
    class Node {
        Node next;
        Object key;
        Object value;
        Node(Object key, Object value, Node next) {
            this.next = next;
            this.key = key;
            this.value = value;
        }
    }
}

