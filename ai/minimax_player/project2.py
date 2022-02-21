"""
FILE:       project2.py
AUTHOR:      Miles Wyner, Jack Kaffenbarger
ASSIGNMENT:  Project 2: Othello
DATE:        March 14, 2021

List of playble OthelloPlayer classes:
    1. RandomPlayer         (provided)
    2. HumanPlayer          (provided)
    3. ShortTermMaximizer   (from hw2.py)
    4. MinimaxPlayer        (minimax algorithm with fixed depth assigned in make_move)
    5. AlphaBeta            (same as minimax but with basic AB pruning (faster minimax))
    6. AggressiveAlpha      (prunes better at the cost of time given practicality of implementation (ironic))
    7. DynamicTimePlayer    (AlphaBeta player but changes depth of search given time left)
    7. TournamentPlayer     (basically DynamicTimePlayer player but never misses mate in 1)

Utility functions:
    1. maximize_self_pieces: generates evaluation that benefits moves resulting
       in more of ones own pieces on the board.
    2. minimize_flankability: generates evaluation that benefits moves resulting
       in fewer empty squares adjacent to the tile placed down
    3. grab_corners: strongly values moves that allow for a corner to be captured

Important Notes:
    1. All players with the exception of the TournamentPlayer class rely on
       implemeted utility functions as well as terminal evaluation within the
       OthelloPlayer class. Provides generality and concision.
    2. For all Minimax Variants, feel free to pick and choose from the 3
       utility functions in the OthelloPlayer class listed above for testing.
       Simply call one or a combination of the different utility functions in
       def utility(self, node):, which is a unique method in all minimax variants.
"""

from othello import *
import random, sys, heapq

class MoveNotAvailableError(Exception):
    """Raised when a move isn't available."""
    pass

class OthelloTimeOut(Exception):
    """Raised when a player times out."""
    pass

class MoveNode():
    """A node in Othello that stores a state, the utility of that state,
    the move applied to reach that state."""

    def __init__(self, state, utility, move):
        self.state = state
        self.utility = utility
        self.move = move

    def __lt__(self, other):
        return self.utility > other.utility

class OthelloPlayer():
    """Parent class for Othello players."""

    def __init__(self, color):
        assert color in ["black", "white"]
        self.color = color

    def check_for_win(self, node):
        "Checks for a 1 move win, returns the move if it exists."
        for move in node.available_moves():
            temp_state = copy.deepcopy(node)
            temp_state = temp_state.apply_move(move)
            if temp_state.count(opposite_color(node.current)) == 0:
                return move
        return

    def maximize_self_pieces(self, node):
        """Utility to maximize own pieces on board."""
        return node.count(node.current) - node.count(opposite_color(node.current))

    def minimize_flankability(self, node):
        """Values positions in which a tile cannot be easily flanked by checking
        for empty square. The commented addition was to evaluate better the tile
        positions where one cannot get flanked on the next move, but practically
        when running tests it performed worse. """
        count = 0
        enemy_count = 0
        for r in range(8):
            for c in range(8):
                if node.board[r][c] == node.current:
                    count += self.minimize_flankability_helper(node, r, c)
                if node.board[r][c] == opposite_color(node.current):
                    enemy_count += self.minimize_flankability_helper(node, r, c)
        return count - enemy_count

    def minimize_flankability_helper(self, node, r, c):
        """Helper for minimize_flankability."""
        val = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr==0 and dc==0:
                    continue # (0, 0) not a valid change to current position
                if (0 > r + dr or r + dr > 7 or
                    0 > c + dc or c + dc > 7 or
                    node.board[r + dr][c + dc] != "empty"):
                    val += 5
                # We thought this would improve utility but results showed otherwise
                # if node.flanking(r, c, dr, dc, node.current, opposite_color(node.current)):
                #     val -= 5
        return val

    def grab_corners(self, node):
        """Strongly assesses corners as valuable positions where possible
        positions arise for a player to grab a corner (+100 utility)."""
        corners = [(0, 0), (0, 7), (7, 0), (7, 7)]

        for corner in corners:
            for move in node.available_moves():
                move = move.pair
                if corner == move:
                    return 100
        return 0

    def minimize_opponent_moves(self, node):
        """ Is not that effective, despite midgame analysis research
            (not used in out tournament class). """
        min_opponent_moves = 64

        for move in node.available_moves():
            temp_state = copy.deepcopy(node)
            temp_state = temp_state.apply_move(move)
            temp_available = temp_state.available_moves()

            if len(temp_available) < min_opponent_moves:
                min_opponent_moves = len(temp_available)

        return min_opponent_moves * -1

    def terminal(self, node, depth):
        """Base case for all minimax variations."""
        return (node.available_moves() == [] or depth < 1)

    def make_move(self, state, remaining_time):
        """Given a game state, return a move to make. Each type of player
        should implement this method. remaining_time is how much time this player
        has to finish the game."""
        pass

