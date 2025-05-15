package roadgraph;

import geography.GeographicPoint;

import java.util.ArrayList;
import java.util.List;

/**
 * @author Created by alina on 01/01/16.
 *
 * A class to represent a Node in a graph which is an intersection at a unique geographic point.
 */
public class MapNode {
    private final GeographicPoint location;
    private final List<MapEdge> edges;

    public MapNode(GeographicPoint location) {
        this.location = location;
        edges = new ArrayList<>();
    }

    /**
     * @return a unique geographic point of this Node on the map
     */
    public GeographicPoint getLocation() {
        return location;
    }

    /**
     * add new out edge for this Node
     *
     * @param edge - new out edge
     */
    public void addEdge(MapEdge edge) {
        edges.add(edge);
    }

    /**
     * @return all out edges for this Node
     */
    public List<MapEdge> getEdges() {
        return edges;
    }

    @Override
    public String toString() {
        return "MapNode{" +
                "location=" + location +
                '}';
    }
}
