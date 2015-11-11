package week08.hw1;

/**
 * A general class: Meal
 */
public abstract class Meal {
	private String name;
	private int t_cook;
	
	/**
	 * Create an instance of Meal
	 * @param name: name of the meal
	 * @param cookTime: cooking time of the meal (ms)
	 */
	public Meal(String name, int cookTime) {
		this.name = name;
		this.t_cook = cookTime;
	}
	
	/**
	 * Get name of the meal
	 * @return: name
	 */
	public String getName() {
		return this.name;
	}
	
	/**
	 * Same as getName()
	 */
	public String toString() {
		return getName();
	}
	
	/**
	 * Get cooking time of the meal
	 * @return: cooking time
	 */
	protected int getCookTime() {
		return this.t_cook;
	}
	
	/**
	 * Cook the meal. It takes time.
	 * The cooking process fails if it is interrupted
	 * @return true: succeeded; false: failed.
	 */
	public boolean cook() {
		try {
			Thread.sleep(getCookTime());
			return true;
		} catch (InterruptedException e) {
			return false;
		}
	}
}

class Set1 extends Meal {
	public Set1() {
		super("Set 1", 3000);
	}
}

class Set2 extends Meal {
	public Set2() {
		super("Set 2", 4000);
	}
}

class Set3 extends Meal {
	public Set3() {
		super("Set 3", 5000);
	}
}
