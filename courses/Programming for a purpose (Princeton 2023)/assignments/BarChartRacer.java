import java.util.ArrayList;
import java.util.Arrays;

public class BarChartRacer {

    // sample client 
    public static void main(String[] args) {
        // javac -cp ".lift/*" .\BarChartRacer.java
        // java -cp "./;./.lift/stdlib.jar" BarChartRacer
        String fileName = args[0];
        int k = Integer.parseInt(args[1]);
        String [] lines = new In(fileName).readAllLines();
        // create the bar chart
        String title = lines[0];
        String xAxis = lines[1];
        String source = lines[2];

        StdDraw.enableDoubleBuffering();
        StdDraw.setCanvasSize(1000, 700);
            
        int i = 4;
        while (i < lines.length) {
            BarChart chart = new BarChart(title, xAxis, source);
            int n = Integer.parseInt(lines[i++]);
            Bar[] bars = new Bar[n];
            for (int j = 0; j < n; ++j) {
                //if (j >= k) { i++; continue;}
                String [] ss = lines[i++].split(",");
                String year = ss[0];
                chart.setCaption(year);
                String name = ss[1];
                int value = Integer.parseInt(ss[3]);
                String category = ss[4];
                bars[j] = new Bar(name, value, category);
                // add the bars to the bar chart
            }    
            Arrays.sort(bars);
            for (int j = n-1; j >= n-k; -- j)
               chart.add(bars[j].getName(), bars[j].getValue(), bars[j].getCategory());        
            i++;
            // draw the bar chart
            StdDraw.clear();
            //StdDraw.setCanvasSize(1000, 700);
            chart.draw();
            StdDraw.show();
            StdDraw.pause(20);
        }
        
    }
}
