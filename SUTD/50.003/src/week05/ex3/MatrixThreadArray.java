package week05.ex3;

public class MatrixThreadArray {
	private static final int NUMBEROFTHREADS = 10;
	
	public static void main(String[] args) {
		int[][] matrixA = new int[10][10];
		int[][] matrixB = new int[10][10];
		int[][] result = new int[10][10];
		
		//Initialize A, B (with my random values)
		for(int i = 0; i < matrixA.length; ++i) {
			for(int j = 0; j < matrixA[0].length; ++j) {
				matrixA[i][j] = (i + 1) * (j + 1);
			}
		}
		for(int i = 0; i < matrixB.length; ++i) {
			for(int j = 0; j < matrixB[0].length; ++j) {
				matrixB[i][j] = (matrixB.length - i) * (matrixB[0].length - j);
			}
		}
		
		System.out.println("Matrix A:");
		printMatrix(matrixA);
		System.out.println("Matrix B:");
		printMatrix(matrixB);
		
		Thread[] threads = new Thread[NUMBEROFTHREADS];
		for(int i = 0; i < NUMBEROFTHREADS; ++i) {
			int[] range = getRange(i, result.length, NUMBEROFTHREADS);
			threads[i] = new Thread(new Calculator(matrixA, matrixB, result,
					range[0], range[1]));
			threads[i].start();
		}
				
		
		try {
			for(int i = 0; i < NUMBEROFTHREADS; ++i) {
				threads[i].join();
			}
			
			System.out.println("Result:");
			printMatrix(result);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	/**
	 * Print a matrix
	 * @param matrix
	 */
	public static void printMatrix(int[][] matrix) {
		for(int i = 0; i < matrix.length; ++i) {
			for(int j = 0; j < matrix[0].length; ++j) {
				System.out.print(matrix[i][j]);
				System.out.print("\t");
			}
			System.out.println();
		}
	}
	
	/**
	 * Split a range into multiple sub-ranges.
	 * For example: (0, 100) -> (0, 25), (25, 50), (50, 75), (75, 100)
	 * @param index
	 * @param total
	 * @param parts
	 * @return
	 */
	public static int[] getRange(int index, int total, int parts) {
		float size = (float)total / parts;
		int[] result = new int[2];
		result[0] = (int)Math.ceil(size * index);
		result[1] = (int)Math.ceil(size * (index + 1));
		if(result[1] > total) result[1] = total;
		return result;
	}
}

class Calculator implements Runnable {
	private int[][] A, B, result;
	private int from, to;
	
	public Calculator(int[][] matrixA, int[][] matrixB, int[][] result, int from, int to) {
		this.A = matrixA; //Matrix A
		this.B = matrixB; //Matrix B
		this.result = result; //Memory space for result
		this.from = from; //Starting line (inclusive)
		this.to = to; //Ending line (exclusive)
	}
	
	public void run() {
		int sum;
		for(int m = from; m < to; ++m) {
			for(int n = 0; n < result[m].length; ++n) {
				sum = 0;
				for(int i = 0; i < A[m].length; ++i) {
					sum += A[m][i] * B[i][n];
				}
				result[m][n] = sum;
			}
		}
	}
}