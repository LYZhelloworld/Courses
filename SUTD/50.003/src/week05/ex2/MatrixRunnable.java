package week05.ex2;

public class MatrixRunnable {
	public static void main(String[] args) {
		int[][] matrixA = {{1, 2, 3}, {4, 5, 6}};
		int[][] matrixB = {{1, 2}, {3, 4}, {5, 6}};
		int[][] result = new int[2][2];
		
		System.out.println("Matrix A:");
		printMatrix(matrixA);
		System.out.println("Matrix B:");
		printMatrix(matrixB);
		
		Thread thread1 = new Thread(new Calculator(matrixA, matrixB, result, 0));
		Thread thread2 = new Thread(new Calculator(matrixA, matrixB, result, 1));
		
		thread1.start();
		thread2.start();
		
		try {
			thread1.join();
			thread2.join();
			
			System.out.println("Result:");
			printMatrix(result);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	public static void printMatrix(int[][] matrix) {
		for(int i = 0; i < matrix.length; ++i) {
			for(int j = 0; j < matrix[0].length; ++j) {
				System.out.print(matrix[i][j]);
				System.out.print("\t");
			}
			System.out.println();
		}
	}
}

class Calculator implements Runnable {
	private int[][] A, B, result;
	private int line;
	
	public Calculator(int[][] matrixA, int[][] matrixB, int[][] result, int line) {
		this.A = matrixA;
		this.B = matrixB;
		this.result = result;
		this.line = line;
	}
	
	public void run() {
		int sum = 0;
		for(int n = 0; n < result[this.line].length; ++n) {
			sum = 0;
			for(int i = 0; i < A[this.line].length; ++i) {
				sum += A[this.line][i] * B[i][n];
			}
			result[this.line][n] = sum;
		}
	}
}