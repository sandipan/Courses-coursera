/******************************************************************************
 *  Compilation:  javac Inversions.java
 *  Execution:    java Inversions
 *
 ******************************************************************************/

public class MaximumSquareSubmatrix {

     // Returns the size of the largest contiguous square submatrix
    // of a[][] containing only 1s.
    public static int size(int[][] a) {
        int n = a.length;
        int [][] s = new int[n][n];
        for (int i = 0; i < n; ++i) {
            s[i][0] = a[i][0];
            s[0][i] = a[0][i];
        }
        for (int i = 1; i < n; ++i) {
            for (int j = 1; j < n; ++j) {
                if (a[i][j] == 0) s[i][j] = 0;
                else s[i][j] = 1 + Math.min(s[i-1][j-1],
                                Math.min(s[i-1][j], s[i][j-1]));
            }
        }
        int max = -1;
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                if (s[i][j] > max) max = s[i][j];
            }
        }
        return max;
    }

    // Reads an n-by-n matrix of 0s and 1s from standard input
    // and prints the size of the largest contiguous square submatrix
    // containing only 1s.
    public static void main(String[] args) {
        // javac -cp ".lift/*" .\MaximumSquareSubmatrix.java
        // java -cp "./;./.lift/stdlib.jar" MaximumSquareSubmatrix
        int n = StdIn.readInt();
        int [][] a = new int[n][n];
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                a[i][j] = StdIn.readInt();
            }
        }
        System.out.println(size(a));
    }

}