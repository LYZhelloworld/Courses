package assignment2;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.security.PublicKey;

import javax.security.cert.X509Certificate;

public class ClientCP2a {
	private static int BUFFER = 8192;
	
	public static void main(String[] args) throws Exception {
		String dir = "./src/assignment2/";
		String input_file = "network/test.txt.txt";
		Socket client = new Socket("localhost", 5001);	
		BufferedReader in = new BufferedReader(
				new InputStreamReader(client.getInputStream()));
		DataInputStream din = new DataInputStream(client.getInputStream());
		PrintWriter out = new PrintWriter(client.getOutputStream(), true);
		DataOutputStream dout = new DataOutputStream(client.getOutputStream());
		out.println("Hello SecStore, please prove your identity!");
		out.flush();
		//signed message from server
		int slen = din.readInt();
		byte[] signed = new byte[slen];
		din.read(signed);
		
		out.println("Give me your certificate signed by CA!");
		out.flush();
		Thread.sleep(1000);
		int len = din.readInt();
		System.out.println("cert is "+len+" byte long!");
		//Thread.sleep(1000);
		byte[] cert = new byte[len];
		din.read(cert, 0, len);
		
		File filePrivateKey = new File(dir + "network/CA.crt");
        @SuppressWarnings("resource")
		FileInputStream fis = new FileInputStream(filePrivateKey);
        byte[] cacert = new byte[(int) filePrivateKey.length()];
        fis.read(cacert);
        
		X509Certificate CAcert = X509Certificate.getInstance(cacert);
		X509Certificate Servercert = X509Certificate.getInstance(cert);
		PublicKey key = CAcert.getPublicKey();
		Servercert.checkValidity();
		Servercert.verify(key);
		System.out.println("Certificate verified!");
		
		RSAPublicSecurity pub = new RSAPublicSecurity(Servercert.getPublicKey());
		byte[] msg = pub.decode(signed);
		String decodedMsg = new String(msg);
		System.out.println(decodedMsg);
		
		if(decodedMsg.startsWith("Hello, this is SecStore!")){
			
			long timestamp = new Long(decodedMsg.replaceAll("Hello, this is SecStore!", "")).longValue();
			
			dout.writeInt(200); //Send success code: 200
			dout.flush();
			dout.writeLong(timestamp);
			dout.flush();
			
			AESSecurity aes = new AESSecurity(); //Generate a new key
			byte[] bytekey = pub.encode(aes.getKey()); //Get encrypted AES key
			
			dout.writeInt(bytekey.length);
			dout.write(bytekey);
			dout.flush();			
			
			System.out.println("Start uploading file...");
			//start uploading file
			File file = new File(dir + input_file);
			FileInputStream fis1 = new FileInputStream(file);
			byte[] filedata = new byte[BUFFER];
			Long start = System.currentTimeMillis();
			while(true) {
				//Read file
				int result = fis1.read(filedata);
				if(result == -1) {
					dout.writeInt(0);
					dout.flush();
					break;
				}
				byte[] sending = aes.encode(filedata);

				dout.writeInt(sending.length);//Length of file
				dout.flush();
				din.readInt();
				dout.write(sending);
				dout.flush();

				if(!(din.readInt()==200)) {//Succeeded
					System.out.println("An error occurs while uploading.");
					return;
				}
			}

			fis1.close();
			System.out.println("Finished uploading file.");
			Thread.sleep(2000);

			Long end = System.currentTimeMillis();
			System.out.println("Server received file, time spent: " + (end-start));
		}else{
			dout.write(400);//send unsuccessful code: 400;
			dout.flush();
		}
		client.close();
	}
}
