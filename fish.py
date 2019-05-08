# David Mead -- April 9th, 2019
# The goal of this program is to create an AI to win fish

import random

# 10 = spades, 20 = clubs, 30 = hearts, 40 = diamonds
# 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14
# a, 2, 3, 4, 5, 6, 7, 8, 9, 10,  j,  q,  k, jj

full_sets = {"low_spades":  [102, 103,  104,  105,  106,  107],
             "high_spades": [101, 109, 1010, 1011, 1012, 1013],
             "low_clubs":   [202, 203,  204,  205,  206,  207],
             "high_clubs":  [201, 209, 2010, 2011, 2012, 2013],
             "low_hearts":  [302, 303,  304,  305,  306,  307],
             "high_hearts": [301, 309, 3010, 3011, 3012, 3013],
             "low_dims":    [402, 403,  404,  405,  406,  407],
             "high_dims":   [401, 409, 4010, 4011, 4012, 4013],
             "mids":        [108, 208,  308,  408, 1014, 3014]}

card_to_set = {102: 'low_spades', 103: 'low_spades', 104: 'low_spades', 105: 'low_spades', 106: 'low_spades', 107: 'low_spades', 101: 'high_spades', 109: 'high_spades', 1010: 'high_spades', 1011: 'high_spades', 1012: 'high_spades', 1013: 'high_spades', 202: 'low_clubs', 203: 'low_clubs', 204: 'low_clubs', 205: 'low_clubs', 206: 'low_clubs', 207: 'low_clubs', 201: 'high_clubs', 209: 'high_clubs', 2010: 'high_clubs', 2011: 'high_clubs', 2012: 'high_clubs', 2013: 'high_clubs', 302: 'low_hearts', 303: 'low_hearts', 304: 'low_hearts', 305: 'low_hearts', 306: 'low_hearts', 307: 'low_hearts', 301: 'high_hearts', 309: 'high_hearts', 3010: 'high_hearts', 3011: 'high_hearts', 3012: 'high_hearts', 3013: 'high_hearts', 402: 'low_dims', 403: 'low_dims', 404: 'low_dims', 405: 'low_dims', 406: 'low_dims', 407: 'low_dims', 401: 'high_dims', 409: 'high_dims', 4010: 'high_dims', 4011: 'high_dims', 4012: 'high_dims', 4013: 'high_dims', 108: 'mids', 208: 'mids', 308: 'mids', 408: 'mids', 1014: 'mids', 3014: 'mids'}

all_cards = [101, 102, 103, 104, 105, 106, 107, 108, 109, 1010, 1011, 1012, 1013, 201, 202, 203, 204, 205, 206, 207, 208, 209, 2010, 2011, 2012, 2013, 301, 302, 303, 304, 305, 306, 307, 308, 309, 3010, 3011, 3012, 3013, 401, 402, 403, 404, 405, 406, 407, 408, 409, 4010, 4011, 4012, 4013, 1014, 3014]

a = {}  # player
b = {}
c = {}
d = {}
e = {}
f = {}


# players: list of players
# players[0]: dictionary of cards to ratings for player 0 (you)
players = []
for x in range(0, 6):
    players.append(dict(zip(all_cards, [4]*len(all_cards))))

# dictionary of card to a list of its rating for each of the players
# eg: {102: [2, 3, 4, 4, 5], ...}
cards_player_ratings = {}
for card in all_cards:
    cards_player_ratings[card] = [4, 4, 4, 4, 4, 4, 4, 4, 4]

y = 5


# ratings for cards:
# 1: positive they have it
# 2: they have asked for/have a card in that class
# 3: pretty sure they don't have it but shouldn't eliminate
# 4: this card has not been eliminated from their deck
# 5: they do NOT have the card
# 6: card is not longer in play

next_player = 0
opponents = {0: [3, 4, 5], 1: [3, 4, 5], 2: [3, 4, 5], 3: [0, 1, 2], 4: [0, 1, 2], 5: [0, 1, 2],}


