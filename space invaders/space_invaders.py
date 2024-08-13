import pygame
import random

# game initialization
pygame.init()
frame_width = 1250
frame_height = 750
frame = pygame.display.set_mode((frame_width, frame_height), pygame.DOUBLEBUF, 32)

# fps
fps = 60
clock = pygame.time.Clock()


class Game:  # main game class

    def __init__(self, player, alien_group, player_bullet_group, alien_bullet_group):
        self.level_no = 1  # level - can increase until 4
        self.point = 0  # score
        self.player = player
        self.difficulty = 2  # 1 : easy, 2 : normal, 3 : hard
        self.alien_group = alien_group
        self.player_bullet_group = player_bullet_group
        self.alien_bullet_group = alien_bullet_group

        # level backgrounds
        self.level_one_bg = pygame.image.load("level_one_background.jpg")
        self.level_two_bg = pygame.image.load("level_two_background.jpg")
        self.level_three_bg = pygame.image.load("level_three_background.jpg")

        self.level_one_bg = pygame.transform.scale(self.level_one_bg, (frame_width, frame_height))
        self.level_two_bg = pygame.transform.scale(self.level_two_bg, (frame_width, frame_height))
        self.level_three_bg = pygame.transform.scale(self.level_three_bg, (frame_width, frame_height))

        # game sounds
        self.alien_hit = pygame.mixer.Sound('ship_down.mp3')
        self.player_hit = pygame.mixer.Sound('alien_dying.mp3')
        pygame.mixer.music.load('space_background.wav')
        pygame.mixer.music.play(-1)

        # game font
        self.game_font = pygame.font.SysFont('arialblack', 30)

    # game update function to run things smoothly
    def update(self):
        self.change_alien_location()
        self.touching()
        self.level_up()

    # draws backgrounds, score and level texts
    def draw(self):
        point_text = self.game_font.render(f'Score: {self.point}', True, (255, 255, 255))
        point_rect = point_text.get_rect(topleft=(15, 10))

        level_no_text = self.game_font.render(f'Level: {self.level_no}', True, (255, 255, 255))
        level_no_rect = level_no_text.get_rect(topright=(frame_width - 15, 10))

        if self.level_no == 1:
            frame.blit(self.level_one_bg, (0, 0))
        elif self.level_no == 2:
            frame.blit(self.level_two_bg, (0, 0))
        elif self.level_no == 3:
            frame.blit(self.level_three_bg, (0, 0))
        elif self.level_no == 4:
            self.game_over(1)

        pygame.draw.rect(frame, (66, 135, 245), (10, 8, 220, 50), border_radius=12)
        pygame.draw.rect(frame, (66, 135, 245), (frame_width - 155, 8, 150, 50), border_radius=12)

        frame.blit(level_no_text, level_no_rect)
        frame.blit(point_text, point_rect)

    # changes alien locations according to difficulty and makes alien waves advance
    def change_alien_location(self):
        movement, crash = False, False
        for alien in self.alien_group.sprites():
            if alien.rect.x <= 0 or alien.rect.x >= frame_width:
                movement = True

        # difficulty options
        if movement:
            for alien in self.alien_group.sprites():
                if self.difficulty == 1:
                    alien.rect.y += 5 * self.level_no
                elif self.difficulty == 2:
                    alien.rect.y += 10 * self.level_no
                elif self.difficulty == 3:
                    alien.rect.y += 15 * self.level_no

                alien.direction *= -1
                if alien.rect.bottom >= frame_height - 70:
                    crash = True

        # if player crashed with an alien
        if crash:
            self.player.health -= 1
            self.game_condition()

    # checks if player bullet hit an alien or alien bullet hit player
    def touching(self):
        # player hit alien
        if pygame.sprite.groupcollide(self.player_bullet_group, self.alien_group, True, True):
            self.player_hit.play()
            self.point += 100 * self.level_no

        # alien hit player
        elif pygame.sprite.spritecollide(self.player, self.alien_bullet_group, True):
            self.alien_hit.play()
            self.player.health -= 1
            self.game_condition()

    # creates game over screens, if game won mode: 1 else mode: 2
    def game_over(self, mode):
        global running
        is_over = True

        # menu texts
        menu_text_font = pygame.font.SysFont("arialblack", 40)
        restart_text = menu_text_font.render('Restart', True, (255, 255, 255))
        restart_text_rect = restart_text.get_rect(center=(frame_width // 2, frame_height // 2 - 90))

        change_diff_text = menu_text_font.render("Difficulty", True, (255, 255, 255))
        change_diff_text_rect = change_diff_text.get_rect(center=(frame_width // 2, frame_height // 2 + 10))

        quit_text = menu_text_font.render('Quit', True, (255, 255, 255))
        quit_text_rect = quit_text.get_rect(center=(frame_width // 2, frame_height // 2 + 110))

        # game won
        if mode == 1:
            pause_text_font = pygame.font.SysFont("timesnewromanblack", 50)
            pause_text = pause_text_font.render(f'YOU WON!', True, (255, 255, 255))
            pause_text_rect = pause_text.get_rect(center=(frame_width // 2, frame_height // 2 - 170))
            frame.blit(self.level_three_bg, (0, 0))

        # game lost
        elif mode == 2:
            pause_text_font = pygame.font.SysFont("timesnewromanblack", 50)
            pause_text = pause_text_font.render(f'GAME OVER', True, (255, 255, 255))
            pause_text_rect = pause_text.get_rect(center=(frame_width // 2, frame_height // 2 - 170))
            if self.level_no == 1:
                frame.blit(self.level_one_bg, (0, 0))
            elif self.level_no == 2:
                frame.blit(self.level_two_bg, (0, 0))
            elif self.level_no == 3:
                frame.blit(self.level_three_bg, (0, 0))

        # game over menu background
        pause_surface = pygame.surface.Surface((frame_width, frame_height))
        pause_surface.set_alpha(128)
        pause_surface.fill((0, 0, 0))

        # game over menu button rectangles
        pygame.draw.rect(frame, (66, 135, 245), (frame_width // 2 - 250, frame_height // 2 - 220, 500, 420),
                         border_radius=12)
        pygame.draw.rect(frame, (24, 73, 150), (frame_width // 2 - 225, frame_height // 2 - 130, 450, 90),
                         border_radius=12)
        pygame.draw.rect(frame, (24, 73, 150), (frame_width // 2 - 225, frame_height // 2 - 30, 450, 90),
                         border_radius=12)
        pygame.draw.rect(frame, (24, 73, 150), (frame_width // 2 - 225, frame_height // 2 + 70, 450, 90),
                         border_radius=12)

        # updates
        frame.blit(pause_surface, (0, 0))
        frame.blit(restart_text, restart_text_rect)
        frame.blit(change_diff_text, change_diff_text_rect)
        frame.blit(quit_text, quit_text_rect)
        frame.blit(pause_text, pause_text_rect)
        pygame.display.update()

        while is_over:  # game over loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # quit
                    is_over = False
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:  # mouse click
                    if event.button == 1:
                        if restart_text_rect.collidepoint(event.pos):  # restart
                            is_over = False
                            self.reset()
                        elif quit_text_rect.collidepoint(event.pos):  # quit
                            is_over = False
                            running = False
                        elif change_diff_text_rect.collidepoint(event.pos):  # change difficulty, creates new menu

                            # change difficulty menu
                            frame.fill((0, 0, 0))
                            pygame.draw.rect(frame, (66, 135, 245),
                                             (frame_width // 2 - 200, frame_height // 2 - 150, 400, 350),
                                             border_radius=12)
                            pygame.draw.rect(frame, (24, 73, 150),
                                             (frame_width // 2 - 175, frame_height // 2 - 120, 350, 90),
                                             border_radius=12)
                            pygame.draw.rect(frame, (24, 73, 150),
                                             (frame_width // 2 - 175, frame_height // 2 - 20, 350, 90),
                                             border_radius=12)
                            pygame.draw.rect(frame, (24, 73, 150),
                                             (frame_width // 2 - 175, frame_height // 2 + 80, 350, 90),
                                             border_radius=12)

                            # change difficulty texts
                            easy_text = menu_text_font.render('Easy', True, (255, 255, 255))
                            easy_text_rect = easy_text.get_rect(center=(frame_width//2, frame_height//2 - 80))

                            normal_text = menu_text_font.render('Normal', True, (255, 255, 255))
                            normal_text_rect = normal_text.get_rect(center=(frame_width//2, frame_height//2 + 20))

                            hard_text = menu_text_font.render('Hard', True, (255, 255, 255))
                            hard_text_rect = hard_text.get_rect(center=(frame_width//2, frame_height//2 + 115))

                            # updates
                            frame.blit(easy_text, easy_text_rect)
                            frame.blit(normal_text, normal_text_rect)
                            frame.blit(hard_text, hard_text_rect)
                            pygame.display.update()

                            is_changed = True
                            while is_changed:  # change difficulty loop
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        is_changed = False
                                        is_paused = False
                                        running = False
                                    elif event.type == pygame.MOUSEBUTTONDOWN:
                                        if event.button == 1:  # left click
                                            if easy_text_rect.collidepoint(event.pos):  # changes to easy
                                                self.difficulty = 1
                                            elif normal_text_rect.collidepoint(event.pos):  # changes to normal
                                                self.difficulty = 2
                                            elif hard_text_rect.collidepoint(event.pos):  # changes to hard
                                                self.difficulty = 3

                                            self.reset()  # reset
                                            is_changed = False
                                            is_over = False
                elif event.type == pygame.KEYDOWN:  # reset
                    if event.key == pygame.K_r:
                        self.reset()
                        is_over = False

    # adjusts alien waves according to difficulty and level
    def level(self):
        if self.difficulty == 1:  # easy
            for i in range(8):
                for j in range(5):
                    alien = Alien(64 + i * 64, 100 + j * 64, self.level_no, self.alien_bullet_group)
                    self.alien_group.add(alien)
        elif self.difficulty == 2:  # normal
            for i in range(10):
                for j in range(5):
                    alien = Alien(64 + i * 64, 100 + j * 64, self.level_no, self.alien_bullet_group)
                    self.alien_group.add(alien)
        elif self.difficulty == 3:  # hard
            for i in range(12):
                for j in range(5):
                    alien = Alien(64 + i * 64, 100 + j * 64, self.level_no, self.alien_bullet_group)
                    self.alien_group.add(alien)

    # pauses screen and resets player when player is hit
    def game_condition(self):

        # resets player and bullets
        self.alien_bullet_group.empty()
        self.player_bullet_group.empty()
        self.player.reset()

        for alien in self.alien_group.sprites():  # resets aliens
            alien.reset()

        if self.player.health == 0:  # checks if player is dead
            self.game_over(2)
        else:  # pause game
            self.pause()

    # if no alien to hit left, increases level
    def level_up(self):
        if not self.alien_group:
            self.level_no += 1
            self.level()

    # pause menu
    def pause(self):
        is_paused = True
        global running

        # pause menu background
        pause_surface = pygame.surface.Surface((frame_width, frame_height))
        pause_surface.set_alpha(128)
        pause_surface.fill((0, 0, 0))
        frame.blit(pause_surface, (0, 0))

        # pause menu rectangles/buttons
        pygame.draw.rect(frame, (66, 135, 245), (frame_width//2 - 250, frame_height//2 - 300, 500, 580), border_radius=12)
        pygame.draw.rect(frame, (24, 73, 150), (frame_width//2 - 225, frame_height//2 - 200, 450, 100), border_radius=12)
        pygame.draw.rect(frame, (24, 73, 150), (frame_width//2 - 225, frame_height//2 - 90, 450, 100), border_radius=12)
        pygame.draw.rect(frame, (24, 73, 150), (frame_width//2 - 225, frame_height//2 + 20, 450, 100), border_radius=12)
        pygame.draw.rect(frame, (24, 73, 150), (frame_width//2 - 225, frame_height//2 + 130, 450, 100), border_radius=12)

        # pause menu texts
        pause_text_font = pygame.font.SysFont("timesnewromanblack", 50)
        pause_text = pause_text_font.render(f'YOU HAVE {self.player.health} LIVES LEFT', True, (255, 255, 255))
        pause_text_rect = pause_text.get_rect(center=(frame_width//2, frame_height//2 - 250))

        menu_text_font = pygame.font.SysFont("arialblack", 40)
        resume_text = menu_text_font.render('Resume', True, (255, 255, 255))
        resume_text_rect = resume_text.get_rect(center=(frame_width//2, frame_height//2 - 150))

        restart_text = menu_text_font.render('Restart', True, (255, 255, 255))
        restart_text_rect = restart_text.get_rect(center=(frame_width//2, frame_height//2 - 40))

        change_diff_text = menu_text_font.render("Difficulty", True, (255, 255, 255))
        change_diff_text_rect = change_diff_text.get_rect(center=(frame_width//2, frame_height//2 + 70))

        quit_text = menu_text_font.render('Quit', True, (255, 255, 255))
        quit_text_rect = quit_text.get_rect(center=(frame_width//2, frame_height//2 + 180))

        # updates
        frame.blit(pause_text, pause_text_rect)
        frame.blit(resume_text, resume_text_rect)
        frame.blit(restart_text, restart_text_rect)
        frame.blit(change_diff_text, change_diff_text_rect)
        frame.blit(quit_text, quit_text_rect)
        pygame.display.update()

        while is_paused:  # pause menu loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # quit
                    is_paused = False
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:  # mouse click
                    if event.button == 1:  # left button
                        if resume_text_rect.collidepoint(event.pos):  # resume
                            is_paused = False
                        elif restart_text_rect.collidepoint(event.pos):  # restart
                            is_paused = False
                            self.reset()
                        elif change_diff_text_rect.collidepoint(event.pos):  # change difficulty menu

                            # change difficulty menu rectangles/buttons
                            frame.fill((0, 0, 0))
                            pygame.draw.rect(frame, (66, 135, 245),
                                             (frame_width // 2 - 200, frame_height // 2 - 150, 400, 350),
                                             border_radius=12)
                            pygame.draw.rect(frame, (24, 73, 150),
                                             (frame_width // 2 - 175, frame_height // 2 - 120, 350, 90),
                                             border_radius=12)
                            pygame.draw.rect(frame, (24, 73, 150),
                                             (frame_width // 2 - 175, frame_height // 2 - 20, 350, 90),
                                             border_radius=12)
                            pygame.draw.rect(frame, (24, 73, 150),
                                             (frame_width // 2 - 175, frame_height // 2 + 80, 350, 90),
                                             border_radius=12)

                            # change menu texts
                            easy_text = menu_text_font.render('Easy', True, (255, 255, 255))
                            easy_text_rect = easy_text.get_rect(center=(frame_width//2, frame_height//2 - 90))

                            normal_text = menu_text_font.render('Normal', True, (255, 255, 255))
                            normal_text_rect = normal_text.get_rect(center=(frame_width//2, frame_height//2 + 20))

                            hard_text = menu_text_font.render('Hard', True, (255, 255, 255))
                            hard_text_rect = hard_text.get_rect(center=(frame_width//2, frame_height//2 + 115))

                            # updates
                            frame.blit(easy_text, easy_text_rect)
                            frame.blit(normal_text, normal_text_rect)
                            frame.blit(hard_text, hard_text_rect)
                            pygame.display.update()

                            is_changed = True
                            while is_changed:  # change difficulty menu loop
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:  # quit
                                        is_changed = False
                                        is_paused = False
                                        running = False
                                    elif event.type == pygame.MOUSEBUTTONDOWN:  # mouse click
                                        if event.button == 1:  # left click
                                            if easy_text_rect.collidepoint(event.pos):  # easy
                                                self.difficulty = 1
                                            elif normal_text_rect.collidepoint(event.pos):  # normal
                                                self.difficulty = 2
                                            elif hard_text_rect.collidepoint(event.pos):  # hard
                                                self.difficulty = 3
                                            self.reset()  # restart
                                            is_changed = False
                                            is_paused = False
                                    elif event.type == pygame.KEYDOWN:
                                        if event.key == pygame.K_ESCAPE:  # back to pause menu
                                            is_changed = False
                                            is_paused = False
                                            self.pause()
                        elif quit_text_rect.collidepoint(event.pos):  # quit
                            is_paused = False
                            running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # resume
                        is_paused = False

    # resets game
    def reset(self):
        self.level_no = 1
        self.point = 0
        self.player.health = 5

        self.alien_group.empty()
        self.alien_bullet_group.empty()
        self.player_bullet_group.empty()

        self.level()


class Player(pygame.sprite.Sprite):  # player class, inherited Sprite

    def __init__(self, player_bullet_group):
        super().__init__()

        # player variables
        self.image = pygame.image.load('spaceship.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.player_bullet_group = player_bullet_group
        self.rect.centerx = frame_width // 2
        self.rect.top = frame_height - 70
        self.speed = 10
        self.health = 5
        self.bullet_sound = pygame.mixer.Sound('bullet_sound.wav')

    # updates player for movement
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:  # leftward movement
            self.rect.x -= self.speed
        elif keys[pygame.K_RIGHT] and self.rect.right < frame_width:  # rightward movement
            self.rect.x += self.speed
        # elif keys[pygame.K_UP] and self.rect.top > 0:  # upward movement
        #     self.rect.y -= self.speed
        # elif keys[pygame.K_DOWN] and self.rect.bottom < frame_height:  # downward movement
        #     self.rect.y += self.speed

    # fires bullets from player
    def fire(self):
        if len(self.player_bullet_group) < 2:  # to not make player fire continuously
            self.bullet_sound.play()
            PlayerBullet(self.rect.centerx, self.rect.top, self.player_bullet_group)

    # resets player
    def reset(self):
        self.rect.centerx = frame_width // 2


class Alien(pygame.sprite.Sprite):  # alien class, inherited Sprite

    def __init__(self, x, y, speed, bullet_group):
        super().__init__()

        # alien variables
        self.image = pygame.image.load('alien.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.x_start = x
        self.y_start = y
        self.direction = 1
        self.speed = speed
        self.bullet_group = bullet_group
        self.alien_bullet_sound = pygame.mixer.Sound('alien_laser.wav')

    # updates alien bullets
    def update(self):
        self.rect.x += self.speed * self.direction
        if random.randint(0, 100) > 99 and len(self.bullet_group) < 3:  # to not make aliens fire continuously, only three at a time
            self.alien_bullet_sound.play()
            self.fire()

    # fires alien bullets
    def fire(self):
        AlienBullet(self.rect.centerx, self.rect.bottom, self.bullet_group)

    # resets alien
    def reset(self):
        self.rect.topleft = (self.x_start, self.y_start)
        self.direction = 1


class PlayerBullet(pygame.sprite.Sprite):  # player bullets class, inherited Sprite

    def __init__(self, x, y, player_bullet_group):
        super().__init__()

        # player bullet variables
        self.image = pygame.image.load('player_bullet.png')
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10
        player_bullet_group.add(self)

    # updates bullets
    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:  # if bullet goes out of screen game destroys the bullet, so it can create new bullets
            self.kill()


class AlienBullet(pygame.sprite.Sprite):  # alien bullet class, inherited Sprite

    def __init__(self, x, y, alien_bullet_group):
        super().__init__()

        # alien bullet variables
        self.image = pygame.image.load('alien_bullet.png')
        self.rect = self.image.get_rect(center=(x, y))
        alien_bullet_group.add(self)
        self.speed = 10

    # updates alien bullets
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > frame_height: # if bullet goes out of screen game destroys the bullet, so it can create new bullets
            self.kill()


player_bullet = pygame.sprite.Group()  # player bullet group for sprites
alien_bullet = pygame.sprite.Group()  # alien bullet group for sprites

player_group = pygame.sprite.Group()  # player group for sprites
player = Player(player_bullet)
player_group.add(player)

alien_group = pygame.sprite.Group()  # alien group for sprites

game = Game(player, alien_group, player_bullet, alien_bullet)  # game object
game.level()  # creates first level

running = True
while running:  #  main game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # quit
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # fire bullets
                player.fire()
            if event.key == pygame.K_p:  # pause game
                game.pause()

    # updates
    game.update()
    game.draw()

    player_bullet.update()
    player_bullet.draw(frame)

    player_group.update()
    player_group.draw(frame)

    alien_group.update()
    alien_group.draw(frame)

    alien_bullet.update()
    alien_bullet.draw(frame)

    pygame.display.update()
    clock.tick(fps)  # fps check

pygame.quit()
