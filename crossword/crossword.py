# David Mead 3/10/2019
# take a series of commands line inputs and construct a crossword puzzle with those characteristics

import sys
import re
from collections import deque
import random
import time

# BLANK = "........................."
letters = "ETAOINSRHDLUCMFYWGPBVKXQJZ"

BAD = "#######DOOR##AAAA##BKKC##BYYK#######"
BLANK = "#######----##----##----##----#######"
seen = set()
conditions_dict = {}
""# # # # # ## A S S E ## S A A D ## S A R D ## E D I - ## # # # # #"

#  # # E E E E #
#  E E N S I E #
#  E E R I L Y #
#  E N O # E O E
#  # S O L E R A
#  # I T U N E S
#  # E S T S # #
#  4.506103582000001




# executes
def main():
    sys.setrecursionlimit(500000)
    solve()


# main function under which the puzzle is solved
def solve():
    global height, width, num_blocked, dict_file, all_words, initial_words, len_all_words, very_begin
    very_begin = time.perf_counter()
    if len(sys.argv) > 1:
        height = int(sys.argv[1][:sys.argv[1].index("x")])
        width = int(sys.argv[1][sys.argv[1].index("x") + 1:])
        num_blocked = int(sys.argv[2])
        dict_file = sys.argv[3]#"wordsC.txt"#
        initial_words = sys.argv[4:]
    else:
        raw = "a " + '5x5 0 dct20k.txt "V3x1D"'
        inp = raw.replace('"', '').split(' ')

        height = int(inp[1][:inp[1].index("x")])
        width = int(inp[1][inp[1].index("x") + 1:])
        num_blocked = int(inp[2])
        dict_file = inp[3]#'morewords.txt'#
        initial_words = inp[4:]

    start = time.perf_counter()

    # height = 11#4
    # width = 13#4
    # num_blocked = 27#0
    # dict_file = "wordsC.txt"
    # initial_words = ['H0x0begin', 'V8x12end']#'H0x0door']#
    # print(height, width, num_blocked, dict_file, initial_words)

    all_words = "\n".join(open(dict_file, 'r').read().splitlines())

    len_all_words = split_all_words(all_words)

    start = time.perf_counter()

    board = setup_blocking()
    print("setup, now filling")

    board = letter_by_letter(board)
    print("done filling, now printing")

    display_edgeless(remove_edges(board))

    print(time.perf_counter()-start)



def split_all_words(all_words):
    len_to_words = dict()
    a_words = all_words.split('\n')
    for length in range(3, 31):
        words = ""
        for word in a_words:
            if len(word) == length:
                words += "\n" + word
        len_to_words[length] = words
    return len_to_words


alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def letter_by_letter(board):
    # if board in seen:
    #     print("already seen 2")
    #     return None
    for spot in get_blank_spots(board):
        # if board in seen:
        #     continue
    #     hor_d, vert_d = find_depth(board, spot)
    #     hor_c, vert_c = get_conditions_for_spot(board, spot)
        letter_to_valids = []
        # for letter in alphabet:
        #     hor_c_new = hor_c[:5+hor_d] + letter + hor_c[5+hor_d:]
        #     vert_c_new = vert_c[:5+vert_d] + letter + vert_c[5+vert_d:]
        #
        #     hor_count = len(re.findall(hor_c_new, all_words, re.I))
        #     vert_count = len(re.findall(vert_c_new, all_words, re.I))
        #
        #     if hor_count > 0 and vert_count > 0:
        #         freq = min(hor_count, vert_count)
        #     else:
        #         freq = -1
        #     letter_to_valids.append((letter, freq))
            # if re.search(hor_c_new, all_words, re.I) and re.find(vert_c_new, all_words, re.I):
            #     letter_to_valids.append((letter, 1))

        # letter_to_valids = sorted(letter_to_valids, key=lambda x: x[1])[::-1]
        found = False
        for letter in letters:#alphabet:#

            new_board = scribe(board, spot, letter)

            if new_board in seen:
                # print("already seen")
                continue
            check = check_feasability(new_board)
            if not check:
                continue
            # found = True
            # new_board = check
            while check and new_board != check:
                new_board = check
                check = check_feasability(new_board)
            if not check:
                continue
            new_board = check
            # # check_board = new_board
            # while check and new_board != check:
            #     new_board = check
            #     check = check_feasability(new_board)
            # if not check:
            #     return None
            # new_board = check
            found = True
            #
            seen.add(new_board)
            display(new_board)
            if check_done(new_board):
                # print("DONE")
                return new_board
            result = letter_by_letter(new_board)
            if result:
                if len(str(result)) > 4:
                    return result
                elif in_same_row(result, spot):
                    continue  #return None #
                else:
                    return result
                    # return result
        if not found:# or board[spot] == '-':
            # print("YUCK")
            return spot#letter_by_letter(board)

    return None


