/******************************************************************************
 *  Compilation:  javac DiscreteDistribution.java
 *  Execution:    java DiscreteDistribution
 *
 ******************************************************************************/

public class DiscreteDistribution {

    public static void main(String[] args) {

        int m = Integer.parseInt(args[0]);
        int[] a = new int[args.length - 1];
        int[] S  = new int[a.length + 1];
        for (int i = 0; i < a.length; ++i) {
            a[i] = Integer.parseInt(args[i+1]);
            S[i+1] = S[i] + a[i];
        }
        for (int j = 0; j < m; ++j) {
            int r = (int) Math.round(Math.random() * (S[S.length - 1] - 1));
            int i = 1;
            while (true) {
                if ((r >= S[i-1]) & (r < S[i])) {
                    System.out.print(i + " ");
                    break;
                }
                i++;
            }
        }
        System.out.println();
    }

}