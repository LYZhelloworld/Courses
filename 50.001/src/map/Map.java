package map;

import java.io.Serializable;
import java.util.ArrayList;

public class Map implements Serializable {
	private static final long serialVersionUID = 7824972083064541323L;
	
	//Width and height of the map
	private int width, height;
	//Elements in the map;
	private ArrayList<MapElement> elements;
	
	public Map(int width, int height) {
		this.width = width;
		this.height = height;
		this.elements = new ArrayList<MapElement>();
	}
	
	//Cloning function
	public Map(Map m) {
		this.width = m.width;
		this.height = m.height;
		this.elements = new ArrayList<MapElement>(m.elements);
	}
	
	//Add an element
	public void addElement(MapElement e) throws ElementsOverlappingException {
		synchronized(elements) {
			for(MapElement i: this.elements) {
				if(i.isOverlapping(e)) {
					throw new ElementsOverlappingException("Elements cannot overlap.");
				}
			}
			this.elements.add(e);
		}
	}
	
	
	public boolean removeElement(MapElement e) {
		synchronized(elements) {
			return this.elements.remove(e);
		}
	}
	
	public ElementType getType(Coordinate point) {
		//Point must be inside the map
		if(point.getX() >= this.width || point.getY() >= this.height) throw new IllegalArgumentException("Invalid point coordinate.");
		ElementType result = ElementType.BLANK;
		
		for(MapElement i: this.elements) {
			if(i.isInside(point)) {//Found
				result = i.type;
			}
		}
		
		return result;
	}
	
	public String toString() {
		String result = "";
		result += "Width: " + this.width + "; Height: " + this.height + "\n";
		for(MapElement i: this.elements) {
			result += i.toString() + "\n";
		}
		return result;
	}
}

class ElementsOverlappingException extends Exception {
	private static final long serialVersionUID = -7010251667418134498L;

	public ElementsOverlappingException(String msg) {
		super(msg);
	}
}
