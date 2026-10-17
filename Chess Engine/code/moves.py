from board import *


board_for_moves = chess.Board()


def set_up_piece_selection_data(sqr_pos_data):
    global selected_piece, current_position, clicked, target_sqr, turn_step

    pos = pygame.mouse.get_pos()
    mouse_pressed_down = pygame.mouse.get_pressed()[0]
    to_move_trigger = False

    if to_do_promotion is not None:
        return pos, False

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


def promotion_check():
    global to_do_promotion
    if selected_piece is None or target_sqr is None or to_do_promotion is not None:
        return
    if (current_position + target_sqr + "q") in get_legal_moves():
        to_do_promotion = "white" if selected_piece[0] == "w" else "black"


def get_promotion_piece():
    global promote_to, to_do_promotion

    if to_do_promotion == "white":
        choose_wq_button.draw()
        choose_wr_button.draw()
        choose_wb_button.draw()
        choose_wn_button.draw()
        if choose_wq_button.click():
            promote_to = "q"
        if choose_wr_button.click():
            promote_to = "r"
        if choose_wb_button.click():
            promote_to = "b"
        if choose_wn_button.click():
            promote_to = "n"

    if to_do_promotion == "black":
        choose_bq_button.draw()
        choose_br_button.draw()
        choose_bb_button.draw()
        choose_bn_button.draw()
        if choose_bq_button.click():
            promote_to = "q"
        if choose_br_button.click():
            promote_to = "r"
        if choose_bb_button.click():
            promote_to = "b"
        if choose_bn_button.click():
            promote_to = "n"


def translate_move():
    global to_do_promotion, promote_to

    translated_move = None
    if current_position is not None and target_sqr is not None:
        translated_move = current_position+target_sqr
        if to_do_promotion in ("white", "black"):
            if promote_to is None:
                return None
            translated_move += promote_to
            to_do_promotion = None
            promote_to = None
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

    return legal_moves


def move_piece(translated_move: str, legal_moves: list, to_move_trigger: bool, is_bot_move: Optional[bool] = False):
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
                    move = chess.Move.from_uci(translated_move)
                    board_for_moves.push(move)
                    move_piece_sound_effect.play()
                    turn_step += 1
                except Exception:
                    pass

                if len(translated_move) == 5:
                    color = selected_piece[0]
                    piece_letter = translated_move[4]
                    objs = white_pieces_objs if color == "w" else black_pieces_objs
                    objs[selected_piece].load_piece_data(
                        ASSETS_DIR/f"images/pieces/{color}{piece_letter}.png", 0, 0)

                print("Legal move")

            else:
                print("Not a legal move")

            selected_piece = None
            current_position = None
            target_sqr = None

            print(translated_move)
            print(legal_moves)


def capture_piece():
    global white_pieces_sqr_mapping, black_pieces_sqr_mapping, white_pieces_names, black_pieces_names

    capture_white = False
    capture_black = False
    captured_piece = None

    if board_for_moves.turn == chess.WHITE:
        prev_turn = "black"
    else:
        prev_turn = "white"

    if prev_turn == "black":
        for white_piece_name, sqr in white_pieces_sqr_mapping.items():
            if sqr in black_pieces_sqr_mapping.values():
                captured_piece = white_piece_name
                capture_white = True

    elif prev_turn == "white":
        for black_piece_name, sqr in black_pieces_sqr_mapping.items():
            if sqr in white_pieces_sqr_mapping.values():
                captured_piece = black_piece_name
                capture_black = True

    if capture_white == True:
        white_pieces_names.remove(captured_piece)
        white_pieces_sqr_mapping.pop(captured_piece)
        move_piece_sound_effect.play()
    elif capture_black == True:
        black_pieces_names.remove(captured_piece)
        black_pieces_sqr_mapping.pop(captured_piece)
        move_piece_sound_effect.play()


