# Word Ladders

from search import Problem
from search import depth_first_tree_search

class WordLaddersProblem(Problem):

	def __is_valid_word(self, word):
	    return word in self.WORDS

	def __init__(self, initial, goal, wordlist):
		super(self.__class__, self).__init__(initial, goal)
		self.WORDS = set(i.lower().strip() for i in open(wordlist))

	def actions(self, state):
		result = []
		for i in range(len(state)):
			if state[i] != self.goal[i]:
				result.append(i)
		for action in result:
			if not self.__is_valid_word(self.result(state, action)):
				result.remove(action)
		return result

	def result(self, state, action):
		tmp_list = list(state)
		tmp_list[action] = self.goal[action]
		return ''.join(tmp_list)

if __name__ == '__main__':
	begin = raw_input('Input beginning word:')
	end = raw_input('Input ending word:')
	solution_node = depth_first_tree_search(WordLaddersProblem(begin, end, './words2.txt'))
	if solution_node is not None:
		print solution_node.solution()
	else:
		print 'No solutions.'
