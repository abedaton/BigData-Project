import java.util.ArrayList;
import java.util.Arrays;
import java.util.Random;

/* Distributed LOF Computing method */
public class DLC {
    public static void main(String[] args) {
        double[][] grid = generate_data(123, 5, 2);
        System.out.println(Arrays.deepToString(grid));

        System.out.println("calc distance");
        for (int i=0; i<grid.length; i++){
            for (int j=i+1; j<grid.length; j++) {
                double dis = dis(grid[i], grid[j]);
                System.out.println(dis);
            }
        }

        System.out.println("calc k distance");
        for (int i=0; i<grid.length; i++){
            double[] disk = disk(grid[i],3, grid);
            System.out.println(disk);
        }
    }

    public static double[][] generate_data(int seed, int number, int dimension) {
        Random generator = new Random(seed);
        double[][] data = new double[number][dimension];
        for (int i=0; i<number; i++){
            for (int j=0; j<dimension; j++){
                data[i][j] = generator.nextDouble();
            }
        }
        return data;
    }

    /*
    The distance between tuples p and q
    */
    public static double dis(double[] p, double[] q){
        int d = p.length;
        double res = 0;
        for (int i=0; i<d; i++){
            res += Math.pow((p[i] - q[i]), 2);
        }
        return Math.sqrt(res);
    }

    /*
    The actual k-distance of p in P
    (a) there exist at least k tuples q that dis(q,o) <= dis(p,o)
    (b) there exist at most k-1 tuples q' that dis(q',o) < dis(p,o)
    */
    public static double[] disk(double[] o, int k, double[][] grid){
        for (int i=0; i<grid.length & grid[i] != o; i++) {
            double[] p = grid[i];
            double d = dis(p,o);
            int countA = 0;
            int countB = 0;
            for (int j=0; i<grid.length & j!=i & grid[j] != o; j++) {
                double[] q = grid[j];
                if (dis(q,o) <= d){
                    countA += 1;
                }
                if (dis(q,o) < d){
                    countB += 1;
                }
            }
            if (countA >= k & countB <= k-1){
                return p;
            }
        }
        return null;
    }

    public static double[] min_max(double[][] grid, int i) {
        double gmax = -1;
        double gmin = -1;
        for (int c=0; c<grid.length; c++){
            if (grid[c][i] > gmax){
                gmax = grid[c][i];
            }
            if (grid[c][i] < gmin){
                gmin = grid[c][i];
            }
        }
        double[] res = {gmax, gmin};
        return res;
    }

    /* Given a tuple p and a grid g', the minimum distance between p and g' on the i-th dimension is */
    public static double disi(double[] p, double[][] grid, int i) {
        double[] min_max = min_max(grid, i);
        double gmax = min_max[0];
        double gmin = min_max[1];
        if (p[i] > gmax){
            return p[i]-gmax;
        } else if (p[i] < gmin) {
            return gmin-p[i];
        } else {
            return 0;
        }
    }

    /* the minimum distance between p and g' is */
    public static double dispPGrid(double[] p, double[][] grid) {
        double res = 0;
        for (int i=0; i<p.length; i++){
            res += Math.pow(disi(p, grid, i), 2);
        }
        return Math.sqrt(res);
    }

    public static boolean is_cross_grid(double[] p, double[][] grid, double localDistK){
        for (int i=0; i<p.length; i++) {
            double[] min_max = min_max(grid, i);
            double gmax = min_max[0];
            double gmin = min_max[1];
            if (p[i]-localDistK < gmin | p[i]+localDistK >= gmax) {
                return false;
            }
        }
        return true;
    }


    /* The local outlier factor of p */
    public static void dlc(int k, double[][] grid, double[][][] neighbours) {
        ArrayList<double[]> cross_grid_list = new ArrayList<double[]>();
        for (double[] p : grid) {
            double localDistK = 1; /* disk(p) !!! TO_DO */
            if (is_cross_grid(p, grid, localDistK)){
                cross_grid_list.add(p);
                for (double[][] adjacent : neighbours) {
                    if (dispPGrid(p, adjacent) < localDistK) {
                        /* Compute the related minimum rectangle in g' */
                    }
                }
            }
        }
        for (double[][] adjacent : neighbours) {
            /* Generate the integrated rectangle for g */
            /* Send the tuples in the integrated rectangle to g */
        }
        for (double[] p : cross_grid_list) {

        }
    }
}
