from board import *

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.VIDEORESIZE:
            pass

    screen.fill((18, 18, 18))
    screen.blit(refined_bg, (0, 0))

    if current_scene == "home":
        screen.blit(refined_logo_data[0], refined_logo_data[1])
        screen.blit(
            play_bot_button_img, play_bot_button_rect)
        screen.blit(
            play_player_button_img, play_player_button_rect)

        if play_bot_button.click():
            current_scene = "play_bot"
        elif play_player_button.click():
            current_scene = "play_player"

    if current_scene == "play_bot":
        prev_scene = "home"

        screen.blit(back_button_img, back_button_rect)
        screen.blit(refined_logo_data[0], refined_logo_data[1])
        screen.blit(play_button_img, play_button_rect)
        screen.blit(choose_white_button_img, choose_white_button_rect)
        screen.blit(choose_black_button_img, choose_black_button_rect)
        screen.blit(choose_random_button_img, choose_random_button_rect)

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

        level_output.setText(f"Bot Level: {slider.getValue()}")
        pygame_widgets.update(events)
        pass

    elif current_scene == "play_player":
        prev_scene = "home"

        screen.blit(back_button_img, back_button_rect)
        screen.blit(refined_logo_data[0], refined_logo_data[1])
        screen.blit(
            play_online_button_img, play_online_button_rect)
        screen.blit(
            play_in_pass_button_img, play_in_pass_button_rect)

        if back_button.click():
            current_scene = prev_scene

    pygame.display.update()
    clock.tick(60)

    if c % 10 == 0:
        fps = round(clock.get_fps(), 1)
        print(f"FPS: {fps}")
    c += 1

pygame.quit()
sys.exit()
