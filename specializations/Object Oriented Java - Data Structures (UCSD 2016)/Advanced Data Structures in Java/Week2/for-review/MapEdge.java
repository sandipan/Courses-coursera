package roadgraph;

/**
 * @author Created by alina on 01/01/16.
 *
 * A class to represent a directed edge between two Nodes of a graph, that are already in the graph.
 * A edge is a street segment, that connect intersections
 */
public class MapEdge {
    private final MapNode from;
    private final MapNode to;
    private final String roadName;
    private final String roadType;
    private final double length;

    public MapEdge(MapNode from, MapNode to, String roadName, String roadType, double length) {
        this.from = from;
        this.to = to;
        this.roadName = roadName;
        this.roadType = roadType;
        this.length = length;
    }

    /**
     * @return from-Node in the graph
     */
    public MapNode getFrom() {
        return from;
    }

    /**
     * @return to-Node in the graph
     */
    public MapNode getTo() {
        return to;
    }

    /**
     * @return a name of the road
     */
    public String getRoadName() {
        return roadName;
    }

    /**
     * @return a kind of road (e.g. "residential")
     */
    public String getRoadType() {
        return roadType;
    }

    /**
     * @return a length of this road segment, in km
     */
    public double getLength() {
        return length;
    }

    @Override
    public String toString() {
        return "MapEdge{" +
                "from=" + from +
                ", to=" + to +
                ", roadName='" + roadName + '\'' +
                ", roadType='" + roadType + '\'' +
                ", length=" + length +
                '}';
    }
}
