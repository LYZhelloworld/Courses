package Week9;

import java.io.*;
import java.security.*;
import java.util.Arrays;
import java.util.Base64;

import javax.crypto.*;


public class DesStartingCode {

	//    private static Cipher ecipher;
	//    private static Cipher dcipher;
	//
	//    private static SecretKey key;

	public static void main(String[] args) throws Exception {
		//TODO: read input file, store in a byte[]
		String fileName = "InputFile1.data";
		File filePrivateKey = new File(fileName);
		FileInputStream fis;
		fis = new FileInputStream(fileName);
		byte[] dataByte = new byte[(int) filePrivateKey.length()];
		fis.read(dataByte);
		fis.close();

		//TODO: generate secret key using DES algorithm
		KeyGenerator keygen = KeyGenerator.getInstance("DES");
		SecretKey key = keygen.generateKey();

		//TODO: Create cipher object, configure it to do DES cryptography, set operation mode to encryption
		Cipher desCipher = Cipher.getInstance("DES/ECB/PKCS5Padding");
		desCipher.init(Cipher.ENCRYPT_MODE, key);
		
		//TODO: Do the DES encryption here, by calling method Cipher.doFinal(). Convert encrypted byte[] to Base64 format
		byte[] result = desCipher.doFinal(dataByte);
		
		byte[] encoded = Base64.getEncoder().encode(result);
		FileOutputStream fos = new FileOutputStream("InputFile1.des.base64.data");
		fos.write(encoded);
		fos.close();
		///////////////////////////////////
		for(byte i: encoded) {
			System.out.print((char) i);
		}
		System.out.println();
		///////////////////////////////////
		
		//TODO: set the cipher object to decryption mode
		desCipher.init(Cipher.DECRYPT_MODE, key);

		//TODO:  Do the DES decryption
		byte[] decrypted = desCipher.doFinal(result);

		System.out.println("The decrypted data and the original data are " + (Arrays.equals(dataByte, decrypted) ? "the same." : "different."));
	}

}