import moves as ms
from engine import *


while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.VIDEORESIZE:
            pass

    screen.fill((18, 18, 18))
    screen.blit(bg_img, (0, 0))

    if current_scene == "home":
        screen.blit(logo_img, logo_rect)
        play_bot_button.draw()
        play_player_button.draw()

        if play_bot_button.click():
            current_scene = "play_bot"
        elif play_player_button.click():
            current_scene = "play_player"

    elif current_scene == "play_bot":
        prev_scene = "home"

        back_button.draw()
        screen.blit(logo_img, logo_rect)
        play_button.draw()
        choose_white_button.draw()
        choose_black_button.draw()
        choose_random_button.draw()

        if back_button.click():
            current_scene = prev_scene

        if choose_white_button.click():
            user_play_as = "White"
        elif choose_black_button.click():
            user_play_as = "Black"
        elif choose_random_button.click():
            user_play_as = "Random"

        if user_play_as == "White":
            pygame.draw.rect(screen, (255, 255, 0),
                             choose_white_button_rect, 3)
        elif user_play_as == "Black":
            pygame.draw.rect(screen, (255, 255, 0),
                             choose_black_button_rect, 3)
        elif user_play_as == "Random":
            pygame.draw.rect(screen, (255, 255, 0),
                             choose_random_button_rect, 3)

        if play_button.click():
            current_scene = "playing_bot"

        level = slider.getValue()
        level_output.setText(f"Bot Level: {level}")
        pygame_widgets.update(events)

    elif current_scene == "playing_bot":
        if engine_lvl_set == False:
            engine_max_branching_depth = set_lvl(level)
            engine_lvl_set = True

        remove_board = False
        prev_scene = "home"
        back_button.draw()

        if back_button.click():
            current_scene = prev_scene
            prev_scene = "playing_bot"

        board.draw_board(bg_img)
        result()

        if side_decided == False:
            if user_play_as == "Random":
                user_play_as = random.choice(["White", "Black"])

            if user_play_as == "White":
                board_for_moves.turn = chess.WHITE

            if user_play_as == "Black":
                board_for_moves.turn = chess.BLACK

            side_decided = True

        sqr_pos_data = load_pieces_position(user_play_as)

        check(sqr_pos_data)

        draw_all_pieces()

        if (user_play_as == "White" and board_for_moves.turn == chess.WHITE) or (user_play_as == "Black" and board_for_moves.turn == chess.BLACK):

            piece_selection_data = set_up_piece_selection_data(sqr_pos_data)
            pos = piece_selection_data[0]
            to_move_trigger = piece_selection_data[1]

            promotion_check()
            get_promotion_piece()

            translated_move = translate_move()

            if translated_move is not None:
                legal_moves = ms.get_legal_moves()

                castling(translated_move, legal_moves)

                en_passant(translated_move, legal_moves)

                move_piece(translated_move, legal_moves,
                           to_move_trigger or len(translated_move) == 5)

                capture_piece()

        else:
            if engine_max_branching_depth is not None:
                try:
                    bot_move = get_bot_move(engine_max_branching_depth)
                except:
                    bot_move = None

            if bot_move is not None:

                print(bot_move)

                bot_move_data = set_up_bot_move_data(bot_move)

                ms.current_position = bot_move_data[0]
                ms.selected_piece = bot_move_data[1]
                ms.target_sqr = bot_move_data[2]

                print([current_position, selected_piece, target_sqr])

                legal_moves = ms.get_legal_moves()
                print(legal_moves)

                castling(bot_move, legal_moves)

                en_passant(bot_move, legal_moves)

                move_piece(bot_move, legal_moves, True)

                capture_piece()

    elif current_scene == "playing_in_pass":
        remove_board = False
        prev_scene = "home"
        back_button.draw()

        if back_button.click():
            current_scene = prev_scene
            prev_scene = "playing_in_pass"

        board.draw_board(bg_img)
        result()

        if board_for_moves.turn == chess.WHITE:
            user_play_as = "White"
        else:
            user_play_as = "Black"

        sqr_pos_data = load_pieces_position(user_play_as)

        check(sqr_pos_data)

        draw_all_pieces()

        piece_selection_data = set_up_piece_selection_data(sqr_pos_data)
        pos = piece_selection_data[0]
        to_move_trigger = piece_selection_data[1]

        promotion_check()
        get_promotion_piece()

        translated_move = translate_move()

        if translated_move is not None:
            legal_moves = get_legal_moves()

            castling(translated_move, legal_moves)

            en_passant(translated_move, legal_moves)

            move_piece(translated_move, to_move_trigger or len(
                translated_move) == 5, legal_moves)

            capture_piece()

    elif current_scene == "play_player":
        prev_scene = "home"

        back_button.draw()
        screen.blit(logo_img, logo_rect)
        play_online_button.draw()
        play_in_pass_button.draw()

        if back_button.click():
            current_scene = prev_scene

        if play_in_pass_button.click():
            user_play_as = "White"
            current_scene = "playing_in_pass"

        if play_online_button.click():
            current_scene = "play_online"

    elif current_scene == "play_online":
        prev_scene = "play_player"

        back_button.draw()
        screen.blit(logo_img, logo_rect)

        view_room_code_button.draw()
        enter_room_code_button.draw()

        if view_room_code_button.click():
            prev_scene = current_scene
            current_scene = "viewing_room_code"

            room_data = set_up_online_room()

        elif enter_room_code_button.click():
            prev_scene = current_scene
            current_scene = "entering_room_code"

    elif current_scene == "viewing_room_code":
        if room_data[0] == "w":
            user_play_as = "White"
        elif room_data[0] == "b":
            user_play_as = "Black"

    pygame.display.update()
    clock.tick(60)

    # fps = clock.get_fps()
    # fps_sum += fps
    # avg_fps = fps_sum/c
    # if c % 60 == 0:
    #     print(f"FPS: {round(fps, 2)}    AVG_FPS: {round(avg_fps, 2)}")
    # c += 1

pygame.quit()
engine.quit()
sys.exit()
