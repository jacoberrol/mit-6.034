# 6.034 Fall 2010 Lab 3: Games
# Name: <Your Name>
# Email: <Your Email>

from util import INFINITY

### 1. Multiple choice

# 1.1. Two computerized players are playing a game. Player MM does minimax
#      search to depth 6 to decide on a move. Player AB does alpha-beta
#      search to depth 6.
#      The game is played without a time limit. Which player will play better?
#
#      1. MM will play better than AB.
#      2. AB will play better than MM.
#      3. They will play with the same level of skill.
ANSWER1 = 3

# 1.2. Two computerized players are playing a game with a time limit. Player MM
# does minimax search with iterative deepening, and player AB does alpha-beta
# search with iterative deepening. Each one returns a result after it has used
# 1/3 of its remaining time. Which player will play better?
#
#   1. MM will play better than AB.
#   2. AB will play better than MM.
#   3. They will play with the same level of skill.
ANSWER2 = 2

### 2. Connect Four
from connectfour import *
from basicplayer import *
from util import *
import tree_searcher

## This section will contain occasional lines that you can uncomment to play
## the game interactively. Be sure to re-comment them when you're done with
## them.  Please don't turn in a problem set that sits there asking the
## grader-bot to play a game!
## 
## Uncomment this line to play a game as white:
#run_game(human_player, basic_player)

## Uncomment this line to play a game as black:
#run_game(basic_player, human_player)

## Or watch the computer play against itself:
#run_game(basic_player, basic_player)

## Change this evaluation function so that it tries to win as soon as possible,
## or lose as late as possible, when it decides that one side is certain to win.
## You don't have to change how it evaluates non-winning positions.

def focused_evaluate(board):
    
    score = 0
    score = prefer_win_fast(score,board)
    score = prefer_long_chains(score,board)
    score = prefer_center_pieces(score,board)    

    return score


## Create a "player" function that uses the focused_evaluate function
quick_to_win_player = lambda board: minimax(board, depth=4,
                                            eval_fn=focused_evaluate)

def alpha_beta_find_board_value(
                            board, 
                            depth, 
                            bounding_val=None,
                            eval_fn=focused_evaluate,
                            get_next_moves_fn=get_all_next_moves,
                            is_terminal_fn=is_terminal):
    """
    Alpha Beta helper function: Return the alphabeta value of a particular board,
    given a particular depth to estimate to
    """
    if is_terminal_fn(depth, board):
        return eval_fn(board)

    best_val = None
    
    for move, new_board in get_next_moves_fn(board):

        val = -1 * alpha_beta_find_board_value(
                                            new_board, depth-1, 
                                            invert_or_none(best_val),
                                            eval_fn,
                                            get_next_moves_fn,
                                            is_terminal_fn)
        
        if bounding_val is not None and val > bounding_val:
            #if a next board value exceeds the bounding value than we can stop (alpha beta optimization)
            return val
        if best_val == None or val > best_val:
            best_val = val
        
    return best_val

## You can try out your new evaluation function by uncommenting this line:
#run_game(basic_player, quick_to_win_player)

## Write an alpha-beta-search procedure that acts like the minimax-search
## procedure, but uses alpha-beta pruning to avoid searching bad ideas
## that can't improve the result. The tester will check your pruning by
## counting the number of static evaluations you make.
##
## You can use minimax() in basicplayer.py as an example.
def alpha_beta_search(board, 
                      depth,
                      eval_fn,
                      get_next_moves_fn=get_all_next_moves,
		              is_terminal_fn=is_terminal):
    
    best_val = None
    best_move = None
    
    for move, new_board in get_next_moves_fn(board):
        
        val = -1 * alpha_beta_find_board_value(
                                            new_board, 
                                            depth-1, 
                                            invert_or_none(best_val), 
                                            eval_fn,
                                            get_next_moves_fn,
                                            is_terminal_fn)
        
        if best_val == None or val > best_val:
            best_val = val
            best_move = move

    return best_move

def invert_or_none(val):
    if val is None:
        return None
    
    return val*-1

## Now you should be able to search twice as deep in the same amount of time.
## (Of course, this alpha-beta-player won't work until you've defined
## alpha-beta-search.)
alphabeta_player = lambda board: alpha_beta_search(board,
                                                   depth=8,
                                                   eval_fn=focused_evaluate)