class RandomPlayer(OthelloPlayer):
    """Plays a random move."""

    def make_move(self, state, remaining_time):
        """Given a game state, return a move to make."""
        return random.choice(state.available_moves())

class HumanPlayer(OthelloPlayer):
    """Allows a human to play the game"""

    def make_move(self, state, remaining_time):
        """Given a game state, return a move to make."""
        available = state.available_moves()
        print("----- {}'s turn -----".format(state.current))
        print("Remaining time: {:0.2f}".format(remaining_time))
        print("Available moves are: ", available)
        move_string = input("Enter your move as 'r c': ")

        # Takes care of errant inputs and bad moves
        try:
            moveR, moveC = move_string.split(" ")
            move = OthelloMove(int(moveR), int(moveC), state.current)
            if move in available:
                return move
            else:
                raise MoveNotAvailableError # Indicates move isn't available

        except (ValueError, MoveNotAvailableError):
            print("({}) is not a legal move for {}. Try again\n".format(move_string, state.current))
            return self.make_move(state, remaining_time)

class ShortTermMaximizer(OthelloPlayer):
    """Player that tries to maximize opponents at each move (depth 1)."""

    def make_move(self, state, remaining_time):
        """Given a game state, return a move to make."""
        available = state.available_moves()
        # print("----- {}'s turn -----".format(state.current))
        # print("Remaining time: {:0.2f}".format(remaining_time))
        # print("Available moves are: ", available)

        color = state.current
        max_move = available[0]
        max_count = state.count(color)
        for move in available:
            temp_state = copy.deepcopy(state)
            temp_state = temp_state.apply_move(move)

            if temp_state.count(color) > max_count:
                max_move = move
                max_count = temp_state.count(color)
        print("STMaximizer: ", max_move)
        return max_move

class MinimaxPlayer(OthelloPlayer):
    """Minimax player with fixed depth and easily adjustable utility calcs."""

    def utility(self, node):
        return self.minimize_flankability(node)

    def minimax(self, node, MAX_turn, depth):
        """ find a move to make for any given game state and recursively return
            the best move to the top of the tree generated """
        # base case for max depth reached or no available moves
        if self.terminal(node, depth):
            return (self.utility(node), None)

        if MAX_turn: # max turn
            val = -10000
            best_move = None

            for move in node.available_moves():
            # find the best move based on the best utility
                temp_state = copy.deepcopy(node)
                temp_state = temp_state.apply_move(move)
                move_val, _ = self.minimax(temp_state, not MAX_turn, depth - 1)

                if move_val > val:
                    val = move_val
                    best_move = move

            return val, best_move

        else: # same as max except min turn
            val = 10000
            best_move = None

            for move in node.available_moves():
                temp_state = copy.deepcopy(node)
                temp_state = temp_state.apply_move(move)
                move_val, _ = self.minimax(temp_state, not MAX_turn, depth - 1)

                if move_val < val:
                    val = move_val
                    best_move = move

            return val, best_move

    def make_move(self, state, remaining_time):
        """Given a game state, return a move to make."""
        available = state.available_moves()
        # print("----- {}'s turn -----".format(state.current))
        # print("Remaining time: {:0.2f}".format(remaining_time))
        # print("Available moves are: ", available)

        answer = self.minimax(state, True, 4)
        return answer[1]

