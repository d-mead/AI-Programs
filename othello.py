import random
import sys

BLANK = "???????????........??........??........??...@o...??...o@...??........??........??........???????????"
DIRECTIONS = [1, -1, 10, -10, 11, -11, 9, -9]
SIZE = 100


def main():
    play(BLANK)


# def play():


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
        print("o" if state.count('o') > state.count('x') else 'x' + "wins!")



def A1_to_index(input):
    letters = ["A", "B", "C", "D", "E", "F", "G", "H"]

    return (letters.index(input[0].upper())+1) * 10 + int(input[1])


def index_to_A1(index):
    letters = ["A", "B", "C", "D", "E", "F", "G", "H"]

    return letters[int(index/10) - 1] + str(index % 10)


def computer_move(state, token):
    global skip
    valid_moves = get_valid_moves(state, token)
    print("my turn")
    if valid_moves:
        skip = False
        spot = valid_moves[random.randint(0, len(valid_moves)-1)]
        print('i choose %s ' % index_to_A1(spot))
        new_state = make_move(state, token, spot)
        # display(new_state)
        new_state = flip_board(new_state, spot)
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
        print("your options are %s" % ", ".join([index_to_A1(x) for x in valid_moves]))
        spot = A1_to_index(input("your move: "))
        while spot not in valid_moves:
            spot = A1_to_index(input("\033[91minvalid move. \033[0m \nyour move: "))
        new_state = make_move(state, token, spot)
        new_state = flip_board(new_state, spot)
        return new_state
    if not skip:
        print("no avalable moves: you must skip")
        skip = True
        return state
    else:
        return False


def make_move(state, token, spot):
    return state[:spot] + token + state[spot+1:]


def flip_board(state, spot):
    token = state[spot]
    opposite_token = opposite(token)
    adjacencies = [spot]*len(DIRECTIONS)
    # for direction in DIRECTIONS:
    #     adjacencies.append(spot)

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
                # print(value)
                if value == opposite_token:
                    hit_opposite_token = True
            if value == token:
                # print('a')
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

# def display_options(state, options):


def display(state):
    letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
    print("\to: %s \t @: %s" % (state.count('o'), state.count('@')))
    for x in range(1, 9):
        to_print = letters[x-1] + "\t" + " ".join(state[x*10+1:(x+1)*10-1])
        print(to_print)
        # print(letters[x] + "\t" + " ".join(state[x*8:(x+1)*8]) + " \t" + " ".join([(str(x*8+y)+ (" " if len(str(x*8+y)) == 1 else "")) for y in range(0, 8)]))
        # print((" ".join(state[x*8:(x+1)*8])) + " \t" + " ".join([(str(x*8+y)+ (" " if len(str(x*8+y)) == 1 else "")) for y in range(0, 8)])
    print()
    print("\t1 2 3 4 5 6 7 8")
    print()


if __name__ == "__main__":
    main()