## This player uses progressive deepening, so it can kick your ass while
## making efficient use of time:
ab_iterative_player = lambda board: \
    run_search_function(board,
                        search_fn=alpha_beta_search,
                        eval_fn=focused_evaluate, timeout=5)
#run_game(human_player, alphabeta_player)

## Finally, come up with a better evaluation function than focused-evaluate.
## By providing a different function, you should be able to beat
## simple-evaluate (or focused-evaluate) while searching to the
## same depth.

def better_evaluate(board):
    score = 0
    score = prefer_win_fast(score,board)
    score = prefer_long_chains_early(score,board)
    score = prefer_center_pieces(score,board)
    return score


def prefer_win_fast(score,board):
    win = board.is_win()
    tokens = board.num_tokens_on_board()
    if win == board.get_current_player_id(): 
        score = (score + 1000 - tokens)
    if win == board.get_other_player_id():
        score = (score - 1000 + tokens)
    elif board.is_tie():
        score = (score - 1000)
    return score

def prefer_long_chains(score,board):
    return (score + (board.longest_chain(board.get_current_player_id()) * 10))

def prefer_long_chains_early(score,board):
    tokens = board.num_tokens_on_board()
    my_longest_chain = board.longest_chain(board.get_current_player_id())
    opp_longest_chain = board.longest_chain(board.get_other_player_id())

    if my_longest_chain > opp_longest_chain:
        score = score + eval_chain(my_longest_chain,tokens)
    elif opp_longest_chain > my_longest_chain:
        score = score - eval_chain(opp_longest_chain,tokens)

    return score

def eval_chain(chain_length,tokens):
    return (chain_length * chain_length * (42-tokens))

def prefer_center_pieces(score,board):
    for row in range(6):
        for col in range(7):
            if board.get_cell(row, col) == board.get_current_player_id():
                score -= abs(3-col)
            elif board.get_cell(row, col) == board.get_other_player_id():
                score += abs(3-col)
    return score

# Comment this line after you've fully implemented better_evaluate
better_evaluate = memoize(better_evaluate)

# Uncomment this line to make your better_evaluate run faster.
# better_evaluate = memoize(better_evaluate)

# For debugging: Change this if-guard to True, to unit-test
# your better_evaluate function.
if False:
    board_tuples = (( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,2,2,1,1,2,0 ),
                    ( 0,2,1,2,1,2,0 ),
                    ( 2,1,2,1,1,1,0 ),
                    )
    test_board_1 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 1)
    test_board_2 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 2)
    # better evaluate from player 1
    print("%s => %s" %(test_board_1, better_evaluate(test_board_1)))
    # better evaluate from player 2
    print("%s => %s" %(test_board_2, better_evaluate(test_board_2)))

## A player that uses alpha-beta and better_evaluate:
your_player = lambda board: run_search_function(board,
                                                search_fn=alpha_beta_search,
                                                eval_fn=better_evaluate,
                                                timeout=5)

#your_player = lambda board: alpha_beta_search(board, depth=4,
#                                              eval_fn=better_evaluate)

## Uncomment to watch your player play a game:
#run_game(your_player, your_player)

## Uncomment this (or run it in the command window) to see how you do
## on the tournament that will be graded.
#run_game(your_player, basic_player)

## These three functions are used by the tester; please don't modify them!
def run_test_game(player1, player2, board):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return run_game(globals()[player1], globals()[player2], globals()[board])
    
def run_test_search(search, board, depth, eval_fn):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=globals()[eval_fn])

## This function runs your alpha-beta implementation using a tree as the search
## rather than a live connect four game.   This will be easier to debug.
def run_test_tree_search(search, board, depth):
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=tree_searcher.tree_eval,
                             get_next_moves_fn=tree_searcher.tree_get_next_move,
                             is_terminal_fn=tree_searcher.is_leaf)
    
## Do you want us to use your code in a tournament against other students? See
## the description in the problem set. The tournament is completely optional
## and has no effect on your grade.
COMPETE = False

## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = "12"
WHAT_I_FOUND_INTERESTING = "simplifying the algorithm and fixing the bug in the tree_searcher"
WHAT_I_FOUND_BORING = "drawing out the data structure"
NAME = "Jacob Johnson"
EMAIL = "jacob.errol@gmail.com"

