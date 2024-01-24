import sys
import pygame
import subprocess
import random

pygame.init()

screen_width = 800
screen_height = 700

fire_image_path = 'foto/pngtree-flame.png'
fire_image = pygame.image.load(fire_image_path)

BLACK = (0, 0, 0)

player_score = 0
total_coins = 0

field = [
    "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "xooooooooooooooooooooooooooooox",
    "xoxxxxoxxxoxxxoxxxxxxxoxxoxxxox",
    "xooooooooooooooooooooooooooooox",
    "xoxxxxoxxxoxxxoxxxxxxxoxxoxxxox",
    "xooooooooooooooooooooooooooooox",
    "xxxxoxxxoxxoxxxxxxxoxxoxxxoxxxx",
    "xxxxoxxxoxxoxxxxxxxoxxoxxxoxxxx",
    "xooooxxxoooooooooooooooxxxoooox",
    "xoxxxxxxxxxoxxxxxxxoxxxxxxxxxox",
    "xoxxxxxxxxxoxxxxxxxoxxxxxxxxxox",
    "xoooooooooooooxxxooooooooooooox",
    "xoxxxxxoxxxxxoxxxoxxxxxoxxxxxox",
    "xoxxxxxoxxxxxoxxxoxxxxxoxxxxxox",
    "xooooooooooooooooooooooooooooox",
    "xoxxoxxxxxoxxxxoxxxxxoxxxxoxxox",
    "xoxxoxxxxxoxxxxoxxxxxoxxxxoxxox",
    "xooooooooooooooooooooooooooooox",
    "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
]

# Установка размеров окна
field_width = len(field[0])
field_height = len(field)

cell_size = int(min(screen_width / field_width, screen_height / field_height))

fire_image = pygame.transform.scale(fire_image, (cell_size, cell_size))

screen = (pygame.display.
          set_mode((cell_size * field_width, cell_size * field_height)))

player_speed = 2
clock = pygame.time.Clock()
fps = 60


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('foto/photo.png')
        self.image = (pygame.
                      transform.scale(self.image,
                                      (cell_size - 2, cell_size - 2)))
        self.rect = self.image.get_rect()
        self.rect.x = x * cell_size
        self.rect.y = y * cell_size

    def update(self, dx=0, dy=0):
        # Вызывается каждый кадр для обновления позиции игрока
        self.move(dx * player_speed, dy * player_speed)

    def move(self, dx=0, dy=0):
        if dx != 0:
            # Перемещение по горизонтали
            step_x = dx // abs(dx)  # Определяем направление для шага
            for _ in range(abs(dx)):
                if not self.collide(step_x, 0):
                    self.rect.x += step_x
        if dy != 0:
            # Перемещение по вертикали
            step_y = dy // abs(dy)
            for _ in range(abs(dy)):
                if not self.collide(0, step_y):
                    self.rect.y += step_y

    def collide(self, dx, dy):
        next_rect = self.rect.move(dx, dy)

        for y, row in enumerate(field):
            for x, cell in enumerate(row):
                if cell == "x":
                    if next_rect.colliderect(pygame.Rect
                                                 (x * cell_size,
                                                  y * cell_size,
                                                  cell_size, cell_size)):
                        return True
        return False


player = Player(1, 1)


chaser_speed = 1


