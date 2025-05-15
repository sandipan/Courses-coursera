/**

 * @author UCSD MOOC development team and YOU
 * 
 * A class which reprsents a graph of geographic locations
 * Nodes in the graph are intersections between 
 *
 */
package roadgraph;


import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.PriorityQueue;
import java.util.Set;
import java.util.function.Consumer;

import geography.GeographicPoint;
import util.GraphLoader;

/**
 * @author UCSD MOOC development team and YOU
 * 
 * A class which represents a graph of geographic locations
 * Nodes in the graph are intersections between 
 *
 */
public class MapGraph {
	
	//TODO: Add your member variables here in WEEK 2
	private int numVertices;
	private int numEdges;
	/** use adjacency list representation for the MapGraph **/
	private Map<GeographicPoint,ArrayList<GeographicPoint>> adjListsMap;
	
	/**
	 * 
	 * A class which represents a road in between two intersections
	 *
	 */
	private class Road {
		
		private String name, type;
		private double length;
		
		/**
		 * Constructor to create a new road 
		 * @param name Name of the road
		 * @param type Type of the road
		 * @param length Lenght of the road
		 */
		public Road(String name, String type, double length) {
			this.name = name;
			this.type = type;
			this.length = length;
		}
		/**
		 * @return the name of the road
		 */
		public String getName() {
			return name;
		}
		/**
		 * 
		 * @return the type of the road
		 */
		public String getType() {
			return type;
		}
		/**
		 * 
		 * @return the length of the road
		 */
		public double getLength() {
			return length;
		}
	}

	/*
	 * This map stores all the roads in between the pairs of intersections
	 */
	private Map<GeographicPoint, Map<GeographicPoint, Road>> roadMap;

	/** 
	 * Create a new empty MapGraph 
	 */
	public MapGraph()
	{
		// TODO: Implement in this constructor in WEEK 2
		numVertices = 0;
		numEdges = 0;
		adjListsMap = new HashMap<GeographicPoint,ArrayList<GeographicPoint>>();
		roadMap = new HashMap<GeographicPoint, Map<GeographicPoint, Road>> ();
	}
	
	/**
	 * Get the number of vertices (road intersections) in the graph
	 * @return The number of vertices in the graph.
	 */
	public int getNumVertices()
	{
		//TODO: Implement this method in WEEK 2
		return numVertices;
	}
	
	/**
	 * Return the intersections, which are the vertices in this graph.
	 * @return The vertices in this graph as GeographicPoints
	 */
	public Set<GeographicPoint> getVertices()
	{
		//TODO: Implement this method in WEEK 2
		return adjListsMap.keySet();
	}
	
	/**
	 * Get the number of road segments in the graph
	 * @return The number of edges in the graph.
	 */
	public int getNumEdges()
	{
		//TODO: Implement this method in WEEK 2
		return numEdges;
	}

	
	
	/** Add a node corresponding to an intersection at a Geographic Point
	 * If the location is already in the graph or null, this method does 
	 * not change the graph.
	 * @param location  The location of the intersection
	 * @return true if a node was added, false if it was not (the node
	 * was already in the graph, or the parameter is null).
	 */
	public boolean addVertex(GeographicPoint location)
	{
		// TODO: Implement this method in WEEK 2
		// System.out.println("Adding vertex "+v);
		if (location != null && !adjListsMap.containsKey(location)) {
			adjListsMap.put(location,  new ArrayList<GeographicPoint>());
			++numVertices;
			return true;
		}
		return false;
	}
	
	/**
	 * Adds a directed edge to the graph from pt1 to pt2.  
	 * Precondition: Both GeographicPoints have already been added to the graph
	 * @param from The starting point of the edge
	 * @param to The ending point of the edge
	 * @param roadName The name of the road
	 * @param roadType The type of the road
	 * @param length The length of the road, in km
	 * @throws IllegalArgumentException If the points have not already been
	 *   added as nodes to the graph, if any of the arguments is null,
	 *   or if the length is less than 0.
	 */
	public void addEdge(GeographicPoint from, GeographicPoint to, String roadName,
			String roadType, double length) throws IllegalArgumentException {

		//TODO: Implement this method in WEEK 2
		if (from == null || to == null || !adjListsMap.containsKey(from) || !adjListsMap.containsKey(to) || length < 0) {
			throw new IllegalArgumentException();
		}
		(adjListsMap.get(from)).add(to);
		++numEdges;
		/**
		 * if the 'from' node already has an entry in the roadMap, retrieve the corresponding entry,
		 * otherwise create a new hashmap of intersection point and road as key-value pairs.
		 * create a new road object with the name, type and length and add the new road created as 
		 * a value along with 'to' node as the key node to the hashmap. Next update the roadMap by
		 * inserting the 'from' node along with this modified hasmap.
		 */
		Map<GeographicPoint, Road> temp = roadMap.get(from);
		if (temp == null) {
			temp = new HashMap<GeographicPoint, Road>();
		}
		temp.put(to, new Road(roadName, roadType, length));
		roadMap.put(from, temp);
	}
	

	/** Find the path from start to goal using breadth first search
	 * 
	 * @param start The starting location
	 * @param goal The goal location
	 * @return The list of intersections that form the shortest (unweighted)
	 *   path from start to goal (including both start and goal).
	 */
	public List<GeographicPoint> bfs(GeographicPoint start, GeographicPoint goal) {
		// Dummy variable for calling the search algorithms
        Consumer<GeographicPoint> temp = (x) -> {};
        return bfs(start, goal, temp);
	}
	
