import java.awt.Color;
import java.awt.Font;
import java.util.ArrayList;
import java.util.TreeMap;

public class BarChartRacer {
    // color palette for bars
    private static final Color[] COLORS = initColors();

    private final String title;               // bar chart title
    private final String xAxisLabel;          // x-axis label
    private final String dataSource;          // data source
    private String caption;                   // caption
    private TreeMap<String, Color> colorOf;   // map category to color
    private ArrayList<Bar> bars;          // list of bars
    private ArrayList<Color> colors;          // list of bar colors
    private boolean isSetMaxValue = false;
    private int maxValue = 0;

    public BarChartRacer(String title, String xAxisLabel, String dataSource) {
        if (title == null) throw new IllegalArgumentException("name is null");
        if (xAxisLabel == null) throw new IllegalArgumentException("x-axis label is null");
        if (dataSource == null) throw new IllegalArgumentException("data source is null");
        this.title = title;
        this.xAxisLabel = xAxisLabel;
        this.dataSource = dataSource;
        colorOf = new TreeMap<String, Color>();
        colors = new ArrayList<Color>();
        reset();
    }

    // initialize the colors
    private static Color[] initColors() {

        // 12 colors from http://colorbrewer2.org/#type=qualitative&scheme=Set3&n=12
        String[] hex12 = {
            "#80b1d3", "#fdb462", "#b3de69", "#fccde5",
            "#8dd3c7", "#ffffb3", "#bebada", "#fb8072",
            "#d9d9d9", "#bc80bd", "#ccebc5", "#ffed6f"
        };

        // 20 colors from https://vega.github.io/vega/docs/schemes/
        // replaced #d62728 with #d64c4c
        String[] hex20 = {
            "#aec7e8", "#c5b0d5", "#c49c94", "#dbdb8d", "#17becf",
            "#9edae5", "#f7b6d2", "#c7c7c7", "#1f77b4", "#ff7f0e",
            "#ffbb78", "#98df8a", "#d64c4c", "#2ca02c", "#9467bd",
            "#8c564b", "#ff9896", "#e377c2", "#7f7f7f", "#bcbd22", 
        };

        // use 20 colors
        Color[] colors = new Color[hex20.length];
        for (int i = 0; i < hex20.length; i++)
            colors[i] = Color.decode(hex20[i]);
        return colors;
    }

    /**
     * Sets the maximum x-value of this bar chart (instead of having it set automatially).
     * This method is useful if you know that the values stay within a given range.
     *
     * @param maxValue the maximum value
     */
    public void setMaxValue(int maxValue) {
        if (maxValue <= 0) throw new IllegalArgumentException("maximum value must be positive");
        this.isSetMaxValue = true;
        this.maxValue = maxValue;
    }

    /**
     * Sets the caption of this bar chart.
     * The caption is drawn in the lower-right part of the window.
     *
     * @param caption the caption
     */
    public void setCaption(String caption) {
        if (caption == null) throw new IllegalArgumentException("caption is null");
        this.caption = caption;
    } 

    /**
     * Adds a bar to the bar chart.
     * The length of a bar is proportional to its value.
     * The bars are drawn from top to bottom in the order they are added.
     * All bars from the same category are drawn with the same color.
     *
     * @param name     the name of the bar
     * @param value    the value of the bar
     * @param category the category of bar
     */
    public void add(Bar bar) {
        String category = bar.getCategory();
        if (!colorOf.containsKey(category)) {
            colorOf.put(category, COLORS[colorOf.size() % COLORS.length]);
        }
        Color color = colorOf.get(category);
        bars.add(bar);
        colors.add(color);
    } 

    /**
     * Removes all of the bars from this bar chart (but keep the color scheme).
     * This method is convenient when drawing an animated bar chart.
     */
    public void reset() {
        bars = new ArrayList<Bar>();
        caption = "";
    } 

    // compute units (multiple of 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, ...)
    // so that between 4 and 8 axes labels
    private static int getUnits(double xmax) {
        int units = 1;
        while (Math.floor(xmax / units) >= 8) {
            // hack to identify 20, 200, 2000, ...
            if (units % 9 == 2)  units = units * 5 / 2;
            else                 units = units * 2;
        }
        return units;
    }

