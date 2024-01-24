import sys
import pygame
import subprocess
from pygame.locals import QUIT
from moviepy.editor import VideoFileClip

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))

total_coins = 0

for i in range(1, 4):
    try:
        with open(f'coin_file_{i}.txt', 'r') as file:
            content = file.read().strip()
            if content:
                total_coins += int(content)
    except FileNotFoundError:
        pass

font = pygame.font.Font(None, 36)
coin_counter = font.render(f"Coins: {total_coins}",
                           True, (255, 255, 255))
coin_rect = coin_counter.get_rect()
coin_rect.topright = (width - 10, 10)

pygame.mixer.music.load("songs/DAGames_-_Press_Start_Together_67639827.mp3")
pygame.mixer.music.play(-1)

music_playing = True

video_file = "foto/1.mp4"
video_clip = VideoFileClip(video_file)
video_start_time = pygame.time.get_ticks()

button_size = (50, 50)

pause_image = pygame.image.load('foto/stop.jpg')
pause_image = pygame.transform.scale(pause_image, button_size)

play_image = pygame.image.load('foto/play.jpg')
play_image = pygame.transform.scale(play_image, button_size)

button_rect = pause_image.get_rect()
button_rect.bottomright = (width - 5, height - 5)

central_image_size = (300, 200)

central_image_path = 'foto/New Piskel (5).png'
central_image = pygame.image.load(central_image_path)
central_image = pygame.transform.scale(central_image, central_image_size)
central_image_rect = central_image.get_rect()
central_image_rect.x = 260
central_image_rect.y = 310

close_button_image = pygame.image.load('foto/free-png.ru-45.png')
close_button_image = pygame.transform.scale(close_button_image, button_size)
close_button_rect = close_button_image.get_rect()
close_button_rect.topleft = (5, 5)

save_button_image = pygame.image.load('foto/2810417.png')
save_button_image = pygame.transform.scale(save_button_image, button_size)
save_button_rect = save_button_image.get_rect()
save_button_rect.bottomright = (width - 10, 100)

running = True
video_ended = False

while running:
    current_time = pygame.time.get_ticks() - video_start_time

    if current_time <= video_clip.duration * 1000.0:
        frame_surface = video_clip.get_frame(current_time / 1000.0)
        frame_surface = pygame.image.frombuffer(frame_surface.tostring(),
                                                frame_surface.shape[1::-1],
                                                "RGB")
        frame_surface = pygame.transform.scale(frame_surface,
                                               (width, height))
        screen.blit(frame_surface, (0, 0))
    else:
        video_start_time = pygame.time.get_ticks()
        current_time = 0

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if central_image_rect.collidepoint(event.pos):
                pygame.quit()
                subprocess.call(['python', 'instruction.py'])
                sys.exit()

            if save_button_rect.collidepoint(event.pos):
                with open('coin_count.txt', 'w') as file1:
                    file1.write(str(total_coins))

            if button_rect.collidepoint(event.pos):
                music_playing = not music_playing
                if music_playing:
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.pause()

            if close_button_rect.collidepoint(event.pos):
                running = False

    if music_playing:
        screen.blit(pause_image, button_rect)
    else:
        screen.blit(play_image, button_rect)

    screen.blit(central_image, central_image_rect)
    screen.blit(coin_counter, coin_rect)
    screen.blit(close_button_image, close_button_rect)
    screen.blit(save_button_image, save_button_rect)

    pygame.display.flip()

pygame.mixer.music.stop()
pygame.quit()

