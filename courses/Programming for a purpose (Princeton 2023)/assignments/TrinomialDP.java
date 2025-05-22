/******************************************************************************
 *  Compilation:  javac GeneralizedHarmonic.java
 *  Execution:    java GeneralizedHarmonic
 *
 ******************************************************************************/

public class TrinomialDP {

     // Returns the trinomial coefficient T(n, k).
     public static long trinomial(int n, int k) {
      if (k > n || k < -n) return 0;
      long [][] T = new long[n+1][2*n+2];
      T[0][n] = 1;
      for (int i = 1; i <= n; ++i) {
         for (int j = -i; j <= i; ++j) {
            T[i][n+j] = T[i-1][n+j] + T[i-1][n+j+1]; 
            if (n + j >= 1) T[i][n+j] += T[i-1][n+j-1];
         }
      }
      /* for (int i = 0; i <= n; ++i) {
         for (int j = -i; j <= i; ++j) {
            System.out.print(T[i][n+j] + " ");
         }
         System.out.println();
      } */
      return T[n][n+k];
     }

     // Takes two integer command-line arguments n and k and prints T(n, k).
     public static void main(String[] args) {
        int n = Integer.parseInt(args[0]);
        int k = Integer.parseInt(args[1]);
        System.out.println(trinomial(n, k));
   }

}