/**
 * @author UCSD MOOC development team and YOU
 * 
 * A class which reprsents a graph of geographic locations
 * Nodes in the graph are intersections between 
 *
 */
package roadgraph;


import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.function.Consumer;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.HashMap;
import java.util.Queue;

import geography.GeographicPoint;
import util.GraphLoader;
import roadgraph.MapEdge;

/**
 * @author UCSD MOOC development team and YOU
 * 
 * A class which represents a graph of geographic locations
 * Nodes in the graph are intersections between 
 *
 */
public class MapGraph {
	//TODO: Add your member variables here in WEEK 2
	private Map<GeographicPoint,ArrayList<MapEdge>> adjListsMap;
	private int numOfEdges;
	
	
	/** 
	 * Create a new empty MapGraph 
	 */
	public MapGraph()
	{
		// TODO: Implement in this constructor in WEEK 2
		adjListsMap = new HashMap<GeographicPoint,ArrayList<MapEdge>>();
		numOfEdges = 0;
	}
	
	/**
	 * Get the number of vertices (road intersections) in the graph
	 * @return The number of vertices in the graph.
	 */
	public int getNumVertices()
	{
		//TODO: Implement this method in WEEK 2
		return adjListsMap.size();
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
		return numOfEdges;
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
		if (location == null || adjListsMap.containsKey(location)) {
			return false;
		}
		adjListsMap.put(location,new ArrayList<MapEdge>());
		return true;
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
		if (from == null || to == null || roadName == null ||
				!adjListsMap.containsKey(from) || !adjListsMap.containsKey(to) 
				|| length <= 0) {
			throw new IllegalArgumentException();
		}

		MapEdge fromEdge = new MapEdge(from, to, roadName, length);
		adjListsMap.get(from).add(fromEdge);
		numOfEdges++;
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
		//	nodeSearched.accept(next.getLocation());
		
		// Initialize
		Set<GeographicPoint> visited = new HashSet<GeographicPoint>();
		Queue<GeographicPoint> queue = new LinkedList<GeographicPoint>();
		Map<GeographicPoint,LinkedList<GeographicPoint>> map = new HashMap<GeographicPoint,
				LinkedList<GeographicPoint>>();
		if (start == null || goal == null || 
				!adjListsMap.containsKey(start) || !adjListsMap.containsKey(goal)) {
			return null;
		}
		
		//Search
		List<GeographicPoint> list = bfs(start, goal, visited, queue, map, nodeSearched);
		if (list.isEmpty()) return null;
		return list;
	}
	
	/*
	 * breath-first search the shortest point list
	 */
	private List<GeographicPoint> bfs(GeographicPoint start, GeographicPoint goal, 
			Set<GeographicPoint> visited, Queue<GeographicPoint> queue, 
			Map<GeographicPoint,LinkedList<GeographicPoint>> map,
			Consumer<GeographicPoint> nodeSearched) {
		List<GeographicPoint> result = new LinkedList<GeographicPoint>();
		queue.add(start);
		visited.add(start);
		LinkedList<GeographicPoint> startList = new LinkedList<GeographicPoint>();
		startList.add(start);
		map.put(start, startList);
		while (!queue.isEmpty()) {
			GeographicPoint curr = queue.poll();
			nodeSearched.accept(curr);
			List<MapEdge> edges = adjListsMap.get(curr);
			for (MapEdge edge : edges) {
				GeographicPoint endPoint = edge.getEndPoint();
				// touch goal point
				if (endPoint.getX() == goal.getX() && endPoint.getY() == goal.getY()) {
					result = map.get(curr);
					result.add(endPoint);
					return result;
				// already visted before
				} else if (visited.contains(endPoint)) {
					continue;
				// add to queue and visited set.Meantime put route to map
				} else {
					visited.add(endPoint);
					LinkedList<GeographicPoint> tempList = 
							new LinkedList<GeographicPoint>(map.get(curr));
					tempList.add(endPoint);
					map.put(endPoint, tempList);
					queue.add(endPoint);
				}
			}
			
		}
		return result;
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
		
		System.out.println(theMap.getNumEdges());
		System.out.println(theMap.getNumVertices());
		GeographicPoint start = new GeographicPoint(1,1);
		GeographicPoint goal = new GeographicPoint(8,-1);
		for (MapEdge edge : theMap.adjListsMap.get(start)) {
			System.out.println(edge.getEndPoint());
			System.out.println(edge.getRoadName());
			System.out.println(edge.getLength());
		}
		
		List<GeographicPoint> result = theMap.bfs(start, goal,null);
		for (GeographicPoint point : result) {
			System.out.println(point);
		}
		
		
		
		// You can use this method for testing.  
		
		/* Use this code in Week 3 End of Week Quiz
		MapGraph theMap = new MapGraph();
		System.out.print("DONE. \nLoading the map...");
		GraphLoader.loadRoadMap("data/maps/utc.map", theMap);
		System.out.println("DONE.");

		GeographicPoint start = new GeographicPoint(32.8648772, -117.2254046);
		GeographicPoint end = new GeographicPoint(32.8660691, -117.217393);
		
		
		List<GeographicPoint> route = theMap.dijkstra(start,end);
		List<GeographicPoint> route2 = theMap.aStarSearch(start,end);

		*/
		
	}
	
}
