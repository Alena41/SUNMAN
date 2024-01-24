import signal
import pygame
from pygame.locals import *
import subprocess
import sys
import os

pygame.init()

window_width = 400
window_height = 300

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Настройки")

button_width = 200
button_height = 50
button_x = (window_width - button_width) // 2
button_y = (window_height - button_height) // 2

button_color = (0, 0, 0)
button_hover_color = (0, 200, 0)
button_font_color = (255, 255, 255)


def draw_button():
    pygame.draw.rect(window, button_color,
                     (button_x, button_y, button_width, button_height))
    text = (pygame.font.Font(None, 30)
            .render("Продолжить", True, button_font_color))
    text_rect = text.get_rect(center=(
        button_x + button_width // 2, button_y + button_height // 2))
    window.blit(text, text_rect)


button2_width = 200
button2_height = 50
button2_x = (window_width - button2_width) // 2
button2_y = (window_height - button2_height) // 2 + 100

button2_color = (255, 0, 0)
button2_hover_color = (200, 0, 0)
button2_font_color = (255, 255, 255)


def draw_button2():
    pygame.draw.rect(window, button2_color,
                     (button2_x, button2_y, button2_width, button2_height))
    text2 = (pygame.font.Font(None, 30)
             .render("Вернуться в меню", True, button2_font_color))
    text2_rect = text2.get_rect(center=(
        button2_x + button2_width // 2, button2_y + button2_height // 2))
    window.blit(text2, text2_rect)


running = True
while running:
    window.fill((255, 255, 255))
    draw_button()
    draw_button2()

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if button_x <= mouse_pos[0] <= button_x + button_width and \
                    button_y <= mouse_pos[1] <= button_y + button_height:
                running = False
            elif button2_x <= mouse_pos[0] <= button2_x + button2_width and \
                    button2_y <= mouse_pos[1] <= button2_y + button2_height:
                pygame.quit()
                subprocess.call(['python', 'main.py'])
                parent_pid = os.getppid()
                os.kill(parent_pid, signal.SIGTERM)
                sys.exit()

    pygame.display.update()

pygame.quit()
