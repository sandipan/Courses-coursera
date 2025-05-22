/******************************************************************************
 *  Compilation:  javac Inversions.java
 *  Execution:    java Inversions
 *
 ******************************************************************************/

public class Inversions {

    // Return the number of inversions in the permutation a[].
    public static long count(int[] a) {
        int count = 0;
        for (int i = 0; i < a.length; ++i) {
            for (int j = i+1; j < a.length; ++j)
                if (a[i] > a[j]) ++count;
        }
        return count;
    }

    // Return a permutation of length n with exactly k inversions.
    public static int[] generate(int n, long k) {
        int [] a = new int[n];
        for (int i = 0; i < n; ++ i) a[i] = i;
        int nInv = 0;
        for (int i = n-1; i > 0; --i) 
            for (int j = i-1; j >= 0; --j) {
                if (nInv == k) return a;
                int temp = a[i];
                a[i] = a[j];
                a[j] = temp;
                ++nInv;
            }
        return a;
    }

    // Takes an integer n and a long k as command-line arguments,
    // and prints a permutation of length n with exactly k inversions.
    public static void main(String[] args) {
        int n = Integer.parseInt(args[0]);
        int k = Integer.parseInt(args[1]);
        int [] a = generate(n, k);
        for (int i = 0; i < n; ++i) {
            System.out.print(a[i] + " ");
        }
        System.out.println();
        //System.out.println(count(a));
      }

}