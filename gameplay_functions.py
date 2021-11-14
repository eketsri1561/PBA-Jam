import pygame
import json
import math

players = [
    ["files/curry/curry", "files/curry/curry2-5.png", "files/curry/curryd"],
    ["files/kd/kd", "files/kd/kd2-5.png", "files/kd/kdd"],
    [
        "files/giannis/giannis",
        "files/giannis/giannis2-5.png",
        "files/giannis/giannisd"
    ],
    [
        "files/lamelo/lamelo",
        "files/lamelo/lamelo2-5.png",
        "files/lamelo""/lamelod"
    ],
]


def choice(bool_1, bool_2, i_1, i_2, numb, bool_3):
    """Returns a pair of integers and a pair of booleans

    Args:
        bool_1: A boolean
        bool_2: A boolean
        i_1: A integer
        i_2: A integer
        numb: A integer
        bool_3: A boolean

    Returns:
        The new assigned values for i_1, 1_2, bool_2, and bool_3.
    """
    if bool_1:
        if bool_2:
            i_1 = numb
            bool_2 = False
        else:
            i_2 = numb
            bool_3 = False

    return i_1, i_2, bool_2, bool_3


def characters(screen, bool_):
    font = pygame.font.Font("files/font/8-BIT WONDER.TTF", 70)
    font2 = pygame.font.Font("files/font/8-BIT WONDER.TTF", 25)
    title = font.render("WELCOME TO PBA JAM", False, (255, 0, 0))
    title_rect = title.get_rect(center=(765, 100))
    if bool_:
        player_selection = font2.render("Please Select your character Player "
                                        "1 ", False, (255, 0, 0))
    else:
        player_selection = font2.render("Please Select your character Player "
                                        "2 ", False, (255, 0, 0))
    player_selection_rect = player_selection.get_rect(center=(765, 190))

    curry_button = pygame.image.load("files/curry/curry_select.png").convert()
    curry_button_rect = curry_button.get_rect(center=(290, 350))

    kd_button = pygame.image.load("files/kd/kd_select.png").convert()
    kd_button_rect = kd_button.get_rect(center=(590, 350))

    giannis_button = pygame.image.load("files/giannis/"
                                       "giannis_select.png").convert()
    giannis_button_rect = giannis_button.get_rect(center=(890, 350))

    lamelo_button = pygame.image.load("files/lamelo/"
                                      "lamelo_select.png").convert()
    lamelo_button_rect = lamelo_button.get_rect(center=(1190, 350))

    screen.blit(curry_button, curry_button_rect)
    screen.blit(kd_button, kd_button_rect)
    screen.blit(giannis_button, giannis_button_rect)
    screen.blit(lamelo_button, lamelo_button_rect)
    screen.blit(title, title_rect)
    screen.blit(player_selection, player_selection_rect)

    return (curry_button_rect, kd_button_rect, giannis_button_rect,
            lamelo_button_rect)


def main_menu(screen, clock):
    """ Returns two integers which represent the indexes of chosen characters.

    Args:
        screen: The screen which the game is displayed on.
         clock: The clock responsible for the frames per second.

    Returns:
        Integers chosen by each player.
    """
    selection = True
    p1_turn = True
    p1_i = 0
    p2_i = 0
    click = False

    while selection:

        screen.fill((1, 1, 45))

        (curry_button_rect, kd_button_rect, giannis_button_rect,
         lamelo_button_rect) = characters(
            screen, p1_turn)

        mx, my = pygame.mouse.get_pos()

        if curry_button_rect.collidepoint((mx, my)):
            p1_i, p2_i, p1_turn, selection = choice(click, p1_turn, p1_i, p2_i,
                                                    0, selection)

        if kd_button_rect.collidepoint((mx, my)):
            p1_i, p2_i, p1_turn, selection = choice(click, p1_turn, p1_i, p2_i,
                                                    1, selection)

        if giannis_button_rect.collidepoint((mx, my)):
            p1_i, p2_i, p1_turn, selection = choice(click, p1_turn, p1_i, p2_i,
                                                    2, selection)

        if lamelo_button_rect.collidepoint((mx, my)):
            p1_i, p2_i, p1_turn, selection = choice(click, p1_turn, p1_i, p2_i,
                                                    3, selection)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(60)

    return p1_i, p2_i


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, possession, p1_i, p2_i):
        super().__init__()
        self.sprites = []
        self.is_animating = False

        if possession:
            for i in range(7):
                self.sprites.append(
                    pygame.image.load(f"{players[p1_i][1]}"))
        else:
            for i in range(7):
                self.sprites.append(
                    pygame.image.load(f"{players[p2_i][1]}"))

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.midbottom = [pos_x, pos_y]

    def animate(self, player1_x, player1_y):
        self.rect.midbottom = [player1_x, player1_y]
        self.is_animating = True

    def update(self):
        if self.is_animating:
            self.current_sprite += 0.3

            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0

            self.image = self.sprites[int(self.current_sprite)]


