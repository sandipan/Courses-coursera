package roadgraph;
import geography.GeographicPoint;

public class MapEdge {
	
	private GeographicPoint start;
	private GeographicPoint end;
	private String roadName;
	private double length;
	
	public MapEdge(GeographicPoint start, GeographicPoint end, String roadName, double length2) {
		this.start = start;
		this.end = end;
		this.roadName = roadName;
		this.length = length2;
	}
	
	public GeographicPoint getStartPoint() {
		return this.start;
	}
	
	public GeographicPoint getEndPoint() {
		return this.end;
	}
	
	public String getRoadName() {
		return this.roadName;
	}
	
	public double getLength() {
		return this.length;
	}
}
