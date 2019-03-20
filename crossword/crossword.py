# David Mead 3/10/2019
# take a series of commands line inputs and construct a crossword puzzle with those characteristics

import sys
import re
from collections import deque
import random

# BLANK = "........................."

BAD = "#######DOOR##AAAA##BKKC##BYYK#######"
BLANK = "#######----##----##----##----#######"
# BAD2 = "# # # # # # # # # # # # #
# # - D - - - # - - - - - #
# # - O - - - # - - - - - #
# # - G - - - # - - - - - #
# # - - - - # # # - - - - #
# # - - - # # - # # - - - #
# # - - - - # # # - - - - #
# # - - - - - # - - - - - #
# # - - - - - # - - - - - #
# # - - - - - # - - - - - #
# # # # # # # # # # # # # #"



# executes
def main():

    solve()


# main function under which the puzzle is solved
def solve():
    global height, width, num_blocked, dict_file, all_words, initial_words
    height = int(sys.argv[1][:sys.argv[1].index("x")])
    width = int(sys.argv[1][sys.argv[1].index("x") + 1:])
    num_blocked = int(sys.argv[2])
    dict_file = sys.argv[3]#"wordsC.txt"#
    initial_words = sys.argv[4:]

    # raw = "a " + '9x24 36 xwords.txt "h4x9d#" "h3x6s#" "h2x6#" "v2x0eye" "V5x1#b" "V8x20f"'
    # inp = raw.replace('"', '').split(' ')
    #
    # height = int(inp[1][:inp[1].index("x")])
    # width = int(inp[1][inp[1].index("x") + 1:])
    # num_blocked = int(inp[2])
    # dict_file = "wordsC.txt"#inp[3]
    # initial_words = inp[4:]

    # height = 11#4
    # width = 13#4
    # num_blocked = 27#0
    # dict_file = "wordsC.txt"
    # initial_words = ['H0x0begin', 'V8x12end']#'H0x0door']#
    print(height, width, num_blocked, dict_file, initial_words)

    all_words = "\n".join(open(dict_file, 'r').read().splitlines())

    board = fill_blocking_squares()
    display(board)

    board_edges = remove_edges(board)
    display_edgeless(board_edges)

    # display(board)


def remove_edges(board):
    result = ""
    for x in range(1, height+1):
        result += board[(x*(width+2))+1:((x+1)*(width+2))-1]
    return result


def display_edgeless(board):
    for x in range(0, height):
        print(" ".join(list(board[x*width:(x+1)*width])))


def find_solution(board):

    starts = find_word_starts(board)
    print(starts)
    conditions = []
    # for index, direction in starts:
    #     conditions.append(find_conditions(board, index, direction))
    # get_match(conditions[0])

    temp_board = board

    print(iterate(temp_board))

    # print(bfs(temp_board, find_word_starts(board)))

    # while '-' in temp_board:
    #     temp_board = board
    #     starts = find_word_starts(temp_board)
    #     while

    return temp_board


def iterate(board):
    # fringe = deque()
    # visited = {board, }
    # fringe.append(board)

    for package in find_all_conditions(board):
        conditions = package[0]
        direction = package[1][1]
        index = package[1][0]
        matches = package[2]
        if not conditions:
            continue
        if not matches:
            continue
        for word in matches:
            new_board = add_word(board, direction, index, word)
            display(new_board)

            if not check_feasability(new_board):
                continue

            else:
                print('yes')
                check_feasability(new_board)

            if check_starts(new_board):
                return new_board

            result = iterate(new_board)
            if result:
                return result

    return False


def find_all_conditions(board):
    starts = find_word_starts(board)
    conds = []
    for index, direction in starts:
        if board[index] is not '-':
            continue
        conds.append(find_conditions(board, index, direction))

    words = []
    for condition in conds:
        matches = search_textfile(condition)
        words.append(matches)
    conds = zip(conds, starts, words)

    return sorted(conds, key=lambda x: len(x[2]))


def sort_starts(starts):
    return starts.sort(key=lambda x: sum(c.isalpha() for c in x[1]))


def bfs(board, starts):
    fringe = deque()
    visited = {board, }
    fringe.append(board)

    while len(fringe) is not 0:
        temp_board = fringe.pop()
        if check_starts(temp_board):
            return board
        children = find_word_starts(temp_board)
        for index, direction in children:
            conditions = find_conditions(temp_board, index, direction)
            if not conditions:
                continue
            matches = search_textfile(conditions)
            for match in matches:
                child_board = add_word(temp_board, direction, index, match)
                if child_board not in visited:
                    fringe.append(child_board)
                    visited.add(child_board)
                    display(child_board)

    if len(fringe) == 0:
        return -1


def check_feasability(board):
    starts = find_word_starts(board)
    for index, direction in starts:
        conditions = find_conditions(board, index, direction)
        if not re.search(conditions, all_words, re.I):
            return False
    return True


