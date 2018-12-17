import random
import sys
import math

BLANK = "???????????........??........??........??...@o...??...o@...??........??........??........???????????"
DIRECTIONS = [1, -1, 10, -10, 11, -11, 9, -9]
SIZE = 100


def main():
    random_game(BLANK)


def random_game(state):
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
        state = random_move(state, 'o')
        if not cont:
            break

    print("Game Over")
    print("Final Score:")
    print("o: %s  @: %s" % (state.count('o'), state.count('@')))
    total_moves = 64 - state.count('.')
    print("o: %s%%  @: %s%%" % (round(state.count('o')*100 / total_moves, 4), round(state.count('@')*100 / total_moves, 4)))
    print(("o" if state.count('o') > state.count('@') else '@') + " wins!")
    print(moves)


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
        return False

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
        to_print = " ".join(state[x * 10 + 1:(x + 1) * 10 - 1]) + " \t" + " ".join(
            [(str(x * 10 + y) + (" " if len(str(x * 10 + y)) == 1 else "")) for y in
             range(1, 9)])  # letters[x-1] + "\t" +
        print(to_print)
        # print(letters[x] + "\t" + " ".join(state[x*8:(x+1)*8]) + " \t" + " ".join([(str(x*8+y)+ (" " if len(str(x*8+y)) == 1 else "")) for y in range(0, 8)]))
        # print((" ".join(state[x*8:(x+1)*8])) + " \t" + " ".join([(str(x*8+y)+ (" " if len(str(x*8+y)) == 1 else "")) for y in range(0, 8)])
    print()
    print(" o: %s  @: %s" % (state.count('o'), state.count('@')))
    # print("\t1 2 3 4 5 6 7 8")
    print()


if __name__ == "__main__":
    main()