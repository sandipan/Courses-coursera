/******************************************************************************
 *  Compilation:  javac GeneralizedHarmonic.java
 *  Execution:    java GeneralizedHarmonic
 *
 ******************************************************************************/

public class AudioCollage {

    // Returns a new array that rescales a[] by a multiplicative factor of alpha.
    public static double[] amplify(double[] a, double alpha) {
        double [] aScaled = new double[a.length];
        for (int i = 0; i < aScaled.length; ++i) {
            aScaled[i] = alpha*a[i];
        }
        return aScaled;
    }

    // Returns a new array that is the reverse of a[].
    public static double[] reverse(double[] a) {
        int n = a.length;
        double [] aRev = new double[n];
        for (int i = 0; i < n; ++i) {
            aRev[i] = a[n-1-i];
        }
        return aRev;
    }

    // Returns a new array that is the concatenation of a[] and b[].
    public static double[] merge(double[] a, double[] b) {
        double [] c = new double[a.length + b.length];
        int i;
        for (i = 0; i < a.length; ++i) {
            c[i] = a[i];
        }
        for (int j = 0; j < b.length; ++j) {
            c[i + j] = b[j];
        }
        return c;
    }

    // Returns a new array that is the sum of a[] and b[],
    // padding the shorter arrays with trailing 0s if necessary.
    public static double[] mix(double[] a, double[] b) {
        double [] c = new double[Math.max(a.length, b.length)];
        for (int i = 0; i < c.length; ++i) {
            if (i < a.length) c[i] += a[i];
            if (i < b.length) c[i] += b[i];
        }
        return c;
    }

    // Returns a new array that changes the speed by the given factor.
    public static double[] changeSpeed(double[] a, double alpha) {
     double [] aChanged = new double[(int) (a.length / alpha)];
        for (int i = 0; i < aChanged.length; ++i) {
            aChanged[i] = a[(int) (i*alpha)];
        }
        return aChanged;       
    }

    // Creates an audio collage and plays it on standard audio.
    // See below for the requirements.
    public static void main(String[] args) {
        // javac -cp ".lift/*" .\AudioCollage.java
        // java -cp "./;./.lift/stdlib.jar" AudioCollage
        double [] piano = StdAudio.read("chimes.wav");
        double [] singer = StdAudio.read("singer.wav");
        double [] cow = StdAudio.read("cow.wav");
        double [] harp = StdAudio.read("harp.wav");
        double [] silence = StdAudio.read("silence.wav");
        double [] collage = amplify(
                                mix(
                                    changeSpeed(
                                        merge(
                                            mix(piano, harp), 
                                            mix(singer, reverse(cow))
                                        ),
                                    2), 
                                silence),
                            2);
        for (int i = 0; i < collage.length; ++i) {
            collage[i] = Math.max(-1, Math.min(1, collage[i]));
        }
        StdAudio.play(collage);
   }    

}