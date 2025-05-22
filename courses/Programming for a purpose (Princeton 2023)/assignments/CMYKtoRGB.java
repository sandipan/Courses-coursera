/******************************************************************************
 *  Compilation:  javac CMYKtoRGB.java
 *  Execution:    java CMYKtoRGB
 *
 *  converts from CMYK format to RGB format
 *  % java CMYKtoRGB 0.0 1.0 0.0 0.0    
 *  red   = 255
 *  green = 0
 *  blue  = 255
 *
 ******************************************************************************/

public class CMYKtoRGB {

    public static void main(String[] args) {
        double cyan = Double.parseDouble(args[0]);
        double magenta = Double.parseDouble(args[1]);
        double yellow = Double.parseDouble(args[2]);
        double black = Double.parseDouble(args[3]);
        double white = 1 - black;
        int red = (int) Math.round(255 * white * (1 - cyan));
        int green = (int) Math.round(255 * white * (1 - magenta));
        int blue = (int) Math.round(255 * white * (1 - yellow));
        // Prints red, green, blue values in the terminal window.
        System.out.println("red = " + red);
        System.out.println("green = " + green);
        System.out.println("blue = " + blue);
    }

}
