/******************************************************************************
 *  Compilation:  javac ColorHSB.java
 *  Execution:    java ColorHSB
 ******************************************************************************/

public class ColorHSB {
    
    private int h, s, b;
    
    // Creates a color with hue h, saturation s, and brightness b.
    public ColorHSB(int h, int s, int b) {
        if (h < 0  || h > 359 || s < 0  || s > 100 || b < 0  || b > 100)
           throw new IllegalArgumentException();        
        this.h = h;
        this.s = s;
        this.b = b;
    }

    // Returns a string representation of this color, using the format (h, s, b).
    public String toString() {
        return "(" + this.h + ", " + this.s + ", " + b + ")";
    }

    // Is this color a shade of gray?
    public boolean isGrayscale() {
        return this.s == 0 || this.b == 0;
    }

    // Returns the squared distance between the two colors.
    public int distanceSquaredTo(ColorHSB that) {
        if (that == null)
           throw new IllegalArgumentException();
           double dh = Math.abs(this.h - that.h);
           double ds = this.s - that.s;
           double db = this.b - that.b;
        return (int) (Math.min(dh*dh, (360 - dh)*(360 - dh)) +
                        ds*ds + db*db);
    }

    // Sample client (see below).
    public static void main(String[] args) {
        // javac -cp ".lift/*" .\ColorHSB.java
        // java -cp "./;./.lift/stdlib.jar" ColorHSB
        int h = Integer.parseInt(args[0]);
        int s = Integer.parseInt(args[1]);
        int b = Integer.parseInt(args[2]);
        ColorHSB targetColor = new ColorHSB(h, s, b);
        String [] lines = StdIn.readAllLines();
        String matchColorName = null;
        ColorHSB matchColor = null;
        double matchDistance = Double.POSITIVE_INFINITY;
        for (int i = 0; i < lines.length; ++i) {
           String [] cs = lines[i].split("\\s+");
           String colorName = cs[0];
           h = Integer.parseInt(cs[1]);
           s = Integer.parseInt(cs[2]);
           b = Integer.parseInt(cs[3]);
           ColorHSB c = new ColorHSB(h, s, b);
           double d = targetColor.distanceSquaredTo(c);
           if (d < matchDistance) {
            matchColorName = colorName;
            matchColor = c;
            matchDistance = d;
           }
        }
        System.out.println(matchColorName + " " + matchColor.toString());
    }
}
