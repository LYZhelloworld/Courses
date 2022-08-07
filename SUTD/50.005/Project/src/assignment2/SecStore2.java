package assignment2;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStreamReader;
import java.net.ServerSocket;
import java.net.Socket;

@Deprecated
public class SecStore2 {
	public static void main(String[] args) throws Exception {
		String dir = "./src/assignment2/";
		ServerSocket serverSocket = new ServerSocket(5001);
    	System.out.println("This server runs on port " + serverSocket.getLocalPort());
        Socket clientSocket = serverSocket.accept();  
        System.out.println("(... connection established ...)");
        

        BufferedReader in = new BufferedReader(
                new InputStreamReader(clientSocket.getInputStream()));
        DataOutputStream dout = new DataOutputStream(
        		clientSocket.getOutputStream());
        
        //configure private key to byte array
        File filePrivateKey = new File(dir+"network/privateServer.der");
        @SuppressWarnings("resource")
		FileInputStream isPrivateKey = new FileInputStream(filePrivateKey);
        byte[] bytePrivateKey = new byte[(int) filePrivateKey.length()];
        isPrivateKey.read(bytePrivateKey);
        
        //configure public key to byte array
        File filePublicKey = new File(dir+"network/publicServer.der");
        @SuppressWarnings("resource")
		FileInputStream isPublicKey = new FileInputStream(filePublicKey);
        byte[] bytePublicKey = new byte[(int) filePublicKey.length()];
        isPublicKey.read(bytePublicKey);
        
        //using private key to encode a message 
        RSAPrivateSecurity rsa = new RSAPrivateSecurity(bytePrivateKey);
		//RSAPublicSecurity rsapub = new RSAPublicSecurity(bytePublicKey);
        
        AESSecurity aes = new AESSecurity(); //Generate a new key
		byte[] bytekey = aes.getKey(); //Get AES key
		//String msg = "Hello, this is SecStore!";
        byte[] returnMsg = rsa.encode(bytekey);
        
        //configure Certificate to byte array
        File certificate = new File(dir+"network/server.crt");
		@SuppressWarnings("resource")
		FileInputStream inStream = new FileInputStream(certificate); 
        byte[] cert = new byte[(int) certificate.length()];
        inStream.read(cert);
        int len = cert.length;
        
        //Sending signed message to client
        String inputLine;
        inputLine = in.readLine();
        if(inputLine.equals("Hello SecStore, please prove your identity!")){
        	dout.writeInt(returnMsg.length);
        	dout.flush();
        	dout.write(returnMsg);
        	dout.flush();
        }
        //send out encoded certificate
        inputLine = in.readLine();
        if(inputLine.equals("Give me your certificate signed by CA!")){
        	System.out.println("Received cert request!");
        	dout.writeInt(len);
        	dout.flush();
        	dout.write(cert);
        	dout.flush();
        }
        DataInputStream din = new DataInputStream(clientSocket.getInputStream());
        Thread.sleep(2000);
		/*
		ServerSocket serverSocket = new ServerSocket(5001);
		System.out.println("This server runs on port " + serverSocket.getLocalPort());
		Socket clientSocket = serverSocket.accept();  
		System.out.println("(... connection established ...)");

		BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
		DataOutputStream dout = new DataOutputStream(clientSocket.getOutputStream());

		AESSecurity aes = new AESSecurity(); //Generate a new key
		byte[] bytekey = aes.getKey(); //Get AES key
		int len = bytekey.length; //Get key length

		String inputLine = in.readLine();
		if(inputLine.equals("Give me your session key!")) { //Require key
			System.out.println("Received session key request!");
			dout.writeInt(len);
			dout.flush();
			dout.write(bytekey);
			dout.flush();
		}
		DataInputStream din = new DataInputStream(clientSocket.getInputStream());
		Thread.sleep(2000);*/

		int returnCode = din.readInt();
		if(returnCode==200) { //Succeeded
			System.out.println("Completed handshake");
			Thread.sleep(3000);
			
			int totalLength = 0;
			byte[] encodedFile;
			
			File f = new File(dir+"network/received_file");
			FileOutputStream fos = new FileOutputStream(f);
			
			while(true) {
				//Receive file
				int fileLen = din.readInt();
				if(fileLen == 0) break;
				dout.writeInt(200);
				dout.flush();
				Thread.sleep(1);
				encodedFile = new byte[fileLen];
				din.read(encodedFile, 0, fileLen);
				
				//System.out.println("Decoding file...");
				byte[] decodedFile = aes.decode(encodedFile);
				
				//File received
				dout.writeInt(200);
				dout.flush();
				
				//System.out.println("File Content: ");
				//System.out.println(new String(decodedFile));
				
				totalLength += fileLen;
				encodedFile = null;
				fos.write(removeTrailingZeros(decodedFile));
			}
			//System.out.println(totalLength + " bytes received.");
			System.out.println("Done.");
			fos.close();
		} else {
			System.out.println("Handshake failed");
		}
		
		serverSocket.close();
		clientSocket.close();
		in.close();
	}
	
	public static byte[] removeTrailingZeros( byte[] str ){
		if (str == null){
			return null;}
		int length,index ;length = str.length;
		index = length -1;
		for (; index >=0;index--)
		{
			if (str[index] != 0){
				break;}
		}
		byte[] result = new byte[index + 1];
		for(int i = 0; i < index + 1; ++i) {
			result[i] = str[i];
		}
		return result;
	}
}
