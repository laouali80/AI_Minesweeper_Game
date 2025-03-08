# Minesweeper

Minesweeper is a puzzle game that consists of a grid of cells, where some of the cells contain hidden "mines." Clicking on a cell that contains a mine detonates the mine and causes the user to lose the game. Clicking on a "safe" cell (i.e., a cell that does not contain a mine) reveals a number that indicates how many neighboring cells—where a neighbor is a cell that is one square to the left, right, up, down, or diagonal from the given cell—contain a mine.

The goal of the game is to flag (i.e., identify) each of the mines. In many implementations of the game, including the one in this project, the player can flag a mine by right-clicking on a cell (or two-finger clicking, depending on the computer).

## Knowledge Representation

The AI's knowledge is represented as the following logical sentence:

```
{A, B, C, D, E, F, G, H} = 1
```

where `{A, B, C, etc.}` are a set of cells, and the number `1` is the count of mines among those cells. This representation allows the following inferences to be made, e.g.:

```
{D, E} = 0  # This implies that none of D, E contain mines, i.e., all are safe cells.
{A, B, C} = 3  # This implies that all cells A, B, and C contain a mine.
```

Furthermore, in general, when we have two sentences where sentence A is a subset of sentence B, a new sentence can be inferred:

```
setB - setA = countB - countA
```

Hence, while playing Minesweeper and clicking on cells, logical sentences are added to the AI's knowledge base. Often, as a new sentence is added to the knowledge base, further inferences can be made, allowing the identification of mines or safe spaces.

## Requirements

To run this project, ensure you have the following:

- **Python** version **3.12.2** or higher  
  Download Python: [https://www.python.org/downloads/](https://www.python.org/downloads/)

---

## Getting Started

Follow these steps to set up and run the project:

1. **Clone the repository** and navigate to the project directory:

   ```bash
   git clone https://github.com/laouali80/AI_Minesweeper_Game.git
   cd AI_Minesweeper_Game
   ```

2. **Install Virtual Environment**:

   - For Windows:
     ```bash
     pip install virtualenv
     ```
   - For Linux/Mac:
     ```bash
     pip3 install virtualenv
     ```

3. **Create a Virtual Environment**:

   - For Windows:
     ```bash
     python -m venv venv
     ```
   - For Linux/Mac:
     ```bash
     python3 -m venv venv
     ```

4. **Activate the Virtual Environment**:

   - For Windows:
     ```bash
     venv\Scripts\activate
     ```
   - For Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

5. **Install Dependencies**:

   Install the required packages using the following command:

   ```bash
   pip install -r requirements.txt
   ```

6. **Run the Game**:

   Start the game by running the following command:

   ```bash
   python runner.py
   ```

---

## Project Structure

- **`minesweeper.py`**:  
  Contains all of the logic for the game itself and for the AI to play the game. There are three classes defined in this file: `Minesweeper`, which handles the gameplay; `Sentence`, which represents a logical sentence that contains both a set of cells and a count; and `MinesweeperAI`, which handles inferring which moves to make based on knowledge.

- **`runner.py`**:  
  Contains all of the code to run the graphical interface for the game.

- **`requirements.txt`**: Lists the dependencies required to run the project.

---

## How It Works

The game keeps track of each non-mine cell and mine cell discovered and continuously updates its knowledge base.

---

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push them to the branch.
4. Submit a pull request.

---

## Acknowledgments

- Inspired by the **CS50 AI** course.

---

Enjoy solving the puzzles! 🎮
