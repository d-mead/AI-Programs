import random
import sys
import time
from heapq import heappush, heappop
from collections import deque
import math

BLANK = "???????????........??........??........??...@o...??...o@...??........??........??........???????????"
OTHER = "???????????........??........??.@...@..??.oooo...??...@@...??...@....??...@....??........???????????"
ROWS  = "???????????@@@@@@@@??@.......??@.......??@..@o...??@..o@...??@.......??@.......??@.......???????????"

DIRECTIONS = [1, -1, 10, -10, 11, -11, 9, -9]
SIZE = 100

# global aa, bb, cc, dd, ee
# aa = {33, 34, 35, 36, 43, 44, 45, 46, 53, 54, 55, 56, 63, 64, 65, 66}
# bb = {32, 42, 52, 62, 23, 24, 25, 26, 37, 47, 57, 67, 73, 74, 75, 76}
# cc = {31, 41, 51, 61, 13, 14, 15, 16, 38, 48, 58, 68, 83, 84, 85, 86}
# dd = {21, 22, 12, 17, 27, 28, 78, 77, 87, 82, 72, 71}
# ee = {11, 18, 81, 88}


class Strategy:
    def best_strategy(self, board, player, best_move, still_running):
        # time.sleep(1)
        best_move_setup()
        best_move.value = get_valid_moves(board, player)[0]
        d = 1
        while still_running:
            best_move.value = maxmin(board, player, d)[0]
            d += 1


def main():
    global maxing
    maxing = '@'
    best_move_setup()
    # display(OTHER)
    # minimax_to_depth(OTHER, "@", 20)
    smart_game(BLANK)


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
            possible_moves.append((spot, 10000000 if board.count('@') > 3*board.count('o') else -1000000))
        else:
            possible_moves.append((spot, maxmin(mov, next_player, depth-1)[1]))
    if len(possible_moves) > 0:
        return best[player](possible_moves, key=lambda x: x[1])
    else:
        return ('d', 'd')


def board_score(board):
    moves_left = board.count('.')
    m_weight = math.pow(int(moves_left/10), 2)
    t_weight = 50
    c_weight = math.pow(2-int(moves_left/10), 2)
    r_weight = 100
    mobility =  (len(get_valid_moves(board, '@')) - len(get_valid_moves(board, 'o')))   * m_weight
    territory = (score_territory(board, '@') - score_territory(board, 'o'))             * t_weight
    count =     board.count('@') - board.count('o')                                     * c_weight
    rows =      score_rows(board, '@') - score_rows(board, 'o')                         * r_weight

    # print(mobility)
    # print(territory)
    # print(count)

    return mobility + territory + count


def score_rows(board, player):
    score = 0
    spots = set([x for x in range(0, 100) if board[x] == player])
    for x in range(11, 82, 10):
        if set(range(x, x+8)).issubset(spots):
            score += 1
    for x in range(11, 19):
        if set(range(x, 90, 10)).issubset(spots):
            score += 1
    return score


def score_territory(board, player):
    global aa, bb, cc, dd, ee
    score = 0
    for spot in [x for x in range(0, 100) if board[x] == player]:
        if spot in aa:
            score += 1
        elif spot in bb:
            score += -1
        elif spot in cc:
            if board.count(".") > 6:
                score += 1
            else:
                score -= 3
        elif spot in dd:
            score += -10
        elif spot in ee:
            score += 3
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
        # print('I choose %s ' % spot)
        print()
        begin = time.perf_counter()
        thresh = 2
        depth = 1
        spot, score = maxmin(state, token, 1)
        while time.perf_counter() - begin < thresh-1:
            spot, score = maxmin(state, token, depth)
            depth += 1
        print(depth)
        new_state = move(state, token, spot)# new_state, score = maxmin(state, token, 3)#move(state, token, spot)
        print(score)
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
    aa = {33, 34, 35, 36, 43, 44, 45, 46, 53, 54, 55, 56, 63, 64, 65, 66}
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