/******************************************************************************
 *  Compilation:  javac GeneralizedHarmonic.java
 *  Execution:    java GeneralizedHarmonic
 *
 ******************************************************************************/

public class ShannonEntropy {

    public static void main(String[] args) {
        // javac -cp ".lift/*" .\ShannonEntropy.java
        // java -cp "./;./.lift/stdlib.jar" ShannonEntropy
        int n = Integer.parseInt(args[0]);
        int [] seq = StdIn.readAllInts();
        double [] probs = new double[n];
        for (int i = 0; i < seq.length; ++i) {
            probs[seq[i]-1]++;
        }
        double sum = 0;
        for (int i = 0; i < n; ++i) {
            sum += probs[i];
        }
        for (int i = 0; i < n; ++i) {
            probs[i] /= sum;
        }
        double e = 0;
        for (int i = 0; i < n; ++i) {
            if (probs[i] != 0)
                e += -probs[i] * Math.log(probs[i]) / Math.log(2);
        }
        //System.out.println(Math.round(e*1e4)/1e4);
        System.out.println(String.format("%.04f", e));
   }

}