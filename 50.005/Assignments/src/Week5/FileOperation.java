package Week5;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.Date;

public class FileOperation {
	private static File currentDirectory = new File(System.getProperty("user.dir"));
	public static void main(String[] args) throws java.io.IOException {

		String commandLine;

		BufferedReader console = new BufferedReader
				(new InputStreamReader(System.in));

		while (true) {
			// read what the user entered
			System.out.print("jsh>");
			commandLine = console.readLine();

			// clear the space before and after the command line
			commandLine = commandLine.trim();

			// if the user entered a return, just loop again
			if (commandLine.equals("")) {
				continue;
			}
			// if exit or quit
			else if (commandLine.equalsIgnoreCase("exit") | commandLine.equalsIgnoreCase("quit")) {
				System.out.println("See you.");
				System.exit(0);
			}

			// check the command line, separate the words
			String[] commandStr = commandLine.split(" ");
			ArrayList<String> command = new ArrayList<String>();
			for (int i = 0; i < commandStr.length; i++) {
				command.add(commandStr[i]);
			}

			if(commandStr[0].equalsIgnoreCase("create")) {
				Java_create(currentDirectory, commandStr[1]);
				continue;
			}

			if(commandStr[0].equalsIgnoreCase("delete")) {
				Java_delete(currentDirectory, commandStr[1]);
				continue;
			}

			if(commandStr[0].equalsIgnoreCase("display")) {
				Java_cat(currentDirectory, commandStr[1]);
				continue;
			}

			if(commandStr[0].equalsIgnoreCase("list")) {
				if(commandStr.length == 1) {
					Java_ls(currentDirectory, "", "");
				} else if(commandStr.length == 2) {
					Java_ls(currentDirectory, commandStr[1], "");
				} else {
					Java_ls(currentDirectory, commandStr[1], commandStr[2]);
				}
				continue;
			}

			if(commandStr[0].equalsIgnoreCase("find")) {
				if(!Java_find(currentDirectory, commandStr[1]))
					System.out.println("The specified file name cannot be found.");
				continue;
			}

			if(commandStr[0].equalsIgnoreCase("tree")) {
				if(commandStr.length == 1) {
					Java_tree(currentDirectory, 0, "");
				} else if(commandStr.length == 2) {
					Java_tree(currentDirectory, Integer.parseInt(commandStr[1]), "");
				} else {
					Java_tree(currentDirectory, Integer.parseInt(commandStr[1]), commandStr[2]);
				}
				continue;
			}

			// other commands
			ProcessBuilder pBuilder = new ProcessBuilder(command);
			pBuilder.directory(currentDirectory);
			try{
				Process process = pBuilder.start();
				// obtain the input stream
				InputStream is = process.getInputStream();
				InputStreamReader isr = new InputStreamReader(is);
				BufferedReader br = new BufferedReader(isr);

				// read what is returned by the command
				String line;
				while ( (line = br.readLine()) != null)
					System.out.println(line);

				// close BufferedReader
				br.close();
			}
			// catch the IOexception and resume waiting for commands
			catch (IOException ex){
				System.out.println(ex);
				continue;
			}
		}
	}

	/**
	 * Create a file
	 * @param dir - current working directory
	 * @param command - name of the file to be created
	 */
	public static void Java_create(File dir, String name) {
		try {
			if(new File(dir, name).createNewFile()) {
				System.out.println("File is created successfully.");
			} else {
				System.out.println("File already exists.");
			}
		} catch (IOException e) {
			System.out.println("An error occurred: " + e.getMessage());
		}
	}

	/**
	 * Delete a file
	 * @param dir - current working directory
	 * @param name - name of the file to be deleted
	 */
	public static void Java_delete(File dir, String name) {
		if(new File(dir, name).delete()) {
			System.out.println("File is deleted successfully.");
		} else {
			System.out.println("File cannot be deleted.");
		}
	}