class AlphaBeta(OthelloPlayer):
    """Minimax variant with fixed depth and implemented Alpha-Beta Pruning to
       save time by not exploring unoptimal branches (in no certain order =
       unoptimal pruning), also easily adjustable utility calcs."""

    def utility(self, node):
        """ Utility calculated at different stages of the game can be easily
            manipulated here; the stages of the game are calcuated using the
            number of pieces on the board."""
        pieces_on_board = node.count(self.color) + node.count(opposite_color(self.color))

        if pieces_on_board < 24: # choose early game group of utility funcs
            return (self.minimize_flankability(node)  +
                    self.maximize_self_pieces(node) +
                    self.grab_corners(node))

        elif pieces_on_board < 44: # choose mid game group of utility funcs
            return (self.minimize_flankability(node)  +
                    self.maximize_self_pieces(node) +
                    self.grab_corners(node))

        else: # choose end game group of utility funcs
            return (self.minimize_flankability(node)  +
                    self.maximize_self_pieces(node) +
                    self.grab_corners(node))

    def alpha_beta(self, node, best_max, best_min, MAX_turn, depth):
        """ find a move to make for any given game state and recursively return
            the best move to the top of the tree generated. If a state is reached
            where there is already a known better move for a player, don't explore
            the subtree. """
        # base case for max depth reached or no available moves
        if self.terminal(node, depth):
            return (self.utility(node), None)

        if MAX_turn: # max turn
            val = -10000

            for move in node.available_moves():
                temp_state = copy.deepcopy(node)
                temp_state = temp_state.apply_move(move)
                val = max(val, self.alpha_beta(temp_state, best_max, best_min, not MAX_turn, depth - 1)[0])

                if val > best_max[0]: # maintain best move
                    best_max = val, move

                if best_max[0] >= best_min[0]: # pruning
                    return val, None

            return best_max

        else: # same as max but min turn
            val = 10000

            for move in node.available_moves():
                temp_state = copy.deepcopy(node)
                temp_state = temp_state.apply_move(move)
                val = min(val, self.alpha_beta(temp_state, best_max, best_min, not MAX_turn, depth - 1)[0])

                if val < best_min[0]:
                    best_min = val, move
                if best_min[0] <= best_max[0]:
                    return val, None

            return best_min

    def make_move(self, state, remaining_time):
        """Given a game state, return a move to make."""
        available = state.available_moves()
        # print("----- {}'s turn -----".format(state.current))
        # print("Remaining time: {:0.2f}".format(remaining_time))
        # print("Available moves are: ", available)

        answer = self.alpha_beta(state, (-10000, None), (10000, None), True, 4)
        return answer[1]

