package week03.ex3;

class Robot {
	String name;
	private IBehaviour behaviour;

	public Robot (String name)
	{
		this.name = name;
		this.behaviour = new normalBehaviour();
	}

	public void behave ()
	{
		//the robots behave differently
		switch(this.behaviour.moveCommand()) {
			case 0:
				System.out.println(this.name + ": normal behaviour");
				break;
			case 1:
				System.out.println(this.name + ": aggressive behaviour");
				break;
			case 2:
				System.out.println(this.name + ": defensive behaviour");
				break;
		}
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}
	
	public void setBehavior(IBehaviour newBehaviour) {
		//todo
		this.behaviour = newBehaviour;
	}
}

interface IBehaviour {
	public int moveCommand();
}

class normalBehaviour implements IBehaviour {
	public int moveCommand() {
		return 0;
	}
}

class aggressiveBehaviour implements IBehaviour {
	public int moveCommand() {
		return 1;
	}
}

class defensiveBehaviour implements IBehaviour {
	public int moveCommand() {
		return 2;
	}
}

class RobotGame {

	public static void main(String[] args) {

		Robot r1 = new Robot("Big Robot");
		Robot r2 = new Robot("George v.2.1");
		Robot r3 = new Robot("R2");

		r1.setBehavior(new normalBehaviour());
		r2.setBehavior(new aggressiveBehaviour());
		r3.setBehavior(new defensiveBehaviour());
		
		r1.behave();
		r2.behave();
		r3.behave();

		//change the behaviors of each robot.
		r1.setBehavior(new aggressiveBehaviour());
		r2.setBehavior(new defensiveBehaviour());
		r3.setBehavior(new normalBehaviour());
		
		r1.behave();
		r2.behave();
		r3.behave();
	}
}