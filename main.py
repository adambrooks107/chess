import io
import chess
import chess.svg
import chess.engine
import pygame
from pygame import gfxdraw
from Square import Square
from Pieces import *
import math
import cv2
import numpy
import asyncio

from svglib.svglib import svg2rlg

#-------------------------------------------------------------------------------- START FUNCTIONS --------------------------------------------------------------------------------#
# draw the border first, followed by the squares, followed by the pieces
def refresh_screen():
    screen.blit(border, (0, 0))
    square_list.draw(screen)
    piece_list.draw(screen)

# helper to draw an antialiased empty circle. Credit: https://stackoverflow.com/questions/64816341/how-do-you-draw-an-antialiased-circular-line-of-a-certain-thickness-how-to-set
def drawAACircle(surf, color, center, radius, width):
    circle_image = numpy.zeros((radius*2+4, radius*2+4, 4), dtype = numpy.uint8)
    circle_image = cv2.circle(circle_image, (radius+2, radius+2), radius-width//2, (*color, 255), width, lineType=cv2.LINE_AA)  
    circle_surface = pygame.image.frombuffer(circle_image.flatten(), (radius*2+4, radius*2+4), 'RGBA')
    circle_surface.set_alpha(100)
    surf.blit(circle_surface, circle_surface.get_rect(center = center))

# once legal_dests list has been filled this will draw circles for all squares
# that are legal destinations for the selected piece. If the destination square
# has a piece then draw an empty circle around the piece to signify capture.
def highlight_legal_moves(legal_dests):
    for s in square_list:
        if s.name in legal_dests:
            s.unhighlight_square()
            if s.piece is not None:
                drawAACircle(s.image, (0,0,0), (45,45), 42, 5)
            else:
                gfxdraw.aacircle(s.image, 45, 45, 20, (0,0,0,100))
                gfxdraw.filled_circle(s.image, 45, 45, 20, (0,0,0,100))
        elif not s.just_moved:
            s.unhighlight_square()

# highlights the move that was just played
def highlight_move(move):
    for sq in square_list:
        if sq.name in str(move):
            sq.highlight_square_moved()
        else:
            sq.just_moved = False
            sq.unhighlight_square()

# perform the move and call highlight_move
def make_move(move):
    highlight_move(move)
    board.push(move)

# highlight the king square red if in check
def highlight_checks():
    if board.is_check():
        if board.turn:
            [sq.highlight_square() for sq in square_list if sq.name == chess.square_name(board.king(chess.WHITE))]
        else:
            [sq.highlight_square() for sq in square_list if sq.name == chess.square_name(board.king(chess.BLACK))]

# helper to calculate the polygon points for arrow drawing. Credit: https://stackoverflow.com/questions/43527894/drawing-arrowheads-which-follow-the-direction-of-the-line-in-pygame
def create_arrow(start, end):
    rotation = math.degrees(math.atan2(start[1]-end[1], end[0]-start[0]))+90
    # move the end point 30 pixels back
    end = point_between(start, end, 30)
    # must be greater than 1 square away
    if end == -1:
        return []
    # move the start point 30 pixels forward
    start = point_between(end, start, 30)

    bottom_left = (start[0]+10*math.sin(math.radians(rotation-120)), start[1]+10*math.cos(math.radians(rotation-120)))
    bottom_right = (start[0]+10*math.sin(math.radians(rotation+120)), start[1]+10*math.cos(math.radians(rotation+120)))
    top_right = (end[0]+10*math.sin(math.radians(rotation+120)), end[1]+10*math.cos(math.radians(rotation+120)))
    triangle_right = (end[0]+30*math.sin(math.radians(rotation+120)), end[1]+30*math.cos(math.radians(rotation+120)))
    triangle_top = (end[0]+30*math.sin(math.radians(rotation)), end[1]+30*math.cos(math.radians(rotation)))
    triangle_left = (end[0]+30*math.sin(math.radians(rotation-120)), end[1]+30*math.cos(math.radians(rotation-120)))
    top_left = (end[0]+10*math.sin(math.radians(rotation-120)), end[1]+10*math.cos(math.radians(rotation-120)))

    return (bottom_left, bottom_right, top_right, top_left), (triangle_right, triangle_top, triangle_left)

# create an arrow when given a chess.Move object
def create_arrow_from_move(move):
    move_str = str(move)
    from_pos = move_str[:2]
    to_pos = move_str[2:4]
    for s in square_list:
        if s.name == from_pos:
            from_square = s
        if s.name == to_pos:
            to_square = s
    return create_arrow(from_square.rect.center, to_square.rect.center)

# create_arrow didn't draw the point of the arrow to the middle of the square. This let's me mathematically 
# find a point on the same line to make the arrow shorter.
def point_between(start, end, distance):
    d = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
    dt = d - distance
    if d != 0:
        t = dt / d
        return ((1 - t)*start[0] + t*end[0]), ((1 - t)*start[1] + t*end[1])
    else:
        return -1

# use chess.engine.analyse to create a list of arrows for the best moves
async def analyse_board(engine):
    result = await engine.analyse(board, chess.engine.Limit(time=0.2), multipv=4)
    analysis_arrow_list = []
    for info in result:
        line = info.get("pv")
        score = info.get("score")
        arw = create_arrow_from_move(line[0])
        if arw:
            analysis_arrow_list.append(arw)
    
    return analysis_arrow_list

# finds where each piece is on the current board and creates them
def createPieces():
    piece_list = pygame.sprite.Group()

    for square in square_names:
        piece_at = str(board.piece_at(chess.parse_square(square)))
        square_sprite = next((s for s in square_list if s.name == square), None)

        if piece_at == 'p':
            piece = BlackPawn(square_sprite)
            square_sprite.piece = piece
        elif piece_at == 'P':
            piece = WhitePawn(square_sprite)
            square_sprite.piece = piece
        elif piece_at == 'n':
            piece = BlackKnight(square_sprite)
            square_sprite.piece = piece
        elif piece_at == 'N':
            piece = WhiteKnight(square_sprite)
            square_sprite.piece = piece
        elif piece_at == 'b':
            piece = BlackBishop(square_sprite)
            square_sprite.piece = piece
        elif piece_at == 'B':
            piece = WhiteBishop(square_sprite)
            square_sprite.piece = piece
        elif piece_at == 'r':
            piece = BlackRook(square_sprite)
            square_sprite.piece = piece
        elif piece_at == 'R':
            piece = WhiteRook(square_sprite)
            square_sprite.piece = piece
        elif piece_at == 'q':
            piece = BlackQueen(square_sprite)
            square_sprite.piece = piece
        elif piece_at == 'Q':
            piece = WhiteQueen(square_sprite)
            square_sprite.piece = piece
        elif piece_at == 'k':
            piece = BlackKing(square_sprite)
            square_sprite.piece = piece
        elif piece_at == 'K':
            piece = WhiteKing(square_sprite)
            square_sprite.piece = piece
        else:
            piece = ""
            square_sprite.piece = None
        
        if piece:
            piece_list.add(piece)
    return piece_list

#-------------------------------------------------------------------------------- END FUNCTIONS --------------------------------------------------------------------------------#

board = chess.Board()
(width, height) = (800, 800)
background_colour = (255, 255, 255)
arrow_colour = (255, 255, 49)
analysis_arrow_colour_r = 0
analysis_arrow_colour_g = 204
analysis_arrow_colour_b = 0

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Chess')
screen.fill(background_colour)

square_list = pygame.sprite.Group()
square_names = ("a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8", "b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8", "c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "d1", "d2", "d3", "d4", "d5", "d6", "d7", "d8", "e1", "e2", "e3", "e4", "e5", "e6", "e7", "e8", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "g1", "g2", "g3", "g4", "g5", "g6", "g7", "g8", "h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8")

border = pygame.image.load("./assets/border.png")

screen.blit(border, (0, 0))

square_length = 92
border_width = 30

xpos = border_width
ypos = border_width + square_length*7
count = 1
odd_even = 0

# create square sprites and populate square_list
for square in square_names:
    if count % 2 == odd_even:
        sq = Square(square, "#189AB4", square_length, square_length, xpos, ypos, None)
    else:
        sq = Square(square, "#add8e6", square_length, square_length, xpos, ypos, None)
    square_list.add(sq)
    if count % 8 == 0:
        xpos += square_length
        ypos = border_width + square_length*7
        count = 1
        odd_even = not odd_even
    else:
        ypos -= square_length
        count += 1

square_list.draw(screen)

piece_list = createPieces()

pygame.display.flip()

async def main() -> None:
    transport, stockfish = await chess.engine.popen_uci("C:/Users/adamb/projects/chess/stockfish/stockfish_13_win_x64_bmi2.exe")
    run = True
    piece_sprite = ""
    piece_dragging = False
    start_arrow = 0
    end_arrow = 0
    arrow_list = []
    analysis_arrow_list = []
    global piece_list
    legal_moves = []
    legal_dests = []
    all_moves = []
    clicking_to_move = 0
    while run:
        for event in pygame.event.get():
            # if quit
            if event.type == pygame.QUIT:
                run = False
            # if not board.turn:
            #     make_move(result.move)
            #     piece_list = createPieces()
            # left and right arrows move through the move list
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if board.move_stack:
                        mv = board.pop()
                        all_moves.append(mv)
                        if board.move_stack:
                            highlight_move(board.peek())
                        else:
                            highlight_move("")
                        piece_list = createPieces()
                        analysis_arrow_list = await analyse_board(stockfish)
                if event.key == pygame.K_RIGHT:
                    if all_moves:
                        last_move = all_moves[len(all_moves)-1]
                        board.push(last_move)
                        all_moves.remove(last_move)
                        highlight_move(last_move)
                        piece_list = createPieces()
                        analysis_arrow_list = await analyse_board(stockfish)
            # check if checkmate
            if board.is_checkmate():
                green_surface = pygame.Surface((width, height))
                green_surface.fill((0, 255, 0))
                green_surface.set_alpha(100)
                refresh_screen()
                screen.blit(green_surface, (0, 0))
                pygame.display.flip()
                continue
            elif event.type == pygame.MOUSEWHEEL:
                continue
            # mouse pressed
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for s in square_list:
                    if s.check_collision(mouse_pos):
                        # left mouse clicked - remove all red highlights and arrows
                        if event.button == 1:
                            [sq.unhighlight_square() for sq in square_list]
                            arrow_list= []
                        # right click - potentially starting to draw an arrow
                        if event.button == 3:
                            start_arrow = s
                        # clicked a piece
                        if s.piece is not None:
                            # assign the piece to a variable to be used when dragging the piece
                            piece_sprite = s.piece
                            if piece_sprite is not None:
                                if event.button == 1:
                                    # ensure the selected piece is drawn on top of others
                                    piece_list.remove(piece_sprite)
                                    piece_list.add(piece_sprite)
                                    piece_dragging = True
                                    # check if NOT moving a piece so we don't call this code when capturing
                                    clicking_to_move = s.can_make_move(legal_dests)
                                    if clicking_to_move == -1:
                                        legal_moves, legal_dests = s.find_legal_moves(board)
                                        highlight_legal_moves(legal_dests)
                                    # highlight if we touch a piece
                                    s.touched_piece()
            # mouse unpressed
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                for s in square_list:
                    if s.check_collision(mouse_pos):
                        # right click
                        if event.button == 3:
                            if start_arrow != 0:
                                end_arrow = s
                                # right click dragged from one square to another. Create an arrow and add it to the list of arrows.
                                if start_arrow.name != end_arrow.name:
                                    arw = create_arrow(start_arrow.rect.center, end_arrow.rect.center)
                                    if arw:
                                        arrow_list.append(arw)
                                # right clicked on one square. Highlight it red.
                                else:
                                    s.highlight_square()
                                start_arrow = 0
                                end_arrow = 0
                            else:
                                s.highlight_square()
                        # left click
                        if event.button == 1:
                            # reset the cursor
                            if s.piece is None:
                                pygame.mouse.set_cursor(0)
                            piece_dragging = False
                            if legal_moves:
                                # check if moving a piece
                                move_index = s.can_make_move(legal_dests)
                                if move_index >= 0:
                                    move = legal_moves[move_index]
                                    # perform the move
                                    make_move(move)
                                    # analyse the best moves and create arrows
                                    analysis_arrow_list = await analyse_board(stockfish)
                                    all_moves = []
                                    legal_moves, legal_dests = [], []
                                    
                            piece_list = createPieces()
            # mouse movement
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                for s in square_list:
                    if s.check_collision(mouse_pos):
                        if s.piece is not None:
                            # set mouse cursor to signify hovering over a piece
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                        elif not piece_dragging:
                            pygame.mouse.set_cursor(0)
                # if holding a piece. Move the piece with the mouse.
                if piece_dragging:
                    piece_sprite.rect.centerx = mouse_pos[0]
                    piece_sprite.rect.centery = mouse_pos[1]

            # for each event
            highlight_checks()
            refresh_screen()
            if arrow_list:
                for arrow in arrow_list:
                    gfxdraw.aapolygon(screen, arrow[0], arrow_colour)
                    gfxdraw.filled_polygon(screen, arrow[0], arrow_colour)
                    gfxdraw.aapolygon(screen, arrow[1], arrow_colour)
                    gfxdraw.filled_polygon(screen, arrow[1], arrow_colour)
            if analysis_arrow_list:
                green = analysis_arrow_colour_g
                for arrow in analysis_arrow_list:
                    gfxdraw.aapolygon(screen, arrow[0], (analysis_arrow_colour_r, green, analysis_arrow_colour_b))
                    gfxdraw.filled_polygon(screen, arrow[0], (analysis_arrow_colour_r, green, analysis_arrow_colour_b))
                    gfxdraw.aapolygon(screen, arrow[1], (analysis_arrow_colour_r, green, analysis_arrow_colour_b))
                    gfxdraw.filled_polygon(screen, arrow[1], (analysis_arrow_colour_r, green, analysis_arrow_colour_b))
                    green = green - 50
            pygame.display.flip()
    pygame.quit()
    await stockfish.quit()

if __name__ == "__main__":
    asyncio.set_event_loop_policy(chess.engine.EventLoopPolicy())
    asyncio.run(main())
    #main()