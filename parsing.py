import chess
import numpy as np

common_variants = [
        ['a 1', '81', 'Day 1', 'Hey 1'],
        ['a 2', '82', 'Day 2'],
        ['a 3', '83', 'Day 3'],
        ['a 4', '84', 'Day 4'],
        ['a 5', '85', 'Day 5'],
        ['a 6', '86', 'Day 6'],
        ['a 7', '87', 'Day 7', 'A sudden'],
        ['a 8', '88', 'Day 8', 'Wait'],
        ['b 1', 'We need 1', '31'],
        ['b 2', 'me too'],
        ['b 3', '33 bing'],
        ['b 4', 'before'],
        ['b 5'],
        ['b 6', 'be sick', 'basic'],
        ['b 7'],
        ['b 8', '378', 'Create'],
        ['c 1', 'see 1'],
        ['c 2', 'seat', '22', 'see 2'],
        ['c 3', '23', 'see 3'],
        ['c 4', 'support', 'see more', 'see 4'],
        ['c 5', 'see 5'],
        ['c 6', 'see sex', 'free sex', 'see 6'],
        ['c 7', 'see 7'],
        ['c 8', 'see 8'],
        ['d 1', 'the 1'],
        ['d 2', 'the 2'],
        ['d 3', 'the 3'],
        ['d 4', 'the 4'],
        ['d 5', 'the 5'],
        ['d 6', 'the 6'],
        ['d 7', 'the 7'],
        ['d 8', 'the 8'],
        ['e 1', ],
        ['e 2', 'youtube'],
        ['e 3'],
        ['e 4', 'even more', 'enforce'],
        ['e 5', 'define', 't5'],
        ['e 6', 'isa', 'please', 'music', 'eat sex'],
        ['e 7'],
        ['e 8', 'y8', 'eat eat', 'eat 8', '8 eat', 'e ate'],
        ['f 1', "Ask 1", "At 1:00"],
        ['f 2', "Afternoon", "At 2:00", "Up to", "After 2"],
        ['f 3', "Got 3", "At 3:00"],
        ['f 4', "At 4:00"],
        ['f 5', "Define, At 5:00"],
        ['f 6', "At 6:00"],
        ['f 7', "At 7:00"],
        ['f 8', "At 8:00"],
        ['g 1', "31"],
        ['g 2', "32"],
        ['g 3', "33"],
        ['g 4', "34"],
        ['g 5', "35"],
        ['g 6', "36", "Music"],
        ['g 7', "37"],
        ['g 8', "38", "GH"],
        ['h 1', "Page 1", "Each 1", "age 1"],
        ['h 2', "Page 2", "Each 2", "age 2"],
        ['h 3', "Page 3", "Each 3", "age 3"],
        ['h 4', "Page 4", "Each 4", "age 4"],
        ['h 5', "Page 5", "Each 5", "age 5"],
        ['h 6', "Page 6", "Each 6", "age 6"],
        ['h 7', "Page 7", "Each 7", "age 7"],
        ['h 8', "Page 8", "Each 8", "age 8"]]


def parse_move(input_st):
    """ Parses Alexa input into a chess readable notation.
    As a tuple (<algebraic notation>, <uci notation>) """

    piece_words = ['rook', 'bishop', 'king', 'queen', 'knight', 'horse', 'pawn', 'night']
    redo_words = ['redo', 'undo', 'do over', 'back', 'return']
    end_words = ['end', 'exit', 'stop', 'yamete']
    ff_words = ['ff', 'forfeit', 'admit defeat', 'surrender', 'give up']
    draw_words = ['draw', 'stalemate', 'tie']

    edited_st = input_st.strip().lower().strip().replace('.', '')
    if contains(redo_words, edited_st):
        return ('redo', None)
    elif contains(end_words, edited_st):
        return ('end', None)
    elif contains(ff_words, edited_st):
        return ('forfeit', None)
    elif contains(draw_words, edited_st):
        return ('draw', None)

    fixed_st = fix_string(input_st.replace('.', ''))

    # Get the piece from the string.
    listed_words = [x.strip().lower() for x in fixed_st.split(' ')]

    # Initializing algebraic and uci moves.
    alg_move = ""
    uci_move = None

    # Avoid any promotion pieces
    if 'promote' in listed_words:
        input_words = listed_words[:listed_words.index('promote')]
    elif 'promotion' in listed_words:
        input_words = listed_words[:listed_words.index('promotion')]
    else:
        input_words = listed_words[:]

    sim_words = []
    sims = []
    for word in input_words:
        w, s = get_most_similar_word(piece_words, word)
        sim_words.append(w)
        sims.append(s)

    piece_index = sims.index(max(sims))
    piece = sim_words[piece_index]

    if not is_coord(input_words[piece_index]):
        if piece == 'rook':
            alg_move += 'R'
        elif piece == 'knight' or piece == 'horse' or piece == 'night':
            alg_move += 'N'
        elif piece == 'bishop':
            alg_move += 'B'
        elif piece == 'king':
            alg_move += 'K'
        elif piece == 'queen':
            alg_move += 'Q'

    # Get the coordinates of the string.
    # Can be either algebraic or uci notation if there is a from/at or to.
    no_space_st = fixed_st.replace(' ', '').strip().lower()

    if 'to' in no_space_st:
        if 'at' in no_space_st:
            initial = get_coord(no_space_st, no_space_st.index('at'))
        elif 'from' in no_space_st:
            initial = get_coord(no_space_st, no_space_st.index('from'))
        else:
            initial = ''
        final = get_coord(no_space_st, no_space_st.index('to'))
    elif count_coords(no_space_st) == 2:
        initial = get_coord(no_space_st)
        final = get_coord(no_space_st, no_space_st.index(initial) + 1)
    else:  # count_coords(no_space_st) == 1 or too many:
        initial = ''
        final = get_coord(no_space_st)

    # Checks for algebraic vs uci notation.
    if initial != '':
        uci_move = initial + final
    alg_move += final

    # Check to see if the user wanted promoted.
    if 'promote' in listed_words or 'promotion' in listed_words:
        # Get the piece from the string.
        if 'promote' in listed_words:
            input_words = listed_words[listed_words.index('promote'):]
        elif 'promotion' in listed_words:
            input_words = listed_words[listed_words.index('promotion'):]

        sim_words = []
        sims = []
        for word in input_words:
            w, s = get_most_similar_word(piece_words, word)
            sim_words.append(w)
            sims.append(s)

        piece = sim_words[sims.index(max(sims))]

        # Begin determining what kind of move it is, a move, a castle, and promotion.
        promote_piece = ''

        if piece == 'rook':
            promote_piece += 'R'
        elif piece == 'bishop':
            promote_piece += 'B'
        elif piece == 'king':
            promote_piece += 'K'
        elif piece == 'queen':
            promote_piece += 'Q'

        alg_move = final + '=' + promote_piece

    # Check to see if the user wanted to castle.
    castle_word, castle_sim = get_most_similar_word(input_words, 'castle', 0.8)

    if castle_sim >= max(sims) or castle_word is not None:
        alg_move = "O-O"
        king_word, king_sim = get_most_similar_word(input_words, 'king')
        queen_word, queen_sim = get_most_similar_word(input_words, 'queen')
        if king_sim < queen_sim:
            alg_move += "-O"

    return (alg_move, uci_move)