def get_blank_spots(board):
    result = [spot for spot, o in enumerate(board) if o == '-']
    directions = [-1, 1, (width+2), -(width+2)]
    to_sort = []
    for blank in result:
        count = 0
        for direction in directions:
            temp = blank + direction
            while board[temp] != '#':
                if board[temp] != '-':
                    count += 1
                temp += direction
        to_sort.append((blank, count + random.random()))

    to_return = sorted(to_sort, key=lambda x: x[1])

    # random.shuffle(result)
    return result# [x[0] for x in to_return][::1]#


def in_same_row(spot1, spot2):
    diff = spot1-spot2
    if diff == 0:
        return False
        # print("AAAAA")
    if diff % (width+2) == 0:
        return True
    else:
        for row in range(1, height):
            if row * (width+2) < spot1 < (row+1) * (width+2):
                if row * (width + 2) < spot2 < (row + 1) * (width + 2):
                    return True
    return False


def check_feasability(board):
    starts = find_word_starts(board)
    new_board = str(board)
    for index, direction in starts:
        conditions = find_conditions(board, index, direction)
        if conditions in conditions_dict.keys():
            search = conditions_dict[conditions]
        else:
        # search = re.search(conditions, all_words, re.I)
            search = search_lengths_list(conditions)
            conditions_dict[conditions] = search
        if len(search) == 1:
            board = add_word(board, direction, index, search[0])
        if not search:
            return False
        if not get_full_words(board):
            return False
    return board


def get_full_words(board):
    starts = find_word_starts(board)
    words = set()
    for index, direction in starts:
        temp = index
        word = ""
        while board[temp] != '#':
            if board[temp] == '-':
                break
            word += board[temp]
            temp += direction
        if board[temp] == '#':
            if word in words:
                return False
            words.add(word)
    return True


def search_lengths_list(conditions):
    length = int(conditions[conditions.index("{")+1:conditions.index("}")])
    letters = conditions[conditions.index('b')+1:conditions.index(')')]
    search = re.findall(conditions, len_all_words.get(length), re.I)
    # if len(search) == 1:
    #     print("YEYEE")
    return search


def check_done(board):
    if not board:
        return False
    if len(str(board)) < 4:
        return False
    if '-' in board:
        return False
    starts = find_word_starts(board)
    for start, direction in starts:
        temp = start
        while board[temp] != '#':
            if board[temp] == '-':
                return False
            temp += direction

    return True


def count_valid_words(hor_c_new, vert_c_new):
    hor = len(re.findall(hor_c_new, all_words, re.I))
    vert = len(re.findall(vert_c_new, all_words, re.I))
    if hor == 0:
        return -1
    if vert == 0:
        return -1
    return hor + vert


# finds the conditions for the spot's or and vert words
# returns (hor, vert) conditions
def get_conditions_for_spot(board, spot):
    direction = -(width + 2)
    temp_spot = spot + direction
    while board[temp_spot] != '#':
        temp_spot += direction
    vert = find_conditions(board, temp_spot-direction, -direction)

    direction = -1
    temp_spot = spot + direction
    while board[temp_spot] != '#':
        temp_spot += direction
    hor = find_conditions(board, temp_spot-direction, -direction)

    return hor, vert


# finds how deep it each word the letter is
# returns (hor, vert) depths
def find_depth(board, spot):
    direction = -(width + 2)
    temp_spot = spot + direction
    count = 0
    while board[temp_spot] != '#':
        temp_spot += direction
        count += 1
    vert = count

    direction = -1
    temp_spot = spot + direction
    count = 0
    while board[temp_spot] != '#':
        temp_spot += direction
        count += 1
    hor = count

    return (hor, vert)



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

    # while '-' in temp_board:x
    #     temp_board = board
    #     starts = find_word_starts(temp_board)
    #     while

    return temp_board


def iterate(board):
    if check_starts(board):
        return board
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
            if new_board == board:
                continue
            # display(new_board)

            if not check_feasability(new_board):
                continue
            else:
                display(new_board)

            result = iterate(new_board)
            if result:
                return result

    return False


