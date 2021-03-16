import chess
import pygame

class Square(pygame.sprite.Sprite):
    def __init__(self, name, fill, height, width, x, y, piece):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.colour = fill
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.name = name
        self.piece = piece
        self.just_moved = False
    
    def highlight_square(self):
        self.image.fill("#880808")

    def touched_piece(self):
        self.image.fill("#dfc98a")
    
    def unhighlight_square(self):
        if self.just_moved:
            self.image.fill("#dfc98a")
        else:
            self.image.fill(self.colour)

    def highlight_square_moved(self):
        self.image.fill("#dfc98a")
        self.just_moved = True

    def check_collision(self, mouse):
        return self.rect.collidepoint(mouse)

    def find_legal_moves(self, board):
        all_moves = list(board.legal_moves)
        legal_moves = []
        legal_dests = []
        for m in all_moves:
            if self.name == str(m)[:2]:
                legal_moves.append(m)
                legal_dests.append(str(m)[2:4])
        return legal_moves,legal_dests

    def can_make_move(self, move):
        i = 0
        for dest in move:
            if self.name == dest:
                return i
            i+=1
        return -1