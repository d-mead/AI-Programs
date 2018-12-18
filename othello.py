import random
import sys
import time
from heapq import heappush, heappop
from collections import deque

BLANK = "???????????........??........??........??...@o...??...o@...??........??........??........???????????"
OTHER = "???????????........??........??.@...@..??.ooo@...??...@@...??...@....??........??........???????????"
DIRECTIONS = [1, -1, 10, -10, 11, -11, 9, -9]
SIZE = 100

# ??????????. . . . . . . . ??. . . . . . . . ??. @ . . . @ . . ??. o o o @ . . . ??. . . @ @ . . . ??. . . @ . . . . ??. . . . . . . . ??. . . . . . . .??????????


def main():
    # print("??????????. . . . . . . . ??. . . . . . . . ??. @ . . . @ . . ??. o o o @ . . . ??. . . @ @ . . . ??. . . @ . . . . ??. . . . . . . . ??. . . . . . . .??????????".replace(" ", ""))
    # display(OTHER)
    global maxing
    maxing = '@'
    best_move_setup()
    # boards = minimax_to_depth(OTHER, '@', 3)
    determine_best_move(OTHER, '@', 4)

    # play_many_games(BLANK, 10)
    # smart_game(BLANK)
    # random_game(BLANK)
    # best_move_setup()


def play_many_games(state, count):
    start = time.perf_counter()
    o_wins = 0
    tot_pct = 0
    for x in range(0, count):
        win, pct = smart_game(state)
        tot_pct += pct
        if win == 'o':
            o_wins += 1
    end = time.perf_counter()
    print("total: %s " % (o_wins*100/count))
    print("avg %%: %s " % (round(tot_pct/count, 5)))
    print("time: %s " % round(end-start, 5))


def determine_best_move(state, token, max_depth):
    # good and bad spots
    # limit the valid moves for the opponent
    # increase your number of valid moves
    global bad, good, sides
    valids = get_valid_moves(state, token)
    fringe = deque([(x, 0, token, 0, x) for x in valids])
    # (spot, depth, token, rating, original)
    visited = set()
    best_rate = -1
    best_spot = valids[0]
    ratings = dict(zip(valids, [0]*len(valids)))

    for valid in valids:
        this_move = move(state, token, valid)
        best_rate = -1
        results_at_depths = minimax_to_depth(this_move, opposite(token), max_depth)
        for result, path in results_at_depths:
            rating = rate(result, token)
            if rating > best_rate:
                best_rate = rating
        ratings[valid] = best_rate

    for mov, rating in ratings.items():
        print("%s: %s" % (mov, rating))

    display(move(state, token, best_spot))

    return best_spot


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

    # for board in boards:
    #     display(board)
    return boards


def minimax_to_depth(state, token, max_depth):
    global maxing
    boards = []
    visited = set()
    valids = get_valid_moves(state, token)

    fringe = deque([(move(state, token, x), 1, token, [state, move(state, token, x)]) for x in valids])

    while len(fringe) > 0:
        this_state, depth, token, so_far = fringe.pop()

        # if this_state in visited:
        #     continue
        visited.add(this_state)
        if depth == max_depth:
            valids = get_valid_moves(this_state, opposite(token))
            if valids:
                for valid in valids:
                    boards.append((move(this_state, opposite(token), valid), so_far))
            else:
                boards.append((this_state, so_far))
        elif depth < max_depth:
            best_rating = -1
            best_move = this_state
            valids = get_valid_moves(this_state, opposite(token))
            if valids:
                for valid in valids:
                    mov = move(this_state, opposite(token), valid)
                    rating = rate(mov, opposite(token))
                    if token == maxing:
                        if rating > best_rating:
                            best_rating = rating
                            best_move = mov
                    else:
                        if rating < best_rating:
                            best_rating = rating
                            best_move = mov
                sf = list(so_far)
                sf.append(best_move)
                fringe.append((best_move, depth + 1, opposite(token), sf))
            # else:
            #     print("A")
            #     display(this_state)

    # for board, path in boards:
    #     print("new path: ")
    #     # for b in path:
    #     #     display(b)
    #     display(board)

    return boards


def rate_layer(state, token):
    # new_state = move(state, token, spot)
    valids = get_valid_moves(state, token)
    if valids:
        best_rate = -100
        best_spot = valids[0]
        for valid in valids:
            new_move = move(state, token, valid)
            rating = rate(state, token)
            if rating > best_rate:
                best_rate = rating
                best_spot = valid

        return best_spot, best_rate

    return -1, -100


def rate(state, token):
    global good, bad, sides, maxing
    rate = 1
    valids = get_valid_moves(state, token)
    opposite_valids = get_valid_moves(state, opposite(token))

    cap = capture(state, token) * 1
    mob = mobility(state, token) * 1
    svs = spot_value(state, token) * 1

    return cap + mob + svs


def capture(state, token):
    g = state.count(token)
    b = state.count(opposite(token))
    if g == b == 0:
        return 0
    return 100 * ((g-b)/(g+b))


def mobility(state, token):
    t = get_valid_moves(state, token)
    if t:
        g = len(t)
    else:
        g = 0
    o = get_valid_moves(state, opposite(token))
    if o:
        b = len(o)
    else:
        b = 0
    if g == b == 0:
        return 0
    return 100 * ((g-b)/(g+b))


