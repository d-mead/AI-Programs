import random
import sys
import time
from heapq import heappush, heappop
from collections import deque
import math

BLANK = "??????????" \
        "?........?" \
        "?........?" \
        "?........?" \
        "?...@o...?" \
        "?...o@...?" \
        "?........?" \
        "?........?" \
        "?........?" \
        "??????????"

DIRECTIONS = [1, -1, 10, -10, 11, -11, 9, -9]
SIZE = 100

SEEN = dict()

WEIGHTS = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 140, -30, 50,  5,  5, 50, -30, 140, 0,
     0, -10, -40, -5, -5, -5, -5, -40, -10, 0,
     0,  50,  -5, 15,  3,  3, 15,  -5,  50, 0,
     0,   5,  -5,  3,  3,  3,  6,  -5,   5, 0,
     0,   5,  -5,  3,  3,  3,  3,  -5,   5, 0,
     0,  50,  -5, 15,  3,  6, 15,  -5,  50, 0,
     0, -10, -40, -5, -5, -5, -5, -40, -10, 0,
     0, 140, -30, 50,  5,  5, 50, -30, 140, 0,
     0,   0,   0,  0,  0,  0,  0,   0,   0, 0]

BORDER = {11, 12, 13, 14, 15, 16, 17, 18, 21, 31, 41, 51, 61, 71, 81, 82, 83, 84, 85, 86, 87, 88, 78, 68, 58, 48, 38, 28}

# ADVANCED: Opening book

#       Here I made 7 potential opening situations that are beneficial for
#   black, and I rated them highly to begin with in the board-score dictionary.

#       When they are 'scored' later on, it will just take the 100000 instead
#   of actually scoring them, so they will always be chosen when compared to other
#   moves at their depth.

op1 =   "??????????" \
        "?........?" \
        "?........?" \
        "?..@o....?" \
        "?..@oo...?" \
        "?..@@@...?" \
        "?........?" \
        "?........?" \
        "?........?" \
        "??????????"

op2 =   "??????????" \
        "?........?" \
        "?........?" \
        "?..o@....?" \
        "?..@@@...?" \
        "?...@o...?" \
        "?........?" \
        "?........?" \
        "?........?" \
        "??????????"

op3 =   "??????????" \
        "?........?" \
        "?........?" \
        "?..o.....?" \
        "?..@o@...?" \
        "?...@o...?" \
        "?........?" \
        "?........?" \
        "?........?" \
        "??????????"

op4 =   "??????????" \
        "?........?" \
        "?........?" \
        "?..@@@...?" \
        "?..o@o...?" \
        "?...@....?" \
        "?........?" \
        "?........?" \
        "?........?" \
        "??????????"

op5 =   "??????????" \
        "?........?" \
        "?........?" \
        "?....o...?" \
        "?..@oo...?" \
        "?..o@@@..?" \
        "?....o@..?" \
        "?........?" \
        "?........?" \
        "??????????"

op6 =   "??????????" \
        "?........?" \
        "?........?" \
        "?....o...?" \
        "?..@@@@..?" \
        "?..o@@@..?" \
        "?....ooo.?" \
        "?........?" \
        "?........?" \
        "??????????"

op7 =   "??????????" \
        "?........?" \
        "?........?" \
        "?....o...?" \
        "?..@@o...?" \
        "?...@@@..?" \
        "?........?" \
        "?........?" \
        "?........?" \
        "??????????"

SEEN[op1] = 100000
SEEN[op2] = 100000
SEEN[op3] = 100000
SEEN[op4] = 100000
SEEN[op5] = 100000
SEEN[op6] = 100000
SEEN[op7] = 100000


class Strategy:
    def best_strategy(self, board, player, best_move, still_running):

        best_move.value = get_valid_moves(board, player)[0]
        d = 1
        while still_running:
            best_move.value = maxmin_ab_2(board, player, d, -999999999999, 999999999999)[0]
            d += 1


def main():
    global maxing, cou
    cou = 0
    maxing = '@'
    smart_game(BLANK)


