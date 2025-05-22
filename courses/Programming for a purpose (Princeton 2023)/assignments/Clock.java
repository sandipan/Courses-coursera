/******************************************************************************
 *  Compilation:  javac Clock.java
 *  Execution:    java Clock
 ******************************************************************************/

public class Clock {

    private int h, m;
    
    private void checkValid(int h, int m) {
        if (h < 0 || h > 23 || m < 0 || m > 59)
          throw new IllegalArgumentException();
    }

    // Creates a clock whose initial time is h hours and m minutes.
    public Clock(int h, int m) {
        checkValid(h, m);
        this.h = h;
        this.m = m;
    }

    private boolean isDigit(String s, int i) {
      return Character.isDigit(s.charAt(i));
    }

    // Creates a clock whose initial time is specified as a string, using the format HH:MM.
    public Clock(String s) {
      int h, m;
      h = m = -1;
      s = s.trim();
      if (s.length() != 5 ||
          !isDigit(s, 0) || !isDigit(s, 1) || 
          s.charAt(2) != ':' || 
          !isDigit(s, 3) || !isDigit(s, 4))
          throw new IllegalArgumentException();
      String[] ss = s.split(":");
      if (ss[0].length() !=2 || ss[1].length() != 2)
        throw new IllegalArgumentException();
      h = Integer.parseInt(ss[0]);
      m = Integer.parseInt(ss[1]);
      checkValid(h, m);
      this.h = h;
      this.m = m;
    }
 
    // Returns a string representation of this clock, using the format HH:MM.
    public String toString() {
      return String.format("%02d:%02d", this.h, this.m);
    }
 
    // Is the time on this clock earlier than the time on that one?
    public boolean isEarlierThan(Clock that) {
        return (this.h < that.h ||
                (this.h == that.h && this.m < that.m));
    }
 
    // Adds 1 minute to the time on this clock.
    public void tic() {
        if (this.m < 59) this.m += 1;
        else {
            this.m = 0;
            this.h += 1;
        }
    }
 
    // Adds Δ minutes to the time on this clock.
    public void toc(int delta) {
        if (delta < 0) throw new IllegalArgumentException();
        this.m += delta;
        if (this.m + delta > 59) {
            this.h += this.m / 60;
            this.m = this.m % 60;
            this.h %= 24;
        }
    }
 
    // Test client (see below).
    public static void main(String[] args) {
        Clock c = new Clock(17, 30);
        System.out.println(c.toString());
        Clock c2 = new Clock("18:15");
        System.out.println(c.isEarlierThan(c2));
        c.tic();
        System.out.println(c.toString());
        c.toc(50);
        System.out.println(c.toString());
    }
}
