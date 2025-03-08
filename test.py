from minesweeper import MinesweeperAI, Sentence
import random

# add_new_sentence = MinesweeperAI().add_knowledge((1,5), 8)
# add_new_sentence = MinesweeperAI().add_knowledge((0,7), 2)

# print(MinesweeperAI().get_neighbors((0,7)))


# sent1 = Sentence({(0,2),(1,2),(1,3)}, 2)
# sent2 = Sentence({(1,3),(0,0),(0,1),(0,2),(1,0),(1,2),(2,0),(2,1),(2,2)}, 0)
# sent1.mark_safe((1,3))

# print(sent1.known_mines())
# print(sent2)

# print(sent1.known_safes().issubset(sent2.known_safes()))

test = {(3,4),(4,7),(7,1)}

print(random.choice(list(test)))