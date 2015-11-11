package week12.ex1;

import java.util.ArrayList;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

/*
 * Apply SPMD (Single Program, Multiple Data) design pattern for concurrent programming to parallelize the program which 
 * approximates $\pi$ by integrating the following formula $4/(1+x^2 )$. Hint: In the SPMD design pattern, all threads 
 * run the same program, operating on different data.
 */
public class Exercise1 {
	public static void main(String[] args) throws Exception {
		int NTHREADS = 1000;
		ExecutorService exec = Executors.newFixedThreadPool(NTHREADS - 1);
		// TODO: complete the program by writing your code below.
		ArrayList<Future<Double>> futures = new ArrayList<Future<Double>>();
		for(int i = 0; i < NTHREADS; ++i) {
			final int ii = i;
			futures.add(exec.submit(new Callable<Double>() {
				@Override
				public Double call() throws Exception {
					return new Double(integrate(getRange(ii, NTHREADS - 1), getRange(ii + 1, NTHREADS - 1)));
				}
			}));
		}
		double sum = 0;
		for(Future<Double> f: futures) {
			sum += f.get().doubleValue();
		}
		
		System.out.println(sum);

		exec.shutdown();
	}
	
	public static double getRange(int i, int parts) {
		double size = (double)1 / parts;
		if(i == parts) return 1;
		else return size * i;
	}

	public static double f(double x) {
		return 4.0 / (1 + x * x);
	}

	// the following does numerical integration using Trapezoidal rule.
	public static double integrate(double a, double b) {
		int N = 10000; // preciseness parameter
		double h = (b - a) / (N - 1); // step size
		double sum = 1.0 / 2.0 * (f(a) + f(b)); // 1/2 terms

		for (int i = 1; i < N - 1; i++) {
			double x = a + h * i;
			sum += f(x);
		}

		return sum * h;
	}
}
