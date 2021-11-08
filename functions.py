import pygame
import json
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, possession):
        super().__init__()
        self.sprites = []
        self.is_animating = False

        if possession == True:
            self.sprites.append(
                pygame.image.load("files/curry2/curry2-5.png"))
            self.sprites.append(
                pygame.image.load("files/curry2/curry2-5.png"))
            self.sprites.append(
                pygame.image.load("files/curry2/curry2-5.png"))
            self.sprites.append(
                pygame.image.load("files/curry2/curry2-5.png"))
            self.sprites.append(
                pygame.image.load("files/curry2/curry2-5.png"))
            self.sprites.append(
                pygame.image.load("files/curry2/curry2-5.png"))
        else:
            self.sprites.append(pygame.image.load("files/kd2/kd2-5.png"))
            self.sprites.append(pygame.image.load("files/kd2/kd2-5.png"))
            self.sprites.append(pygame.image.load("files/kd2/kd2-5.png"))
            self.sprites.append(pygame.image.load("files/kd2/kd2-5.png"))
            self.sprites.append(pygame.image.load("files/kd2/kd2-5.png"))
            self.sprites.append(pygame.image.load("files/kd2/kd2-5.png"))

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.midbottom = [pos_x, pos_y]

    def animate(self, player1_X, player1_Y):
        self.rect.midbottom = [player1_X, player1_Y]
        self.is_animating = True

    def update(self):
        if self.is_animating == True:
            self.current_sprite += 0.3

            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0

            self.image = self.sprites[int(self.current_sprite)]

class Points(pygame.sprite.Sprite):
    def __init__(self, X, Y):
        super().__init__()

        self.image = pygame.image.load("files/png/2pnts.png").convert()
        self.rect = self.image.get_rect(midtop=(X, Y))

class Spritesheet:
    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert()
        self.meta_data = self.filename.replace("png", "json")
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        return sprite

    def parse_sprite(self, name):
        sprite = self.data["frames"][name]["frame"]
        x, y, w, h = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        image = self.get_sprite(x, y, w, h)
        return image

def collision_sprites(sprite1, sprite2):
    if pygame.sprite.spritecollide(sprite1, sprite2, False):
        return 2
    else:
        return 3

def ballPath(startx, starty, power, ang, time_):
    velx = math.cos(ang) * power
    vely = math.sin(ang) * power

    distX = velx * time_
    distY = (vely * time_) + ((9 * (time_) ** 2) / 2)


    newx = round(startx - distX)
    newy = round(starty + distY)

    return [newx, newy]

def findAngle(player1_X, player1_Y, midpnt):
    sX = midpnt[0]
    sY = midpnt[1]
    try:
        angle = math.atan((sY - player1_Y) / (sX - player1_X))
    except:
        angle = math.pi / 2

    if player1_Y < sY and player1_X > sX:
        angle = abs(angle)
    elif player1_Y < sY and player1_X < sX:
        angle = math.pi - angle
    elif player1_Y > sY and player1_X < sX:
        angle = math.pi + abs(angle)
    elif player1_Y > sY and player1_X > sX:
        angle = (math.pi * 2) - angle
    
    return angle

def midpoint(playerX, playerY, posX, posY):
    midX = ((playerX + posX) / 2)
    midY = ((playerY + posY) / 2) 

    return [midX, midY]

def bucket(p1_score, p2_score, points, possession):
    if possession == True:
        p1_score += points
    else:
        p2_score += points
    
    return p1_score, p2_score

def flip(boolean):
    boolean = not boolean
    return boolean

def p_soda(possession):
    if possession == True:
        p1_spritesheet = Spritesheet("files/curry/curry.png")
        player1 = [
            p1_spritesheet.parse_sprite("files/curry/curry-0.png"),
            p1_spritesheet.parse_sprite("files/curry/curry-1.png"),
            p1_spritesheet.parse_sprite("files/curry/curry-2.png"),
            p1_spritesheet.parse_sprite("files/curry/curry-3.png"),
            p1_spritesheet.parse_sprite("files/curry/curry-4.png"),
            p1_spritesheet.parse_sprite("files/curry/curry-5.png"),
            p1_spritesheet.parse_sprite("files/curry/curry-6.png"),
            p1_spritesheet.parse_sprite("files/curry/curry-7.png"),
            p1_spritesheet.parse_sprite("files/curry/curry-7.png"),
            p1_spritesheet.parse_sprite("files/curry/curry-8.png"),
            p1_spritesheet.parse_sprite("files/curry/curry-9.png")
        ]
        player2_d = pygame.image.load("files/kd/kdd.png").convert_alpha()
    else:
        p1_spritesheet = Spritesheet("files/kd/kd.png")
        player1 = [
            p1_spritesheet.parse_sprite("files/kd/kd-0.png"),
            p1_spritesheet.parse_sprite("files/kd/kd-1.png"),
            p1_spritesheet.parse_sprite("files/kd/kd-2.png"),
            p1_spritesheet.parse_sprite("files/kd/kd-3.png"),
            p1_spritesheet.parse_sprite("files/kd/kd-4.png"),
            p1_spritesheet.parse_sprite("files/kd/kd-5.png"),
            p1_spritesheet.parse_sprite("files/kd/kd-6.png"),
            p1_spritesheet.parse_sprite("files/kd/kd-7.png"),
            p1_spritesheet.parse_sprite("files/kd/kd-7.png"),
            p1_spritesheet.parse_sprite("files/kd/kd-8.png"),
            p1_spritesheet.parse_sprite("files/kd/kd-9.png")
        ]
        player2_d = pygame.image.load("files/curry/curryd.png").convert_alpha()
    
    return p1_spritesheet, player1, player2_d

