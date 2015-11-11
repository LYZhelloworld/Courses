package assignment2;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Random;

public class randomFileGenerator {
	private static final String CHARACTERS = 
			"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 ";
	private static final int LENGTH = CHARACTERS.length();
	
	public static void main(String[] args) throws Exception {
		String dir = "./src/assignment2/";
		File file = new File(dir + "network/input_1.txt");
		FileOutputStream fos = new FileOutputStream(file);
		outputRandomCharacters(fos, 1024);
		fos.close();

		file = new File(dir + "network/input_2.txt");
		fos = new FileOutputStream(file);
		outputRandomCharacters(fos, 2048);
		fos.close();
		
		file = new File(dir + "network/input_4.txt");
		fos = new FileOutputStream(file);
		outputRandomCharacters(fos, 4096);
		fos.close();
		
		file = new File(dir + "network/input_8.txt");
		fos = new FileOutputStream(file);
		outputRandomCharacters(fos, 8192);
		fos.close();
		
		file = new File(dir + "network/input_16.txt");
		fos = new FileOutputStream(file);
		outputRandomCharacters(fos, 16384);
		fos.close();
		
		file = new File(dir + "network/input_32.txt");
		fos = new FileOutputStream(file);
		outputRandomCharacters(fos, 32768);
		fos.close();
		
		file = new File(dir + "network/input_64.txt");
		fos = new FileOutputStream(file);
		outputRandomCharacters(fos, 65536);
		fos.close();
	}
	
	private static void outputRandomCharacters(FileOutputStream fos, int size) throws Exception {
		Random rnd = new Random();
		for(int i = 0; i < size; ++i) {
			fos.write(CHARACTERS.charAt(rnd.nextInt(LENGTH)));
		}
	}
}
