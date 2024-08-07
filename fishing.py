import pygame
import random

pygame.init()
frame_width, frame_height = 750, 750
frame = pygame.display.set_mode((frame_width, frame_height))

fps = 30
clock = pygame.time.Clock()


class FishingGame:
    def __init__(self, fisherman, fish_group):
        self.fisherman = fisherman
        self.fish_group = fish_group

        self.time = 0
        self.fps_counter = 0
        self.level = 0

        fish_one = pygame.image.load('fish1.png')
        fish_two = pygame.image.load('fish2.png')
        fish_three = pygame.image.load('fish3.png')
        fish_four = pygame.image.load('fish4.png')

        fish_one = pygame.transform.scale(fish_one, (30, 30))
        fish_two = pygame.transform.scale(fish_two, (30, 30))
        fish_three = pygame.transform.scale(fish_three, (30, 30))
        fish_four = pygame.transform.scale(fish_four, (30, 30))

        self.fish_list = [fish_one, fish_two, fish_three, fish_four]
        self.fish_list_index = random.randint(0, len(self.fish_list) - 1)
        self.target_fish_image = self.fish_list[self.fish_list_index]
        self.target_fish_location = self.target_fish_image.get_rect()
        self.target_fish_location.top = 35
        self.target_fish_location.centerx = frame_width // 2

        self.game_font = pygame.font.SysFont("Arial", 26)
        self.fish_bait_sound = pygame.mixer.Sound('bait.wav')
        self.game_over_sound = pygame.mixer.Sound('game_over.wav')
        self.death_sound = pygame.mixer.Sound('death.wav')
        pygame.mixer.music.load("piano_background.wav")
        pygame.mixer.music.play(-1)
        self.game_background = pygame.image.load('water_background.jpg')
        self.game_background = pygame.transform.scale(self.game_background, (frame_width, frame_height))
        self.game_over_background = pygame.image.load('game_over.jpg')
        self.game_over_background = pygame.transform.scale(self.game_over_background, (frame_width, frame_height))
        self.game_over_background = pygame.transform.scale(self.game_over_background, (0, 0))

    def update(self):
        self.fps_counter += 1
        if self.fps_counter == fps:
            self.time += 1
            self.fps_counter = 0
        self.touch()

    def draw(self):
        frame.blit(self.game_background, (0, 0))
        pygame.draw.rect(frame, (0, 0, 170), (0, 0, 750, 100))
        pygame.draw.rect(frame, (186, 166, 112), (0, frame_height - 50, 750, 50))

        # health bar
        pygame.draw.rect(frame, (255, 150, 255), (frame_width - 150, 25, 130, 50), border_top_left_radius=12,
                         border_bottom_right_radius=12, border_bottom_left_radius=12, border_top_right_radius=12)
        if fisherman.health == 3:
            pygame.draw.rect(frame, (255, 50, 0), (frame_width - 147, 29, 40, 42), border_top_left_radius=10, border_bottom_left_radius=10)
            pygame.draw.rect(frame, (255, 50, 0), (frame_width - 105, 29, 40, 42))
            pygame.draw.rect(frame, (255,50, 0), (frame_width - 63, 29, 40, 42), border_top_right_radius=10, border_bottom_right_radius=10)
        elif fisherman.health == 2:
            pygame.draw.rect(frame, (255, 50, 0), (frame_width - 147, 29, 40, 42), border_top_left_radius=10, border_bottom_left_radius=10)
            pygame.draw.rect(frame, (255, 50, 0), (frame_width - 105, 29, 40, 42))
        elif fisherman.health == 1:
            pygame.draw.rect(frame, (255, 50, 0), (frame_width - 147, 29, 40, 42), border_top_left_radius=10, border_bottom_left_radius=10)

        # time bar
        clock_image = pygame.image.load('clock.png')
        clock_image = pygame.transform.scale(clock_image, (50, 50))
        pygame.draw.rect(frame, (186, 166, 112), (25, 20, 100, 60), border_top_left_radius=16,
                         border_bottom_right_radius=16, border_bottom_left_radius=16, border_top_right_radius=16)
        time_text = self.game_font.render(str(self.time), True, (255, 255, 255))
        time_text_rect = time_text.get_rect(topleft=(100, 35))
        frame.blit(clock_image, (30, 25))
        frame.blit(time_text, time_text_rect)

        level_text = self.game_font.render(f"Level: {self.level}", True, (200, 255, 255))
        level_text_rect = level_text.get_rect(bottomright=(frame_width - 50, frame_height - 12))
        frame.blit(level_text, level_text_rect)
        frame.blit(self.target_fish_image, self.target_fish_location)

        pygame.draw.rect(frame, (255, 255, 255), (350, 25, 50, 50), 5)
        pygame.draw.rect(frame, (255, 0, 255), (0, 100, 750, frame_height - 150), 5)

    def touch(self):
        is_touching = pygame.sprite.spritecollideany(self.fisherman, self.fish_group)
        if is_touching:
            if is_touching.fish_type == self.fish_list_index:
                is_touching.remove(self.fish_group)
                self.fish_bait_sound.play()
                if self.fish_group:
                    self.create_new_target()
                else:
                    self.target_new()
            else:
                self.fisherman.health -= 1
                self.death_sound.play()
                self.safe_zone()
                if self.fisherman.health <= 0:
                    self.game_over()

    def game_over(self):
        global running
        game_over_font = pygame.font.SysFont("Times New Roman", 80)
        game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
        frame.blit(game_over_text, game_over_text.get_rect(center=(frame_width//2, frame_height//2 - 30)))

        replay_text_font = pygame.font.SysFont("Arial", 26)
        replay_text = replay_text_font.render("Press Space to replay", True, (255, 255, 255))
        frame.blit(replay_text, replay_text.get_rect(center=(frame_width//2, frame_height//2 + 55)))
        pygame.display.update()

        is_over = True
        while is_over:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    is_over = False
                    running = False
                elif ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_SPACE:
                        self.reset()
                        is_over = False

    def reset(self):
        self.fisherman.health = 3
        self.level = 0
        self.time = 0
        self.target_new()
        self.safe_zone()

    def safe_zone(self):
        self.fisherman.rect.top = frame_height - 40

    def create_new_target(self):
        targeted_fish = random.choice(self.fish_group.sprites())
        self.target_fish_image = targeted_fish.image
        self.fish_list_index = targeted_fish.fish_type

    def target_new(self):
        self.level += 1
        for f in self.fish_group:
            self.fish_group.remove(f)
        for g in range(self.level):
            self.fish_group.add(Fish(random.randint(0, frame_width - 30), random.randint(105, frame_height - 150), self.fish_list[0], 0))
            self.fish_group.add(Fish(random.randint(0, frame_width - 30), random.randint(105, frame_height - 150), self.fish_list[1], 1))
            self.fish_group.add(Fish(random.randint(0, frame_width - 30), random.randint(105, frame_height - 150), self.fish_list[2], 2))
            self.fish_group.add(Fish(random.randint(0, frame_width - 30), random.randint(105, frame_height - 150), self.fish_list[3], 3))


class Fish(pygame.sprite.Sprite):
    def __init__(self, x, y, image, fish_type):
        super().__init__()
        self.image = image
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.fish_type = fish_type
        self.speed = random.randint(1, 5)
        self.dir_x = random.choice([-1, 1])
        self.dir_y = random.choice([-1, 1])

    def update(self):
        self.rect.x += self.dir_x * self.speed
        self.rect.y += self.dir_y * self.speed
        if self.rect.left <= 0 or self.rect.right >= frame_width:
            self.dir_x *= -1
        if self.rect.top <= 100 or self.rect.bottom >= frame_height-50:
            self.dir_y *= -1


class Fisherman(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('fisherman.png')
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.health = 3
        self.speed = 10

    def update(self):
        self.movement()

    def movement(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        elif key[pygame.K_RIGHT] and self.rect.right < frame_width:
            self.rect.x += self.speed
        elif key[pygame.K_UP] and self.rect.top > 105:
            self.rect.y -= self.speed
        elif key[pygame.K_DOWN] and self.rect.bottom < frame_height-5:
            self.rect.y += self.speed


fisherman_group = pygame.sprite.Group()
fisherman = Fisherman(frame_width // 2, frame_height // 2)
fisherman_group.add(fisherman)

fish_group = pygame.sprite.Group()
game = FishingGame(fisherman, fish_group)
game.target_new()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    frame.fill(pygame.Color('black'))
    game.update()
    game.draw()
    fisherman_group.update()
    fisherman_group.draw(frame)
    fish_group.update()
    fish_group.draw(frame)

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