def poss_tru(player1_X, player1_Y, player1_X_change, player1_Y_change, player2_d_X_change, player2_d_Y_change, possession, jumping, moving_sprites, jumper, shoot, line, midpnt, x, y, t_ime, power, angle):

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
    
            if event.key == pygame.K_d:
                player1_X_change = 5
            if event.key == pygame.K_a:
                player1_X_change = -5
            if event.key == pygame.K_w:
                player1_Y_change = -5
            if event.key == pygame.K_s:
                player1_Y_change = 5

            if event.key == pygame.K_c:
                player = Player(player1_X, player1_Y, possession)
                moving_sprites.add(player)
                player.animate(player1_X + 15, player1_Y + 100)
                jumper = flip(jumper)
                if shoot == False:
                    shoot = True
                    x = player1_X
                    y = player1_Y
                    t_ime = 0

                    power = math.sqrt((line[1][1] - line[0][1])**2 +
                                        (line[1][0] - line[0][0])**2) / 2
                    angle = findAngle(player1_X + 30, player1_Y + 30,
                                        midpnt)

            if event.key == pygame.K_RIGHT:
                player2_d_X_change = 5
            if event.key == pygame.K_LEFT:
                player2_d_X_change = -5

            if jumping == False:
                if event.key == pygame.K_UP:
                    player2_d_Y_change = -5
                if event.key == pygame.K_DOWN:
                    player2_d_Y_change = 5

                if event.key == pygame.K_SPACE:
                    jumping = True

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_d or event.key == pygame.K_a:
                player1_X_change = 0
            if event.key == pygame.K_w or event.key == pygame.K_s:
                player1_Y_change = 0

            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                player2_d_X_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player2_d_Y_change = 0
    
    return player1_X, player1_Y, player1_X_change, player1_Y_change, player2_d_X_change, player2_d_Y_change, possession, jumping, moving_sprites, jumper, shoot, line, midpnt, x, y, t_ime, power, angle

def poss_false(player1_X, player1_Y, player1_X_change, player1_Y_change, player2_d_X_change, player2_d_Y_change, possession, jumping, moving_sprites, jumper, shoot, line, midpnt, x, y, t_ime, power, angle):

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RIGHT:
                player1_X_change = 5
            if event.key == pygame.K_LEFT:
                player1_X_change = -5
            if event.key == pygame.K_UP:
                player1_Y_change = -5
            if event.key == pygame.K_DOWN:
                player1_Y_change = 5

            if event.key == pygame.K_n:
                player = Player(player1_X, player1_Y, possession)
                moving_sprites.add(player)
                player.animate(player1_X + 15, player1_Y + 100)
                jumper = flip(jumper)
                if shoot == False:
                    shoot = True
                    x = player1_X
                    y = player1_Y
                    t_ime = 0

                    power = math.sqrt((line[1][1] - line[0][1])**2 +
                                        (line[1][0] - line[0][0])**2) / 2
                    angle = findAngle(player1_X + 30, player1_Y + 30,
                                        midpnt)

            if event.key == pygame.K_d:
                player2_d_X_change = 5
            if event.key == pygame.K_a:
                player2_d_X_change = -5

            if jumping == False:
                if event.key == pygame.K_w:
                    player2_d_Y_change = -5
                if event.key == pygame.K_s:
                    player2_d_Y_change = 5

                if event.key == pygame.K_v:
                    jumping = True

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                player1_X_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player1_Y_change = 0

            if event.key == pygame.K_d or event.key == pygame.K_a:
                player2_d_X_change = 0
            if event.key == pygame.K_w or event.key == pygame.K_s:
                player2_d_Y_change = 0
    
    return player1_X, player1_Y, player1_X_change, player1_Y_change, player2_d_X_change, player2_d_Y_change, possession, jumping, moving_sprites, jumper, shoot, line, midpnt, x, y, t_ime, power, angle

def boundary(Y, point1, point2):
    if Y >= point1:
        Y = point1
    if Y <= point2:
        Y = point2
    
    return Y

def pre_func(pre_buck, buck, pre_swat, swat):
    if buck:
        pre_buck = buck
    elif swat:
        pre_swat = swat
    
    return pre_buck, pre_swat

def show_score(screen, font, p1_score, p2_score):
    p1_points = font.render(f"{p1_score}", False, (255,255,255))
    p1_points_rect = p1_points.get_rect(center = (861, 274))
    p2_points = font.render(f"{p2_score}", False, (255,255,255))
    p2_points_rect = p2_points.get_rect(center = (668, 274))
    
    screen.blit(p1_points, p1_points_rect)
    screen.blit(p2_points, p2_points_rect)

def home_away(screen, font2):
    home = font2.render("PLAYER 1", False, (0,0,0))
    home_rect = home.get_rect(center = (862, 294))
    away = font2.render("PLAYER 2", False, (0,0,0))
    away_rect = away.get_rect(center = (670, 294))

    screen.blit(home, home_rect)
    screen.blit(away, away_rect)

def game_over(p1_score, p2_score, font3, font4, screen):
    if p1_score >= 21:
        winner = "PLAYER 1"
    elif p2_score >= 21:
        winner = "PLAYER 2"
    
    win = font3.render(f"{winner} WINS!", False, (255,255,255))
    win_rect = win.get_rect(center = (765, 100))

    restart = font4.render("PRESS R TO RESTART", False, (255,255,255))
    restart_rect = restart.get_rect(center = (765, 130))

    screen.blit(win, win_rect)
    screen.blit(restart, restart_rect)