package week03.ex2;

public class PizzaStore {

	public Pizza orderPizza (String type) {
		Pizza pizza = null;
		PizzaFactory pizzaFactory = new PizzaFactory();
		
		if ((pizza = pizzaFactory.makePizza(type)) != null) {
			pizza.prepare();
			pizza.bake();
			pizza.cut();
			pizza.box();
			
			return pizza;
		} else return null;
		
	}
}

class Pizza {

	public void prepare() {
	}

	public void box() {
	}

	public void cut() {
	}

	public void bake() {
	}
}

class CheesePizza extends Pizza {}
class GreekPizza extends Pizza {}
class PepperoniPizza extends Pizza {}

class PizzaFactory {
	public Pizza makePizza(String type) {
		if (type.equals("cheese")) {
			return new CheesePizza();
		} else
		if (type.equals("greek")) {
			return new GreekPizza();
		} else
		if (type.equals("pepperoni")) {
			return new PepperoniPizza();
		} else return null;
	}
}