def check_starts(board):
    starts = find_word_starts(board)
    for index, direction in starts:
        conditions = find_conditions(board, index, direction)
        if not conditions:
            return False
        if '.' in conditions:
            return False
        if not get_match(conditions):
            return False
    return True


def conditions_list(board, starts):
    conditions = []
    for index, direction in starts:
        conditions.append(find_conditions(board, index, direction))
    return conditions


def get_match(conditions):
    matches = re.findall(conditions, all_words, re.I)
    if len(matches) > 0:
        return matches[random.randrange(len(matches))]
    return []


# finds the beginings of unsolved words and then finds their solutions
# returns _
def find_word_starts(board):
    starts = []
    for index, letter in enumerate(board):
        if letter == '#':
            for direction in (width+2, 1):
                if 0 < (index + direction) < len(board):
                    if board[index + direction] != '#':
                        starts.append((index+direction, direction))
    return starts


# takes the general conditions for the regex search and makes it better
# returns a regex string
def format_conditions(conditions):
    conditions = conditions.replace("-", '.')
    if len(conditions) > 3:
        if re.match(".*\.+$", conditions):
            count = len(conditions[re.search("\.+$", conditions).start():])
            return "(?=\\b"+conditions[:re.search("\.+$", conditions).start()]+"\.{0,"+ str(count) + "}).{"+str(len(conditions))+"}\\b"
        return "(?=\\b"+conditions+"\\b).{"+str(len(conditions))+"}\\b"
    else:
        return conditions


# finds the regex expression to find a word starting at a certain point
# returns the formatted expression
def find_conditions(board, start, direction):
    position = start + direction
    conditions = board[start]
    while board[position] != '#':
        conditions += board[position]
        position += direction
    # print(conditions)
    # print(format_conditions(conditions))
    return format_conditions(conditions)


# fills the board with the appropriate number of legal blocking squares
# returns the board with blocking squares
def fill_blocking_squares():
    global illegals
    board = add_initial_words(initial_words)
    display(board)
    if num_blocked % 2 != 0 and width % 2 != 0 and height % 2 != 0:
        board = scribe(board, ((int(height/2)+1)*int(width+2)+(int(width/2)+1)), '#')
        board = propogate(board)
    display(board)
    legs = []
    illegals = find_illegal_squares(board)
    for index, letter in enumerate(board):
        if letter == '-':
            if index not in illegals:
                legs.append(index)

    legals = order_legal_spaces(board, legs)

    total_ideal_blockers = num_blocked + (width*2) + (height*2) + 4
    temp_board = board
    while temp_board.count('#') != total_ideal_blockers or not legal(temp_board):
        temp_board = board
        temp_legals = list(legals)

        count = 0

        while temp_board and temp_board.count('#') < total_ideal_blockers:

            move = temp_legals[random.randint(0, len(temp_legals)-1)]#[int(random.randint(0, count))]#
            count += 1
            if rotate(move) in legals:
                temp_board = scribe(temp_board, move, '#')
                temp_board = scribe(temp_board, rotate(move), '#')
                temp_board = propogate(temp_board)
            a = 5

    long = longest_in_board(temp_board, legs)
    if long > max(width, height):
        return fill_blocking_squares()

    if temp_board and legal(temp_board) and temp_board.count('#') == total_ideal_blockers:
        return temp_board
    else:
        return fill_blocking_squares()


def longest_in_board(board, legals):
    longest = 0
    for legal in legals:
        long = longest_chunk(board, legal)
        if long > longest:
            longest = long
    return longest


def order_legal_spaces(board, legals):
    values = []
    for legal in legals:
        values.append((abs(-longest_chunk(board, legal)+int(width ** 0.5)+5), legal)) #
    values = sorted(values, key=lambda x: x[0])
    return [value[1] for value in values]


def longest_chunk(board, legal):
    longest = 0
    directions = [1, -1, (width + 2), -(width + 2)]
    for direction in directions:
        move = legal + direction
        count = 0
        while -1 < move < len(board) and board[move] != '#':
            count += 1
            move += direction
        if count > longest:
            longest = count
    return longest


def find_longest_words(board):
    lengths_and_middles = []
    directions = [1, -1, (width + 2), -(width + 2)]
    for index, letter in enumerate(board):
        if letter == '#':
            for direction in directions:
                move = index + direction
                count = 0
                while -1 < move < len(board) and board[move] != '#':
                    count += 1
                    move += direction
                middle = index + int(count/2)*direction
                lengths_and_middles.append((count, middle))
    lengths_and_middles = sorted(lengths_and_middles, key=lambda x: len(x[0]))
    return lengths_and_middles


# checks all the different legality tests on the board
# returns true or false
def legal(board):
    return check_too_many_blocked(board) and check_word_lengths(board) and check_connectivity(board)


