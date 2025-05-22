/******************************************************************************
 *  Compilation:  javac GeneralizedHarmonic.java
 *  Execution:    java GeneralizedHarmonic
 *
 ******************************************************************************/

public class GeneralizedHarmonic {

    public static void main(String[] args) {

        int n = Integer.parseInt(args[0]);
        int r = Integer.parseInt(args[1]);
        
        double sum = 0;
        for (int i = 1; i <= n; ++i) {
            sum += 1 / Math.pow(i, r);
        }
        // Prints "Hello, World" in the terminal window.
        System.out.println(sum);
    }

}