def spot_value(state, token):
    global good, bad, sides
    value = 0
    if len(state) < 99:
        print("B")
    tokens = [x for x in range(0, 99) if state[x] == token]
    for x in tokens:
        if x in good:
            value += 2
        elif x in sides:
            value += 1
        elif x in bad:
            value -= 2

    if value < 0:
        return 0

    return 100 * value/len(tokens)


def best_move_setup():
    global bad, good, sides, maxing
    bad = set([a1_to_index(x) for x in ['b2', 'b7', 'g2', 'g7']])
    good = set([a1_to_index(x) for x in ['a1', 'a8', 'h1', 'h8']])
    sides = set(list(range(21, 81, 10)) + list(range(12, 18)) + list(range(28, 88, 10)) + list(range(82, 88)))
    maxing = 'o'


def smart_move(state, token):
    global skip, cont, moves
    # cont = True
    valid_moves = get_valid_moves(state, token)

    if valid_moves:
        print(token + "'s turn")
        print("valid moves: " + ", ".join([str(x) for x in valid_moves]))
        skip = False
        spot = determine_best_move(state, token, 0)#valid_moves[random.randint(0, len(valid_moves) - 1)]
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


def smart_game(state):
    best_move_setup()
    global skip, cont, moves
    skip = False
    cont = True
    moves = []

    while state:
        display(state)
        state = random_move(state, '@')
        if not cont:
            break

        display(state)
        state = smart_move(state, 'o')
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

    return ("o" if state.count('o') > state.count('@') else '@'), round(state.count('o') * 100 / total_moves, 4)


def random_game(state):
    best_move_setup()
    global skip, cont, moves
    skip = False
    cont = True
    moves = []

    while state:
        # display(state)
        state = random_move(state, '@')
        if not cont:
            break

        # display(state)
        state = random_move(state, 'o')
        if not cont:
            break

    # print("Game Over")
    # print("Final Score:")
    print("o: %s  @: %s" % (state.count('o'), state.count('@')))
    total_moves = 64 - state.count('.')
    print("o: %s%%  @: %s%%" % (round(state.count('o')*100 / total_moves, 4), round(state.count('@')*100 / total_moves, 4)))
    print(("o" if state.count('o') > state.count('@') else '@') + " wins!")

    # print(moves)
    print()

    return "o" if state.count('o') > state.count('@') else '@'


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

    print()
    print(" o: %s  @: %s" % (state.count('o'), state.count('@')))
    print()



# beyond this point is old code no longer in use


def play(state):
    display(state)
    human = input("your token (o or @): ")
    comp = opposite(human)
    global skip
    skip = False

    while state:
        state = computer_move(state, comp)
        if state:
            display(state)
        else:
            break

        state = human_move(state, human)
        if state:
            display(state)
        else:
            break

    if state.count('.') == 0:
        print("Game Over")
        print("Final Score:")
        print("o: %s \t @: %s" % (state.count('o'), state.count('@')))
        print("o wins!" if state.count('o') > state.count('@') else "@ wins!")


def a1_to_index(input):
    letters = ["A", "B", "C", "D", "E", "F", "G", "H"]

    return (letters.index(input[0].upper())+1) * 10 + int(input[1])


def index_to_a1(index):
    letters = ["A", "B", "C", "D", "E", "F", "G", "H"]

    return letters[int(index/10) - 1] + str(index % 10)


def computer_move(state, token):
    global skip
    valid_moves = get_valid_moves(state, token)
    print("my turn")
    if valid_moves:
        skip = False
        spot = valid_moves[random.randint(0, len(valid_moves)-1)]
        print('i choose %s ' % index_to_a1(spot))
        new_state = move(state, token, spot)
        return new_state
    if not skip:
        print("no available moves: I'll skip")
        skip = True
        return state
    else:
        return False


def human_move(state, token):
    global skip
    valid_moves = get_valid_moves(state, token)
    print("your turn")
    if valid_moves:
        skip = False
        # print("your options are %s" % ", ".join([str(x) for x in valid_moves]))
        # inp =
        print("your options are %s" % ", ".join([index_to_a1(x) for x in valid_moves]))
        spot = a1_to_index(input("your move: "))
        while spot not in valid_moves:
            spot = a1_to_index(input("\033[91minvalid move. \033[0m \nyour move: "))
        new_state = move(state, token, spot)
        return new_state
    if not skip:
        print("no avalable moves: you must skip")
        skip = True
        return state
    else:
        return False


def display_old(state):
    letters = ["A", "B", "C", "D", "E", "F", "G", "H"]

    for x in range(1, 9):
        to_print = letters[x-1] + "\t" + " ".join(state[x * 10 + 1:(x + 1) * 10 - 1]) + " \t" + " ".join(
            [(str(x * 10 + y) + (" " if len(str(x * 10 + y)) == 1 else "")) for y in
             range(1, 9)])  #
        print(to_print)
        # print(letters[x] + "\t" + " ".join(state[x*8:(x+1)*8]) + " \t" + " ".join([(str(x*8+y)+ (" " if len(str(x*8+y)) == 1 else "")) for y in range(0, 8)]))
        # print((" ".join(state[x*8:(x+1)*8])) + " \t" + " ".join([(str(x*8+y)+ (" " if len(str(x*8+y)) == 1 else "")) for y in range(0, 8)])
    print()
    print("\t1 2 3 4 5 6 7 8")
    print(" o: %s  @: %s" % (state.count('o'), state.count('@')))

    print()


if __name__ == "__main__":
    main()