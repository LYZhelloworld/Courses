package week08.ex5;

import java.util.Collections;
import java.util.Vector;


public class FirstExample {
	public static Object getLast(Vector list) {
		java.util.List l = Collections.synchronizedList(list);
		synchronized(l) {
			int lastIndex = l.size()-1;
			if(lastIndex == -1)
				return null;
			else
				return l.get(lastIndex);
		}
	}

	public static void deleteLast(Vector list) {
		java.util.List l = Collections.synchronizedList(list);
		synchronized(l) {
			int lastIndex = l.size()-1;
			if(lastIndex != -1)
				l.remove(lastIndex);
		}
		
	}	

	public static boolean contains(Vector list, Object obj) {
		java.util.List l = Collections.synchronizedList(list);
		synchronized(l) {
			for (int i = 0; i < l.size(); i++) {
				if (l.get(i).equals(obj)) {
					return true;
				}
			}
			
			return false;
		}
	}
}
