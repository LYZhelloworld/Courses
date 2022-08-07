package week03.hw4;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class LineCounter {
	private String path;
	
	public LineCounter(String path) {
		this.path = path;
	}
	
	public String getCount() {
		BufferedReader br = null;
		int result = 0;
		try {
			br = new BufferedReader(new FileReader(this.path));
			for(;br.readLine() != null;) {
				++result;
			}
			return "Number of lines in " + this.path + ": " + result;
		} catch(IOException e) {
			e.printStackTrace();
			return null;
		} finally {
			try {
				if(br != null) br.close();
			} catch(IOException e) {
				e.printStackTrace();
				return null;
			}
		}
	}
	
	public static void main(String args[]) {
		System.out.println(new LineCounter(".\\src\\LineCounter.java").getCount());
	}
}