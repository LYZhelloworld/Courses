package assignment2;

import java.security.KeyFactory;
import java.security.NoSuchAlgorithmException;
import java.security.PublicKey;
import java.security.spec.InvalidKeySpecException;
import java.security.spec.PKCS8EncodedKeySpec;
import java.security.spec.X509EncodedKeySpec;
import java.util.ArrayList;
import java.util.Base64;

import javax.crypto.Cipher;


public class RSAPublicSecurity extends Security {
	private PublicKey pubKey = null;
	public RSAPublicSecurity(PublicKey key){
		pubKey = key;
	}
	public RSAPublicSecurity(byte[] publicKeyData) {
		try {
			pubKey = KeyFactory.getInstance("RSA").generatePublic(
					new X509EncodedKeySpec(publicKeyData));
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
				rsaCipher.init(Cipher.DECRYPT_MODE, pubKey);
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
	public byte[] encode(byte[] data){
		int block = 117;
		int pointer = 0;
		byte[] thisblock;
		ArrayList<byte[]> result = new ArrayList<byte[]>();
		Cipher rsaCipher;
		try {
			while(pointer < data.length){
				if(data.length-pointer<block){
					thisblock = new byte[data.length-pointer];
					for(int i=0;i<thisblock.length;i++)
						thisblock[i] = data[pointer+i];
				}else{
					thisblock = new byte[block];
					for(int i=0;i<block;i++)
						thisblock[i] = data[pointer+i];
				}
				pointer += block;
				rsaCipher = Cipher.getInstance("RSA/ECB/PKCS1Padding");
				rsaCipher.init(Cipher.ENCRYPT_MODE, pubKey);
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
	public static void main(String[] args){
		
	}
}
