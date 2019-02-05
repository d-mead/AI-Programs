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
FRONT = "???????????oooooooo??@@@@@@@@??oooooooo??........??........??........??........??........???????????"
SHOTS = "???????????oooo....??o.......??o.......??........??........??........??........??......oo???????????"
PAR_1 = "???????????........??........??........??...@@@..??...o@...??........??........??........???????????"
PAR_2 = "???????????........??........??........??...@@@..??...o@o..??....@...??........??........???????????"
SPECIAL = "??????????" \
        "?o@.....o?" \
        "?@.......?" \
        "?@.......?" \
        "?...@o...?" \
        "?...o@...?" \
        "?........?" \
        "?.......@?" \
        "?......@o?" \
        "??????????"


DIRECTIONS = [1, -1, 10, -10, 11, -11, 9, -9]
SIZE = 100

HUNDRED = False

SEEN = dict()


global WEIGHTS
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
        # time.sleep(1)

        best_move_setup()
        best_move.value = get_valid_moves(board, player)[0]
        d = 1
        while still_running:
            best_move.value = maxmin_ab_2(board, player, d, -999999999999, 999999999999)[0]
            d += 1


def main():
    global maxing, cou
    cou = 0
    maxing = '@'
    # smart_game(BLANK)
    # print(cou)
    display(FRONT)
    print(score_frontier(FRONT, '@'))
    # board_score(SPECIAL)
    # print(score_special_corners(SPECIAL, '@'))
    # begin = time.perf_counter()
    # print(maxmin_ab_2(BLANK, "@", 7, -999999999999, 999999999999))
    # # print(maxmin(BLANK, "@", 6))
    # end = time.perf_counter()
    # print(end-begin)


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
                    possible_moves.append((spot, 99999999999))
                    return None, 99999999999999
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
                    return None, 99999999999999
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
    m_weight = 50 if moves_left > 10 else 20
    c_weight = 30 if moves_left < 15 else -100
    t_weight = 25 #if moves_left > 5 else 25
    s_weight = 20 if moves_left > 10 else 10
    f_weight = 100 if moves_left > 5 else 5
    # k_weight = -15
    l_weight = 20
    sp_weight = 1500
    # r_weight = 10

    mobility =  (len(get_valid_moves(board, '@')) - len(get_valid_moves(board, 'o')))   * m_weight
    territory = (score_territory(board, '@') - score_territory(board, 'o'))             * t_weight
    count =     (board.count('@') - board.count('o'))                                   * c_weight
    shots =     (score_shots(board, '@') - score_shots(board, 'o'))                     * s_weight
    frontier =  (score_frontier(board, 'o') - score_frontier(board, '@'))               * f_weight
    special  =  (score_special_corners(board, '@') - score_special_corners(board, 'o')) * sp_weight
    lines =     (score_lines(board, 'o') - score_lines(board, '@'))                            * l_weight
    # keep =      (score_keep(board, '@') - score_keep(board, 'o'))                       * k_weight
    # rows =      score_rows(board, '@') - score_rows(board, 'o')                         * r_weight

    SEEN[board] = mobility + territory + count + shots + frontier + lines + special

    if moves_left < 10:
        display(board)
        print("m: %s\nt: %s\nc: %s\ns: %s\nf: %s\nl: %s\ns: %s\n TOTAL: %s" % (mobility, territory, count, shots, frontier, lines, special, SEEN[board]))

    return mobility + territory + count + shots + frontier + lines + special


def score_special_corners(board, player):
    score = 0
    op = opposite(player)
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


def score_frontier(board, player):
    score = 0
    spots = set([x for x in range(0, 100) if board[x] == player])
    directions = [1, 10, -1, -10]
    for spot in spots:
        found = False
        for direction in directions:
            if board[spot + direction] == '.':
                score += 1
                found = True
            elif board[spot + direction] == '?':
                found = True
        if not found:
            score -= 1
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


def score_territory(board, player):
    global aa, bb, cc, dd, ee
    score = 0
    for spot in [x for x in range(0, 100) if board[x] == player]:
        score += WEIGHTS[spot]

    return score