def maxmin_ab_2(board, player, depth, a, b):
    global cou
    opponent = {'o':'@', '@': 'o'}[player]
    best = {'o': min, '@': max}
    if depth == 0:  # if we've reached the desired depth
        return None, board_score(board)  # return the score

    possible_moves = []  # empty list of possible moves
    if player == '@':
        value = -999999999999
        for spot in get_valid_moves(board, player):
            mov = move(board, player, spot)                    
            next_players_moves = get_valid_moves(mov, opponent)
            if len(next_players_moves) != 0:
                next_player = opponent
            elif len(get_valid_moves(board, player)) != 0:
                next_player = player
            else:
                next_player = '?'
            if next_player == '?':
                a = board.count('@')
                o = board.count('o')
                if o == 0:
                    possible_moves.append((spot, 999999999))
                elif a > 3*o:
                    possible_moves.append((spot, 500000000))
                elif a > o:
                    possible_moves.append((spot, 100000000 + board_score(mov)))
                else:
                    possible_moves.append((spot, -100000000 + board_score(mov)))
            else:
                this_val = maxmin_ab_2(mov, next_player, depth-1, a, b)[1]
                value = max(value, this_val)
                a = max(a, value)
                possible_moves.append((spot, this_val))
                if a >= b:
                    break

    else:
        value = 999999999999
        for spot in get_valid_moves(board, player):
            mov = move(board, player, spot)
            next_players_moves = get_valid_moves(mov, opponent)
            if len(next_players_moves) != 0:
                next_player = opponent
            elif len(get_valid_moves(board, player)) != 0:
                next_player = player
            else:
                next_player = '?'
            if next_player == '?':
                a = board.count('@')
                o = board.count('o')
                if o == 0:
                    possible_moves.append((spot, 999999999))
                elif a > 3 * o:
                    possible_moves.append((spot, 500000000))
                elif a > o:
                    possible_moves.append((spot, 100000000 + board_score(mov)))
                else:
                    possible_moves.append((spot, -100000000 + board_score(mov)))
            else:
                this_val = maxmin_ab_2(mov, next_player, depth - 1, a, b)[1]
                value = min(value, this_val)
                b = min(b, value)
                possible_moves.append((spot, this_val))
                if a >= b:
                    break

    if len(possible_moves) > 0:
        return best[player](possible_moves, key=lambda x: x[1])

    else:
        a = board.count('@')
        o = board.count('o')
        if o == 0:
            return None, 999999999
        elif a > 3 * o:
            return None, 500000000
        elif a > o:
            return None, 100000000 + board_score(board)
        else:
            return None, -100000000 + board_score(board)

# ADVANCED: edge building
# The values 'shots', 'lines', and 'special' in the board_score method all work to
#   prioritize moves that result in more secure pieces along the edge of the board.

# shots: if there is a corner piece secured, it adds to it's value for every        @ @ @ . .   @ o @ .
#   disk in the row along the two edges connected by the corner if it is     -->    @           o
#                                                                                   @  good     @ bad
# lines: adds to its value if there is a row or column of just one token, as        .           .
#   this makes the tokens hard to flip

# special: the weight key (WEIGHTS) negatively values pieces adjacent to the
#   corners however if the corner is already taken, this position is pretty
#   valuable, so this counteracts the negative 'territory' score if a corner
#   is taken


def board_score(board):
    if board in SEEN.keys():
        # print('a')
        return SEEN[board]

    moves_left = board.count('.')
    m_weight = 80 if moves_left > 10 else 20
    c_weight = 30 if moves_left < 10 else -100
    t_weight = 20 if moves_left > 10 else 25
    s_weight = 20 if moves_left > 10 else 10
    f_weight = 90 if moves_left > 10 else 5
    l_weight = 20
    sp_weight = 800

    mobility =  (len(get_valid_moves(board, '@')) - len(get_valid_moves(board, 'o')))   * m_weight
    territory = (score_territory(board, '@') - score_territory(board, 'o'))             * t_weight
    count =     (board.count('@') - board.count('o'))                                   * c_weight
    shots =     (score_shots(board, '@') - score_shots(board, 'o'))                     * s_weight
    frontier =  (score_frontier(board, 'o') - score_frontier(board, '@'))               * f_weight
    special  =  (score_special_corners(board, '@') - score_special_corners(board, 'o')) * sp_weight
    lines =     (score_lines(board, 'o') - score_lines(board, '@'))                     * l_weight

    SEEN[board] = mobility + territory + count + shots + frontier + lines + special

    if moves_left < 10:
        display(board)
        print("m: %s\nt: %s\nc: %s\ns: %s\nf: %s\nl: %s\ns: %s\n TOTAL: %s" % (mobility, territory, count, shots, frontier, lines, special, SEEN[board]))

    return mobility + territory + count + shots + frontier + lines + special


