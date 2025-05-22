class test {

  public static int Q2(int n) {
      if (n <= 0) return 1;
      return 1 + Q2(n-2) + Q2(n-3);
  }

  public static void Q3(int n) {
    if (n <= 0) return;
    System.out.println(n);
    Q3(n-2);
    Q3(n-3);
    System.out.println(n);
  }

  public static void Q4(int n) {
   if (n <= 0) return;
   System.out.println(n);
   Q4(n-2);
   Q4(n-3);
   System.out.println(n);
  }
  public static int Q5(int n) {
      int[] b = new int[n+1];
      b[0] = 1;
      for (int i = 2;	i <=n; i++)
      {
          b[i] = 0;
          for	(int j = 0; j <	i; j++)
              b[i] += b[j];
      }
      return b[n];
  }
  public static String duplicate(String s) {
   String t = s + s;
   return t;
 }



  public static void main(String[] args) {

    // System.out.println(Q2(6));
    // System.out.println(Q5(8));
    // Q3(6);
    // Q4(7);
    /*
    String s1 = "Hi";
    s1 = duplicate(s1);
    String t1 = "Bye";
    t1 = duplicate(duplicate(t1));
    System.out.println(s1 + t1);
    
    String example = "abcdabcdeabcd";
    String s = example.substring(1, 4);
    String t = example.substring(5, 8);
    System.out.println((s== t));
    System.out.println(s.equals(t)); 
    System.out.println(s.length() == t.length());
    
    String string1 = "hello";
    String string2 = string1;
    string1 = "world";
    System.out.println(string1 + string2);
  }
  int i, j;
  for (i = 0, j = 0; i < 10; i++)
    j += i;
  System.out.println(j);
  
  int n = 123456789;
  int m = 0;
  while (n != 0)
  {
    m = (10 * m) + (n % 10);
    n = n / 10;
  }
  System.out.println(m);


 int a = 3;
 int b = 2;
 int c = 4;
 if (a < b)
 {
     if (b < c)
     {
         if (c < a) System.out.println(a + " " + b + " " + c);
         else System.out.println(c + " " + b + " " + a);
     }
     else System.out.println(a + " " + c + " " + b);
 }
 else System.out.println(b + " " + a + " " + c);
  }
  int[] a = new int[10];
      
  for (int i = 0; i < 10; i++)
      a[i] = 9 - i;
        
  for (int i = 0; i < 10; i++)
    a[i] = a[a[i]];
      
  System.out.println(a[5]);
  int[] b = { 1, 2, 3 };
        int[] c = b;
        c[0] += b[2];
        c[1] += b[1];
        c[2] += b[0];
        System.out.println(c[0] + c[1] + c[2]);
        
        String string1 = "hello";
        String string2 = string1;
        string1 = "world";
        System.out.println(string1 + string2);
        */
        // javac -cp ".lift/*" .\test.java
        // java -cp "./;./.lift/stdlib.jar" test
        // cmd /c --% java -cp "./;./.lift/stdlib.jar" test < input.txt | java  -cp "./;./.lift/stdlib.jar" test | java  -cp "./;./.lift/stdlib.jar" test

        while (!StdIn.isEmpty())
        {
            int x = StdIn.readInt();
            if (!StdIn.isEmpty()) x += StdIn.readInt();
            StdOut.print(x + " ");
        }
        StdOut.println();

 }
}