def smart_move(state, token):
    global skip, cont, moves
    # cont = True
    valid_moves = get_valid_moves(state, token)

    if valid_moves:
        print(token + "'s turn")
        print("valid moves: " + ", ".join([str(x) for x in valid_moves]))
        skip = False
        # spot = maxmin(state, token, 2)
        # moves.append(spot)
        print()
        begin = time.perf_counter()
        thresh = 1
        depth = 3
        spot, score = maxmin_ab_2(state, token, 5, -999999999999, 999999999999)
        # while time.perf_counter() - begin < thresh:
        #     spot, score = maxmin(state, token, depth)
        #     depth += 1
        print(depth)
        new_state = move(state, token, spot)# new_state, score = maxmin(state, token, 3)#move(state, token, spot)
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


def best_move_setup():
    global aa, bb, cc, dd, ee

    weightings = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 120, -20, 20,  5,  5, 20, -20, 120, 0,
     0, -20, -40, -5, -5, -5, -5, -40, -20, 0,
     0,  20,  -5, 15,  3,  3, 15,  -5,  20, 0,
     0,   5,  -5,  3,  3,  3,  3,  -5,   5, 0,
     0,   5,  -5,  3,  3,  3,  3,  -5,   5, 0,
     0,  20,  -5, 15,  3,  3, 15,  -5,  20, 0,
     0, -20, -40, -5, -5, -5, -5, -40, -20, 0,
     0, 120, -20, 20,  5,  5, 20, -20, 120, 0,
     0,   0,   0,  0,  0,  0,  0,   0,   0, 0)

    # print(weightings)

    aa = {13, 23, 33, 32, 31, 16, 16, 36, 37, 38, 61, 62, 63, 73, 83, 86, 76, 66, 67, 68}#{33, 34, 35, 36, 43, 44, 45, 46, 53, 54, 55, 56, 63, 64, 65, 66}
    bb = {32, 42, 52, 62, 23, 24, 25, 26, 37, 47, 57, 67, 73, 74, 75, 76}
    cc = {31, 41, 51, 61, 13, 14, 15, 16, 38, 48, 58, 68, 83, 84, 85, 86}
    dd = {21, 22, 12, 17, 27, 28, 78, 77, 87, 82, 72, 71}
    ee = {11, 18, 81, 88}

    # bads = {22, 27, 77, 72, 12, 21, 22,  17, 27, 28,  71, 72, 82,  87, 77, 78, 33, 34, 35, 36, 43, 44, 45 ,46, 53, 54 ,55, 56, 63, 64 ,65, 66}
    # corners = {11, 18, 81, 88}
    # brackets = {13, 23, 33, 32, 31,  16, 26, 36, 37, 37,  68, 67, 66, 76, 86,  83, 73, 63, 62, 61}
    # sides = {31, 41, 51, 61, 13, 14, 15, 16, 38, 48, 58, 68, 83, 84, 85, 86}


def get_best_move(state, token):
    best_score = -1001
    best_move = 0
    depth = 7#state.count(".")
    valid_spots = get_valid_moves(state, token)
    for valid_spot in valid_spots:
        mov = move(state, token, valid_spot)
        result = maxi_to_depth(mov, opposite(token), depth+1)
        score = score_board(result, token)
        # display(result)
        # print(score)
        score += add_loction(valid_spot) * 10
        # score += (8-(valid_spot/10)) * 100
        if score > best_score:
            best_score = score
            best_move = valid_spot
        print("%s: %s" % (valid_spot, score))

    r = maxi_to_depth(move(state, token, best_move), opposite(token), depth+1)
    s = score_board(r, token)
    print(r, s)

    return best_move


def maxi(state, token):
    global corners
    valid_spots = get_valid_moves(state, token)
    best_score = -50000
    best_move = state
    if len(valid_spots) == 0:
        return state, 1000

    for valid_spot in valid_spots:
        mov = move(state, token, valid_spot)
        score = score_board(mov, token)
        if score > best_score:
            best_score = score
            best_move = mov

    return best_move, best_score


