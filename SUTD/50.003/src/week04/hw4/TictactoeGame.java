package week04.hw4;


public class TictactoeGame {
	private Tictactoe gameState;
	private TictactoeView gameView;
	private char turn;
	
	public TictactoeGame(TictactoeView gameView) {
		this.gameState = new Tictactoe();
		this.gameView = gameView;
		this.turn = 'O';
	}
	
	/**
	 * Start game.
	 */
	public void start() {
		for(;gameState.getWinner() == GameState.IN_PROGRESS;) {
			switch(this.turn) {
			case 'O':
				for(;;) {
					try {
						if(gameState.putO(gameView.putO())) {
							gameView.printState(gameState.getStates());
							break;
						}
					} catch(IllegalArgumentException e) {
						System.out.println(e.getMessage());
					}
				}
				this.turn = 'X';
				break;
			case 'X':
				for(;;) {
					try {
						if(gameState.putX(gameView.putX())) {
							gameView.printState(gameState.getStates());
							break;
						}
					} catch(IllegalArgumentException e) {
						System.out.println(e.getMessage());
					}
				}
				this.turn = 'O';
				break;
			}
		}
		
		if(gameState.getWinner() == GameState.X_WIN) {
			gameView.printWinner('X');
		} else if(gameState.getWinner() == GameState.O_WIN) {
			gameView.printWinner('O');
		} else {
			gameView.printWinner(' ');
		}
	}
}
