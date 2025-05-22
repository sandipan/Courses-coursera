/******************************************************************************
 *  Compilation:  javac GeneralizedHarmonic.java
 *  Execution:    java GeneralizedHarmonic
 *
 ******************************************************************************/

public class RecursiveSquares {

     
    // Draws a square centered on (x, y) of the given side length
    // with a light gray background and a black border.
    public static void drawSquare(double x, double y, double length) {
      StdDraw.setPenColor(StdDraw.LIGHT_GRAY);
      StdDraw.filledSquare(x, y, length / 2.0);
      StdDraw.setPenColor(StdDraw.BLACK);
      StdDraw.square(x, y, length / 2.0);
    }

    // Draws a recursive square pattern of order n, centered on (x, y)
    // of the given side length.
    public static void draw(int n, double x, double y, double length) {
      if (n == 1) {
         drawSquare(x, y, length);
      } else {
         double lh = length / 2.0;
         draw(n-1, x - lh, y + lh, lh);
         draw(n-1, x + lh, y + lh, lh);
         draw(n-1, x, y, length);
         draw(n-1, x - lh, y - lh, lh);
         draw(n-1, x + lh, y - lh, lh);
      }
    }

    // Takes an integer command-line argument n and draws a recursive
    // square pattern of order n, centered on (0.5, 0.5) with side length 0.5.
    public static void main(String[] args) {
      // javac -cp ".lift/*" .\RecursiveSquares.java
      // java -cp "./;./.lift/stdlib.jar" RecursiveSquares
      int n = Integer.parseInt(args[0]);
      draw(n, 0.5, 0.5, 0.5);
   }

}