/******************************************************************************
 *  Compilation:  javac GreatCircle.java
 *  Execution:    java GreatCircle
 *
 *  takes four double command-line arguments x1, y1, x2, and y2 — the latitude 
 *  and longitude (in degrees) of two points on the surface of the earth—and 
 *  prints the great-circle distance (in kilometers) between them.
 *  %  java GreatCircle 40.35 74.65 48.87 -2.33
 *  5902.927099258561 kilometers
 *
 ******************************************************************************/

public class GreatCircle {

    public static void main(String[] args) {
        double x1 = Math.toRadians(Double.parseDouble(args[0]));
        double y1 = Math.toRadians(Double.parseDouble(args[1]));
        double x2 = Math.toRadians(Double.parseDouble(args[2]));
        double y2 = Math.toRadians(Double.parseDouble(args[3]));
        double r = 6371.0;
        double t1 = Math.sin(0.5*(x2-x1));
        t1 = t1 * t1;
        double t2 = Math.sin(0.5*(y2-y1));
        t2 = Math.cos(x1) * Math.cos(x2) * t2 * t2;
        // Prints the distance in the terminal window.
        System.out.println(2*r*Math.asin(Math.sqrt(t1 + t2)) + " kilometers");
    }

}
