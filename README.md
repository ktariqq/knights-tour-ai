# Knight’s Tour AI Solver
Interactive AI-based Knight’s Tour implementation using heuristic search and recursive backtracking with real-time GUI visualization.

![Python](https://img.shields.io/badge/Python-3.x-8A2BE2.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-4B0082.svg)
![AI](https://img.shields.io/badge/Algorithm-Heuristic%20Search-6A0DAD.svg)
![License](https://img.shields.io/badge/License-MIT-4B0082.svg)

<div align="center">

━━━━━━━━━━━━━━ ✦ ✧ ✦ ━━━━━━━━━━━━━━

</div>

## 🟣 Overview

This project implements an intelligent Knight’s Tour solver on an 8×8 chessboard using Python. The system combines recursive backtracking with heuristic lookahead strategies to guide the knight’s movement across the board.

A graphical user interface (Tkinter) allows users to select a starting position and choose between two AI modes: 1-step and 2-step lookahead. The knight’s movement is animated in real time, providing a visual representation of the algorithm’s decision-making process.

<br><br>

## 🟣 Key Features

- Interactive 8×8 chessboard GUI using Tkinter
- Click-based starting position selection
- Animated knight movement with move tracking
- Two AI strategies:
  - 1-step heuristic (greedy selection)
  - 2-step lookahead heuristic (deeper evaluation)
- Recursive backtracking search algorithm
- Real-time board updates and visualization
- Failure handling with backtracking limit
- Reset and restart functionality
<br><br>

## 🔧 System Components

| Component | Description |
|-----------|------------|
| Board Model | 8×8 grid representing chessboard state |
| Search Engine | Recursive backtracking + heuristic ordering |
| Heuristics | 1-step and 2-step lookahead evaluation |
| GUI Layer | Tkinter-based interactive visualization |
| Animation Engine | Step-by-step move rendering with delays |

<br><br>

## 🟣 Algorithm Summary

The system uses a depth-first recursive search enhanced with heuristics:

- Knight moves follow standard L-shaped chess rules:
```python
moves = [(2, 1), (1, 2), (-1, 2), (-2, 1),
         (-2, -1), (-1, -2), (1, -2), (2, -1)]
```

- Move selection strategies:
    1-step: chooses next move with minimum onward moves, 2-step: evaluates second-level mobility for better long-term planning
- Backtracking occurs when no valid continuation exists
- A maximum backtracking threshold prevents infinite recursion

<br><br>

## 🟣 GUI Design
- Built using Python Tkinter
- 8×8 grid of interactive buttons
- Each cell represents a chessboard square
- Knight icon overlays visited positions
- Move numbers displayed on visited cells
- Status label shows current progress in real time
- Buttons provided for:
Starting search (1-step / 2-step)
Reset
Quit
<br><br>

## 🟣 System Behavior
- User selects starting square
- AI executes recursive search based on selected heuristic
- Knight moves are animated step-by-step
- Board updates dynamically after each move
- Success condition: all 64 squares visited exactly once
- Failure condition: backtracking limit exceeded or no valid path
<br><br>

## 🟣 Limitations
- Fixed 8×8 board size
- Performance depends on starting position
- Heuristic does not guarantee solution in all cases
- Tkinter-based rendering limits scalability for larger boards
<br><br>

## 🟣 Future Improvements
- Support variable board sizes (N×N Knight’s Tour)
- Replace heuristic with Warnsdorff’s full rule implementation
- Introduce AI optimization techniques (e.g., genetic algorithms / RL)
- Improve GUI using PyQt or web-based visualization
- Add step-by-step playback controls (pause, rewind, speed control)
<br><br>


## 🟣 Technologies Used
- Python 3
- Tkinter (GUI)
- Pillow (Image handling)
- Recursive Backtracking Algorithm
- Heuristic Search (1-step / 2-step lookahead) 