class AggressiveAlpha(OthelloPlayer):
    """AphaBeta variant with fixed depth and implemented Alpha-Beta Pruning to
       save time by not exploring unoptimal branches. The moves are explored
       for min (least to greatest) and max (greatest to least) optimally to
       prune more efficiently and more often by exploring potential better
       branches first. Excuse the misleading name of the player, it is more of
       an optimal alpha but AggressiveAlpha has more of a ring to it."""

    def utility(self, node):
        """ Utility calculated at different stages of the game can be easily
            manipulated here; the stages of the game are calcuated using the
            number of pieces on the board."""
        pieces_on_board = node.count(self.color) + node.count(opposite_color(self.color))

        if pieces_on_board < 24: # choose early game utility func
            return (self.minimize_flankability(node)  +
                    self.maximize_self_pieces(node) +
                    self.grab_corners(node))

        elif pieces_on_board < 44: # choose midgame utility func
            return (self.minimize_flankability(node)  +
                    self.maximize_self_pieces(node) +
                    self.grab_corners(node))

        else: # choose endgame utility func
            return (self.minimize_flankability(node)  +
                    self.maximize_self_pieces(node) +
                    self.grab_corners(node))

    def aggressive_alpha_beta(self, node, best_max, best_min, MAX_turn, depth):
        """ find a move to make for any given game state and recursively return
            the best move to the top of the tree generated. For pruning, using
            a priority queue for any state create a queue of moves in either
            descending order for max turn or ascending order for min turn.
            This provides the more promising subtrees to be explored first,
            allowing for pruning to occur more often."""
        # base case for max depth reached or no available moves
        if self.terminal(node, depth):
            return (self.utility(node), None)

        priority_queue = []
        for move in node.available_moves():
            temp_state = copy.deepcopy(node)
            temp_state = temp_state.apply_move(move)
            heapq.heappush(priority_queue, MoveNode(temp_state, self.utility(temp_state), move))

        if MAX_turn: # max turn
            val = -10000

            largest_first = heapq.nlargest(len(priority_queue), priority_queue)
            for move_node in largest_first:
                heapq.heappop(priority_queue)
                temp_state = move_node.state
                move = move_node.move
                val = max(val, self.aggressive_alpha_beta(temp_state, best_max, best_min, not MAX_turn, depth - 1)[0])

                if val > best_max[0]: # maintain best move
                    best_max = val, move
                if best_max[0] >= best_min[0]: # pruning
                    return val, None

            return best_max

        else: # same as max but min turn
            val = 10000
            smallest_first = heapq.nsmallest(len(priority_queue), priority_queue)
            for move_node in smallest_first:
                heapq.heappop(priority_queue)
                temp_state = move_node.state
                move = move_node.move
                val = min(val, self.aggressive_alpha_beta(temp_state, best_max, best_min, not MAX_turn, depth - 1)[0])

                if val < best_min[0]:
                    best_min = val, move
                if best_min[0] <= best_max[0]:
                    return val, None

            return best_min

    def make_move(self, state, remaining_time):
        """Given a game state, return a move to make."""
        available = state.available_moves()
        # print("----- {}'s turn -----".format(state.current))
        # print("Remaining time: {:0.2f}".format(remaining_time))
        # print("Available moves are: ", available)

        answer = self.aggressive_alpha_beta(state, (-10000, None), (10000, None), True, 7)
        print("aggressive_alpha_beta move: ", answer[1])
        return answer[1]

