import time
import sys
from collections import deque
import tracemalloc

class PuzzleState:
    
    def __init__(self, board, parent=None, move=None, depth=0):
        self.board = board
        self.parent = parent
        self.move = move
        self.depth = depth
        self.null_pos = board.index(0)
    
    #make board to tuple to use in dictionary key
    def get_board(self):
        return tuple(self.board)
    
    #check if board is in state 1-15 last state 0
    def the_goal(self):
        return self.board == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
    
    #next states by moving empty tiles and return list of new board and the direction move as tuples
    def next_to(self):
        next = []
        row, col = self.null_pos // 4, self.null_pos % 4
        moves = [
            ('R', 0, 1),
            ('D', 1, 0),
            ('L', 0, -1),
            ('U', -1, 0)
        ]
        for direction, dr, dc in moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 4 and 0 <= new_col < 4:
                new_pos = new_row * 4 + new_col
                new_board = self.board.copy()
                new_board[self.null_pos], new_board[new_pos] = \
                    new_board[new_pos], new_board[self.null_pos]
                next.append((new_board, direction))
        return next
    
    #track back from current state to start state to find the path and return the moves
    def get_path(self):
        moves = []
        current = self
        while current.parent is not None:
            moves.append(current.move)
            current = current.parent
        return ''.join(reversed(moves))

#solve the puzzle by bfs and returning the dict with moves, the nodes that expanded, the time taken to solve and the memory used
def breadth_first_search(initial_board):
    start_time = time.time()
    tracemalloc.start()
    
    node = PuzzleState(initial_board)
    
    if node.the_goal():
        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return {
            'moves': '',
            'nodes_expanded': 0,
            'time_taken': end_time - start_time,
            'memory_used': peak / 1024
        }
    
    #FIFO queue
    front = deque([node])
    reached = {node.get_board()}
    nodes_expanded = 0
    
    #
    while front:
        node = front.popleft()
        nodes_expanded += 1
        
        for new_board, move in node.next_to():
            s = tuple(new_board)
            
            if s not in reached:
                child = PuzzleState(
                    new_board,
                    parent=node,
                    move=move,
                    depth=node.depth + 1
                )
                
                if child.the_goal():
                    end_time = time.time()
                    current, peak = tracemalloc.get_traced_memory()
                    tracemalloc.stop()
                    return {
                        'moves': child.get_path(),
                        'nodes_expanded': nodes_expanded,
                        'time_taken': end_time - start_time,
                        'memory_used': peak / 1024
                    }
                
                reached.add(s)
                front.append(child)
    
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {
        'moves': 'No solution found',
        'nodes_expanded': nodes_expanded,
        'time_taken': end_time - start_time,
        'memory_used': peak / 1024
    }


def main():
    print("15 Puzzle BFS Solver")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        try:
            initial_board = [int(x) for x in sys.argv[1:]]
        except ValueError:
            print("Error: Invalid input. Please provide 16 integers.")
            return
    else:
        print("Enter the initial board configuration (16 numbers separated by spaces):")
        print("Use 0 for the empty space.")
        print("Example: 1 0 2 4 5 7 3 8 9 6 11 12 13 10 14 15")
        user_input = input("> ")
        try:
            initial_board = [int(x) for x in user_input.split()]
        except ValueError:
            print("Error: Invalid input. Please provide 16 integers.")
            return
    
    if len(initial_board) != 16:
        print(f"Error: Expected 16 numbers, got {len(initial_board)}")
        return
    
    if sorted(initial_board) != list(range(16)):
        print("Error: Board must contain numbers 0-15 exactly once")
        return
    
    print(f"\nInitial board: {initial_board}")
    print("\nSolving...\n")
    
    result = breadth_first_search(initial_board)
    
    print("=" * 50)
    print("RESULTS")
    print("=" * 50)
    print(f"Moves: {result['moves']}")
    print(f"Number of Nodes expanded: {result['nodes_expanded']}")
    print(f"Time Taken: {result['time_taken']:.3f} seconds")
    print(f"Memory Used: {result['memory_used']:.0f} KB")
    print("=" * 50)


if __name__ == "__main__":
    main()