	/** Find the path from start to goal using breadth first search
	 * 
	 * @param start The starting location
	 * @param goal The goal location
	 * @param nodeSearched A hook for visualization.  See assignment instructions for how to use it.
	 * @return The list of intersections that form the shortest (unweighted)
	 *   path from start to goal (including both start and goal).
	 */
	public List<GeographicPoint> bfs(GeographicPoint start, 
			 					     GeographicPoint goal, Consumer<GeographicPoint> nodeSearched)
	{
		// TODO: Implement this method in WEEK 2
		
		// Hook for visualization.  See writeup.
		
		 Set<GeographicPoint> visited = new HashSet<GeographicPoint>(); /* stores the nodes already visited */
		 Map<GeographicPoint, GeographicPoint> parent = new HashMap<GeographicPoint, GeographicPoint>(); /* stores the parents of the nodes visited */ 
		 List<GeographicPoint> fringe = new ArrayList<GeographicPoint>(); /* stores the nodes to be visited next */
		 
		 fringe.add(start); /* start from the source node */
		 
		 GeographicPoint point = null;
		 
		 while (fringe.size() > 0) {
		
			 point = fringe.remove(0);
			 nodeSearched.accept(point);
		 	 
			 List<GeographicPoint> neighbors = adjListsMap.get(point);
			 for (GeographicPoint neighbor:neighbors) { // loop through all the neighbors of the nodes
				 if (!visited.contains(neighbor)) {		// if the neighbor is not already visited then only visit
					 fringe.add(neighbor);
					 parent.put(neighbor, point);		// add the node as parent to its neighbor node
					 visited.add(point);	
					 if (neighbor.equals(goal)) {	// goal found
						 point = goal;
						 break;
					 }
				 }
			 }			 
			 
			 if (point.equals(goal)) {	// goal found
				 break;
			 }
		 
		 }
		 
		 /* use the parent hashmap to find the path from start to goal by traversing from goal to start */
		 if (point.equals(goal)) {	/* if goal is reachable from source */
			 List <GeographicPoint> path = new ArrayList<GeographicPoint>();
			 while (!point.equals(start)) {
				path.add(0, point); 
				point = parent.get(point);
			 }
			 path.add(0, start);
			 return path;
		 }
		 /* return null if no path between source and goal found */ 
		 return null;
	}
	

	/** Find the path from start to goal using Dijkstra's algorithm
	 * 
	 * @param start The starting location
	 * @param goal The goal location
	 * @return The list of intersections that form the shortest path from 
	 *   start to goal (including both start and goal).
	 */
	public List<GeographicPoint> dijkstra(GeographicPoint start, GeographicPoint goal) {
		// Dummy variable for calling the search algorithms
		// You do not need to change this method.
        Consumer<GeographicPoint> temp = (x) -> {};
        return dijkstra(start, goal, temp);
	}
	
	/** Find the path from start to goal using Dijkstra's algorithm
	 * 
	 * @param start The starting location
	 * @param goal The goal location
	 * @param nodeSearched A hook for visualization.  See assignment instructions for how to use it.
	 * @return The list of intersections that form the shortest path from 
	 *   start to goal (including both start and goal).
	 */
	public List<GeographicPoint> dijkstra(GeographicPoint start, 
										  GeographicPoint goal, Consumer<GeographicPoint> nodeSearched)
	{
		// TODO: Implement this method in WEEK 3

		// Hook for visualization.  See writeup.
		//nodeSearched.accept(next.getLocation());
		
		return null;
	}

	/** Find the path from start to goal using A-Star search
	 * 
	 * @param start The starting location
	 * @param goal The goal location
	 * @return The list of intersections that form the shortest path from 
	 *   start to goal (including both start and goal).
	 */
	public List<GeographicPoint> aStarSearch(GeographicPoint start, GeographicPoint goal) {
		// Dummy variable for calling the search algorithms
        Consumer<GeographicPoint> temp = (x) -> {};
        return aStarSearch(start, goal, temp);
	}
	
	/** Find the path from start to goal using A-Star search
	 * 
	 * @param start The starting location
	 * @param goal The goal location
	 * @param nodeSearched A hook for visualization.  See assignment instructions for how to use it.
	 * @return The list of intersections that form the shortest path from 
	 *   start to goal (including both start and goal).
	 */
	public List<GeographicPoint> aStarSearch(GeographicPoint start, 
											 GeographicPoint goal, Consumer<GeographicPoint> nodeSearched)
	{
		// TODO: Implement this method in WEEK 3
		
		// Hook for visualization.  See writeup.
		//nodeSearched.accept(next.getLocation());
		
		return null;
	}

	
	
	public static void main(String[] args)
	{
		System.out.print("Making a new map...");
		MapGraph theMap = new MapGraph();
		System.out.print("DONE. \nLoading the map...");
		GraphLoader.loadRoadMap("data/testdata/simpletest.map", theMap);
		System.out.println("DONE.");
		
		// You can use this method for testing.  
		
		// Use this code in Week 3 End of Week Quiz
		/*
		MapGraph theMap = new MapGraph();
		System.out.print("DONE. \nLoading the map...");
		GraphLoader.loadRoadMap("data/maps/utc.map", theMap);
		System.out.println("DONE.");

		GeographicPoint start = new GeographicPoint(32.868629, -117.215393);
		GeographicPoint end = new GeographicPoint(32.868629, -117.215393);
		
		List<GeographicPoint> route = theMap.dijkstra(start,end);
		List<GeographicPoint> route2 = theMap.aStarSearch(start,end);
		*/
		
		
	}
	
}
