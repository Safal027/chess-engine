from package import *


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


def get_refined_image_data_for_pieces(image, x_percent_w_r_to_board: float, y_percent_w_r_to_board: float, x_rect: float, y_rect: float):

    target_x = board_size*x_percent_w_r_to_board
    target_y = board_size*y_percent_w_r_to_board

    scale_x = target_x/image.get_width()
    scale_y = target_y/image.get_height()

    scale_factor = min(scale_x, scale_y)

    scaled_image = pygame.transform.scale_by(image, scale_factor)

    scaled_image_rect = scaled_image.get_rect()

    scaled_image_rect.x = x_rect
    scaled_image_rect.y = y_rect

    return scaled_image, scaled_image_rect


logo = pygame.image.load(
    ASSETS_DIR/"images/other_images/MateX_logo.png").convert_alpha()
refined_logo_data = get_refined_image_data(
    logo, 0.4, 0.4, True, False, False)
logo_img = refined_logo_data[0]
logo_rect = refined_logo_data[1]

pygame.display.set_icon(logo)

bg = pygame.image.load(
    ASSETS_DIR/"images/other_images/main_screen_bg.png").convert()
refined_bg_data = get_refined_image_data(bg, 1, 1, True, True, True)
bg_img = refined_bg_data[0]
bg_rect = refined_bg_data[1]
