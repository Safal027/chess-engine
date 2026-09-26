from board import *


board_for_moves = chess.Board()


def set_up_piece_selection_data(sqr_pos_data):
    global selected_piece, current_position, clicked, target_sqr, turn_step

    pos = pygame.mouse.get_pos()
    mouse_pressed_down = pygame.mouse.get_pressed()[0]
    to_move_trigger = False

    if mouse_pressed_down == True and clicked == False:
        clicked = True

        if selected_piece is None:
            if turn_step % 2 != 0:
                for piece_name, sqr in white_pieces_sqr_mapping.items():
                    if white_pieces_objs[piece_name].obtain_rect().collidepoint(pos):
                        selected_piece = piece_name
                        current_position = sqr
                        break

            else:
                for piece_name, sqr in black_pieces_sqr_mapping.items():
                    if black_pieces_objs[piece_name].obtain_rect().collidepoint(pos):
                        selected_piece = piece_name
                        current_position = sqr
                        break

        else:
            for chess_coord, rect in sqr_pos_data.items():
                if rect.collidepoint(pos):
                    target_sqr = chess_coord
                    to_move_trigger = True
                    break

    if mouse_pressed_down == False:
        clicked = False

    return pos, to_move_trigger


def translate_move():
    translated_move = None
    if current_position is not None and target_sqr is not None:
        translated_move = current_position+target_sqr
        print(translated_move)
    return translated_move


def get_legal_moves():
    global turn_step, current_position

    if turn_step % 2 != 0:
        board_for_moves.turn = chess.WHITE
    else:
        board_for_moves.turn = chess.BLACK

    legal_moves = []

    if current_position is None:
        return legal_moves

    selected_sqr = chess.parse_square(current_position)

    for move in board_for_moves.legal_moves:
        if move.from_square == selected_sqr:
            legal_moves.append(move.uci())

    print(legal_moves)

    return legal_moves


def move_piece(translated_move: str, to_move_trigger: bool, legal_moves: list):
    if to_move_trigger:
        global selected_piece, current_position, target_sqr, turn_step

        if selected_piece and current_position and target_sqr:
            print("outside is working")
            if translated_move in legal_moves:
                print("inside is working")
                if selected_piece[:-2] == "w":
                    white_pieces_sqr_mapping[selected_piece] = target_sqr
                else:
                    black_pieces_sqr_mapping[selected_piece] = target_sqr

                try:
                    chess_move = chess.Move.from_uci(translated_move)
                    board_for_moves.push(chess_move)
                except Exception:
                    pass

                turn_step += 1
                print("Legal move")
            else:
                print("Not a legal move")

            selected_piece = None
            current_position = None
            target_sqr = None


def capture_piece():
    global turn_step, white_pieces_sqr_mapping, black_pieces_sqr_mapping, white_pieces_names, black_pieces_names

    capture_white = False
    capture_black = False

    if board_for_moves.turn == chess.WHITE:
        prev_turn = "black"
    else:
        prev_turn = "white"

    if prev_turn == "black":
        for white_piece_name, sqr in white_pieces_sqr_mapping.items():
            if sqr in black_pieces_sqr_mapping.values():
                captured_piece = white_piece_name
                capture_white = True

    else:
        for black_piece_name, sqr in black_pieces_sqr_mapping.items():
            if sqr in white_pieces_sqr_mapping.values():
                captured_piece = black_piece_name
                capture_black = True

    if capture_white == True:
        white_pieces_names.remove(captured_piece)
        white_pieces_sqr_mapping.pop(captured_piece)
    elif capture_black == True:
        black_pieces_names.remove(captured_piece)
        black_pieces_sqr_mapping.pop(captured_piece)
