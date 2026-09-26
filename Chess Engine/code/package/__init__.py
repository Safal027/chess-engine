import pygame
import chess
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
fps_sum = 0
avg_fps = 0

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
white_pieces_sqr_mapping = {
    "wr1": "a1",
    "wn1": "b1",
    "wb1": "c1",
    "wq0": "d1",
    "wk0": "e1",
    "wb2": "f1",
    "wn2": "g1",
    "wr2": "h1",
    "wp1": "a2",
    "wp2": "b2",
    "wp3": "c2",
    "wp4": "d2",
    "wp5": "e2",
    "wp6": "f2",
    "wp7": "g2",
    "wp8": "h2"
}

black_pieces_sqr_mapping = {
    "br1": "a8",
    "bn1": "b8",
    "bb1": "c8",
    "bq0": "d8",
    "bk0": "e8",
    "bb2": "f8",
    "bn2": "g8",
    "br2": "h8",
    "bp1": "a7",
    "bp2": "b7",
    "bp3": "c7",
    "bp4": "d7",
    "bp5": "e7",
    "bp6": "f7",
    "bp7": "g7",
    "bp8": "h7",
}

white_pieces_objs = {}
black_pieces_objs = {}
selected_piece = None
current_position = None
target_sqr = None
turn_step = 1

screen = pygame.display.set_mode(
    (screen_width, screen_height), pygame.RESIZABLE)
screen_rect = screen.get_rect()

running = True
clock = pygame.time.Clock()
