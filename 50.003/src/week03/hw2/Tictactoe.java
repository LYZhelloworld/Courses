package week03.hw2;

public class Tictactoe {
	private char state[]; //State of nine grids
	
	public Tictactoe() {
		this.state = new char[9];
		for(int i = 0; i < 9; ++i) {
			state[i] = ' ';
		}
	}
	
	/**
	 * Put an O mark at a grid.
	 * @param position: 0 to 8
	 * @return true: success; false: fail
	 * @throws IllegalArgumentException
	 */
	public boolean putO(int position) throws IllegalArgumentException {
		if(position < 0 || position > 8) throw new IllegalArgumentException("Invalid position number.");
		
		if(state[position] == ' ') {
			state[position] = 'O';
			return true;
		} else {
			return false;
		}
	}
	
	/**
	 * Put an X mark at a grid.
	 * @param position: 0 to 8
	 * @return true: success; false: fail
	 * @throws IllegalArgumentException
	 */
	public boolean putX(int position) throws IllegalArgumentException {
		if(position < 0 || position > 8) throw new IllegalArgumentException("Invalid position number.");
		
		if(state[position] == ' ') {
			state[position] = 'X';
			return true;
		} else {
			return false;
		}
	}
	
	/**
	 * Get states of grids.
	 * @return state of the grid
	 */
	public char[] getStates() {
		return state;
	}
	
	/**
	 * Decide who is the winner
	 * @return a GameState enum
	 */
	public GameState getWinner() {
		if(state[0] == 'O' && state[1] == 'O' && state[2] == 'O') {
			return GameState.O_WIN;
		}
		if(state[3] == 'O' && state[4] == 'O' && state[5] == 'O') {
			return GameState.O_WIN;
		}
		if(state[6] == 'O' && state[7] == 'O' && state[8] == 'O') {
			return GameState.O_WIN;
		}
		if(state[0] == 'O' && state[3] == 'O' && state[6] == 'O') {
			return GameState.O_WIN;
		}
		if(state[1] == 'O' && state[4] == 'O' && state[7] == 'O') {
			return GameState.O_WIN;
		}
		if(state[2] == 'O' && state[5] == 'O' && state[8] == 'O') {
			return GameState.O_WIN;
		}
		if(state[0] == 'O' && state[4] == 'O' && state[8] == 'O') {
			return GameState.O_WIN;
		}
		if(state[2] == 'O' && state[4] == 'O' && state[6] == 'O') {
			return GameState.O_WIN;
		}
		
		if(state[0] == 'X' && state[1] == 'X' && state[2] == 'X') {
			return GameState.X_WIN;
		}
		if(state[3] == 'X' && state[4] == 'X' && state[5] == 'X') {
			return GameState.X_WIN;
		}
		if(state[6] == 'X' && state[7] == 'X' && state[8] == 'X') {
			return GameState.X_WIN;
		}
		if(state[0] == 'X' && state[3] == 'X' && state[6] == 'X') {
			return GameState.X_WIN;
		}
		if(state[1] == 'X' && state[4] == 'X' && state[7] == 'X') {
			return GameState.X_WIN;
		}
		if(state[2] == 'X' && state[5] == 'X' && state[8] == 'X') {
			return GameState.X_WIN;
		}
		if(state[0] == 'X' && state[4] == 'X' && state[8] == 'X') {
			return GameState.X_WIN;
		}
		if(state[2] == 'X' && state[4] == 'X' && state[6] == 'X') {
			return GameState.X_WIN;
		}
		
		for(char i: state) {
			if(i == ' ') return GameState.IN_PROGRESS;
		}
		
		return GameState.DRAW;
	}
}

enum GameState {
	IN_PROGRESS,
	X_WIN,
	O_WIN,
	DRAW
}