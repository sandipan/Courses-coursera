/******************************************************************************
 *  Compilation:  javac Birthday.java
 *  Execution:    java Birthday
 *
 ******************************************************************************/

 public class Birthday {

    public static void main(String[] args) {

        int n = Integer.parseInt(args[0]);
        int trials = Integer.parseInt(args[1]);
        int[] counts = new int[n+1];
        for (int i = 0; i < n+1; ++i) counts[i] = 0;
        for (int trial = 0; trial < trials; trial++) {
            int [] days = new int[n];
            int i = 0;
            boolean found = false;                
            while (!found) {
                int day = (int) Math.round(Math.random() * (n - 1));
                found = false;
                for (int j = 0; j < i; ++j) {
                    if (days[j] == day) {
                        found = true;
                        break;
                    }
                }
                if (!found) {
                    days[i] = day;
                    ++i;
                }
            }
            counts[i] += 1;
        }
        int i = 0, cumsum = 0;
        double prob = 0;
        while (prob < 0.5) {
            cumsum += counts[i];
            prob = (1.0 * cumsum) / trials;
            System.out.println(i+1 + " " + counts[i] + " " + prob);
            i += 1;
        }
    }

}