def en_passant(translated_move, legal_moves, is_bot_move: Optional[bool] = False):
    global white_pieces_sqr_mapping, black_pieces_sqr_mapping, white_pieces_names, black_pieces_names, target_sqr

    capture_white = False
    capture_black = False
    captured_piece = None

    if board_for_moves.turn == chess.WHITE:
        prev_turn = "black"
    else:
        prev_turn = "white"

    try:
        if prev_turn == "black":
            if translated_move in legal_moves:
                if board_for_moves.is_en_passant(chess.Move.from_uci(translated_move)):
                    for black_piece_name, sqr in black_pieces_sqr_mapping.items():
                        captured_piece_sqr = target_sqr[:-1] + \
                            str(int(target_sqr[-1])-1)
                        if sqr == captured_piece_sqr:
                            captured_piece = black_piece_name
                            capture_black = True

        elif prev_turn == "white":
            if translated_move in legal_moves:
                if board_for_moves.is_en_passant(chess.Move.from_uci(translated_move)):
                    for white_piece_name, sqr in white_pieces_sqr_mapping.items():
                        captured_piece_sqr = target_sqr[:-1] + \
                            str(int(target_sqr[-1])+1)
                        if sqr == captured_piece_sqr:
                            captured_piece = white_piece_name
                            capture_white = True

        if capture_white == True:
            white_pieces_names.remove(captured_piece)
            white_pieces_sqr_mapping.pop(captured_piece)
            move_piece_sound_effect.play()
        elif capture_black == True:
            black_pieces_names.remove(captured_piece)
            black_pieces_sqr_mapping.pop(captured_piece)
            move_piece_sound_effect.play()

    except chess.InvalidMoveError:
        pass


def castling(translated_move, legal_moves, is_bot_move: Optional[bool] = False):
    global white_pieces_sqr_mapping, black_pieces_sqr_mapping

    try:
        if board_for_moves.turn == chess.WHITE:
            if translated_move in legal_moves:
                if board_for_moves.is_kingside_castling(chess.Move.from_uci(translated_move)):
                    white_pieces_sqr_mapping["wk0"] = "g1"
                    white_pieces_sqr_mapping["wr2"] = "f1"
                    move_piece_sound_effect.play()
                elif board_for_moves.is_queenside_castling(chess.Move.from_uci(translated_move)):
                    white_pieces_sqr_mapping["wk0"] = "c1"
                    white_pieces_sqr_mapping["wr1"] = "d1"
                    move_piece_sound_effect.play()

        elif board_for_moves.turn == chess.BLACK:
            if translated_move in legal_moves:
                if board_for_moves.is_kingside_castling(chess.Move.from_uci(translated_move)):
                    black_pieces_sqr_mapping["bk0"] = "g8"
                    black_pieces_sqr_mapping["br2"] = "f8"
                    move_piece_sound_effect.play()
                elif board_for_moves.is_queenside_castling(chess.Move.from_uci(translated_move)):
                    black_pieces_sqr_mapping["bk0"] = "c8"
                    black_pieces_sqr_mapping["br1"] = "d8"
                    move_piece_sound_effect.play()

    except chess.InvalidMoveError:
        pass


def check(sqr_pos_data):
    if board_for_moves.is_check():
        turn = board_for_moves.turn
        king_sqr = chess.square_name(
            board_for_moves.king(turn))
        pygame.draw.rect(screen, (255, 0, 0),
                         sqr_pos_data[king_sqr])


def result():
    outcome = board_for_moves.outcome()

    if outcome is not None:
        if outcome.winner == True:
            winner = "white"

        elif outcome.winner == False:
            winner = "black"

        else:
            winner = "draw"

    if outcome is not None:
        if outcome:
            if winner == "white":
                txt_surface = font.render("White Won!", True,
                                          (255, 255, 255), (000, 000, 000))
            elif winner == "black":
                txt_surface = font.render("Black Won!", True,
                                          (000, 000, 000), (255, 255, 255))
            elif winner == "draw":
                txt_surface = font.render(
                    "It's a Draw!", True, (255, 255, 255))
            try:
                txt_surface_rect = txt_surface.get_rect()
                txt_surface_rect.centerx = screen_rect.centerx
                txt_surface_rect.centery = screen_rect.centery
            except UnboundLocalError:
                pass
    try:
        screen.blit(txt_surface, txt_surface_rect)
    except:
        pass
