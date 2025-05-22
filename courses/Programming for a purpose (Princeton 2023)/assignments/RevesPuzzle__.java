/******************************************************************************
 *  Compilation:  javac GeneralizedHarmonic.java
 *  Execution:    java GeneralizedHarmonic
 *
 ******************************************************************************/

public class RevesPuzzle__ {
     
     private static char [] getOtherSticks(char [] asticks, 
                                       char [] esticks) {
      char [] osticks = new char[asticks.length - esticks.length];
      int k = 0;
      for (int i = 0; i < asticks.length; ++i) {
         boolean found =false;
         for (int j = 0; j < esticks.length; ++j) {
            if (asticks[i] == esticks[j]) {
               found = true;
               break;
            }
         }
         if (!found) osticks[k++] = asticks[i];
      }
      return osticks;
     }

     /* private static void printSticks(char [] sticks) {
      for (int k = 0; k < sticks.length; ++k) {
         System.out.print(sticks[k]);
      }
      System.out.println();
     } */

     private static void towersHanoi(int s, int e, 
                     char i, char j, char [] sticks) {
      //printSticks(sticks);
      if (e == s) {
         System.out.println("Move disc " +  s + " from " + 
                              i + " to " + j);
      } else {
         char [] excludeSticks = {i, j};
         char l = getOtherSticks(sticks, excludeSticks)[0];
         towersHanoi(s, e-1, i, l, sticks);
         System.out.println("Move disc " + e + " from " +
                              i + " to " + j);
         towersHanoi(s, e-1, l, j, sticks);
      }
     }

     public static void move(int n, char i, char j, char [] sticks ) {
      if (n == 1) {
         System.out.println("Move disc 1 from " +
                              i + " to " + j);
      } else {
         int k = (int) Math.round(n+1 - Math.sqrt(2*n+1));
         //System.out.println(k);
         char [] excludeSticks = {i, j};
         char l = getOtherSticks(sticks, excludeSticks)[0];         
         move(k, i, l, sticks);
         //printSticks(getOtherSticks(sticks, new char[] {l}));
         char [] excludeSticks2 = {l};
         towersHanoi(k+1, n, i, j, 
                     getOtherSticks(sticks, excludeSticks2));
         move(k, l, j, sticks);
      }
     }

     // Takes two integer command-line arguments n and k and prints T(n, k).
     public static void main(String[] args) {
        int n = Integer.parseInt(args[0]);
        // towersHanoi(1, 3, 'A', 'C', new char[] {'A', 'B', 'C'});
        char [] sticks = {'A','B','C','D'};
        move(n, 'A', 'D', sticks);
   }     

}