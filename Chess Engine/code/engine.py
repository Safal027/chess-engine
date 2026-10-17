from moves import *


engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_FILE_PATH)


def set_lvl(level):
    global bot_blunder_percentage

    skill_lvl_mapping = {1: 0, 2: 0, 3: 1, 4: 2,
                         5: 3, 6: 4, 7: 5, 8: 6, 9: 7, 10: 8}
    depth_mapping = {1: 1, 2: 1, 3: 1, 4: 2,
                     5: 2, 6: 2, 7: 3, 8: 3, 9: 3, 10: 3, 11: 4, 12: 4, 13: 4, 14: 4, 15: 5, 16: 5, 17: 5, 18: 5, 19: 6, 20: 6, 21: 6, 22: 6, 23: 7, 24: 7, 25: 7}
    if level <= 10:
        limit_strength = True
        elo = None
        skl_lvl = skill_lvl_mapping[level]
        depth = depth_mapping[level]
        bot_blunder_percentage = -0.05*level+0.55

    elif level > 10:
        limit_strength = True
        elo = round(131.43*level-95.714)
        skl_lvl = None
        depth = depth_mapping[level]

    try:
        if elo is None:
            engine.configure({
                "UCI_LimitStrength": limit_strength,
                "Skill Level": skl_lvl,
            })

        elif elo is not None:
            engine.configure({
                "UCI_LimitStrength": limit_strength,
                "UCI_Elo": elo
            })
    except:
        pass

    print(level)
    print(elo)
    print(bot_blunder_percentage)

    return depth


def get_bot_move(max_depth):
    global bot_blunder_percentage

    limit = chess.engine.Limit(depth=max_depth)

    if random.random() < bot_blunder_percentage:
        bot_move = random.choice(list(board_for_moves.legal_moves)).uci()
        print("random")
    else:
        bot_move = engine.play(board_for_moves, limit).move.uci()
        print("calculated")

    return bot_move


def set_up_bot_move_data(move: str):

    current_position = move[:2]

    for white_piece_name, sqr in white_pieces_sqr_mapping.items():
        if sqr == current_position:
            selected_piece = white_piece_name
    for black_piece_name, sqr in black_pieces_sqr_mapping.items():
        if sqr == current_position:
            selected_piece = black_piece_name

    if len(move) == 4:
        target_sqr = move[-2:]
    else:
        target_sqr = move[-3:-1]

    return current_position, selected_piece, target_sqr
