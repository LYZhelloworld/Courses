package map;

import java.io.DataOutputStream;
import java.io.FileOutputStream;

//Test function
public class Main {
	public static void main(String[] args) throws Exception {
		Map m = new Map(8, 5);
		m.addElement(new MapObstacle(new Coordinate(1, 1), 3, 2));
		m.addElement(new MapObstacle(new Coordinate(3, 4), 2, 2));
		
		System.out.println(m.toString());
		
		byte[] b = MapParser.SerializeMap(m);
		Map newMap = MapParser.UnserializeMap(b);
		
		System.out.println(newMap);
		
		System.out.println("If two results are the same, the serialization process is successful.");
		
		//Writing part
		/*
		DataOutputStream out = new DataOutputStream(new 
                FileOutputStream("test.txt"));
		out.write(b);
		out.flush();
		out.close();
		*/
	}
}
