/******************************************************************************
 *  Compilation:  javac Birthday.java
 *  Execution:    java Birthday
 *
 ******************************************************************************/

public class Minesweeper {

    public static void main(String[] args) {

        int m = Integer.parseInt(args[0]);
        int n = Integer.parseInt(args[1]);
        int k = Integer.parseInt(args[2]);
        int[] xs = new int[k];
        int[] ys = new int[k];
        boolean [][] isMine = new boolean[m][n];
        for (int i = 0; i <  m; ++i) {
            for (int j = 0; j < n; ++j) {
                isMine[i][j] = false;
            }
        }
        int x = -1, y = -1;
        for (int i = 0; i < k; i++) {
            boolean found = true;
            while (found) {
                x = (int) Math.round(Math.random() * (m - 1));
                y = (int) Math.round(Math.random() * (n - 1));
                found = false;                
                for (int j = 0; j < i; ++j) {
                    if ((xs[j] == x) && (ys[j] == y)) {
                        found = true;
                        break;
                    }
                }                
            }                
            xs[i] = x;
            ys[i] = y;
            isMine[x][y] = true;
        }
              
        int [][] M = new int[m][n];
        for (int i = 0; i < m; ++i)
            for (int j = 0; j < n; ++j) 
                M[i][j] = 0;

        for (int i = 0; i < k; ++i) {
            x = xs[i];
            y = ys[i];
            M[x][y] = -1;
            if (x > 0) {
                if (!isMine[x-1][y]) M[x-1][y] += 1;
                if ((y > 0) && (!isMine[x-1][y-1])) M[x-1][y-1] += 1;
                if ((y < n-1) && (!isMine[x-1][y+1])) M[x-1][y+1] += 1;
            }
            if (x < m-1) {
                if (!isMine[x+1][y]) M[x+1][y] += 1;
                if ((y < n-1) && (!isMine[x+1][y+1])) M[x+1][y+1] += 1;
                if ((y > 0) && (!isMine[x+1][y-1])) M[x+1][y-1] += 1;
            }
            if ((y > 0) && (!isMine[x][y-1])) M[x][y-1] += 1;
            if ((y < n-1) && (!isMine[x][y+1])) M[x][y+1] += 1;
        }
        for (int i = 0; i < m; ++i) {
            for (int j = 0; j < n; ++j) {
                if (M[i][j] < 0) {
                    System.out.print("*  ");
                } else {    
                    System.out.print(M[i][j] + "  ");
                }
            }   
            System.out.println();         
        }
    }

}