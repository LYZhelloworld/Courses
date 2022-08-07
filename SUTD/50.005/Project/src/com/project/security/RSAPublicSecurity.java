package com.project.security;

import java.security.KeyFactory;
import java.security.NoSuchAlgorithmException;
import java.security.PublicKey;
import java.security.spec.InvalidKeySpecException;
import java.security.spec.X509EncodedKeySpec;
import java.util.Base64;

import javax.crypto.Cipher;

public class RSAPublicSecurity extends Security {
	private PublicKey pubKey = null;
	
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
		Cipher rsaCipher;
		try {
			rsaCipher = Cipher.getInstance("RSA/ECB/PKCS1Padding");
			rsaCipher.init(Cipher.DECRYPT_MODE, pubKey);
			return rsaCipher.doFinal(Base64.getDecoder().decode(ciphertext));
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return null;
		}
	}
}