class Pathfinder(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('foto/red.png')
        self.image = (pygame.transform
                      .scale(self.image, (cell_size - 1, cell_size - 1)))
        self.rect = self.image.get_rect()
        self.rect.x = x * cell_size
        self.rect.y = y * cell_size
        self.dx = 0
        self.dy = 0
        self.move_timer = pygame.time.get_ticks()
        self.move_interval = 1000

    def update(self):
        if (pygame.time.get_ticks() -
                self.move_timer > self.move_interval):
            self.dx = random.randint(-1, 1)
            self.dy = random.randint(-1, 1)
            self.move_timer = pygame.time.get_ticks()
        self.move(self.dx * player_speed, self.dy * chaser_speed)

    def move(self, dx=0, dy=0):
        if dx != 0:
            # Перемещение по горизонтали
            step_x = dx // abs(dx)  # Определяем направление для шага
            for _ in range(abs(dx)):
                if not self.collide(step_x, 0):
                    self.rect.x += step_x
        if dy != 0:
            # Перемещение по вертикали
            step_y = dy // abs(dy)
            for _ in range(abs(dy)):
                if not self.collide(0, step_y):
                    self.rect.y += step_y

    def collide(self, dx, dy):
        next_rect = self.rect.move(dx, dy)

        for y, row in enumerate(field):
            for x, cell in enumerate(row):
                if cell == "x":
                    if (next_rect.colliderect
                        (pygame.Rect(x * cell_size,
                                     y * cell_size,
                                     cell_size, cell_size))):
                        return True
        return False


chaser = Pathfinder(11, 10)
chaser1 = Pathfinder(18, 5)
chaser2 = Pathfinder(11, 14)
chaser3 = Pathfinder(21, 14)

heart_frames = [pygame.image.load(f'foto/heart.png')]
heart_frames = [pygame.transform.scale(frame,
                                       (20, 20)) for
                frame in heart_frames]

player_lives = 3


def draw_hearts():
    for i in range(player_lives):
        heart_frame = heart_frames[pygame.time
                                   .get_ticks() // 250 % len(heart_frames)]
        screen.blit(heart_frame, (i * 30, 5))


def handle_collision():
    global player_lives
    if player.rect.colliderect(chaser.rect) or player.rect.colliderect(
            chaser1.rect) or player.rect.colliderect(
            chaser2.rect) or player.rect.colliderect(chaser3.rect):
        player_lives -= 1
        if player_lives <= 0:
            return True
        player.rect.x, player.rect.y = cell_size, cell_size
    return False


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, cell_size):
        super().__init__()
        self.sprite_sheet = pygame.image.load(
            'foto/money.jpg').convert_alpha()
        self.cell_size = cell_size
        self.frames = self.load_frames()
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = (self.image.
                     get_rect(topleft=(x * cell_size, y * cell_size)))
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 130

    def load_frames(self):
        frames = []
        number_of_frames = 7  # количество кадров в анимации
        frame_width = self.sprite_sheet.get_width() // number_of_frames
        for i in range(number_of_frames):
            frame = (self.sprite_sheet.
                     subsurface(i * frame_width, 0,
                                frame_width, self.sprite_sheet
                                .get_height()))
            frame = pygame.transform.scale(frame,
                                           (self.cell_size,
                                            self.cell_size))
            frames.append(frame)
        return frames

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame = ((self.current_frame + 1) % len(self.frames))
            self.image = self.frames[self.current_frame]


coins = pygame.sprite.Group()


def place_coins():
    count = 0
    for y, row in enumerate(field):
        for x, cell in enumerate(row):
            if cell == "o":
                coin = Coin(x, y, cell_size)
                coins.add(coin)
                count += 1
    return count


place_coins()

coin_sound = (pygame.mixer.
              Sound('songs/nyam-nyam_(mp3IQ.net).mp3'))

font = pygame.font.Font(None, 36)
coin_counter = font.render(f"Coins: {total_coins}",
                           True, (0, 0, 0))
coin_counter_rect = coin_counter.get_rect()
coin_counter_rect.topleft = (250, 2)


def update_coins_counter():
    global total_coins, coin_counter
    total_coins += 1
    if music_enabled:
        coin_sound.play()
    coin_counter = font.render(f"Coins: {total_coins}",
                               True, (255, 255, 255))
    with open('coin_file_3.txt', 'w') as file:
        file.write(str(total_coins))


button_music_on_image = pygame.image.load('foto/play.jpg')
button_music_on_image = pygame.transform.scale(button_music_on_image,
                                               (25, 25))
button_music_off_image = pygame.image.load('foto/stop.jpg')
button_music_off_image = pygame.transform.scale(button_music_off_image,
                                                (25, 25))
button_music_rect = button_music_on_image.get_rect()
button_music_rect.bottomleft = (725, 26)

music_enabled = True


def toggle_music():
    global music_enabled
    music_enabled = not music_enabled


button_image = pygame.image.load('foto/nastr1.jpg')
button_image = pygame.transform.scale(button_image, (25, 25))
button_rect = button_image.get_rect()
button_rect.topright = (
    775, 1)


def try_again_button():
    button_image5 = pygame.image.load('foto/md_5aaeb1e070494.jpg')
    button_image5 = pygame.transform.scale(button_image5, (150, 100))
    button_rect5 = button_image5.get_rect(center=(340, 220))
    screen.blit(button_image5, button_rect5)

    mouse_x, mouse_y = pygame.mouse.get_pos()
    click, _, _ = pygame.mouse.get_pressed()

    if button_rect5.collidepoint(mouse_x, mouse_y) and click:
        return True

    return False


player_moved = False
game_over_flag = False
running = True
paused = False
while running:
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if not paused:  # Проверяем, не находится ли игра на паузе
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy = -1
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -1
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = 1

    for coin in pygame.sprite.spritecollide(player, coins, True):
        update_coins_counter()

    if any([dx, dy]):  # Проверяем, было ли нажатие клавиш для движения
        player.update(dx, dy)
        player_moved = True
    if player_moved:
        chaser.update()
        chaser1.update()
        chaser2.update()
        chaser3.update()

    coins.update()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # если нажат esc то программа закрывается
                running = False
        elif event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if button_rect.collidepoint(event.pos):
                    subprocess.call(['python', 'setting.py'])
                elif button_music_rect.collidepoint(event.pos):
                    toggle_music()
                    if music_enabled:
                        pygame.mixer.unpause()
                    else:
                        pygame.mixer.pause()

    screen.fill(BLACK)

    for y in range(len(field)):
        for x in range(len(field[y])):
            if field[y][x] == "x":
                screen.blit(fire_image,
                            (x * cell_size, y * cell_size))
    if handle_collision() and not paused:
        game_over_flag = True
        paused = True

    if not coins and not game_over_flag:
        pygame.quit()
        subprocess.call(['python', 'end_screen.py'])
        sys.exit()

    if music_enabled:
        screen.blit(button_music_on_image, button_music_rect)
    else:
        screen.blit(button_music_off_image, button_music_rect)

    screen.blit(button_image, button_rect)
    screen.blit(coin_counter, coin_counter_rect)
    coins.draw(screen)
    draw_hearts()
    screen.blit(player.image, player.rect)
    screen.blit(chaser.image, chaser.rect)
    screen.blit(chaser1.image, chaser1.rect)
    screen.blit(chaser2.image, chaser2.rect)
    screen.blit(chaser3.image, chaser3.rect)

    if game_over_flag:
        if try_again_button():
            game_over_flag = False
            player_lives = 3
            total_coins = 0
            player.rect.x, player.rect.y = cell_size, cell_size
            place_coins()
            paused = False

    clock.tick(fps)
    pygame.display.flip()
pygame.quit()
