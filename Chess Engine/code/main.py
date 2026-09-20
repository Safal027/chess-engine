import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import sys
from pathlib import Path
from typing import Optional

pygame.init()


class Button:

    def draw(self, img_path, x_percent_w_r_to_win: float, y_percent_w_r_to_win: float, center_x: bool, center_y: bool, to_fill: bool, x_rect: Optional[float] = None, y_rect: Optional[float] = None):
        self.button_img = pygame.image.load(img_path).convert_alpha()
        self.refined_button_data = get_refined_image_data(
            self.button_img, x_percent_w_r_to_win, y_percent_w_r_to_win, center_x, center_y, to_fill, x_rect, y_rect)
        self.refined_button_img = self.refined_button_data[0]
        return self.refined_button_img

    def rect(self):
        self.button_rect = self.refined_button_data[1]
        return self.button_rect

    def click(self):
        global clicked
        action = False

        pos = pygame.mouse.get_pos()

        if self.button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and clicked == False:
                clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            clicked = False

        return action


def get_refined_image_data(image, x_percent_w_r_to_win: float, y_percent_w_r_to_win: float, center_x: bool, center_y: bool, to_fill: bool, x_rect: Optional[float] = None, y_rect: Optional[float] = None):

    target_x = screen.get_width()*x_percent_w_r_to_win
    target_y = screen.get_height()*y_percent_w_r_to_win

    scale_x = target_x/image.get_width()
    scale_y = target_y/image.get_height()

    if to_fill == True:
        scale_factor = max(scale_x, scale_y)
    else:
        scale_factor = min(scale_x, scale_y)

    scaled_image = pygame.transform.scale_by(image, scale_factor)

    screen_rect = screen.get_rect()
    scaled_image_rect = scaled_image.get_rect()

    if center_x == True:
        scaled_image_rect.centerx = screen_rect.centerx
    if center_y == True:
        scaled_image_rect.centery = screen_rect.centery

    if x_rect != None:
        scaled_image_rect.x = x_rect
    if y_rect != None:
        scaled_image_rect.y = y_rect

    return scaled_image, scaled_image_rect


pygame.display.set_caption("MateX")

current_scene = "home"
prev_scene = None
user_play_as = "Random"

clicked = False

screen_width = 800
screen_height = 450
ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"


screen = pygame.display.set_mode(
    (screen_width, screen_height), pygame.RESIZABLE)
screen_rect = screen.get_rect()

running = True
clock = pygame.time.Clock()

logo = pygame.image.load(
    ASSETS_DIR/"images/other_images/MateX_logo.png").convert_alpha()
refined_logo_data = get_refined_image_data(
    logo, 0.4, 0.4, True, False, False)

pygame.display.set_icon(logo)

bg = pygame.image.load(
    ASSETS_DIR/"images/other_images/main_screen_bg.png").convert()
refined_bg = get_refined_image_data(bg, 1, 1, True, True, True)[0]

play_bot_button = Button()
play_bot_button_img = play_bot_button.draw(
    ASSETS_DIR/"images/other_images/button_play-against-a-bot.png", 0.4, 0.4, True, False, False, y_rect=185)
play_bot_button_rect = play_bot_button.rect()

play_player_button = Button()
play_player_button_img = play_player_button.draw(
    ASSETS_DIR/"images/other_images/button_play-against-a-player.png", 0.45, 0.45, True, False, False, y_rect=300)
play_player_button_rect = play_player_button.rect()

play_online_button = Button()
play_online_button_img = play_online_button.draw(
    ASSETS_DIR/"images/other_images/button_play-online.png", 0.4, 0.4, False, False, False, x_rect=50, y_rect=225)
play_online_button_rect = play_online_button.rect()

play_in_pass_button = Button()
play_in_pass_button_img = play_in_pass_button.draw(
    ASSETS_DIR/"images/other_images/button_play-in-pass.png", 0.4, 0.4, False, False, False, x_rect=400, y_rect=225)
play_in_pass_button_rect = play_in_pass_button.rect()

slider = Slider(win=screen, x=150, y=180, width=500, height=10, min=1, max=25,
                step=1, valueColour=(000, 000, 000), colour=(200, 200, 200), handleColour=(100, 100, 100), initial=1)
level_output = TextBox(win=screen, x=310, y=200,
                       width=183, height=46, fontSize=30, borderThickness=1, radius=1)

level_output.disable()

choose_white_button = Button()
choose_white_button_img = choose_white_button.draw(
    ASSETS_DIR/"images/other_images/choose_white.png", 0.15, 0.15, False, False, False, x_rect=200, y_rect=265)
choose_white_button_rect = choose_white_button.rect()

choose_black_button = Button()
choose_black_button_img = choose_black_button.draw(
    ASSETS_DIR/"images/other_images/choose_black.png", 0.15, 0.15, False, False, False, x_rect=525, y_rect=265)
choose_black_button_rect = choose_black_button.rect()

choose_random_button = Button()
choose_random_button_img = choose_random_button.draw(
    ASSETS_DIR/"images/other_images/choose_random.png", 0.15, 0.15, True, False, False, y_rect=265)
choose_random_button_rect = choose_random_button.rect()

play_button = Button()
play_button_img = play_button.draw(
    ASSETS_DIR/"images/other_images/button_play.png", 0.15, 0.15, True, False, False, y_rect=380)
play_button_rect = play_button.rect()

back_button = Button()
back_button_img = back_button.draw(
    ASSETS_DIR/"images/other_images/button_back.png", 0.15, 0.15, False, False, False, x_rect=20, y_rect=20)
back_button_rect = back_button.rect()

click_sound_effect = pygame.mixer.Sound(ASSETS_DIR/"sounds/button_click.mp3")


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
            click_sound_effect.play()
            current_scene = "play_bot"
        elif play_player_button.click():
            click_sound_effect.play()
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
            click_sound_effect.play()
            current_scene = prev_scene

        if choose_white_button.click():
            click_sound_effect.play()
            user_play_as = "White"
        elif choose_black_button.click():
            click_sound_effect.play()
            user_play_as = "Black"
        elif choose_random_button.click():
            click_sound_effect.play()
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
            click_sound_effect.play()
            current_scene = prev_scene

    pygame.display.update()
    clock.tick(60)

    fps = round(clock.get_fps(), 1)
    print(f"FPS: {fps}")

pygame.quit()
sys.exit()
