/******************************************************************************
 *  Compilation:  javac Inversions.java
 *  Execution:    java Inversions
 *
 ******************************************************************************/

public class Ramanujan {

    /// Is n a Ramanujan number?
    public static boolean isRamanujan(long n) {
        long m = (long) Math.pow(n, 1./3);
        double eps = 1e-6;
        for (long i = 1; i <= m; ++i) {
            double j = Math.pow(n - i*i*i, 1./3);
            //System.out.println(Math.abs(j - (long) j));
            if (Math.abs(j - Math.round(j)) < eps &&
               Math.abs(i - j) > eps && j > 0) {
                return true;
            }

        }
        return false;
    }

    // Takes a long integer command-line arguments n and prints true if
    // n is a Ramanujan number, and false otherwise.
    public static void main(String[] args) {
        long n = Long.parseLong(args[0]);
        System.out.println(isRamanujan(n));
    }

}