    /**
     * Draws this bar chart to standard draw.
     */
    public void draw() {
        // nothing to draw
        if (bars.isEmpty()) return;

        // leave room for at least 8 bars
        int numberOfBars = Math.max(8, bars.size());

        // set the scale of the coordinate axes
        double xmax = Double.NEGATIVE_INFINITY;
        for (Bar bar : bars) {
            int value = bar.getValue();
            if (value > xmax) xmax = value;
        }
        if (isSetMaxValue) xmax = maxValue;

        StdDraw.setXscale(-0.01 * xmax, 1.2 * xmax);
        StdDraw.setYscale(-0.01 * numberOfBars, numberOfBars * 1.25);

        // draw title
        StdDraw.setPenColor(StdDraw.BLACK);
        StdDraw.setFont(new Font("SansSerif", Font.BOLD, 24));
        StdDraw.text(0.6 * xmax, numberOfBars * 1.2, title);

        // draw x-axis label
        StdDraw.setPenColor(StdDraw.GRAY);
        StdDraw.setFont(new Font("SansSerif", Font.PLAIN, 16));
        StdDraw.textLeft(0, numberOfBars * 1.10, xAxisLabel);

        // draw axes
        int units = getUnits(xmax);
        StdDraw.setFont(new Font("SansSerif", Font.PLAIN, 12));
        for (int unit = 0; unit <= xmax; unit += units) {
            StdDraw.setPenColor(StdDraw.GRAY);
            StdDraw.text(unit, numberOfBars * 1.02, String.format("%,d", unit));
            StdDraw.setPenColor(new Color(230, 230, 230));
            StdDraw.line(unit, 0.1, unit, numberOfBars * 1.0);
        }

        // draw caption
        StdDraw.setPenColor(StdDraw.LIGHT_GRAY);
        if      (caption.length() <= 4) StdDraw.setFont(new Font("SansSerif", Font.BOLD, 100));
        else if (caption.length() <= 8) StdDraw.setFont(new Font("SansSerif", Font.BOLD, 60));
        else                            StdDraw.setFont(new Font("SansSerif", Font.BOLD, 40));
        StdDraw.textRight(1.15 * xmax, 0.2 * numberOfBars, caption);

        // draw data source acknowledgment
        StdDraw.setPenColor(StdDraw.LIGHT_GRAY);
        StdDraw.setFont(new Font("SansSerif", Font.PLAIN, 14));
        StdDraw.textRight(1.14 * xmax, 0.1 * numberOfBars, dataSource);

        // draw bars
        for (int i = 0; i < bars.size(); i++) {
            Bar bar = bars.get(i);
            String name = bar.getName();
            int value = bar.getValue();
            Color color = colors.get(i);
            StdDraw.setPenColor(color);
            StdDraw.filledRectangle(0.5 * value, numberOfBars - i - 0.5, 0.5 * value, 0.4); 
            StdDraw.setPenColor(StdDraw.BLACK);
            int fontSize = (int) Math.ceil(14 * 10.0 / numberOfBars);
            StdDraw.setFont(new Font("SansSerif", Font.BOLD, fontSize));
            StdDraw.textRight(value - 0.01 * xmax, numberOfBars - i - 0.5, name);
            StdDraw.setFont(new Font("SansSerif", Font.PLAIN, fontSize));
            StdDraw.setPenColor(StdDraw.DARK_GRAY);
            StdDraw.textLeft(value + 0.01 * xmax, numberOfBars - i - 0.5, String.format("%,d", value));
        }
    }


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
            BarChartRacer chart = new BarChartRacer(title, xAxis, source);
            int n = Integer.parseInt(lines[i++]);
            for (int j = 0; j < n; ++j) {
                if (j >= k) { i++; continue;}
                String [] ss = lines[i++].split(",");
                String year = ss[0];
                chart.setCaption(year);
                String name = ss[1];
                int value = Integer.parseInt(ss[3]);
                String category = ss[4];
                // add the bars to the bar chart
                chart.add(new Bar(name, value, category));        
            }    
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