# finds all squares that are illegal to block
# returns a list of indecies
def find_illegal_squares(board):
    illegal_squares = []
    temp_board = board
    for index, letter in enumerate(board):
        if letter == '-':
            temp_board = scribe(board, index, '#')
            temp_board = scribe(temp_board, rotate(index), '#')
            if not temp_board:
                illegal_squares.append(index)
                continue
            new_board = propogate(temp_board)
            while new_board != False and check_connectivity(board) and new_board != temp_board and check_too_many_blocked(new_board):
                temp_board = new_board
                new_board = propogate(new_board)
            if not new_board:
                illegal_squares.append(index)
            elif not check_connectivity(new_board):
                illegal_squares.append(index)
            elif not check_too_many_blocked(new_board):
                illegal_squares.append(index)
        elif letter != '#':
            illegal_squares.append(index)
    return illegal_squares


# checks if there is too many squares blocked on the board
# returns true or false
def check_too_many_blocked(board):
    return (board.count('#')-(width*2 + height*2 + 4)) <= num_blocked


# given the board with blocking squares, is fills up the other spots that need squares
# returns the propogated board or False
def propogate(board):
    directions = [1, -1, (width + 2), -(width + 2)]
    for index, letter in enumerate(board):
        if letter == '#':
            for direction in directions:
                move = index + direction
                count = 0
                while move > -1 and move < len(board) and board[move] != '#':
                    count += 1
                    move += direction
                if count != 0 and count < 3:
                    move = index + direction
                    count = 0
                    while move > -1 and move < len(board) and board[move] != '#':
                        if board[move] == '-' and board[rotate(move)] == '-':
                            board = scribe(board, move, '#')
                            board = scribe(board, rotate(move), '#')
                        move += direction
    return board


# checks that there are no blocking squares resulting in words less than 3 letters being placed
# returns true or false
def check_word_lengths(board):
    directions = [1, -1, (width + 2), -(width + 2)]
    for index, letter in enumerate(board):
        if letter == '#':
            for direction in directions:
                move = index + direction
                count = 0
                while -1 < move < len(board) and board[move] != '#':
                    count += 1
                    move += direction
                if count != 0 and count < 3:
                    return False
    return True


# checks that all spaces (dots or letters) are connected to each other
# returns true or false
def check_connectivity(board):
    directions = [1, -1, (width+2), -(width+2)]
    top_left = 0

    if '-' in board:
        while top_left <= len(board) and board[top_left] == '#':
            top_left += 1

    visited = {top_left}
    fringe = deque()
    fringe.append(top_left)
    while len(fringe) > 0:
        spot = fringe.popleft()
        visited.add(spot)
        board = force_scribe(board, spot, '@')
        if not board:
            print('no')
        # display(board)
        for direction in directions:
            move = spot + direction
            if board[move] != '#':
                if move not in visited:
                    visited.add(move)
                    fringe.append(move)
    if '-' in board:
        return False
    return True


# checks that the correct number of blocked are blocked
# returns True or False
def check_num_blocked(board):
    total_num_blocked = (2*width) + (2*height) + 4 + num_blocked
    if board.count('#') == total_num_blocked:
        return True
    return False


# searches the dictionary string for the specified regex and orders them longest to shortest
# returns the first match
def search_textfile(conditions):
    if not conditions:
        return None
    matches = re.findall(conditions, all_words, re.I)
    return matches


# adds the given words from a list of their V#x#word form
# returns the newly constructed board
def add_initial_words(words):
    board = "#" * (width+2) + ("#" + "-"*width + "#")*height + "#" * (width+2)
    display(board)
    for thing in words:
        index = (int(thing[1:thing.index('x')]) + 1) * (width + 2) + int(thing[thing.index('x')+1:re.search("\D+$", thing).start()]) + 1
        board = add_initial_word(board, thing[0].upper(), index, thing[re.search("\D+$", thing).start():])
    return board


# add a specific word in a specific location
# returns new board, or False if the word doesn't word there
def add_word(board, add_to_shift, location, word):
    word = word.upper()

    for letter in word:
        board = force_scribe(board, location, letter)
        location += add_to_shift

    return board


# add a specific word in a specific location
# returns new board, or False if the word doesn't word there
def add_initial_word(board, orient, location, word):
    add_to_shift = {"V": width+2, "H": 1}[orient]
    word = word.upper()

    for letter in word:
        board = scribe(board, location, letter)
        if letter == '#':
            board = scribe(board, rotate(location), letter)
        location += add_to_shift

    return board


# returns the index of the spot rotated 180 degrees from the specified spot
def rotate(index):
    row = int(index/(width+2))
    col = index%(width+2)-1
    new_row = height-row+1
    new_col = width-col+1
    return new_row * (width + 2) + new_col -1


# adds the specified letter to the board in the specified spot
# returns the new board
def scribe(board, index, letter):
    # if board[index] in "#-":
    return board[:index] + letter + board[index+1:]
    # return False


def force_scribe(board, index, letter):
    return board[:index] + letter + board[index+1:]


# prints the board neatly to the console
# returns nothing
def display(board):
    if not board:
        print('yuck')
    for row in range(0, height+3):
        print(" ".join(list(board[row*(width+2):(row+1)*(width+2)])))


# runs the main function
if __name__ == "__main__":
    main()