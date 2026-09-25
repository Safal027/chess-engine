from board import *

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
            current_scene = "playing"

        level_output.setText(f"Bot Level: {slider.getValue()}")
        pygame_widgets.update(events)
        pass

    elif current_scene == "playing":
        board.draw_board(bg_img)

        if user_play_as == "Random":
            user_play_as = random.choice(["White", "Black"])

        load_pieces_position(user_play_as)

        for white_piece_name in white_pieces_names:
            white_pieces_objs[white_piece_name].draw()
        for black_piece_name in black_pieces_names:
            black_pieces_objs[black_piece_name].draw()

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
            current_scene = "playing"

    pygame.display.update()
    clock.tick(60)

    if c % 10 == 0:
        fps = round(clock.get_fps(), 1)
        print(f"FPS: {fps}")
    c += 1

pygame.quit()
sys.exit()