def score_shots(board, player):
    score = 0
    if board[11] == player:
        for check in range(11, 71, 10):
            if board[check] == player:
                score += 1
            else:
                break
        for check in range(11, 17):
            if board[check] == player:
                score += 1
            else:
                break

    if board[18] == player:
        for check in range(18, 78, 10):
            if board[check] == player:
                score += 1
            else:
                break
        for check in range(18, 12, -1):
            if board[check] == player:
                score += 1
            else:
                break

    if board[88] == player:
        for check in range(88, 28, -10):
            if board[check] == player:
                score += 1
            else:
                break
        for check in range(88, 82, -1):
            if board[check] == player:
                score += 1
            else:
                break

    if board[81] == player:
        for check in range(81, 21, -10):
            if board[check] == player:
                score += 1
            else:
                break
        for check in range(82, 87):
            if board[check] == player:
                score += 1
            else:
                break

    return score


def score_lines(board, player):
    score = 0
    spots = set([x for x in range(0, 100) if board[x] == player])
    spots = spots.difference(BORDER)
    directions = [1, 10, -1, -10]
    for spot in spots:
        for direction in directions:
            count = 0
            look = spot
            while board[look] == player:
                count += 1
                look += direction
            if count > 3:
                score += 1
    return score


def score_special_corners(board, player):
    score = 0
    if board[11] != '.':
        if board[12] == player:
            score += 1
        if board[21] == player:
            score += 1
    if board[18] != '.':
        if board[17] == player:
            score += 1
        if board[21] == player:
            score += 1
    if board[81] != '.':
        if board[71] == player:
            score += 1
        if board[82] == player:
            score += 1
    if board[88] != '.':
        if board[78] == player:
            score += 1
        if board[87] == player:
            score += 1

    return score


def score_territory(board, player):
    global aa, bb, cc, dd, ee
    score = 0
    for spot in [x for x in range(0, 100) if board[x] == player]:
        score += WEIGHTS[spot]

    return score


def score_keep(board, player):
    spots = set([x for x in range(0, 100) if board[x] == player])
    opponent_moves = get_valid_moves(board, opposite(player))
    score = 0
    for move_spot in opponent_moves:
        mov = move(board, opposite(player), move_spot)
        move_spots = set([x for x in range(0, 100) if board[x] == player])
        for spot in spots:
            if spot in move_spots:
                score += 1

    return score


def score_frontier(board, player):
    score = 0
    spots = set([x for x in range(0, 100) if board[x] == player])
    directions = [1, 10, -1, -10]
    for spot in spots:
        found = False
        for direction in directions:
            if board[spot+direction] == '.':
                score += 1
                found = True
            elif board[spot+direction] == '?':
                found = True
        if not found:
            score -= 1
    return score


def smart_move(state, token):
    global skip, cont, moves
    valid_moves = get_valid_moves(state, token)

    if valid_moves:
        print(token + "'s turn")
        print("valid moves: " + ", ".join([str(x) for x in valid_moves]))
        skip = False
        print()
        spot, score = maxmin_ab_2(state, token, 5, -999999999999, 999999999999)
        new_state = move(state, token, spot)
        print(score)
        print('I choose %s ' % spot)
        return new_state
    if not skip:
        if state.count('.') != 64:
            moves.append(-1)
            print(token + "'s turn")
            print("no valid moves available: skip")
            print()
            skip = True
        else:
            cont = False
        return state
    else:
        cont = False
        return state


