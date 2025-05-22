/******************************************************************************
 *  Compilation:  javac KernelFilter.java
 *  Execution:    java KernelFilter
 *
 ******************************************************************************/

public class KernelFilter {

    private static int[][] convolve(int [][] image, double [][] kernel) {
        int m = image.length;
        int n = image[0].length;
        int k = kernel.length;
        int [][] out = new int[m][n];
        for (int i = 0; i < m; ++i) {
            for (int j = 0; j < n; ++j) {
                double p = 0;
                for (int ii = (i - k/2 + m)%m, ki = 0; ki < k; ++ki, ii = (ii+1)%m) {
                    for (int jj = (j - k/2 + n)%n, kj = 0; kj < k; ++kj, jj = (jj+1)%n) {
                        p += kernel[ki][kj] * image[ii][jj];
                    }
                }
                out[i][j] = Math.max(0, Math.min(255, (int) Math.round(p)));
            }
        }
        return out;
    }

    private static int[][][] prictureToArray(Picture picture) {
        int m = picture.width();
        int n = picture.height();
        int [][][] image = new int[m][n][4];
        for (int i = 0; i < m; ++i) {
            for (int j = 0; j < n; ++j) {
                int rgb = picture.getRGB(i, j);
                int a = (rgb >> 24) & 0xFF;
                int r = (rgb >> 16) & 0xFF;
                int g = (rgb >>  8) & 0xFF;
                int b = (rgb >>  0) & 0xFF;
                image[i][j][0] = r;
                image[i][j][1] = g;
                image[i][j][2] = b;
                image[i][j][3] = a;
            }
        }
        return image;
    } 

    private static int[][] getChannel(int [][][] image, int channel) {
        int m = image.length;
        int n = image[0].length;
        int [][] grayImage = new int[m][n];
        for (int i = 0; i < m; ++i) {
            for (int j = 0; j < n; ++j) {
                grayImage[i][j] = image[i][j][channel];
            }
        }
        return grayImage;
    }  

    private static int [][][] setChannel(int [][][] image, int [][] grayImage, int channel) {
        int m = image.length;
        int n = image[0].length;
        for (int i = 0; i < m; ++i) {
            for (int j = 0; j < n; ++j) {
                image[i][j][channel] = grayImage[i][j];
            }
        }
        return image;
    }  

    private static Picture arrayToPicture(int [][][] image) {
        int m = image.length;
        int n = image[0].length;
        Picture p = new Picture(m, n);
        for (int i = 0; i < m; ++i) {
            for (int j = 0; j < n; ++j) {
                int r = image[i][j][0];
                int g = image[i][j][1];
                int b = image[i][j][2];
                int a = image[i][j][3];
                int argb = (a << 24) | (r << 16) | (g << 8) | (b << 0);
                p.setRGB(i, j, argb);             
            }
        }
        return p;
    }

    private static Picture convolvePictureWithKernel(Picture picture, double[][] kernel) {
       int [][][] image = prictureToArray(picture);
       for (int channel = 0; channel < 3; ++channel) {
        int [][] gray = getChannel(image, channel);
        //System.out.println(channel);
        gray = convolve(gray, kernel);
        setChannel(image, gray, channel);
       }
       return arrayToPicture(image);
    }

    // Returns a new picture that applies the identity filter to the given picture.
    public static Picture identity(Picture picture) {
       double [][] kernel = {{0,0,0}, {0,1,0}, {0,0,0}};
       return convolvePictureWithKernel(picture, kernel);
    }

    // Returns a new picture that applies a Gaussian blur filter to the given picture.
    public static Picture gaussian(Picture picture) {
       double [][] kernel = {{1./16,2./16,1./16}, 
                             {2./16,4./16,2./16}, 
                             {1./16,2./16,1./16}};
       return convolvePictureWithKernel(picture, kernel);
     }

    // Returns a new picture that applies a sharpen filter to the given picture.
    public static Picture sharpen(Picture picture) {
       double [][] kernel = {{0,-1,0}, {-1,5,-1}, {0,-1,0}};
       return convolvePictureWithKernel(picture, kernel);
      }

    // Returns a new picture that applies an Laplacian filter to the given picture.
    public static Picture laplacian(Picture picture) {
       double [][] kernel = {{-1,-1,-1}, {-1,8,-1}, {-1,-1,-1}};
       return convolvePictureWithKernel(picture, kernel);
    }

    // Returns a new picture that applies an emboss filter to the given picture.
    public static Picture emboss(Picture picture) {
       double [][] kernel = {{-2,-1,0}, {-1,1,1}, {0,1,2}};
       return convolvePictureWithKernel(picture, kernel);
     }

    // Returns a new picture that applies a motion blur filter to the given picture.
    public static Picture motionBlur(Picture picture) {
       double [][] kernel = new double[9][9];
       for (int i = 0; i < 9; ++i) {
        kernel[i][i] = 1./9;
       }
       return convolvePictureWithKernel(picture, kernel);
    }

    // Test client (ungraded).
    public static void main(String[] args) {
        // javac -cp ".lift/*" .\KernelFilter.java
        // java -cp "./;./.lift/stdlib.jar" KernelFilter
        Picture p = new Picture("baboon1.png");
        Picture out = motionBlur(p); 
        out.show();
        //out.save("out.png");
   }

}