	/**
	 * Display the file
	 * @param dir - current working directory
	 * @param name - name of the file to be displayed
	 */
	public static void Java_cat(File dir, String name) {
		try {
			FileReader reader = new FileReader(new File(dir, name));
			int data;
			for(; (data = reader.read()) != -1; ) {
				System.out.print(Character.toChars(data));
			}
			System.out.println();
			reader.close();
		} catch (IOException e) {
			System.out.println("Cannot display file content.");
		}
	}

	/**
	 * Function to sort the file list
	 * @param list - file list to be sorted
	 * @param sort_method - control the sort type
	 * @return sorted list - the sorted file list
	 */
	private static File[] sortFileList(File[] list, String sort_method) {
		// sort the file list based on sort_method
		// if sort based on name
		if (sort_method.equalsIgnoreCase("name")) {
			Arrays.sort(list, new Comparator<File>() {
				public int compare(File f1, File f2) {
					return (f1.getName()).compareTo(f2.getName());
				}
			});
		}
		else if (sort_method.equalsIgnoreCase("size")) {
			Arrays.sort(list, new Comparator<File>() {
				public int compare(File f1, File f2) {
					return Long.valueOf(f1.length()).compareTo(f2.length());
				}
			});
		}
		else if (sort_method.equalsIgnoreCase("time")) {
			Arrays.sort(list, new Comparator<File>() {
				public int compare(File f1, File f2) {
					return Long.valueOf(f1.lastModified()).compareTo(f2.lastModified());
				}
			});
		}
		return list;
	}

	/**
	 * List the files under directory
	 * @param dir - current directory
	 * @param function - control the list type
	 * @param sort_method - control the sort type
	 */
	public static void Java_ls(File dir, String display_method, String sort_method) {
		File[] result = dir.listFiles();
		if(result == null) {
			System.out.println("Invalid path or an error occurs.");
			return;
		}
		result = sortFileList(result, sort_method);
		if(display_method.equalsIgnoreCase("property")) {
			for(File f: result) {
				System.out.println(f.getName() + "\t\tSize: " + f.length() + "\t\tLast Modified: " + new Date(f.lastModified()).toString());
			}
		} else {
			for(File f: result) {
				System.out.println(f.getName());
			}
		}
	}

	/**
	 * Find files based on input string
	 * @param dir - current working directory
	 * @param name - input string to find in file's name
	 * @return flag - whether the input string is found in this directory and its subdirectories
	 */
	public static boolean Java_find(File dir, String name) {
		boolean flag = false;

		File[] files = dir.listFiles();
		for(File f: files) {
			if(f.getName().contains(name)) {
				System.out.println(f.getAbsolutePath());
				flag = true;
			}
		}
		for(File f: files) {
			if(f.isDirectory()) {
				if(Java_find(f, name)) flag = true;
			}
		}
		
		return flag;
	}

	/**
	 * Print file structure under current directory in a tree structure
	 * @param dir - current working directory
	 * @param depth - maximum sub-level file to be displayed
	 * @param sort_method - control the sort type
	 */
	public static void Java_tree(File dir, int depth, String sort_method) {
		Java_tree_function(dir, depth, 1, sort_method);
	}

	// TODO: define other functions if necessary for the above functions
	private static void Java_tree_function(File dir, int depth, int currentDepth, String sort_method) {
		File[] files = sortFileList(dir.listFiles(), sort_method);

		for(File f: files) {
			if(currentDepth > 1) {
				for(int i = 1; i < currentDepth; ++i) {
					System.out.print("  ");
				}
				System.out.print("|-");
			}
			System.out.println(f.getName());
			if(f.isDirectory()) {
				if(depth > 0 && currentDepth < depth) {
					Java_tree_function(f, depth, currentDepth + 1, sort_method);
				} else if(depth == 0) {
					Java_tree_function(f, depth, currentDepth + 1, sort_method);
				}
			}
		}
	}
}