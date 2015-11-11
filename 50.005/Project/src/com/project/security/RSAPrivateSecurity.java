package com.project.security;

import java.security.KeyFactory;
import java.security.NoSuchAlgorithmException;
import java.security.PrivateKey;
import java.security.spec.InvalidKeySpecException;
import java.security.spec.PKCS8EncodedKeySpec;
import java.util.Base64;

import javax.crypto.Cipher;

public final class RSAPrivateSecurity extends Security {
	private PrivateKey privKey = null;
	
	public RSAPrivateSecurity(String privateKeyData) {
		try {
	        privKey = KeyFactory.getInstance("RSA").generatePrivate(
	        		new PKCS8EncodedKeySpec(Base64.getDecoder().decode(privateKeyData)));
		} catch (InvalidKeySpecException | NoSuchAlgorithmException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	@Override
	public byte[] encode(byte[] data) {
		Cipher rsaCipher;
		try {
			rsaCipher = Cipher.getInstance("RSA/ECB/PKCS1Padding");
			rsaCipher.init(Cipher.ENCRYPT_MODE, privKey);
			return Base64.getEncoder().encode(rsaCipher.doFinal(data));
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return null;
		}	
	}
}
