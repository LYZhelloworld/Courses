package week09.ex6;

import java.util.concurrent.BrokenBarrierException;
import java.util.concurrent.CyclicBarrier;
import java.util.concurrent.Phaser;

public class ExamSimulator {
	public static final int NUMBEROFSTUDENTS = 10;
	
	public static void main(String[] args) throws Exception {
		Phaser phaser = new Phaser();
		CyclicBarrier cb = new CyclicBarrier(NUMBEROFSTUDENTS + 1);
		
		phaser.register();
		for(int i = 1; i <= NUMBEROFSTUDENTS; ++i) {
			System.out.println("Student " + i + " arrives.");
			phaser.register();
			new Thread(new Student(phaser, cb), "Student " + i).start();
		}
		System.out.println("Exam starts.");
		phaser.arriveAndDeregister();
		
		cb.await();
		System.out.println("Done.");
	}
}

class Student implements Runnable {
	private Phaser p;
	private CyclicBarrier cb;
	
	public Student(Phaser p, CyclicBarrier cb) {
		this.p = p;
		this.cb = cb;
	}
	
	public void run() {
		p.arriveAndAwaitAdvance();
		System.out.println(Thread.currentThread().getName() + " is taking exam...");
		try {
			Thread.sleep(new java.util.Random().nextInt(10000));
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		System.out.println(Thread.currentThread().getName() + " has finished the exam.");
		try {
			cb.await();
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (BrokenBarrierException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}