class DynamicTimePlayer(OthelloPlayer):
    """AlphaBeta but with better time management; to do so, we use
           1. time_left (generally decrease depth as time gets low)
           2. the number of available_moves in the given state (if there are a
              lot of moves in a state, odds are the breadth of the tree will be
              large and take significantly more time so we should decrease depth)
           3. the time left at different stages of the game (in the midgame,
              if we still have a lot of time and there aren't too many moves in
              the state, explore further for better moves)
       These calculations allow us to use time as best as wel can while still
       ensuring that the player doesn't lose on time."""

    def utility(self, node):
        """ Utility calculated at different stages of the game can be easily
            manipulated here; the stages of the game are calcuated using the
            number of pieces on the board."""

        pieces_on_board = node.count(self.color) + node.count(opposite_color(self.color))

        if pieces_on_board < 24: # choose early game utility func
            return (self.minimize_flankability(node)  +
                    self.grab_corners(node))

        elif pieces_on_board < 44: # choose midgame utility func
            return (self.minimize_flankability(node)  +
                    self.maximize_self_pieces(node) +
                    self.grab_corners(node))

        else: # choose endgame utility func
            return (self.minimize_flankability(node)  +
                    self.maximize_self_pieces(node) +
                    self.grab_corners(node))

    def timed_alpha_beta(self, node, best_max, best_min, MAX_turn, depth):
        """Same as AlphaBeta. Ideas here were to include time_left as a
           paramater, to manually calculate the time the agent has used whilst
           exploring. This idea fell through, however, as there was no simple
           implementation and setting a depth based on the time left at the
           beginning of a move, while not guarunteeing never losing on time,
           usually succeeds and is much simpler."""

        # base case for max depth reached or no available moves
        if self.terminal(node, depth):
            return (self.utility(node), None)

        if MAX_turn: # max turn
            val = -10000

            for move in node.available_moves():
                temp_state = copy.deepcopy(node)
                temp_state = temp_state.apply_move(move)
                val = max(val, self.timed_alpha_beta(temp_state, best_max, best_min, not MAX_turn, depth - 1)[0])

                if val > best_max[0]: # maintain best move
                    best_max = val, move
                if best_max[0] >= best_min[0]: # pruning
                    return val, None

            return best_max

        else: # same as max but min turn
            val = 10000

            for move in node.available_moves():
                temp_state = copy.deepcopy(node)
                temp_state = temp_state.apply_move(move)
                val = min(val, self.timed_alpha_beta(temp_state, best_max, best_min, not MAX_turn, depth - 1)[0])

                if val < best_min[0]:
                    best_min = val, move
                if best_min[0] <= best_max[0]:
                    return val, None

            return best_min

    def make_move(self, state, remaining_time):
        """Given a game state, return a move to make."""
        available = state.available_moves()
        # print("----- {}'s turn -----".format(state.current))
        # print("Remaining time: {:0.2f}".format(remaining_time))
        # print("Available moves are: ", available)

        if remaining_time < 10: # hurry!
            depth = 3
        elif remaining_time < 20: # hurry!...kind of
            depth = 4
        elif remaining_time < 40: # hurry!...kind of but no so much
            depth = 5
        elif remaining_time < 110: # make strong moves at the cost of extra time
            depth = 6
        else: # make relatively strong moves at the start of the game
            depth = 5
            if state.count(state.current) + state.count(opposite_color(state.current)) > 24:
                depth = 6 # if midgame reached early, use more time

        return self.timed_alpha_beta(state, (-10000, None), (10000, None), True, depth)[1]