def smart_game(state):
    global skip, cont, moves
    skip = False
    cont = True
    moves = []

    while state:
        display(state)
        state = smart_move(state, '@')
        if not cont:
            break

        display(state)
        state = random_move(state, 'o')
        if not cont:
            break

    print("Game Over")
    print("Final Score:")
    print("o: %s  @: %s" % (state.count('o'), state.count('@')))
    total_moves = 64 - state.count('.')
    print("o: %s%%  @: %s%%" % (
    round(state.count('o') * 100 / total_moves, 4), round(state.count('@') * 100 / total_moves, 4)))
    print(("o" if state.count('o') > state.count('@') else '@') + " wins!")

    # print(moves)
    print()

    return ("o" if state.count('o') > state.count('@') else '@'), round(state.count('@') * 100 / total_moves, 4)


def random_move(state, token):
    global skip, cont, moves
    # cont = True
    valid_moves = get_valid_moves(state, token)

    if valid_moves:
        print(token + "'s turn")
        print("valid moves: " + ", ".join([str(x) for x in valid_moves]))
        skip = False
        spot = valid_moves[random.randint(0, len(valid_moves) - 1)]
        moves.append(spot)
        print('I choose %s ' % spot)
        print()
        new_state = move(state, token, spot)
        return new_state
    if not skip:
        if state.count('.') != 64:
            moves.append(-1)
            print(token + "'s turn")
            print("no valid moves available: skip")
            print()
            skip = True
        else:
            cont = False
        return state
    else:
        cont = False
        return state


def move(state, token, spot):
    new_state = make_move(state, token, spot)
    new_state = flip_board(new_state, spot)
    return new_state


def make_move(state, token, spot):
    return state[:spot] + token + state[spot+1:]


def flip_board(state, spot):
    token = state[spot]
    opposite_token = opposite(token)
    adjacencies = [spot]*len(DIRECTIONS)

    to_flip = set()

    for adj in adjacencies:
        index = adj
        for direction in DIRECTIONS:
            hit_opposite = False
            examined = set()
            index = index + direction
            if index >= SIZE or index < 0:
                continue
            value = state[index]
            if value == opposite_token:
                examined.add(index)
                hit_opposite = True
            while value == opposite_token:
                index = index + direction
                value = state[index]
                examined.add(index)
                hit_opposite = True

            if value == token and hit_opposite:
                for index in examined:
                    to_flip.add(index)
            index = adj

    for flip in to_flip:
        state = make_move(state, token, flip)

    return state


def get_valid_moves(state, token):
    opposite_token = opposite(token)

    empty_spots = [x for x in range(0, len(state)) if state[x] == '.']
    valid_move_indecies = []
    for move_index in empty_spots:
        changing_index = move_index
        for direction in DIRECTIONS:
            hit_opposite_token = False
            changing_index = changing_index+direction
            if changing_index >= SIZE or changing_index < 0:
                continue
            value = state[changing_index]
            if value == opposite_token:
                hit_opposite_token = True
            while value == opposite_token:
                changing_index = changing_index + direction
                value = state[changing_index]
                if value == opposite_token:
                    hit_opposite_token = True
            if value == token:
                if hit_opposite_token:
                    valid_move_indecies.append(move_index)
                    break
            changing_index = move_index

    if len(valid_move_indecies) == 0:
        return []

    return valid_move_indecies


def opposite(token):
    if token == '@':
        return 'o'
    return '@'


def display(state):
    for x in range(1, 9):
        to_print = " ".join(state[x * 10 + 1:(x + 1) * 10 - 1]) + " \t" + " ".join(
            [(str(x * 10 + y) + (" " if len(str(x * 10 + y)) == 1 else "")) for y in
             range(1, 9)])
        print(to_print)

    # print()
    print(" o: %s  @: %s" % (state.count('o'), state.count('@')))
    # print()
    pct = int(100*(state.count(maxing)/(state.count(maxing) + state.count(opposite(maxing)))))
    print("|                       |                        |                        |                        |")
    print("".join(["#"]*pct))


if __name__ == "__main__":
    main()