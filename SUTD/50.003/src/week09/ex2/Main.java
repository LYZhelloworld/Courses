package week09.ex2;

import java.io.File;

public class Main {
	public static void main(String[] args) {
		GDesktopProb.startIndexing(new File(".").listFiles());
	}
}
