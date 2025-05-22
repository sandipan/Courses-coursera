//import java.util.Arrays;

public class RightTriangle__ {

    public static void main(String[] args) {
        int a = Integer.parseInt(args[0]);
        int b = Integer.parseInt(args[1]);
        int c = Integer.parseInt(args[2]);
        //int[] sides = {a, b, c};
        //Arrays.sort(sides);
        //System.out.println(sides[0] > 0 & 
        //    sides[0]*sides[0] + sides[1]*sides[1] == sides[2]*sides[2] ? 
        //    true : false);
        System.out.println(a > 0 & b > 0 & c > 0 & 
            (a*a+b*b==c*c | b*b+c*c==a*a | c*c+a*a==b*b) ? 
            true : false);
    }

}
