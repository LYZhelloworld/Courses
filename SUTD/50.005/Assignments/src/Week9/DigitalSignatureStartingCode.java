package Week9;

import javax.crypto.Cipher;

import java.io.*;
import java.security.*;
import java.util.Base64;


public class DigitalSignatureStartingCode{

	public static void main(String[] args) throws Exception {
		//TODO: Read a file (arbitrary file), store to byte[]

		//TODO: read input file, store in a byte[]
		String fileName = "InputFile1.data";
		File filePrivateKey = new File(fileName);
		FileInputStream fis;
		fis = new FileInputStream(fileName);
		byte[] dataByte = new byte[(int) filePrivateKey.length()];
		fis.read(dataByte);
		fis.close();

		//TODO: generate a RSA keypair, obtain public key and private key from this keypair
		KeyPairGenerator keyGen = KeyPairGenerator.getInstance("RSA");
		keyGen.initialize(1024);
		KeyPair keyPair = keyGen.generateKeyPair();
		Key publicKey =  keyPair.getPublic();
		Key privateKey =  keyPair.getPrivate();  

		//TODO: Calculate message digest, using MD5 hash function
		MessageDigest md = MessageDigest.getInstance("MD5");
		md.update(dataByte);
		byte[] digest = md.digest();

		//TODO: Create RSA cipher object, configure it to do RSA cryptography,set operation mode to encryption with PRIVATE key.
		Cipher rsaCipher = Cipher.getInstance("RSA/ECB/PKCS1Padding");
		rsaCipher.init(Cipher.ENCRYPT_MODE, privateKey);

		//TODO: sign the  message digest
		byte[] signature = rsaCipher.doFinal(digest);
		byte[] encoded = Base64.getEncoder().encode(signature);
		FileOutputStream fos = new FileOutputStream("InputFile1.rsa.base64.data");
		fos.write(encoded);
		fos.close();
		///////////////////////////////////
		for(byte i: encoded) {
			System.out.print((char) i);
		}
		System.out.println();
		///////////////////////////////////
	}
}