def find_all_conditions(board):
    starts = find_word_starts(board)
    conds = []
    for index, direction in starts:
        if board[index] is '-':
            continue
        conds.append(find_conditions(board, index, direction))

    words = []
    for condition in conds:
        matches = search_textfile(condition)
        for match in matches:
            words.append(matches)
    conds = zip(conds, starts, words)

    return conds#sorted(conds, key=lambda x: len(x[2]))


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


def check_starts(board):
    starts = find_word_starts(board)
    for index, direction in starts:
        conditions = find_conditions(board, index, direction)
        if not conditions:
            return False
        if not get_match(conditions):
            return False
    if board.count('-') == 0:
        return True
    return False


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
    if len(conditions) >= 3:
        if re.match(".*\.+$", conditions):
            count = len(conditions[re.search("\.+$", conditions).start():])
            return "(?=\\b"+conditions[:re.search("\.+$", conditions).start()]+").{"+str(len(conditions))+"}\\b"
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


def setup_blocking():
    global illegals
    global best_board
    best_board = (0, 10000)
    board = add_initial_words(initial_words)
    # display(board)
    a = 5
    if num_blocked % 2 != 0 and width % 2 != 0 and height % 2 != 0:
        board = scribe(board, ((int(height / 2) + 1) * int(width + 2) + (int(width / 2) + 1)), '#')
        board = propogate(board)
    # display(board)
    legs = []
    illegals = find_illegal_squares(board)
    # for il in illegals:
    #     board = scribe(board, il, '@')
    # display(board)
    for index, letter in enumerate(board):
        if letter == '-':
            if index not in illegals:
                legs.append(index)

    legals = order_legal_spaces(board, legs)

    total_ideal_blockers = num_blocked + (width * 2) + (height * 2) + 4
    temp_board = str(board)

    global full_start
    full_start = time.perf_counter()

    return fill_blocking_squares(board, legals, total_ideal_blockers)



# fills the board with the appropriate number of legal blocking squares
# returns the board with blocking squares
def fill_blocking_squares(board, legals, total_ideal_blockers):
    global best_board
    # global illegals
    # board = add_initial_words(initial_words)
    # display(board)
    # a = 5
    # if num_blocked % 2 != 0 and width % 2 != 0 and height % 2 != 0:
    #     board = scribe(board, ((int(height/2)+1)*int(width+2)+(int(width/2)+1)), '#')
    #     board = propogate(board)
    # # display(board)
    # legs = []
    # illegals = find_illegal_squares(board)
    # # for il in illegals:
    # #     board = scribe(board, il, '@')
    # # display(board)
    # for index, letter in enumerate(board):
    #     if letter == '-':
    #         if index not in illegals:
    #             legs.append(index)
    #
    # legals = order_legal_spaces(board, legs)
    #
    # total_ideal_blockers = num_blocked + (width*2) + (height*2) + 4
    temp_board = str(board)
    # display(temp_board)
    # for il in illegals:
    #     temp_board = scribe(temp_board, il, '@')
    # display(temp_board)
    #
    # new_board = fill_squares(board, legals, total_ideal_blockers)
    # display(new_board)
    # print(longest_in_board(board, legals))
    # return new_board
    # sorte = sort_next_blocks(temp_board, legals)
    # print(sorte)

    while temp_board.count('#') != total_ideal_blockers or not legal(temp_board):
        temp_board = board
        temp_legals = order_legal_spaces(board, legals)#list(legals)#sort_next_blocks(board, legals)##list(legals)

        count = 0

        begin = time.perf_counter()

        while temp_board and temp_board.count('#') < total_ideal_blockers:# and legal(board):

            moves = sort_next_blocks(temp_board, legals)
            if len(moves) > 0:
                if len(moves) > 3:
                    move = moves[random.randint(0, 2)]
                else:
                    move = moves[random.randint(0, len(moves)-1)]#temp_legals[random.randint(0, len(temp_legals)-1)]#
            else:
                break

            # if abs(time.perf_counter() - begin) > .5:
            #     break

            count += 1
            if rotate(move) in legals:
                temp_board = scribe(temp_board, move, '#')
                temp_board = scribe(temp_board, rotate(move), '#')
                temp_board = propogate(temp_board)
            else:
                move = moves[random.randint(0, len(moves) - 1)]
                if rotate(move) in legals:
                    temp_board = scribe(temp_board, move, '#')
                    temp_board = scribe(temp_board, rotate(move), '#')
                    temp_board = propogate(temp_board)

            # display(temp_board)
                # if longest_in_board_a(temp_board2, legals) < longest_in_board_a(temp_board, legals):
                # temp_board = temp_board2
            # print(longest_in_board(temp_board, legals))
            # display(temp_board)
            # a = 5

    long = longest_in_board_a(temp_board, legals)

    if abs(time.perf_counter()-full_start) > 7:
        return best_board[0]

    if long < best_board[1]:
        best_board = (temp_board, long)

    if long > 5:#max(width, height)/3:
        return fill_blocking_squares(board, legals, total_ideal_blockers)

    if temp_board and legal(temp_board) and temp_board.count('#') == total_ideal_blockers:
        # print(longest_in_board(temp_board, legals), width, height)
        return temp_board
    else:
        return fill_blocking_squares(board, legals, total_ideal_blockers)


