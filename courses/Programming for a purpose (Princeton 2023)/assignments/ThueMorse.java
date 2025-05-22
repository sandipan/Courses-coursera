/******************************************************************************
 *  Compilation:  javac DiscreteDistribution.java
 *  Execution:    java DiscreteDistribution
 *
 ******************************************************************************/

public class ThueMorse {

    public static void main(String[] args) {

        int n = Integer.parseInt(args[0]);
        int[] a = {0};
        for (int i = 0; i < Math.log(n) / Math.log(2); ++i) {
            int m = a.length;
            int[] b = new int[2*m];
            for (int j = 0; j < m; ++j) {
                b[j] = a[j];
                b[j + m] = 1 - b[j];
            }
            a = b;            
        }
        char[][] m = new char[n][n];
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                if (a[i] == a[j]) {
                    m[i][j] = '+';
                } else {
                    m[i][j] = '-';
                }
            }    
        }
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                System.out.print(m[i][j] + "  ");
            }    
            System.out.println();
        }
    }

}