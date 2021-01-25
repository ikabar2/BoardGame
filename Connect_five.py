

import numpy as np
import random
import pygame
import sys
import math

gray = (220,220,220)
blu =(42,126,226)
RED = (255,0,0)
YELLOW = (255,255,0)

row_size = 8
colum_size = 8

Human_player = 0
AI = 1

EMPTY = 0
human_piece = 1
AI_PIECE = 2

WINDOW_LENGTH = 5

def create_board():
    board = np.zeros((row_size,colum_size))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[row_size-1][col] == 0

def get_next_open_row(board, col):
    for r in range(row_size):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(colum_size-4):
        for r in range(row_size):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece and board[r][c+4] == piece:
                return True

    # Check vertical locations for win
    for c in range(colum_size):
        for r in range(row_size-4):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece and board[r+4][c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(colum_size-4):
        for r in range(row_size-4):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece and board[r+4][c+4] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(colum_size-4):
        for r in range(4, row_size):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece and board[r-4][c+4] == piece:
                return True




def heuristic_function(window, piece):
    score = 0
    opp_piece = human_piece
    if piece == human_piece:
        opp_piece = AI_PIECE

    if window.count(piece) == 5:
        score += 1000
    elif window.count(piece) == 4 and window.count(EMPTY) == 1:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 2:
        score += 50

    if window.count(opp_piece) == 2 and window.count(EMPTY) == 1:
        score -= 90

    return score






def score_position(board, piece):
    score = 0

    ## Score center column
    center_array = [int(i) for i in list(board[:, colum_size//2])]
    center_count = center_array.count(piece)
    score += center_count * 4

    ## Score Horizontal
    for r in range(row_size):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(colum_size-4):
            window = row_array[c:c+WINDOW_LENGTH]
            score += heuristic_function(window, piece)

    ## Score Vertical
    for c in range(colum_size):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(row_size-4):
            window = col_array[r:r+WINDOW_LENGTH]
            score += heuristic_function(window, piece)

    ## Score posiive sloped diagonal
    for r in range(row_size-4):
        for c in range(colum_size-4):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += heuristic_function(window, piece)

    for r in range(row_size-4):
        for c in range(colum_size-4):
            window = [board[r+4-i][c+i] for i in range(WINDOW_LENGTH)]
            score += heuristic_function(window, piece)

    return score

def is_terminal_node(board):
    return winning_move(board, human_piece) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, human_piece):
                return (None, -10000000000000)
            else: # Game is over, no more valid moves
                return (None, 0)
        else: # Depth is zero
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else: # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, human_piece)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value



def get_valid_locations(board):
    valid_locations = []
    for col in range(colum_size):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def best_move(board, piece):

    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col






def draw_board(board):
    for c in range(colum_size):
        for r in range(row_size):
            pygame.draw.rect(screen, gray, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, blu, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
    for c in range(colum_size):
        for r in range(row_size):        
            if board[r][c] == human_piece:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == AI_PIECE: 
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()

board = create_board()
print_board(board)
game_over = False

pygame.init()

SQUARESIZE = 70

width = colum_size * SQUARESIZE
height = (row_size+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

turn = random.randint(Human_player, AI)




while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, blu, (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == Human_player:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, blu, (0,0, width, SQUARESIZE))
            #print(event.pos)
            # Ask for Player 1 Input
            if turn == Human_player:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, human_piece)

                    if winning_move(board, human_piece):
                        label = myfont.render("Player 1 wins!!", 1, RED)
                        screen.blit(label, (40,10))
                        game_over = True

                    turn += 1
                    turn = turn % 2

                    print_board(board)
                    draw_board(board)


    # # Ask for Player 2 Input
    if turn == AI and not game_over:                

        #col = random.randint(0, colum_size-1)
        #col = best_move(board, AI_PIECE)
        col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

        if is_valid_location(board, col):
            #pygame.time.wait(500)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)

            if winning_move(board, AI_PIECE):
                label = myfont.render("The AI has won!", 1, YELLOW)
                screen.blit(label, (40,10))
                game_over = True

            print_board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2

    if game_over:
                pygame.time.wait(3000)