seen_filled = set()


def fill_squares(board, legals, ideal):
    # if board in seen_filled:
    #     print('seened')
    #     return None
    # else:
    #     seen_filled.add(board)
    if not board:
        return None
    print(longest_in_board(board, legals))
    # display(board)
    if is_done(board, ideal):
        if num_blocked == 0:
            return board
        if longest_in_board(board, legals) <= min(width, height):
            return board
        return None

    moves = sort_next_blocks(board, legals)
    for move in moves:
        if rotate(move) in legals:
            temp_board = scribe(board, move, '#')
            temp_board = scribe(temp_board, rotate(move), '#')
            temp_board = propogate(temp_board)
        else:
            temp_board = None
        if not temp_board:
            continue
        if temp_board in seen_filled:
            continue
        seen_filled.add(temp_board)
        if temp_board.count('#') > ideal or not legal(temp_board):
            continue
        result = fill_squares(temp_board, legals, ideal)
        if result:
            return result
    return None


def is_done(board, ideal):
    if not board:
        return False
    elif board.count('#') > ideal:
        return False
    elif board.count('#') < ideal:
        return False
    elif not legal(board):
        return False
    return True


def sort_next_blocks(board, legals):
    directions = [-1, 1, (width+2), -(width+2)]
    values = []
    for legal in legals:
        if board[legal] == '#':
            continue
        count_h = 0
        temp = legal
        while board[temp] != '#':
            temp += 1
            count_h += 1
        temp = legal-1
        while board[temp] != '#':
            temp -= 1
            count_h += 1

        count_v = 0
        temp = legal
        while board[temp] != '#':
            temp += (width+2)
            count_v += 1
        temp = legal-(width+2)
        while board[temp] != '#':
            temp -= (width+2)
            count_v += 1

        ajs = 1
        for direction in directions:
            if board[legal + direction] == '#':
                ajs += 1

        values.append((legal, count_h + count_v - 3*ajs + random.random()))
    values = sorted(values, key=lambda x: x[1])

    return [x[0] for x in values][::-1]

#  - D - - - # - - - # - - -
#  - O - - - # - - - # - - -
#  - G - - - # - - - - - - -
#  # # # - - - - - # - - - -
#  - - - - - - # - - - - - -
#  - - - - # - - - - - # # #
#  - - - - - - - # - - - - -
#  - - - # - - - # - - - - -
#  - - - # - - - # - - - - -
#  1.169584241


def longest_in_board(board, legals):
    longest = 0
    for move in range(0, len(board)-1):
        long = longest_chunk(board, move)
        if long > longest:
            longest = long
    return longest


def longest_in_board_a(board, legals):
    longest = 0
    moves = [x for x in range(0, len(board)) if board[x] != '#']
    for legal in moves:
        long = longest_chunk(board, legal)
        # if long > longest:
        longest += long
    return longest/len(moves)


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
    # display(board)
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
    print(board.count('-'))
    if not board:
        print('yuck')
    for row in range(0, height+3):
        print(" ".join(list(board[row*(width+2):(row+1)*(width+2)])))


def display_num(board):
    print(board.count('-'))
    if not board:
        print('yuck')
    for row in range(0, height + 2):
        nums = ""
        for x in range(row * (width + 2), (row + 1) * (width + 2)):
            nums += ("  " if len(str(x)) == 1 else " ") + str(x)
        print(" ".join(list(board[row * (width + 2):(row + 1) * (width + 2)])) + "\t" + nums)


# runs the main function
if __name__ == "__main__":
    main()