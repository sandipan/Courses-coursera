/******************************************************************************
 *  Compilation:  javac GeneralizedHarmonic.java
 *  Execution:    java GeneralizedHarmonic
 *
 ******************************************************************************/

public class Huntingtons {

    // Returns the maximum number of consecutive repeats of CAG in the DNA string.
    public static int maxRepeats(String dna) {
        boolean started = false;
        int count = 0, maxCount = 0;
        for (int i = 0; i <= dna.length()-3; ) {
            String subs = dna.substring(i, i+3);
            if (subs.equals("CAG")) {
               if (!started) started = true;
               ++count;
               i += 3;
               if (count > maxCount) maxCount = count;
            } else {
                if (started) {
                    started = false;
                    count = 0;
                }
                ++i;
            }
        }
        return maxCount;
    }

    // Returns a copy of s, with all whitespace (spaces, tabs, and newlines) removed.
    public static String removeWhitespace(String s) {
        return s.replace(" ", "")
                .replace("\n", "")
                .replace("\t", "");
    }

    // Returns one of these diagnoses corresponding to the maximum number of repeats:
    // "not human", "normal", "high risk", or "Huntington's".
    public static String diagnose(int maxRepeats) {
        String out = "";
        if (maxRepeats <= 9 || maxRepeats >= 181) {
            out = "not human";
        } else if (maxRepeats <= 35) {
            out ="no Huntington's";
        } else if (maxRepeats <= 39) {
            out = "high risk";
        } else if (maxRepeats <= 180) {
            out = "Huntington's";
        } 
        return out;
    }

    // Sample client (see below).
    public static void main(String[] args) {
        // javac -cp ".lift/*" .\Huntingtons.java
        // java -cp "./;./.lift/stdlib.jar" Huntingtons
        String fileName = args[0];
        String [] ss = new In(fileName).readAllStrings();
        String s = String.join("", ss);
        s = removeWhitespace(s);
        int maxRepeats = maxRepeats(s);
        System.out.println(maxRepeats);
        System.out.println(diagnose(maxRepeats));
   }

}