def main():
    # print(len(all_cards))
    deal_random_cards()
    print(player_key)
    me = player_key[0]#[206, 3013, 204, 103, 403, 104, 101, 102, 305]
    for card in me:
        card_found(card)
        rate_player_card(0, card, 1)
        # print(num_to_name(card))

    for x in range(0, 5):
    # print_all_players_special()
    # print(me)
        random_move(next_player)
        print_all_players_special()
    # asked_for_card(next_player, opponents[next_player][random.randint(0, 2)], 306, True)

    # asked_for_card(3, 1, 3012, False)
    print_all_players_special()


player_key = []
def deal_random_cards():
    not_used = list(all_cards)
    random.shuffle(not_used)
    for p in range(0, 6):
        hand = []
        for ca in range(0, 9):
            hand.append(not_used[p*9+ca])
        player_key.append(hand)


def random_move(player_turn):
    global next_player
    player_ask = opponents[player_turn][random.randint(0, 2)]
    card_a = pick_random_card(player_turn, player_ask)
    found = card_a in player_key[player_ask]
    print(player_turn, player_ask, card_a, found)
    asked_for_card(player_turn, player_ask, card_a, found)
    if found:
        next_player = player_turn
    else:
        next_player = player_ask


def pick_random_card(player_1, player_2):
    options = []
    best_rate = 4
    for card_x, rating in players[player_2].items():
        if card_in_player_set(player_1, card_x):
            if rating < best_rate:
                options = [card_x]
                best_rate = rating
            elif rating == best_rate:
                options.append(card_x)
    print(options)
    return options[random.randint(0, len(options)-1)]


def card_in_player_set(player_1, card_b):
    the_sets = set()
    for card_a in player_key[player_1]:
        the_sets.add(card_to_set[card_a])
    if card_to_set[card_b] in the_sets:
        return True


def asked_for_card(player_index_1, player_index_2, card, had_card):
    # 1: asked for the card
    # 2: was asked for card
    rate_player_card(player_index_1, card, 5)
    asked_in_set(player_index_1, card)
    if had_card:
        rate_player_card(player_index_1, card, 1)
    else:
        rate_player_card(player_index_2, card, 5)


def propagate():
    for card, ratings in cards_player_ratings.items():
        if ratings.count(5) == 5:
            for player_index, rate in enumerate(ratings):
                if rate != 5:
                    rate_player_card(player_index, card, 1)
                    card_found(card)


def asked_in_set(player_1, card):
    for set, cards in full_sets.items():
        if card in cards:
            for c in cards:
                if c != card:
                    rate_player_card(player_1, c, 2)


# assigns the rating for that card for that player to the given rating
# puts this rating in the list of players and the card to ratings dictionary
def rate_player_card(player_index, card, rating):
    players[player_index][card] = rating
    cards_player_ratings[card][player_index] = rating


# when it is known that the player does not have that card
# assigns 5 to the card rating for that player
def doesnt_have_card(player_index, card):
    rate_player_card(player_index, card, 5)


# prints the card ratings for all cards for all players
def print_all_players():
    for player in players:
        # print()
        print(player)



def print_all_players_special():
    count = 0
    for i, player in enumerate(players):
        print("player:", count)
        print(player_key[i])
        to_print = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
        for card, rating in player.items():
            to_print[rating].append(card)
        for rate, card in to_print.items():
            print(rate, ":", card)
        print()
        count += 1


# input: card that was just found
# assigns the rating for that card as 5 for all other players than the holder of the card
def card_found(card):
    global players
    for player_index in range(0, 6):
        if players[player_index][card] != 0 or 5:
            rate_player_card(player_index, card, 5)


suits = {10: "spades", 20: "clubs", 30: "hearts", 40: "diamonds"}
classes = {1: "ace", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "jack", 12: "queen", 13: "king"}


# takes the integer representation of the card
# returns it as a neat string
def num_to_name(num):
    suit = suits[int(str(num)[:2])]
    clas = classes[int(str(num)[2:])]
    return clas + " of " + suit


if __name__ == "__main__":
    main()