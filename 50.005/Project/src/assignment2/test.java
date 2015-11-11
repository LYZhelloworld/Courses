package assignment2;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.Charset;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.security.NoSuchProviderException;
import java.security.PublicKey;
import java.security.SignatureException;

import javax.security.cert.CertificateException;
import javax.security.cert.X509Certificate;

import java.util.Base64;

public class test {
	public static void main(String[] args) throws CertificateException, InvalidKeyException, NoSuchAlgorithmException, 
	NoSuchProviderException, SignatureException, IOException{
		/*InputStream inStream = new FileInputStream("/Users/zikhan/CA.crt"); 
		X509Certificate CAcert = X509Certificate.getInstance(inStream);
		PublicKey key = CAcert.getPublicKey();
		CAcert.checkValidity();
		CAcert.verify(key);*/
		//configure private key to byte array
        File filePrivateKey = new File("/Users/zikhan/network/privateServer.der");
        @SuppressWarnings("resource")
		FileInputStream isPrivateKey = new FileInputStream(filePrivateKey);
        byte[] bytePrivateKey = new byte[(int) filePrivateKey.length()];
        isPrivateKey.read(bytePrivateKey);
        
        //configure public key to byte array
        File filePublicKey = new File("/Users/zikhan/network/publicServer.der");
        FileInputStream isPublicKey = new FileInputStream(filePublicKey);
        byte[] bytePublicKey = new byte[(int) filePublicKey.length()];
        isPublicKey.read(bytePublicKey);
        
        //using private key to encode a message 
        RSAPrivateSecurity rsa = new RSAPrivateSecurity(bytePrivateKey);
        RSAPublicSecurity rsapub = new RSAPublicSecurity(bytePublicKey);
        String msg = "Hello, this is SecStore!";
        byte[] returnMsg = rsa.encode(msg.getBytes());
        byte[] decoded = rsapub.decode(returnMsg);
        System.out.println(new String(decoded));
        
        File filecert = new File("/Users/zikhan/CA.crt");
        @SuppressWarnings("resource")
		FileInputStream fis = new FileInputStream(filecert);
        byte[] cacert = new byte[(int) filecert.length()];
        fis.read(cacert);
        
        File certificate = new File("/Users/zikhan/network/server.crt");
		@SuppressWarnings("resource")
		FileInputStream inStream = new FileInputStream(certificate); 
        byte[] cert = new byte[(int) certificate.length()];
        inStream.read(cert);
        
		X509Certificate CAcert = X509Certificate.getInstance(cacert);
		X509Certificate Servercert = X509Certificate.getInstance(cert);
		PublicKey key = CAcert.getPublicKey();
		Servercert.checkValidity();
		Servercert.verify(key);
		System.out.println("Certificate verified!");
		
		PublicKey pubKey = Servercert.getPublicKey();
		RSAPublicSecurity pub = new RSAPublicSecurity(pubKey);
		byte[] decodedmsg = pub.decode(returnMsg);
		System.out.println(new String(decodedmsg));
        
	}
}
