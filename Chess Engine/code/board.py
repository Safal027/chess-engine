from buttons import *


class ChessBoard:

    def draw_board(self, surface):

        for row in range(8):
            for col in range(8):
                if (row+col) % 2 == 0:
                    color = LIGHT_COLOR
                else:
                    color = DARK_COLOR

                rect_x = board_start_x+(col*sqr_size)
                rect_y = board_start_y+(row*sqr_size)

                pygame.draw.rect(
                    surface, color, (rect_x, rect_y, sqr_size, sqr_size))

    def get_sqr_pos_data_for_white(self):
        self.square_positions = {}

        for row in range(8):
            for col in range(8):
                rect_x = board_start_x+(col*sqr_size)
                rect_y = board_start_y+(row*sqr_size)

                chess_coord = f"{files[col]}{8 - row}"

                self.square_positions[chess_coord] = pygame.Rect(
                    rect_x, rect_y, sqr_size, sqr_size)

        return self.square_positions

    def get_sqr_pos_data_for_black(self):
        self.square_positions = {}

        for row in range(8):
            for col in range(8):
                rect_x = board_start_x + (col * sqr_size)
                rect_y = board_start_y + (row * sqr_size)
                chess_coord = f"{files[7 - col]}{row + 1}"
                self.square_positions[chess_coord] = pygame.Rect(
                    rect_x, rect_y, sqr_size, sqr_size
                )

        return self.square_positions


class Piece:

    def load_piece_data(self, img_path, x_rect: float, y_rect: float):
        self.piece_img = pygame.image.load(img_path).convert_alpha()
        self.refined_piece_data = get_refined_image_data_for_pieces(
            self.piece_img, 0.1116, 0.1116, x_rect, y_rect)
        self.piece_img = self.refined_piece_data[0]
        self.piece_rect = self.refined_piece_data[1]

    def draw(self):
        screen.blit(self.piece_img, self.piece_rect)

    def obtain_rect(self):
        return self.piece_rect


def load_pieces_position(user_play_as):
    global white_pieces_objs, black_pieces_objs

    if user_play_as == "White":
        sqr_pos_data = board.get_sqr_pos_data_for_white()
    elif user_play_as == "Black":
        sqr_pos_data = board.get_sqr_pos_data_for_black()

    for white_piece_name, sqr in white_pieces_sqr_mapping.items():
        white_pieces_objs[white_piece_name].obtain_rect(
        ).center = sqr_pos_data[sqr].center

    for black_piece_name, sqr in black_pieces_sqr_mapping.items():
        black_pieces_objs[black_piece_name].obtain_rect(
        ).center = sqr_pos_data[sqr].center

    return sqr_pos_data


board = ChessBoard()

for white_piece_name in white_pieces_names:
    in_str = white_piece_name
    white_piece = Piece()
    white_piece.load_piece_data(
        ASSETS_DIR/f"images/pieces/{in_str[:-1]}.png", 0, 0)
    white_pieces_objs[white_piece_name] = white_piece

for black_piece_name in black_pieces_names:
    black_piece = Piece()
    black_piece.load_piece_data(
        ASSETS_DIR/f"images/pieces/{black_piece_name[:-1]}.png", 0, 0)
    black_pieces_objs[black_piece_name] = black_piece
