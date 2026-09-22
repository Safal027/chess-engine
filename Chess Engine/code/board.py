from buttons import *


class ChessBoard:
    def draw_board(self, surface):
        for row in range(8):
            for col in range(8):
                if (row+col) % 2 == 0:
                    color = LIGHT_COLOR
                else:
                    color = DARK_COLOR

                x = col*SQR_SIZE
                y = row*SQR_SIZE

                pygame.draw.rect(surface, color, (x, y, SQR_SIZE, SQR_SIZE))


board = ChessBoard()
