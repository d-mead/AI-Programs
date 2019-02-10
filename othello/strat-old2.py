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
OTHER = "???????????........??........??.@...@..??.oooo...??...@@...??...@....??...@....??........???????????"
ROWS  = "???????????@@@@@@@@??@.......??@.......??@..@o...??@..o@...??@.......??@.......??@.......???????????"
FRONT = "???????????........??oooooooo??@@@@@@@@??........??........??........??........??........???????????"
SHOTS = "???????????oooo....??o.......??o.......??........??........??........??........??......oo???????????"
PAR_1 = "???????????........??........??........??...@@@..??...o@...??........??........??........???????????"
PAR_2 = "???????????........??........??........??...@@@..??...o@o..??....@...??........??........???????????"


DIRECTIONS = [1, -1, 10, -10, 11, -11, 9, -9]
SIZE = 100

HUNDRED = False

SEEN = dict()
VALID_MOVES = dict()

SEEN[PAR_1] = 100000
SEEN[PAR_1] = 100000

global WEIGHTS

WEIGHTS = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 170, -30, 50,  5,  5, 50, -30, 170, 0,
     0, -30, -50,  5, -5, -5,  5, -50, -30, 0,
     0,  50,   5, 15,  3,  3, 15,   5,  50, 0,
     0,   5,  -5,  3,  3,  3,  6,  -5,   5, 0,
     0,   5,  -5,  3,  3,  3,  3,  -5,   5, 0,
     0,  50,   5, 15,  3,  6, 15,   5,  50, 0,
     0, -30, -50,  5, -5, -5,  5, -50, -30, 0,
     0, 170, -30, 50,  5,  5, 50, -30, 170, 0,
     0,   0,   0,  0,  0,  0,  0,   0,   0, 0]

BORDER = {11, 12, 13, 14, 15, 16, 17, 18, 21, 31, 41, 51, 61, 71, 81, 82, 83, 84, 85, 86, 87, 88, 78, 68, 58, 48, 38, 28}


class Strategy:
    def best_strategy(self, board, player, best_move, still_running):
        best_move.value = get_valid_moves(board, player)[0]
        d = 1
        done = False
        while still_running and not done:
            best_move.value = maxmin_ab_2(board, player, d, -999999999999, 999999999999)[0]
            d += 1
            if abs(best_move.value) > 99999999:
                done = True


def main():
    # global maxing
    # maxing = '@'
    display(SHOTS)
    print(score_shots(SHOTS, 'o'))
    # smart_game(BLANK)


def play_many_games(state, count):
    start = time.perf_counter()
    wins = 0
    tot_pct = 0
    for x in range(0, count):
        win, pct = smart_game(state)
        tot_pct += pct
        if win == maxing:
            wins += 1
    end = time.perf_counter()
    print("total: %s " % (wins*100/count))
    print("avg %%: %s " % (round(tot_pct/count, 5)))
    print("time: %s " % round(end-start, 5))


def maxmin(board, player, depth):
    opponent = {'o':'@', '@': 'o'}[player]
    best = {'o': min, '@': max}
    if depth == 0:  # if we've reached the desired depth
        return (None, board_score(board))  # return the score

    possible_moves = []  # empty list of possible moves
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
            possible_moves.append((spot, maxmin(mov, next_player, depth-1)[1]))
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


def maxmin_ab_2(board, player, depth, a, b):
    # print("AAAAAAAA")
    global cou
    opponent = {'o':'@', '@': 'o'}[player]
    best = {'o': min, '@': max}
    if depth == 0:  # if we've reached the desired depth
        return (None, board_score(board))  # return the score

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


