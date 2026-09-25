import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import sys
from pathlib import Path
from typing import Optional
import random


pygame.init()

pygame.display.set_caption("MateX")

current_scene = "home"
prev_scene = None
user_play_as = "Random"

c = 1

clicked = False

screen_width = 800
screen_height = 450
ASSETS_DIR = Path(__file__).resolve().parent.parent.parent / "assets"

LIGHT_COLOR = (240, 235, 255)
DARK_COLOR = (36, 75, 62)
sqr_size = screen_height//8
board_size = sqr_size*8
board_start_x = (screen_width-board_size)//2
board_start_y = (screen_height-board_size)//2
files = ["a", "b", "c", "d", "e", "f", "g", "h"]

white_pieces_names = ["wr1", "wn1", "wb1", "wq0", "wk0", "wb2", "wn2", "wr2",
                      "wp1", "wp2", "wp3", "wp4", "wp5", "wp6", "wp7", "wp8"]
black_pieces_names = ["br1", "bn1", "bb1", "bq0", "bk0", "bb2", "bn2", "br2",
                      "bp1", "bp2", "bp3", "bp4", "bp5", "bp6", "bp7", "bp8"]
white_pieces_objs = {}
black_pieces_objs = {}
turn_step = 1
current_legal_moves_for_white = []
current_legal_moves_for_black = []

screen = pygame.display.set_mode(
    (screen_width, screen_height), pygame.RESIZABLE)
screen_rect = screen.get_rect()

running = True
clock = pygame.time.Clock()
