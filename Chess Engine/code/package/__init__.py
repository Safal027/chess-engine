import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import sys
from pathlib import Path
from typing import Optional


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
SQR_SIZE = screen_height//8


screen = pygame.display.set_mode(
    (screen_width, screen_height), pygame.RESIZABLE)
screen_rect = screen.get_rect()

running = True
clock = pygame.time.Clock()
