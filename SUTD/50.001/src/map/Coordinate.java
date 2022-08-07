package map;

import java.io.Serializable;

//A simple coordinate class
public class Coordinate implements Serializable {
	private static final long serialVersionUID = 8988213089144817392L;
	private int x, y;
	
	public Coordinate(int x, int y) {
		this.x = x;
		this.y = y;
	}
	
	/**
	 * Get X coordinate
	 * @return X coordinate
	 */
	public int getX() {
		return this.x;
	}
	
	/**
	 * Get Y coordinate
	 * @return Y coordinate
	 */
	public int getY() {
		return this.y;
	}
	
	public boolean equals(Coordinate o) {
		return (this.x == o.x && this.y == o.y);
	}
}
