/******************************************************************************
 *  Compilation:  javac WorldMap.java
 *  Execution:    java WorldMap
 *
 ******************************************************************************/

public class WorldMap {

    public static void main(String[] args) {
        // javac -cp ".lift/*" .\WorldMap.java
        // java -cp "./;./.lift/stdlib.jar" WorldMap 
        // cmd /c --% java -cp "./;./.lift/stdlib.jar" WorldMap < world.txt
        int width = StdIn.readInt();
        int height = StdIn.readInt();
        StdDraw.setCanvasSize(width, height);
        StdDraw.setXscale(0, width);
        StdDraw.setYscale(0, height);  
        System.out.println(StdIn.readLine());
        while (StdIn.hasNextLine()) {
          StdIn.readLine();
          StdIn.readLine();
          if (!(StdIn.hasNextLine())) break;
          int n = StdIn.readInt();
          double [] x = new double[n];
          double [] y = new double[n];
          for (int i = 0; i < n; ++i) {
             x[i] = StdIn.readDouble();
             y[i] = StdIn.readDouble();  
          }
          StdDraw.polygon(x, y);
          StdIn.readLine();
       } 
   }

}