def maxi_to_depth(state, token, depth):
    for x in range(0, depth):
        state, score = maxi(state, token)
        if score == 1000:
            break
        token = opposite(token)

    return state


def minimax_to_depth(state, token, depth):
    # dictionary mapping moves to worst score
    # from 0 to depth/2:
    #   find the best move for the current token
    #   for each subsequent move for the next token:
    #       score it and if it is worse than the worst score in its original move dictionary
    #       swap it in to the dictionary
    # return the best of the worst scores
    move_to_worst_score = dict()
    fringe = deque()
    next_fringe = deque()
    original_token = token
    for valid_token in get_valid_moves(state, token):
        move_to_worst_score[valid_token] = 10000
        fringe.append((move(state, token, valid_token), valid_token))
    if len(get_valid_moves(state, token)) > 0:
        for x in range(0, int(depth/2)):  # goes down depth/2 (each itteration is two move levels)
            while len(fringe) > 0:  # while the current fringe ( black dots ) isn't empty;
                prev_mov, original = fringe.pop()  # pop the examiing move and direivative move off the fringe
                token = opposite(token)  # swap the token
                valid_moves = get_valid_moves(prev_mov, token)
                if len(valid_moves) == 0:
                    break
                for next_spot in valid_moves:  # looping through all of the next white moves:
                    this_mov = move(prev_mov, token, next_spot)  # make the current move
                    this_score = score_board(this_mov, original_token)  # score it

                    if this_score < move_to_worst_score[original]:  # if this score is the worst for the derivative move:
                        move_to_worst_score[original] = this_score  # swap it out in the dictionary
                    # display(this_mov)
                    next_mov = maxi(this_mov, opposite(token))  # the next move is the maximum for the black dot
                    next_fringe.append((next_mov, original))  # add this maximum black dot to the next layer to examine
                token = opposite(token)
            while len(next_fringe) > 0:
                fringe.append(next_fringe.pop())

    # for spot, score in move_to_worst_score.items():
    #     print(spot)
    #     print(score)
    #     display(move(state, token, spot))
    #     print()

    best_score = -100000
    best_spot = 0

    for spot, score in move_to_worst_score.items():
        score += add_loction(spot)*10
        score += (8-(spot/10)) * 1000
        print("%s: %s" % (spot, score))
        if score  > best_score:
            best_score = score
            best_spot = spot

    return best_spot


def add_loction(spot):
    global aa, bb, cc, dd, ee
    if spot in ee:
        return 200
    elif spot in cc:
        return 100
    elif spot in bb or dd:
        return -100
    return 0


def score_board(state, token):
    score = 0
    if len(get_valid_moves(state, token)) == 0:
        if len(get_valid_moves(state, opposite(token))) == 0:
            if state.count(token) >= 3*state.count(opposite(token)):
                return 100000*(state.count(token)/(state.count(token)+state.count(opposite(token))))
            elif state.count(token) >= state.count(opposite(token)):
                return 50000 * (state.count(token) / (state.count(token) + state.count(opposite(token))))
            else:
                return -900

    # if state.count('.') < 5:
    #     capture_score(state, token) * 2
    # else:
    if state.count('.') < 5:
        score += state.count(token)
    else:
        score -= (2*state.count(token)-state.count(opposite(token)))
    score += territory_score(state, token) * 15
    # score -= territory_score(state, opposite(token)) * 15
    # score +=
    # score += mobility_score(state, token) * -1
    return score


def mobility_score(state, token):
    return 10-len(get_valid_moves(state, opposite(token)))


def capture_score(state, token):
    # returns the percentage of tokens you have, from 0 to 100
    return state.count(token)/(100-state.count('.'))*100


def territory_score(state, token):
    global aa, bb, cc, dd, ee
    score = 0
    for territory in [x for x in range(0, 100) if state[x] == token]:
        if territory in ee or cc:
            score += 10
        elif territory in bb or dd:
            score -= 10
    return score


def smart_game(state):
    best_move_setup()
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