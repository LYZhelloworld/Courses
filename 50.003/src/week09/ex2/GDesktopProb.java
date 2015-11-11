package week09.ex2;

import java.io.File;
import java.io.FileFilter;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

public class GDesktopProb {
	private final static int N_CONSUMERS = 4;
	
	//it starts here
	public static void startIndexing (File[] roots) {
		BlockingQueue<File> queue = new LinkedBlockingQueue<File>();
		FileFilter filter = new FileFilter() {
			public boolean accept(File file) {return true;}
		};
		
		for (File root : roots) {
			(new FileCrawlerProb(queue, filter, root)).start();;
		}
		
		for (int i = 0; i < N_CONSUMERS; i++) {
			(new IndexerProb(queue)).start();
		}
	}
}

class FileCrawlerProb extends Thread {
	private final BlockingQueue<File> fileQueue; 
	private final FileFilter fileFilter; 	
	private final File root;
	
	FileCrawlerProb (BlockingQueue<File> queue, FileFilter filter, File root) {
		this.fileQueue = queue;
		this.fileFilter = filter;
		this.root = root;
	}
	
	public void run() {
		try {
			crawl(root);
		} catch (InterruptedException e) {
			Thread.currentThread().interrupt();
		}
	}
	
	private void crawl(File root) throws InterruptedException {
		File[] entries = root.listFiles(fileFilter);
		
		if (entries != null) {
			for (File entry : entries) {
				if (entry.isDirectory()) {
					crawl(entry);
				}
				else {
					fileQueue.put(entry);	
				}
			}
		}
	}
}

class IndexerProb extends Thread {
	private final BlockingQueue<File> queue;
	
	public IndexerProb (BlockingQueue<File> queue) {
		this.queue = queue;
	}
	
	public void run() {
		while (true) {
			try {
				indexFile(queue.take());
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				break;
			}
		}
	}

	private void indexFile(File file) {
		// code for analyzing the context of the file is skipped for simplicity	
		System.out.println(file.getName());
	}
}