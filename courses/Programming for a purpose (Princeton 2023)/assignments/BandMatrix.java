/******************************************************************************
 *  Compilation:  javac GeneralizedHarmonic.java
 *  Execution:    java GeneralizedHarmonic
 *
 ******************************************************************************/

public class BandMatrix {

    public static void main(String[] args) {

        int n = Integer.parseInt(args[0]);
        int width = Integer.parseInt(args[1]);
        
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                if (Math.abs(i - j) > width) {
                    System.out.print("0  ");
                } else {
                    System.out.print("*  ");
                }
            }
            System.out.println();
        }
    }

}