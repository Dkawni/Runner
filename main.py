import pygame
from sys import exit
from random import randint, choice

pygame.init()
screen = pygame.display.set_mode((700, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font(None, 50)
game_active = True
start_time = 0

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load('graphics/player_walk1.png').convert_alpha()
        player_walk2 = pygame.image.load('graphics/player_walk2.png').convert_alpha()
        player_walk1 = pygame.transform.scale(player_walk1, (90, 90))
        player_walk2 = pygame.transform.scale(player_walk2, (90,90))
        self.player_walk = [player_walk1, player_walk2]
        self.player_index = 0
        self.player_jump = player_walk1

        self.image = self.player_walk[self.player_index]
        self.image = pygame.transform.scale(self.image, (90,90))
        self.rect = self.image.get_rect(midbottom = (80,330))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 330:
            self.gravity = -20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 330:
            self.rect.bottom = 330

    def animation_state(self):
        if self.rect.bottom < 330:
            self.image = self.player_jump
        else:
            self.player_index += 0.15
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__() #needed to avoid error

        if type == 'bird':
            bird_frame_1 = pygame.image.load('graphics/bird1.png').convert_alpha()
            bird_frame_1 = pygame.transform.scale(bird_frame_1, (85, 35))
            bird_frame_2 = pygame.image.load('graphics/bird2.png').convert_alpha()
            bird_frame_2 = pygame.transform.scale(bird_frame_2, (85, 35))
            self.frames = [bird_frame_1, bird_frame_2]
            y_pos = 210
        else:
            turtle_frame_1 = pygame.image.load('graphics/turtle1.png').convert_alpha()
            turtle_frame_1 = pygame.transform.scale(turtle_frame_1, (90, 40))
            turtle_frame_2 = pygame.image.load('graphics/turtle2.png').convert_alpha()
            turtle_frame_2 = pygame.transform.scale(turtle_frame_2, (90, 40))
            self.frames = [turtle_frame_1, turtle_frame_2]
            y_pos = 330


        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(800,1000), y_pos))
    def animation_state(self):
        self.animation_index += 0.15
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 7
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center = (350, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 7

            # Render turtle or bird dynamically based on position
            if obstacle_rect.bottom == 330:  # Turtle
                screen.blit(turtle_frames[turtle_frame_index], obstacle_rect)
            else:  # Bird
                screen.blit(bird_frames[bird_frame_index], obstacle_rect)

        # Remove obstacles that have moved off screen
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):#bool, snail is deleted or not
        obstacle_group.empty()
        return False
    else:
        return True

def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 330:
        #jump
        player_surf = player_jump
    else:
        #walk
        player_index += 0.15
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = pygame.transform.scale(player_walk[int(player_index)], (90, 90))
    #play walking if player is on the floor
    #display jump if player is not on the floor


#Groups
player = pygame.sprite.GroupSingle()
player.add(Player()) #group that has sprite that has player

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('graphics/Sky.png')

score_surf = test_font.render('Runner', False, (64, 64, 64)) #False, means all sharp edges
score_rect = score_surf.get_rect(center = (350,80))


#game over screen
game_title_surf = test_font.render('Runner', False, (64, 64, 64))
game_title_rect = game_title_surf.get_rect(center = (350, 70))

instruction_surf = test_font.render('Press Space to Start', False, (64, 64, 64))
instruction_rect = instruction_surf.get_rect(center = (350, 330))


#obstacles
turtle_surface = pygame.image.load('graphics/turtle1.png').convert_alpha()
turtle_frame_1 = pygame.transform.scale(turtle_surface, (90,40))
turtle_surface2 = pygame.image.load('graphics/turtle2.png').convert_alpha()
turtle_frame_2 = pygame.transform.scale(turtle_surface, (90,40))
turtle_frames = [turtle_frame_1, turtle_frame_2]
turtle_frame_index = 0
turtle_surf = turtle_frames[turtle_frame_index]

#turtle_rect = turtle_surface.get_rect(bottomright = (650, 330))

bird_frame_1 = pygame.image.load('graphics/bird1.png').convert_alpha()
bird_frame_1 = pygame.transform.scale(bird_frame_1, (85,35))
bird_frame_2 = pygame.image.load('graphics/bird2.png').convert_alpha()
bird_frame_2 = pygame.transform.scale(bird_frame_2, (85,35))
bird_frames = [bird_frame_1, bird_frame_2]
bird_frame_index = 0
bird_surface = bird_frames[bird_frame_index]


obstacle_rect_list = []


#rectangle hit box
player_walk1 = pygame.image.load('graphics/player_walk1.png').convert_alpha()
player_walk2 = pygame.image.load('graphics/player_walk2.png').convert_alpha()
player_surf_scaled = pygame.transform.scale(player_walk1,(100,100))
player_walk = [player_walk1, player_walk2]
player_index = 0
player_jump = player_surf_scaled
player_surf = player_walk[player_index]

#Game Over Screen
player_rect = player_surf_scaled.get_rect(midbottom = (80,330))
player_gravity = 0

player_stand = pygame.image.load('graphics/kitty.png').convert_alpha()
player_stand_scaled = pygame.transform.scale(player_stand,(100,150))
player_stand_rect = player_stand_scaled.get_rect(midbottom = (350, 270))


#Timer
obstacle_timer = pygame.USEREVENT + 1 #importance of + 1 - avoid conflict with events
pygame.time.set_timer(obstacle_timer, 1500)

turtle_animation_timer = pygame.USEREVENT  + 2
pygame.time.set_timer(turtle_animation_timer, 500)

bird_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(bird_animation_timer,200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 250:
                    player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 250:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks()/1000)
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['bird','turtle', 'turtle'])))

            if event.type == turtle_animation_timer:
                if turtle_frame_index == 0: turtle_frame_index = 1
                else: turtle_frame_index = 0
                turtle_surf = turtle_frames[turtle_frame_index]

            if event.type == bird_animation_timer:
                if bird_frame_index == 0:
                    bird_frame_index = 1
                else:
                    bird_frame_index = 0
                bird_surf = bird_frames[bird_frame_index]

    if game_active: #game
        screen.blit(sky_surface, (-10,-40))

        #pygame.draw.rect(screen, 'Pink', score_rect)
        #pygame.draw.line(screen, 'Gold', (0,0), pygame.mouse.get_pos())
        #          where to draw, color, starting pos, follows the mouse pos
        #screen.blit(score_surf, score_rect)
        score = display_score()

        #Player
        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()

    else: #menu screen/game over
        screen.fill('#9bc99e')
        screen.blit(player_stand_scaled, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,330)
        player_gravity = 0

        score_message = test_font.render(f'Your score: {score}', False, (64, 64, 64))
        score_message_rect = score_message.get_rect(center = (350, 330))
        screen.blit(game_title_surf, game_title_rect)
        if score == 0:
            screen.blit(instruction_surf, instruction_rect)
        else:
            screen.blit(score_message, score_message_rect)


    pygame.display.update()
    clock.tick(60)
