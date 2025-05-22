/******************************************************************************
 *  Compilation:  javac GeneralizedHarmonic.java
 *  Execution:    java GeneralizedHarmonic
 *
 ******************************************************************************/

public class RevesPuzzle {     
     
     private static void towersHanoi(int s, int e, 
                     char i, char j) {
      if (e == s) {
         System.out.println("Move disc " +  s + " from " + 
                              i + " to " + j);
      } else {
         towersHanoi(s, e-1, i, 'B');
         System.out.println("Move disc " + e + " from " +
                              i + " to " + j);
         towersHanoi(s, e-1, 'B', j);
      }
     }

     public static void move(int n, char i, char j) {
      if (n == 1) {
         System.out.println("Move disc 1 from " +
                              i + " to " + j);
      } else {
         int k = (int) Math.round(n+1 - Math.sqrt(2*n+1));
         //System.out.println(k);
         move(k, i, 'B');
         towersHanoi(k+1, n, i, 'C');
         move(k, 'B', j);
      }
     }

     // Takes two integer command-line arguments n and k and prints T(n, k).
     public static void main(String[] args) {
        int n = Integer.parseInt(args[0]);
        move(n, 'A', 'D');
   }     

}