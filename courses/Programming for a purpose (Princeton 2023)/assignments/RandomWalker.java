/******************************************************************************
 *  Compilation:  javac GeneralizedHarmonic.java
 *  Execution:    java GeneralizedHarmonic
 *
 ******************************************************************************/

public class RandomWalker {

    public static void main(String[] args) {

        int r = Integer.parseInt(args[0]);
        int x0 = 0, y0 = 0;
        int x = x0, y = y0;
        int steps = 0;
        System.out.println("(" + x + "," + y + ")");
        while (Math.abs(x - x0) + Math.abs(y - y0) < r) {
            double dir = Math.random();
            if (dir < 0.25) {
                y -= 1;
            } else if (dir < 0.5) {
                x += 1;
            } else if (dir < 0.75) {
                y += 1;
            } else {
                x -= 1;
            }
            ++steps;
            System.out.println("(" + x + "," + y + ")");
        }
        System.out.println("steps = " + steps);
    }

}