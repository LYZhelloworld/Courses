package map;

public class MapObstacle extends MapElement {
	private static final long serialVersionUID = -8440610004820050770L;

	public MapObstacle(Coordinate startPoint, int width, int height) {
		super(startPoint, width, height);
		this.type = ElementType.OBSTACLE;//Set element type, which is not set in the abstract class
	}
}
