package week08.ex3;

import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap; //this is thread-safe!
import java.util.concurrent.ConcurrentMap; //this is thread-safe!

//is this class thread-safe?
public class DelegatingTracker {
	private final ConcurrentMap<String, Point> locations;
	
	public DelegatingTracker(Map<String, Point> locations) {
		this.locations = new ConcurrentHashMap<String, Point>(locations);
	}
	
	public synchronized Map<String, Point> getLocations () {
		return Collections.unmodifiableMap(new HashMap<String, Point>(locations));
	}
	
	//is this an escape?
	public synchronized Point getLocation (String id) {
		//return locations.get(id);
		return new Point(locations.get(id));
	}
	
	public synchronized void setLocation (String id, int x, int y) {		
		if (!locations.containsKey(id)) {
			throw new IllegalArgumentException ("No such ID: " + id);			
		}
		
		locations.get(id).set(x, y);
	}
	
	//is this class not thread-safe?
	//is a Point object mutable?
	class Point {
		private int x, y;
		
		private Point (int[] a) { 
			this(a[0], a[1]);
		}
		
		public Point (Point p) {
			this(p.get());
		}
		
		public Point (int x, int y) {
			this.x = x;
			this.y = y;
		}
		
		public synchronized int[] get() {
			return new int[] {x, y};
		}
		
		public synchronized void set(int x, int y) {
			this.x = x;
			this.y = y;
		}
	}
}
