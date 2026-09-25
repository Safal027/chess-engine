from refine_img import *


class Button:

    def load_button_data(self, img_path, x_percent_w_r_to_win: float, y_percent_w_r_to_win: float, center_x: bool, center_y: bool, to_fill: bool, x_rect: Optional[float] = None, y_rect: Optional[float] = None):
        self.button_img = pygame.image.load(img_path).convert_alpha()
        self.refined_button_data = get_refined_image_data(
            self.button_img, x_percent_w_r_to_win, y_percent_w_r_to_win, center_x, center_y, to_fill, x_rect, y_rect)
        self.button_img = self.refined_button_data[0]
        self.button_rect = self.refined_button_data[1]

    def draw(self):
        screen.blit(self.button_img, self.button_rect)

    def obtain_rect(self):
        return self.button_rect

    def click(self):
        global clicked
        action = False

        pos = pygame.mouse.get_pos()

        if self.button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and clicked == False:
                click_sound_effect.play()
                clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            clicked = False

        return action


play_bot_button = Button()
play_bot_button.load_button_data(
    ASSETS_DIR/"images/other_images/button_play-against-a-bot.png", 0.4, 0.4, True, False, False, y_rect=185)

play_player_button = Button()
play_player_button.load_button_data(
    ASSETS_DIR/"images/other_images/button_play-against-a-player.png", 0.45, 0.45, True, False, False, y_rect=300)

play_online_button = Button()
play_online_button.load_button_data(
    ASSETS_DIR/"images/other_images/button_play-online.png", 0.4, 0.4, False, False, False, x_rect=50, y_rect=225)

play_in_pass_button = Button()
play_in_pass_button.load_button_data(
    ASSETS_DIR/"images/other_images/button_play-in-pass.png", 0.4, 0.4, False, False, False, x_rect=400, y_rect=225)

slider = Slider(win=screen, x=150, y=180, width=500, height=10, min=1, max=25,
                step=1, valueColour=(000, 000, 000), colour=(200, 200, 200), handleColour=(100, 100, 100), initial=1)
level_output = TextBox(win=screen, x=310, y=200,
                       width=183, height=46, fontSize=30, borderThickness=1, radius=1)

level_output.disable()

choose_white_button = Button()
choose_white_button.load_button_data(
    ASSETS_DIR/"images/other_images/choose_white.png", 0.15, 0.15, False, False, False, x_rect=200, y_rect=265)
choose_white_button_rect = choose_white_button.obtain_rect()

choose_black_button = Button()
choose_black_button.load_button_data(
    ASSETS_DIR/"images/other_images/choose_black.png", 0.15, 0.15, False, False, False, x_rect=525, y_rect=265)
choose_black_button_rect = choose_black_button.obtain_rect()

choose_random_button = Button()
choose_random_button.load_button_data(
    ASSETS_DIR/"images/other_images/choose_random.png", 0.15, 0.15, True, False, False, y_rect=265)
choose_random_button_rect = choose_random_button.obtain_rect()

play_button = Button()
play_button.load_button_data(
    ASSETS_DIR/"images/other_images/button_play.png", 0.15, 0.15, True, False, False, y_rect=380)

back_button = Button()
back_button.load_button_data(
    ASSETS_DIR/"images/other_images/button_back.png", 0.15, 0.15, False, False, False, x_rect=20, y_rect=20)

click_sound_effect = pygame.mixer.Sound(ASSETS_DIR/"sounds/button_click.mp3")
