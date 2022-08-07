package assignment2;

import java.security.NoSuchAlgorithmException;
import java.util.Base64;

import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;

public final class AESSecurity extends Security {
	private SecretKey key;
	
	/**
	 * Create an instance of AESSecurity, with a generated key.
	 */
	public AESSecurity() {
		try { 
			key = KeyGenerator.getInstance("AES").generateKey();
		} catch (NoSuchAlgorithmException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	/**
	 * Create an instance of AESSecurity, with a specific key.
	 * @param key: the key received from another AESSecurity instance.
	 */
	public AESSecurity(byte[] key) {
		byte[] decodedKey = Base64.getDecoder().decode(key); 
		this.key = new SecretKeySpec(decodedKey, 0, decodedKey.length, "AES");
	}
	
	/**
	 * Get the AES key.
	 * @return AES key (in Base64 form)
	 */
	public byte[] getKey() {
		return Base64.getEncoder().encode(key.getEncoded());
	}

	/**
	 * Encode data with key.
	 */
	@Override
	public byte[] encode(byte[] data) {
		Cipher aesCipher;
		try {
			aesCipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
			aesCipher.init(Cipher.ENCRYPT_MODE, key);
			return Base64.getEncoder().encode(aesCipher.doFinal(data));
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return null;
		}	
	}
	
	/**
	 * Decode data with key.
	 */
	@Override
	public byte[] decode(byte[] data) {
		Cipher aesCipher;
		try {
			aesCipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
			aesCipher.init(Cipher.DECRYPT_MODE, key);
			return aesCipher.doFinal(Base64.getDecoder().decode(data));
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return null;
		}
	}
}
