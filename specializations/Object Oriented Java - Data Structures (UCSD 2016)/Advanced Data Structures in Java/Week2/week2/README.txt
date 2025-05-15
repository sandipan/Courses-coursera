Class: MapGraph

Modifications made to MapGraph (what and why):
1.add a member variable adjlistsmap. This map store the vertex and it's neighbors.
2.add a member variable numOfEdges. This variable store the edges number.

Class name: public MapGraph()

Purpose and description of class:initialize the class

Class name: public int getNumVertices()

Purpose and description of class:get the number of vertices.use the adjlistsmap's size.

Class name: public Set<GeographicPoint> getVertices()

Purpose and description of class:get the set of vertices. use the adjListMap's keySet.

Class name: public int getNumEdges()

Purpose and description of class:get the num of edges. use the member variable numOfEdges.

Class name: public boolean addVertex(GeographicPoint location)

Purpose and description of class:add a vertex

Class name: public void addEdge(GeographicPoint from, GeographicPoint to, String roadName,
			String roadType, double length) throws IllegalArgumentException

Purpose and description of class:add a edge. use MapEdge class construction method.

Class name: public List<GeographicPoint> bfs(GeographicPoint start, 
			 					     GeographicPoint goal, Consumer<GeographicPoint> nodeSearched)

Purpose and description of class:bfs search the shortest path from start point to goal point.

Class name: private List<GeographicPoint> bfs(GeographicPoint start, GeographicPoint goal, 
			Set<GeographicPoint> visited, Queue<GeographicPoint> queue, 
			Map<GeographicPoint,LinkedList<GeographicPoint>> map,
			Consumer<GeographicPoint> nodeSearched)

Purpose and description of class:private bfs  method.Seperate this method form public bfs method. In order to short the public bfs method.


Class: MapEdge

Modifications made to MapEdge (what and why):
1.add a member variable start. The start point of edge.
2.add a member variable end. The end point of edge.
3.add a member variable roadName.The name of edge.
4.add a member variable length.The length of edge.

Class name: public MapEdge(GeographicPoint start, GeographicPoint end, String roadName, double length2)

Purpose and description of class:initialize the class

Class name: public GeographicPoint getStartPoint()

Purpose and description of class:get the start point.

Class name: public GeographicPoint getEndPoint()

Purpose and description of class:get the end point.

Class name: public String getRoadName()

Purpose and description of class:get the name of road.

Class name: public double getLength()

Purpose and description of class:get the length of road.


Overall Design Justification (4-6 sentences):
I use the adjust to represent the graph. I add a new class MapEdge to represent the edge because of the edge has so many attribute. But I don't add class like MapNode because the node just a geography point, we already import this class. Then I use a map represent the adjust.The key of map is the node, then the value is the neighbors. I also put some get methods.Last, I put a public bfs method, but it's too long. So I refract it use a private bfs method.