def fix_string(st):
    """ Fixes any similar occurences of coordinates. """
    i = 0
    new_st = st.lower()
    for square_variants in common_variants:
        for variant in square_variants:
            if variant.lower().strip() in st.strip().lower():
                new_st = new_st.replace(variant.lower().strip(), num_to_square(i))
        i += 1
    return new_st


def num_to_square(n):
    """ Return the square number of a given integer from [0,63]. """
    rank = n % 8
    file = n // 8
    return 'abcdefgh'[file] + str(rank + 1)


def is_coord(st):
    """ Determines if a word is a coordinate. """
    return len(st) == 2 and st[0].lower() in 'abcdefgh' and st[1] in '12345678'


def get_most_similar_word(words, target, threshold=0.0):
    """ Get the most similar word to target in a list of words. """
    closest_word = ''
    curr_sim = -1.0

    for word in words:
        sim = similarity(word, target)
        if sim > curr_sim and sim > threshold:
            closest_word = word
            curr_sim = sim

    if curr_sim == -1.0:
        return (None, 0)
    return (closest_word, curr_sim)


def count_coords(st):
    """ Returns the number of occuring coordinate. """
    count = 0
    i = 0
    while i < len(st) - 1:
        if st[i].lower() in 'abcdefgh' and st[i + 1] in '12345678':
            count += 1
            i += 2
        else:
            i += 1
    return count


def get_coord(st, start=0):
    """ Returns the first occuring coordinate. """
    for i in range(start, len(st) - 1):
        if st[i].lower() in 'abcdefgh' and st[i + 1] in '12345678':
            return st[i:i + 2]
    return ''


def coord_to_int(coord):
    """ Coordinate to integer. """
    return (ord(coord[0]) - 96) + \
           (8 - int(coord[1])) * 8


def similarity(st1, st2):
    """ Return the similarity of two strings as a ratio. """
    # (lensum - ldist) / lensum
    len_sum = len(st1) + len(st2)

    if len_sum > 0:
        return (len_sum - levenshtein(st1, st2)) / len_sum
    else:
        return len_sum - levenshtein(st1, st2)


def levenshtein(seq1, seq2):
    """ Get the levenshtein distance between two strings. """

    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros((size_x, size_y))
    for x in range(size_x):
        matrix[x, 0] = x
    for y in range(size_y):
        matrix[0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x - 1] == seq2[y - 1]:
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,
                    matrix[x - 1, y - 1],
                    matrix[x, y - 1] + 1
                )
            else:
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,
                    matrix[x - 1, y - 1] + 1,
                    matrix[x, y - 1] + 1
                )
    return matrix[size_x - 1, size_y - 1]


def contains(words, st):
    """ Returns if any of the words are in the string. """
    for word in words:
        if word in st:
            return True
    return False


if __name__ == '__main__':

    inputs = [
              # 'pawn to e4',
              # 'rook from g6 to h7',
              # 'robot to a2', 'ronald e4', 'move queen to e4',
              # 'bean at h7 to A1', 'ring TO B6 at E7',
              # 'kling E6 E7',
              # 'bishop to C3 from c8', 'bishow c3 c8', 'Fishing a1 a2',
              # 'Castle on queen side',
              # 'casetLA ON KING SIDE',
              # 'KING FROM E6 TO E7 CASTLE'
              # 'Pawn to e7 promote to queen', 'e4 e6 promotion rook', 'e8 promote bean',
              'E 6.', 'd4.',
              'Night to g5', 'horse at e6 go to g5', 'redo that move', 'undo the move', 'end the game', 'game exit'
              'i give up', 'take back one', 'i surrender', 'admit defeat', 'offer draw'
              ]

    for inp in inputs:
        print(inp, parse_move(inp))