class Points(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load("files/png/2pnts.png").convert()
        self.rect = self.image.get_rect(midtop=(x, y))


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


def ball_path(startx, starty, power, ang, time_):
    """Returns a new set of coordinates using projectile motion based on the
    starting position

    Args:
        startx: Start x coordinate value
        starty: Start y coordinate value
        power: The amount of power
        ang: The angle
        time_: An amount of time

    Returns:
        A list containing a newly calculated x and y value.
    """
    velx = math.cos(ang) * power
    vely = math.sin(ang) * power

    distx = velx * time_
    disty = (vely * time_) + ((9 * time_ ** 2) / 2)

    newx = round(startx - distx)
    newy = round(starty + disty)

    return [newx, newy]


def find_angle(player1_x, player1_y, midpnt):
    """Returns an integer representing the angle the ball will be shot at.

    Args:
        player1_x: Player's current x value.
        player1_y: Player's current y value.
        midpnt: List containing the x and y values of the calculated midpoint

    Returns:
        An integer representing an angle value.
    """
    s_x = midpnt[0]
    s_y = midpnt[1]
    try:
        angle = math.atan((s_y - player1_y) / (s_x - player1_x))
    except:
        angle = math.pi / 2

    if player1_y < s_y and player1_x > s_x:
        angle = abs(angle)
    elif player1_y < s_y and player1_x < s_x:
        angle = math.pi - angle
    elif player1_y > s_y and player1_x < s_x:
        angle = math.pi + abs(angle)
    elif player1_y > s_y and player1_x > s_x:
        angle = (math.pi * 2) - angle

    return angle


def midpoint(playerx, playery, posx, posy):
    midx = ((playerx + posx) / 2)
    midy = ((playery + posy) / 2)

    return [midx, midy - 13]


def bucket(p1_score, p2_score, points, possession):
    if possession:
        p1_score += points
    else:
        p2_score += points

    return p1_score, p2_score


def flip(boolean):
    boolean = not boolean
    return boolean


def p_soda(possession, p1_i, p2_i):
    """Returns a spritehseet, list of images, and a image.

    Args:
        possession: A boolean that represents who currently has the ball.
        p1_i: An integer
        p2_i: An integer

    Returns: A spritehseet, a list containing images of both players'
    characters dribbling, and images of the players' characters while on
    defense.
    """
    if possession:
        p1_spritesheet = Spritesheet(f"{players[p1_i][0]}.png")
        player1 = []
        for i in range(10):
            player1.append(p1_spritesheet.parse_sprite
                           (f"{players[p1_i][0]}-{i}.png"))
        player2_d = pygame.image.load(
            f"{players[p2_i][2]}.png").convert_alpha()
    else:
        p1_spritesheet = Spritesheet(f"{players[p2_i][0]}.png")
        player1 = []
        for i in range(10):
            player1.append(p1_spritesheet.parse_sprite
                           (f"{players[p2_i][0]}-{i}.png"))
        player2_d = pygame.image.load(
            f"{players[p1_i][2]}.png").convert_alpha()

    return p1_spritesheet, player1, player2_d


def poss_tru(player1_x, player1_y, player1_x_change, player1_y_change,
             player2_d_x_change, player2_d_y_change,
             possession, jumping, moving_sprites, jumper, shoot, line, midpnt,
             x, y, t_ime, power, angle, p1_i, p2_i):
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_d:
                player1_x_change = 5
            if event.key == pygame.K_a:
                player1_x_change = -5
            if event.key == pygame.K_w:
                player1_y_change = -5
            if event.key == pygame.K_s:
                player1_y_change = 5

            if event.key == pygame.K_c:
                player = Player(player1_x, player1_y, possession, p1_i, p2_i)
                moving_sprites.add(player)
                player.animate(player1_x + 15, player1_y + 100)
                jumper = flip(jumper)
                if not shoot:
                    shoot = True
                    x = player1_x
                    y = player1_y
                    t_ime = 0

                    power = math.sqrt((line[1][1] - line[0][1]) ** 2 +
                                      (line[1][0] - line[0][0]) ** 2) * 0.45
                    angle = find_angle(player1_x + 30, player1_y + 30,
                                       midpnt)

            if event.key == pygame.K_RIGHT:
                player2_d_x_change = 5
            if event.key == pygame.K_LEFT:
                player2_d_x_change = -5

            if not jumping:
                if event.key == pygame.K_UP:
                    player2_d_y_change = -5
                if event.key == pygame.K_DOWN:
                    player2_d_y_change = 5

                if event.key == pygame.K_SPACE:
                    jumping = True

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_d or event.key == pygame.K_a:
                player1_x_change = 0
            if event.key == pygame.K_w or event.key == pygame.K_s:
                player1_y_change = 0

            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                player2_d_x_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player2_d_y_change = 0

    return (player1_x, player1_y, player1_x_change, player1_y_change,
            player2_d_x_change, player2_d_y_change, possession, jumping,
            moving_sprites, jumper, shoot, line, midpnt, x, y, t_ime, power,
            angle, p1_i, p2_i)


def poss_false(player1_x, player1_y, player1_x_change, player1_y_change,
               player2_d_x_change, player2_d_y_change,
               possession, jumping, moving_sprites, jumper, shoot, line,
               midpnt, x, y, t_ime, power, angle, p1_i, p2_i):
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RIGHT:
                player1_x_change = 5
            if event.key == pygame.K_LEFT:
                player1_x_change = -5
            if event.key == pygame.K_UP:
                player1_y_change = -5
            if event.key == pygame.K_DOWN:
                player1_y_change = 5

            if event.key == pygame.K_n:
                player = Player(player1_x, player1_y, possession, p1_i, p2_i)
                moving_sprites.add(player)
                player.animate(player1_x + 15, player1_y + 100)
                jumper = flip(jumper)
                if not shoot:
                    shoot = True
                    x = player1_x
                    y = player1_y
                    t_ime = 0

                    power = math.sqrt((line[1][1] - line[0][1]) ** 2 +
                                      (line[1][0] - line[0][0]) ** 2) * 0.45
                    angle = find_angle(player1_x + 30, player1_y + 30,
                                       midpnt)

            if event.key == pygame.K_d:
                player2_d_x_change = 5
            if event.key == pygame.K_a:
                player2_d_x_change = -5

            if not jumping:
                if event.key == pygame.K_w:
                    player2_d_y_change = -5
                if event.key == pygame.K_s:
                    player2_d_y_change = 5

                if event.key == pygame.K_v:
                    jumping = True

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                player1_x_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player1_y_change = 0

            if event.key == pygame.K_d or event.key == pygame.K_a:
                player2_d_x_change = 0
            if event.key == pygame.K_w or event.key == pygame.K_s:
                player2_d_y_change = 0

    return (player1_x, player1_y, player1_x_change, player1_y_change,
            player2_d_x_change, player2_d_y_change, possession, jumping,
            moving_sprites, jumper, shoot, line, midpnt, x, y, t_ime,
            power, angle, p1_i, p2_i)


def boundary(y, point1, point2):
    """Returns a Y value which simulates a boundary

    Args:
        y: Current y value
        point1: A integer
        point2: A integer

    Returns:
        An integer representing Y's new given value.
    """
    if y >= point1:
        y = point1
    if y <= point2:
        y = point2

    return y


def pre_func(pre_buck, buck, pre_swat, swat):
    """Returns 2 booleans

    Args:
        pre_buck: A boolean
        buck: A boolean
        pre_swat: A boolean
        swat: A boolean

    Returns:
        The stored boolean values of buck and swat.
    """
    if buck:
        pre_buck = buck
    elif swat:
        pre_swat = swat

    return pre_buck, pre_swat


def show_score(screen, p1_score, p2_score):
    font = pygame.font.Font("files/font/pixel-love.ttf", 25)
    p1_points = font.render(f"{p1_score}", False, (255, 255, 255))
    p1_points_rect = p1_points.get_rect(center=(861, 274))
    p2_points = font.render(f"{p2_score}", False, (255, 255, 255))
    p2_points_rect = p2_points.get_rect(center=(668, 274))

    screen.blit(p1_points, p1_points_rect)
    screen.blit(p2_points, p2_points_rect)


def home_away(screen):
    font2 = pygame.font.Font("files/font/dogicapixel.ttf", 6)
    home = font2.render("PLAYER 1", False, (0, 0, 0))
    home_rect = home.get_rect(center=(862, 294))
    away = font2.render("PLAYER 2", False, (0, 0, 0))
    away_rect = away.get_rect(center=(670, 294))

    screen.blit(home, home_rect)
    screen.blit(away, away_rect)


def game_over(p1_score, p2_score, screen):
    if p1_score >= 21:
        winner = "PLAYER 1"
    elif p2_score >= 21:
        winner = "PLAYER 2"

    font3 = pygame.font.Font("files/font/dogicapixelbold.ttf", 25)
    win = font3.render(f"{winner} WINS!", False, (255, 255, 255))
    win_rect = win.get_rect(center=(765, 100))

    font4 = pygame.font.Font("files/font/dogicapixel.ttf", 14)
    restart = font4.render("PRESS R TO RESTART", False, (255, 255, 255))
    restart_rect = restart.get_rect(center=(765, 130))

    screen.blit(win, win_rect)
    screen.blit(restart, restart_rect)


def swish_sound():
    swish_snd = pygame.mixer.Sound("files/sound/44.wav")
    swish_snd.play()


class GameConstants:
    def __init__(self, ph_x, ph_y, player2_d_x_change, player2_d_y_change,
                 index,
                 image_interval, last_update, player1_x, player1_y,
                 player1_x_change, player1_y_change, jumping,
                 jump_height, x, y, t_ime, power, angle, shoot, pre_buck,
                 pre_swat, game_active):
        self.ph_x = ph_x
        self.ph_y = ph_y

        self.player2_d_x_change = player2_d_x_change
        self.player2_d_y_change = player2_d_y_change

        self.index = index
        self.image_interval = image_interval
        self.last_update = last_update

        self.player1_x = player1_x
        self.player1_y = player1_y
        self.player1_x_change = player1_x_change
        self.player1_y_change = player1_y_change

        self.jumping = jumping
        self.jump_height = jump_height

        self.x = x
        self.y = y
        self.t_ime = t_ime
        self.power = power
        self.angle = angle
        self.shoot = shoot

        self.pre_buck = pre_buck
        self.pre_swat = pre_swat

        self.game_active = game_active


def offensive_player(player1_x, player1_y, player1_x_change, player1_y_change,
                     player2_d_x_change, player2_d_y_change, possession,
                     jumping, moving_sprites, jumper, shoot, line, midpnt,
                     x, y, t_ime, power, angle, p1_i, p2_i):
    if possession:
        (player1_x, player1_y, player1_x_change, player1_y_change,
         player2_d_x_change, player2_d_y_change, possession, jumping,
         moving_sprites, jumper, shoot, line, midpnt, x, y, t_ime, power,
         angle, p1_i, p2_i) = poss_tru(
            player1_x, player1_y, player1_x_change, player1_y_change,
            player2_d_x_change, player2_d_y_change,
            possession, jumping, moving_sprites, jumper, shoot, line, midpnt,
            x, y, t_ime,
            power, angle, p1_i, p2_i)
    else:
        (player1_x, player1_y, player1_x_change, player1_y_change,
         player2_d_x_change, player2_d_y_change, possession, jumping,
         moving_sprites, jumper, shoot, line, midpnt, x, y, t_ime, power,
         angle, p1_i, p2_i) = poss_false(
            player1_x, player1_y, player1_x_change, player1_y_change,
            player2_d_x_change, player2_d_y_change,
            possession, jumping, moving_sprites, jumper, shoot, line, midpnt,
            x, y, t_ime,
            power, angle, p1_i, p2_i)

    return (player1_x, player1_y, player1_x_change, player1_y_change,
            player2_d_x_change, player2_d_y_change, possession, jumping,
            moving_sprites, jumper, shoot, line, midpnt, x, y, t_ime, power,
            angle, p1_i, p2_i)
