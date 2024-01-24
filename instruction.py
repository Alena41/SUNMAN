import sys
import pygame
from moviepy.editor import VideoFileClip
import subprocess

pygame.init()

width = 800
height = 600
window = pygame.display.set_mode((width, height))

background = pygame.image.load('foto/instruc.jpg')

button_color = (0, 255, 0)
button_position = [700, 500]
button_size = [80, 30]
button_rect = pygame.Rect(button_position[0], button_position[1],
                          button_size[0], button_size[1])

close_button_image = pygame.image.load('foto/skeep.png')
close_button_image = pygame.transform.scale(close_button_image, button_size)
close_button_rect = close_button_image.get_rect()
close_button_rect.topright = (width - 10, 10)

button_visible = True
close_button_visible = False
background_current = background

video_file = "foto/video_2024.mp4"
video_clip = VideoFileClip(video_file)
video_start_time = pygame.time.get_ticks()

pygame.mixer.music.load('songs/video-1.mp3')
pygame.mixer.music.set_volume(0.5)

video_playing = False
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos) and button_visible:
                button_visible = False
                close_button_visible = True
                video_start_time = pygame.time.get_ticks()
                video_playing = True
                pygame.mixer.music.play()
            elif close_button_rect.collidepoint(event.pos):
                pygame.quit()
                subprocess.call(['python', 'one_lvl.py'])
                sys.exit()

    if running:
        if video_playing:
            current_time = pygame.time.get_ticks() - video_start_time
            if current_time <= video_clip.duration * 1000.0:
                frame = video_clip.get_frame(current_time / 1000.0)
                frame_surface = pygame.image.frombuffer(frame.tostring(),
                                                        frame.shape[1::-1],
                                                        "RGB")
                frame_surface = pygame.transform.scale(frame_surface,
                                                       (width, height))
                window.blit(frame_surface, (0, 0))
                if close_button_visible:
                    window.blit(close_button_image, close_button_rect)
            else:
                video_playing = False
                pygame.mixer.music.stop()
                pygame.quit()
                subprocess.call(['python', 'one_lvl.py'])
                sys.exit()
        else:
            window.blit(background_current, (0, 0))

            if button_visible:
                pygame.draw.rect(window, button_color, button_rect)

    pygame.display.flip()

pygame.quit()
