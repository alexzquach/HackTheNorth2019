import chess
import tkinter

def get_coord_to_int(coord):
    """coordinate to integer"""
    return (ord(coord[0]) - 96) + (8 - int(coord[1])) * 8
def output_board(board_st):
    """"""
    lines = board_st.split('\n')
    for i in range(len(lines)):
        print(abs(8 - i), lines[i].strip())
    print("  a b c d e f g h")

