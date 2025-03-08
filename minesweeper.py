import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """

        if len(self.cells) == self.count or self.count != 0:
            return self.cells
        
        return set()


    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """

        if self.count == 0:
            return self.cells
        
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """

        if cell in self.cells:
            self.cells.discard(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        
        if cell in self.cells:
            self.cells.discard(cell)
            

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        
        # update the moves_made set with this new move
        self.moves_made.add(cell)

        # mark the cell safe        
        self.mark_safe(cell)

        # Get the cell's neighbors that are still unknown
        neighbors, count = self.get_neighbors(cell, count)

        # creation of a sentence and add it to the knowledge base
        self.knowledge.append(Sentence(neighbors, count))
        
        # Loop over the knowledge to derive new knowledge
        self.update_knowledge()

        # print(self.mines)



    def get_neighbors(self, cell, count):
        """Returns a set of unknown neighboring cells and an adjusted mine count."""
        
        sentence_set = set()
        
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                
                # ignoring the current cell i discover
                if (i, j) == cell:
                    continue
                
                # ignoring the cell if it is already safe
                if (i, j) in self.safes:
                    continue

                # ignoring the cell if it is already a mine and decrease the count as we already know that it is a mine
                if (i, j) in self.mines:
                    count -= 1
                    continue 
                
                if 0 <= i < 8 and 0 <= j < 8:
                    sentence_set.add((i, j))
        
        return sentence_set, count
    

 
    def update_knowledge(self):
        """Processes known information and derives new conclusions."""
        
        updated = True
        while updated:
            updated = False

            new_safes, new_mines = set(), set()

            # Identify known safe and mine cells
            for sentence in self.knowledge:
                new_safes.update(sentence.known_safes())
                new_mines.update(sentence.known_mines())

            # Mark all the new safes cells as safe and update each sentence that contains the cell to safe
            for cell in new_safes:
                if cell not in self.safes:
                    self.mark_safe(cell)
                    updated = True

            # Mark all the new mines cells as mine and update each sentence that contains the cell to mine
            for cell in new_mines:
                if cell not in self.mines:
                    self.mark_mine(cell)
                    updated = True

            # Generate new inferences
            inferred_sentences = []
            for s1 in self.knowledge:
                for s2 in self.knowledge:
                    if s1 == s2:
                        continue

                    # if s1 is a subset of s2 e.g: s1={a,b}  s2={a,b,c,d}; we derive a new sentence from the difference of the sets and counts
                    if s1.cells.issubset(s2.cells):
                        inferred_sentences.append(Sentence(s2.cells - s1.cells, s2.count - s1.count))
                    # Vice versa
                    elif s2.cells.issubset(s1.cells):
                        inferred_sentences.append(Sentence(s1.cells - s2.cells, s1.count - s2.count))
            
            # Add new inferences to the knowledge base
            for sentence in inferred_sentences:
                if sentence not in self.knowledge and sentence.cells:
                    self.knowledge.append(sentence)
                    updated = True
            
            # Remove empty sentences
            self.knowledge = [s for s in self.knowledge if s.cells]


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        safe_moves = self.safes.difference(self.moves_made)

        if safe_moves:
            return random.choice(list(safe_moves))
        
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        number_mines = 8
        undiscovered_mines = number_mines - len(self.mines)

        # Get the number of unexplored cells
        unexplored_cells = (self.height * self.width) - (len(self.moves_made) + len(self.mines))

        
        # If no unexplored cells remain, return None
        if unexplored_cells == 0:
            return None
        
        # Basic probability of any unexplored cell being a mine
        unexplored_cells_probability = undiscovered_mines / unexplored_cells

        # Possible moves on the board excluding known moves and mines
        possible_moves = dict()

        # get all the safe cells
        for i in range(self.width):
            for j in range(self.height):
                # only add the cell to possible_move if the cell is not in moves_made and not consider as mines
                if (i, j) not in self.moves_made and (i, j) not in self.mines:

                    # adding the cell to the possible_moves dictionary with the unexplored_cells_probality 
                    possible_moves[(i,j)] = unexplored_cells_probability
        
        # If this is the AI's first move (no knowledge yet), choose randomly
        if possible_moves and not self.knowledge:  
            return random.choice(list(possible_moves.keys()))
        

        # Improve move selection using knowledge
        else:
            # we go through each sentence cells and calculate each cell probability being a mine
            for sentence in self.knowledge:
                num_cells = len(sentence.cells)
                count = sentence.count

                # Probability of each cell being a mine in a sentence
                if num_cells > 0:
                    sentence_cells_probability = count / num_cells
                else:
                    continue

                # loop over each cell of the sentence
                for cell in sentence.cells:
                    # checks if the sentence_cells_probability is smaller then the unexplored_cells_probability(probality of each unexplored cell)
                    # Only update probability if cell is still in possible_moves
                    if cell in possible_moves and possible_moves[cell] > sentence_cells_probability:
                        # if so change the probability of the cell being a mine
                        possible_moves[cell] = sentence_cells_probability
                  
            # lowest_probability = 1
            # best_move = None
            # for move in possible_moves:
            #     # get the minimun probality 
            #     probability = min(lowest_probability, possible_moves[move])
            #     if probability <= lowest_probability :
            #         best_move = move
            #         lowest_probability = probability    


            # Select the move with the lowest probability
            best_move = min(possible_moves, key=possible_moves.get)

            return best_move