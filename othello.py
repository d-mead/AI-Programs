import random
import sys
import time
from heapq import heappush, heappop
from collections import deque

BLANK = "???????????........??........??........??...@o...??...o@...??........??........??........???????????"
OTHER = "???????????........??........??.@...@..??.ooo@...??...@@...??...@....??...@....??........???????????"
DIRECTIONS = [1, -1, 10, -10, 11, -11, 9, -9]
SIZE = 100


def main():
    global maxing
    maxing = '@'
    best_move_setup()
    smart_game(BLANK)
    # display(OTHER)
    # display(get_best_move(OTHER, 'o'))
    # display(maxi_to_depth(OTHER, 'o', 100))


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


def get_best_move(state, token):
    best_score = 0
    best_move = 0
    valid_spots = get_valid_moves(state, token)
    for valid_spot in valid_spots:
        mov = move(state, token, valid_spot)
        result = maxi_to_depth(mov, opposite(token), 90)
        score = score_board(result, token)
        # display(result)
        # print(score)
        if score > best_score:
            best_score = score
            best_move = valid_spot
        print("%s: %s" % (valid_spot, score))

    r = maxi_to_depth(state, opposite(token), 91)
    s = score_board(r, token)
    print(r, s)

    return best_move


def maxi(state, token):
    valid_spots = get_valid_moves(state, token)
    best_score = -5000
    best_move = -100
    if len(valid_spots) == 0:
        return state, 1000

    for valid_spot in valid_spots:
        mov = move(state, token, valid_spot)
        score = score_board(mov, token)
        if score > best_score:
            best_score = score
            best_move = mov
    if best_move == -100:
        print("B")
    return best_move, best_score


def maxi_to_depth(state, token, depth):

    for x in range(0, depth):
        state, score = maxi(state, token)
        if type(state) == int:
            print("A")
        if score == 1000:
            break
        token = opposite(token)
    return state


def score_board(state, token):
    if len(get_valid_moves(state, token)) == 0:
        if len(get_valid_moves(state, opposite(token))) == 0:
            if state.count(token) > 3*state.count(opposite(token)):
                return 1000
            else:
                if state.count(token) > state.count(opposite(token)):
                    return 500
                else:
                    return -1000
            # else:
            #     if state.count(token) > state.count(opposite(token)):
            #         return 1000
            #     else:
            #         return -1000
    score = capture_score(state, token) * 1
    score += territory_score(state, token) * 5
    return score


def capture_score(state, token):
    # returns the percentage of tokens you have, from 0 to 100
    return state.count(token)/(100-state.count('.'))*100


def territory_score(state, token):
    global corners, sides, bads
    score = 0
    for territory in [x for x in range(0, 100) if state[x] == token]:
        if territory in corners:
            score += 3
        elif territory in sides:
            score += 2
        elif territory in bads:
            score -=3
    # returns the percentage of sides and corner pieces they own from 0-100
    return 100 * score/36


def best_move_setup():
    global corners, sides, bads, maxing
    bads = {22, 27, 77, 71}
    corners = {11, 18, 81, 88}
    sides = {31, 41, 51, 61, 71, 12, 13, 14, 15, 16, 17, 28, 38, 48, 58, 68, 78, 82, 83, 84, 85, 86, 87, 21, 12, 17, 71, 82, 87, 78}


def smart_move(state, token):
    global skip, cont, moves
    # cont = True
    valid_moves = get_valid_moves(state, token)

    if valid_moves:
        print(token + "'s turn")
        print("valid moves: " + ", ".join([str(x) for x in valid_moves]))
        skip = False
        spot = get_best_move(state, token)
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