class TournamentPlayer(OthelloPlayer):
    """Our DynamicTimePlayer, but always makes the mate in 1's.
       See above for descriptions of all functions (they are simply repeated
       here so that our TournamentPlayer can play in the tournamnet without
       relying on the methods inherited by our implementations in OthelloPlayer
       that we made use of for generalized testing purposes)."""

    def check_for_win(self, node):
        for move in node.available_moves():
            temp_state = copy.deepcopy(node)
            temp_state = temp_state.apply_move(move)
            if temp_state.count(opposite_color(node.current)) == 0:
                return True, move
        return False, None

    def maximize_self_pieces(self, node):
        return node.count(node.current) - node.count(opposite_color(node.current))

    def minimize_flankability(self, node):
        """Values positions in which a tile cannot be easily flanked by checking
           for empty square."""
        count = 0
        enemy_count = 0
        for r in range(8):
            for c in range(8):
                if node.board[r][c] == node.current:
                    count += self.minimize_flankability_helper(node, r, c)
                if node.board[r][c] == opposite_color(node.current):
                    enemy_count += self.minimize_flankability_helper(node, r, c)
        return (count - enemy_count) / 2

    def minimize_flankability_helper(self, node, r, c):
        val = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr==0 and dc==0:
                    continue # (0, 0) not a valid change to current position
                if (0 > r + dr or r + dr > 7 or
                    0 > c + dc or c + dc > 7 or
                    node.board[r + dr][c + dc] != "empty"):
                    val += 5
                # We thought this would work but results show otherwise
                # if node.flanking(r, c, dr, dc, node.current, opposite_color(node.current)):
                #     val -= 5
        return val

    def grab_corners(self, node):
        """Strongly assesses corners as valuable positions where possible
        positions arise for a player to grab a corner."""
        corners = [(0, 0), (0, 7), (7, 0), (7, 7)]

        for corner in corners:
            for move in node.available_moves():
                move = move.pair
                if corner == move:
                    return 10
        return 0

    def minimize_opponent_moves(self, node):
        """ is not that effective, despite midgame analysis research"""
        min_opponent_moves = 64
        for move in node.available_moves():
            temp_state = copy.deepcopy(node)
            temp_state = temp_state.apply_move(move)
            temp_available = temp_state.available_moves()
            if len(temp_available) < min_opponent_moves:
                min_opponent_moves = len(temp_available)
        return min_opponent_moves * -1

    def terminal(self, node, depth):
        return (node.available_moves() == [] or depth < 1)

    def utility(self, node):
        pieces_on_board = node.count(self.color) + node.count(opposite_color(self.color))

        if pieces_on_board < 24: # choose early game utility func
            return self.minimize_flankability(node)

        elif pieces_on_board < 44: # choose midgame utility func
            return (self.minimize_flankability(node)  +
                    self.grab_corners(node))

        else: # choose endgame utility func
            return (self.minimize_flankability(node)  +
                    self.maximize_self_pieces(node) +
                    self.grab_corners(node))

    def timed_alpha_beta(self, node, best_max, best_min, MAX_turn, depth):

        # base case for max depth reached or no available moves
        if self.terminal(node, depth):
            return (self.utility(node), None)

        if MAX_turn: # max turn
            val = -10000

            for move in node.available_moves():
                temp_state = copy.deepcopy(node)
                temp_state = temp_state.apply_move(move)
                val = max(val, self.timed_alpha_beta(temp_state, best_max, best_min, not MAX_turn, depth - 1)[0])

                if val > best_max[0]: # maintain best move
                    best_max = val, move
                if best_max[0] >= best_min[0]: # pruning
                    return val, None

            return best_max

        else: # same as max but min turn
            val = 10000

            for move in node.available_moves():
                temp_state = copy.deepcopy(node)
                temp_state = temp_state.apply_move(move)
                val = min(val, self.timed_alpha_beta(temp_state, best_max, best_min, not MAX_turn, depth - 1)[0])

                if val < best_min[0]:
                    best_min = val, move
                if best_min[0] <= best_max[0]:
                    return val, None

            return best_min

    def make_move(self, state, remaining_time):
        """Given a game state, return a move to make."""
        available = state.available_moves()
        # print("----- {}'s turn -----".format(state.current))
        # print("Remaining time: {:0.2f}".format(remaining_time))
        # print("Available moves are: ", available)
        if remaining_time < 10: # hurry!
            depth = 2
        elif remaining_time < 25: # hurry!...kind of
            depth = 3
        elif len(available) > 8:
            depth = 4
        elif remaining_time < 50: # hurry!...kind of but no so much
            depth = 4
        elif remaining_time < 120: # make strong moves at the cost of extra time
            depth = 5
        else: # make relatively strong moves at the start of the game
            depth = 4
            if state.count(state.current) + state.count(opposite_color(state.current)) > 24:
                depth = 5 # if midgame reached early, use more time

        # don't miss mate in 1!
        is_win, winning_move = self.check_for_win(state)
        if is_win:
            return winning_move

        return self.timed_alpha_beta(state, (-10000, None), (10000, None), True, depth)[1]


################################################################################

def main():
    """Plays the game."""

    black_player = TournamentPlayer("black")
    white_player = DynamicTimePlayer("white")

    game = OthelloGame(black_player, white_player, verbose=True)

    winner = game.play_game_timed()

    ###### Use this method if you want to use a HumanPlayer
    # winner = game.play_game()


    if not game.verbose:
        print("Winner is", winner)


if __name__ == "__main__":
    main()
