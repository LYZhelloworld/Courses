package assignment2;

import java.security.KeyFactory;
import java.security.NoSuchAlgorithmException;
import java.security.PrivateKey;
import java.security.spec.InvalidKeySpecException;
import java.security.spec.PKCS8EncodedKeySpec;
import java.security.spec.X509EncodedKeySpec;
import java.util.ArrayList;
import java.util.Base64;

import javax.crypto.Cipher;

public final class RSAPrivateSecurity extends Security {
	private PrivateKey privKey = null;
	
	public RSAPrivateSecurity(byte[] privateKeyData) {
		
		try { 
	        privKey = KeyFactory
	        		.getInstance("RSA")
	        		.generatePrivate(new PKCS8EncodedKeySpec(
	        				privateKeyData));
		} catch (InvalidKeySpecException | NoSuchAlgorithmException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	@Override
	public byte[] decode(byte[] ciphertext) {
		int block = 128;
		int pointer = 0;
		byte[] thisblock;
		ArrayList<byte[]> result = new ArrayList<byte[]>();
		Cipher rsaCipher;
		try {
			while(pointer < ciphertext.length){
				if(ciphertext.length-pointer<block){
					thisblock = new byte[ciphertext.length-pointer];
					for(int i=0;i<thisblock.length;i++)
						thisblock[i] = ciphertext[pointer+i];
				}else{
					thisblock = new byte[block];
					for(int i=0;i<block;i++)
						thisblock[i] = ciphertext[pointer+i];
				}
				pointer += block;
				rsaCipher = Cipher.getInstance("RSA/ECB/PKCS1Padding");
				rsaCipher.init(Cipher.DECRYPT_MODE, privKey);
				result.add(rsaCipher.doFinal(thisblock));
			}
			int len = 0;
			for(byte[] b: result)len += b.length;
			int index = 0;
			byte[] output = new byte[len];
			for(byte[] b: result) {
				for(byte bb: b) output[index++] = bb;
			}
			return output;
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return null;
		}
	}
	public byte[] encode(byte[] ciphertext) {
		int block = 117;
		int pointer = 0;
		byte[] thisblock;
		ArrayList<byte[]> result = new ArrayList<byte[]>();
		Cipher rsaCipher;
		try {
			while(pointer < ciphertext.length){
				if(ciphertext.length-pointer<block){
					thisblock = new byte[ciphertext.length-pointer];
					for(int i=0;i<thisblock.length;i++)
						thisblock[i] = ciphertext[pointer+i];
				}else{
					thisblock = new byte[block];
					for(int i=0;i<block;i++)
						thisblock[i] = ciphertext[pointer+i];
				}
				pointer += block;
				rsaCipher = Cipher.getInstance("RSA/ECB/PKCS1Padding");
				rsaCipher.init(Cipher.ENCRYPT_MODE, privKey);
				result.add(rsaCipher.doFinal(thisblock));
			}
			int len = 0;
			for(byte[] b: result)len += b.length;
			int index = 0;
			byte[] output = new byte[len];
			for(byte[] b: result) {
				for(byte bb: b) output[index++] = bb;
			}
			return output;
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return null;
		}
	}
}