def board_score(board):
    global WEIGHTS, WEIGHTS_O
    if board in SEEN.keys():
        # print('a')
        return SEEN[board]

    moves_left = board.count('.')
    m_weight = 2000 if moves_left > 5 else 0
    c_weight = 600 if moves_left < 5 else 0 if moves_left < 10 else -300
    t_weight = 75 if moves_left > 5 else 25
    s_weight = 200 if moves_left > 10 else 100
    f_weight = 200 if moves_left > 5 else 50

    mobility =  (len(get_valid_moves(board, '@')) - len(get_valid_moves(board, 'o')))   * m_weight
    territory = (score_territory(board, '@') - score_territory(board, 'o'))             * t_weight
    count =     (board.count('@') - board.count('o'))                                   * c_weight
    shots =     (score_shots(board, '@') - score_shots(board, 'o'))                     * s_weight
    frontier =  (score_frontier(board, 'o') - score_frontier(board, '@'))               * f_weight
    # lines =   (score_lines(board, 'o') - score_lines(board, '@'))                       * l_weight
    # keep =      (score_keep(board, '@') - score_keep(board, 'o'))                       * k_weight
    # rows =      score_rows(board, '@') - score_rows(board, 'o')                         * r_weight

    SEEN[board] = mobility + territory + count + shots + frontier

    print("m: %s\nt: %s\nc: %s\ns: %s\nf: %s\nTOTAL: %s" % (mobility, territory, count, shots, frontier, SEEN[board]))

    return mobility + territory + count + shots + frontier


def score_territory(board, player):
    global aa, bb, cc, dd, ee
    score = 0
    for spot in [x for x in range(0, 100) if board[x] == player]:
        score += WEIGHTS[spot]

    return score


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


def score_frontier(board, player):
    score = 0
    spots = set([x for x in range(0, 100) if board[x] == player])
    directions = [1, 10, -1, -10]
    for spot in spots:
        for direction in directions:
            if board[spot+direction] == '.':
                score += 1
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


def score_rows(board, player):
    score = 0
    spots = set([x for x in range(0, 100) if board[x] == player])
    if set(range(11, 19)).issubset(spots) or set(range(81, 89)).issubset(spots) or set(range(11, 82, 10)).issubset(spots) or set(range(18, 89, 10)).issubset(spots):
        score += 2

    if set(range(12, 18)).issubset(spots) or set(range(82, 88)).issubset(spots) or set(range(21, 81, 10)).issubset(spots) or set(range(28, 88, 10)).issubset(spots):
        score += -1

    op = opposite(player)
    op_spots = set([x for x in range(0, 100) if board[x] == op])

    if set(range(12, 18)).issubset(op_spots) or set(range(82, 88)).issubset(op_spots) or set(range(21, 81, 10)).issubset(op_spots) or set(range(28, 88, 10)).issubset(op_spots):
        score += 1

    if set(range(11, 19)).issubset(op_spots) or set(range(81, 89)).issubset(op_spots) or set(range(11, 82, 10)).issubset(op_spots) or set(range(18, 89, 10)).issubset(op_spots):
        score += -2

    return score


def smart_move(state, token):
    global skip, cont, moves
    # cont = True
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


def a1_to_index(input):
    letters = ["A", "B", "C", "D", "E", "F", "G", "H"]

    return (letters.index(input[0].upper())+1) * 10 + int(input[1])


def index_to_a1(index):
    letters = ["A", "B", "C", "D", "E", "F", "G", "H"]

    return letters[int(index/10) - 1] + str(index % 10)


def boards_at_depth(state, token, max_depth):
    boards = []
    visited = set()
    valids = get_valid_moves(state, token)
    if not valids:
        valids = []
    fringe = deque([(move(state, token, x), 1, token) for x in valids])

    while len(fringe) > 0:
        this_state, depth, token = fringe.pop()
        if this_state in visited:
            continue
        visited.add(this_state)
        if depth == max_depth:
            for valid in get_valid_moves(this_state, opposite(token)):
                boards.append(move(this_state, opposite(token), valid))
        elif depth < max_depth:
            for valid in get_valid_moves(this_state, opposite(token)):
                fringe.append((move(this_state, opposite(token), valid), depth+1, opposite(token)))

    return boards


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
    if (state+token) in VALID_MOVES.keys():
        return VALID_MOVES[(state+token)]

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

    VALID_MOVES[(state+token)] = valid_move_indecies

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
    pct = int(100*(state.count('@')/(state.count('@') + state.count(opposite("@")))))
    print("|                       |                        |                        |                        |")
    print("".join(["#"]*pct))


if __name__ == "__main__":
    main()