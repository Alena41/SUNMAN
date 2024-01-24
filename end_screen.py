import sys
import pygame
from moviepy.editor import VideoFileClip
import subprocess

pygame.init()

width = 800
height = 600
window = pygame.display.set_mode((width, height))

video_file = "foto/video2.mp4"
video_clip = VideoFileClip(video_file)
video_start_time = pygame.time.get_ticks()

pygame.mixer.music.load('songs/video-2.mp3')
pygame.mixer.music.set_volume(0.5)

video_playing = True
music_playing = False
running = True

close_button_image = pygame.image.load('foto/skeep.png')
close_button_image = pygame.transform.scale(close_button_image, (50, 50))
close_button_rect = close_button_image.get_rect()
close_button_rect.topright = (width - 10, 10)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if close_button_rect.collidepoint(event.pos):
                pygame.quit()
                subprocess.call(['python', 'main.py'])
                sys.exit()

    if video_playing:
        current_time = pygame.time.get_ticks() - video_start_time
        if current_time <= video_clip.duration * 1000.0:
            if not music_playing:
                pygame.mixer.music.play()
                music_playing = True

            frame = video_clip.get_frame(current_time / 1000.0)
            frame_surface = pygame.image.frombuffer(frame.tostring(),
                                                    frame.shape[1::-1],
                                                    "RGB")
            frame_surface = pygame.transform.scale(frame_surface,
                                                   (width, height))
            window.blit(frame_surface, (0, 0))
            window.blit(close_button_image, close_button_rect)
        else:
            video_playing = False
            pygame.mixer.music.stop()
            pygame.quit()
            subprocess.call(['python', 'main.py'])
            sys.exit()

    pygame.display.flip()

pygame.quit()
