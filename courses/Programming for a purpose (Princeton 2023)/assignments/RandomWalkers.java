/******************************************************************************
 *  Compilation:  javac GeneralizedHarmonic.java
 *  Execution:    java GeneralizedHarmonic
 *
 ******************************************************************************/

public class RandomWalkers {

    public static void main(String[] args) {

        int r = Integer.parseInt(args[0]);
        int trials = Integer.parseInt(args[1]);
        long totalSteps = 0;
        for (int trial = 0; trial < trials; ++trial) {
            int x0 = 0, y0 = 0;
            int x = x0, y = y0;
            int steps = 0;
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
            }
            totalSteps += steps;
        }
        System.out.println("average number of steps = " + (1.0 * totalSteps) / trials);
    }

}