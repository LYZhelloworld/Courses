package Week1;
import java.io.BufferedReader;
import java.io.File;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Arrays;

public class SimpleShell {
	public static void main(String[] args) throws java.io.IOException {
		String commandLine;
		ArrayList<String> cmd;
		File currentDir = new File(".");
		BufferedReader console = new BufferedReader
				(new InputStreamReader(System.in));
		// we break out with ctrl + C
		
		ArrayList<ArrayList<String>> history = new ArrayList<ArrayList<String>>();
		
		while (true) {
			// read what the user entered
			System.out.print("jsh>");
			commandLine = console.readLine();
			
			// TODO: adding a history feature

			// if the user entered a return, just loop again
			if (commandLine.equals("")) {
				continue;
			}
			
			cmd = new ArrayList<String>(Arrays.asList(commandLine.split(" ")));
			
			if(cmd.get(0).trim().toLowerCase().equals("history")) {
				for(int i = 0; i < history.size(); ++i) {
					System.out.print(i);
					System.out.print(" ");
					System.out.println(String.join(" ", history.get(i)));
				}
				continue;
			} else if(cmd.get(0).trim().startsWith("!")) {
				if(cmd.get(0).charAt(1) == '!') {
					if(history.size() == 0) {
						System.out.println("The previous command does not exist.");
						continue;
					} else {
						cmd = history.get(history.size() - 1);
					}
				} else {
					int index = Integer.parseInt(cmd.get(0).substring(1));
					if(index < 0 || index >= history.size()) {
						System.out.println("Index out of range.");
						continue;
					} else {
						cmd = history.get(index);
					}
				}
			}
			
			if(cmd.get(0).trim().toLowerCase().equals("cd")) {
				history.add(cmd);
				if(cmd.size() == 1) {
					System.out.println(currentDir.getAbsolutePath());
					continue;
				}
				File path = new File(currentDir, cmd.get(1));
				if(!path.exists()) {
					System.out.println("Path does not exist.");
					continue;
				} else if(!path.isDirectory()) {
					System.out.println("Path is not a directory.");
					continue;
				} else {
					currentDir = path;
					continue;
				}
			}
			
			history.add(cmd);
			// TODO: creating the external process and executing the command in that process
			ProcessBuilder pBuilder = new ProcessBuilder(cmd);
			pBuilder = pBuilder.directory(currentDir);
			try {
				Process process = pBuilder.start();
				InputStream is = process.getInputStream();
				BufferedReader output = new BufferedReader(new InputStreamReader(is));
				String line;
				while((line = output.readLine()) != null) {
					System.out.println(line);
				}
			} catch(java.io.IOException e) {
				System.out.println(e.getMessage());
				continue;
			}
						
			// TODO: modifying the shell to allow changing directories
		}
	}
}