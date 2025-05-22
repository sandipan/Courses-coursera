/******************************************************************************
 *  Compilation:  javac RightTriangle.java
 *  Execution:    java RightTriangle
 *
 *  takes three int command-line arguments and determines whether they constitute
 *  the side lengths of some right triangle..
 *  % java RightTriangle 3 4 5
true
 *
 *
 ******************************************************************************/

 public class RightTriangle {

    public static void main(String[] args) {
        int a = Integer.parseInt(args[0]);
        int b = Integer.parseInt(args[1]);
        int c = Integer.parseInt(args[2]);
        // Prints true or false in the terminal window.
        boolean positiveSide = (a > 0) & (b > 0) & (c > 0);
        boolean pythTripple = (a*a+b*b == c*c) | (b*b+c*c == a*a) | (c*c+a*a == b*b);
        boolean rightTriangle = positiveSide & pythTripple;
        System.out.println(rightTriangle);
    }

}
