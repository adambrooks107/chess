import chess
import pygame
import io

from svglib.svglib import svg2rlg

class Piece(pygame.sprite.Sprite):
    def __init__(self, square):
        super().__init__()
        self.square = square
    def load_svg(self, svg_string):
        svg_io = io.StringIO(svg_string)
        drawing = svg2rlg(svg_io)
        strng = drawing.asString("png")
        byte_io = io.BytesIO(strng)
        return pygame.image.load(byte_io)

class WhiteKnight(Piece):
    def __init__(self, square):
        super().__init__(square)
        self.image = pygame.image.load("./assets/white_knight.png")
        self.image = pygame.transform.scale(self.image, (92, 92))
        self.rect = self.image.get_rect()
        self.rect.x = square.rect.x
        self.rect.y = square.rect.y

class BlackKnight(Piece):
    def __init__(self, square):
        super().__init__(square)
        self.image = pygame.image.load("./assets/black_knight.png")
        self.image = pygame.transform.scale(self.image, (92, 92))
        self.rect = self.image.get_rect()
        self.rect.x = square.rect.x
        self.rect.y = square.rect.y

class BlackPawn(Piece):
    def __init__(self, square):
        super().__init__(square)
        self.image = pygame.image.load("./assets/black_pawn.png")
        self.image = pygame.transform.scale(self.image, (92, 92))
        self.rect = self.image.get_rect()
        self.rect.x = square.rect.x
        self.rect.y = square.rect.y

class WhitePawn(Piece):
    def __init__(self, square):
        super().__init__(square)
        self.image = pygame.image.load("./assets/white_pawn.png")
        self.image = pygame.transform.scale(self.image, (92, 92))
        self.rect = self.image.get_rect()
        self.rect.x = square.rect.x
        self.rect.y = square.rect.y

class BlackQueen(Piece):
    def __init__(self, square):
        super().__init__(square)
        self.image = pygame.image.load("./assets/black_queen.png")
        self.image = pygame.transform.scale(self.image, (92, 92))
        self.rect = self.image.get_rect()
        self.rect.x = square.rect.x
        self.rect.y = square.rect.y

class WhiteQueen(Piece):
    def __init__(self, square):
        super().__init__(square)
        self.image = pygame.image.load("./assets/white_queen.png")
        self.image = pygame.transform.scale(self.image, (92, 92))
        self.rect = self.image.get_rect()
        self.rect.x = square.rect.x
        self.rect.y = square.rect.y

class BlackKing(Piece):
    def __init__(self, square):
        super().__init__(square)
        self.image = pygame.image.load("./assets/black_king.png")
        self.image = pygame.transform.scale(self.image, (92, 92))
        self.rect = self.image.get_rect()
        self.rect.x = square.rect.x
        self.rect.y = square.rect.y

class WhiteKing(Piece):
    def __init__(self, square):
        super().__init__(square)
        self.image = pygame.image.load("./assets/white_king.png")
        self.image = pygame.transform.scale(self.image, (92, 92))
        self.rect = self.image.get_rect()
        self.rect.x = square.rect.x
        self.rect.y = square.rect.y

class BlackBishop(Piece):
    def __init__(self, square):
        super().__init__(square)
        self.image = pygame.image.load("./assets/black_bishop.png")
        self.image = pygame.transform.scale(self.image, (92, 92))
        self.rect = self.image.get_rect()
        self.rect.x = square.rect.x
        self.rect.y = square.rect.y

class WhiteBishop(Piece):
    def __init__(self, square):
        super().__init__(square)
        self.image = pygame.image.load("./assets/white_bishop.png")
        self.image = pygame.transform.scale(self.image, (92, 92))
        self.rect = self.image.get_rect()
        self.rect.x = square.rect.x
        self.rect.y = square.rect.y

class BlackRook(Piece):
    def __init__(self, square):
        super().__init__(square)
        self.image = pygame.image.load("./assets/black_rook.png")
        self.image = pygame.transform.scale(self.image, (92, 92))
        self.rect = self.image.get_rect()
        self.rect.x = square.rect.x
        self.rect.y = square.rect.y

class WhiteRook(Piece):
    def __init__(self, square):
        super().__init__(square)
        self.image = pygame.image.load("./assets/white_rook.png")
        self.image = pygame.transform.scale(self.image, (92, 92))
        self.rect = self.image.get_rect()
        self.rect.x = square.rect.x
        self.rect.y = square.rect.y