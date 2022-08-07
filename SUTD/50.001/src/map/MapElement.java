package map;

import java.io.Serializable;

public abstract class MapElement implements Serializable {
	private static final long serialVersionUID = 2111211331955929700L;
	//Width and height of the element
	protected int width, height;
	//Type of the element (initialized in derived classes)
	protected ElementType type;
	//The coordinate of the top-left corner
	protected Coordinate startPoint;
	
	public MapElement(Coordinate startPoint, int width, int height) {
		if(width <=0 || height <= 0) throw new IllegalArgumentException("Width and height must be greater than 0.");
		this.width = width;
		this.height = height;
		this.startPoint = startPoint;
	}
	
	public int getWidth() {
		return this.width;
	}
	
	public int getHeight() {
		return this.height;
	}
	
	public Coordinate getStartPoint() {
		return this.startPoint;
	}
	
	public ElementType getType() {
		return this.type;
	}
	
	public boolean equals(MapElement o) {
		return (this.width == o.width && this.height == o.height &&
				this.type == o.type && this.startPoint.equals(o.startPoint));
	}
	
	//Whether a point is inside this area
	public boolean isInside(Coordinate point) {
		return (this.startPoint.getX() <= point.getX() && this.startPoint.getY() <= point.getY() &&
				this.width > point.getX() && this.height > point.getY());
	}
	
	//Whether another element is overlapping
	public boolean isOverlapping(MapElement e) {
		return !((e.startPoint.getX() < this.startPoint.getX()) ||
				(e.startPoint.getX() + e.width >= this.startPoint.getX() + this.width) ||
				(e.startPoint.getY() > this.startPoint.getY()) ||
				(e.startPoint.getY() + e.height <= this.startPoint.getY() + this.height));
	}
	
	public String toString() {
		String result = "";
		result += "(" + this.startPoint.getX() + "," + this.startPoint.getY() + "): ";
		if(this.type == ElementType.OBSTACLE) {
			result += "Obstacle, ";
		}
		result += this.width + "X" + this.height;
		return result;
	}
}
