import pygame
# from replit import audio
from functions import collision_sprites, ballPath, midpoint, bucket, Player, Points, p_soda, poss_tru, poss_false, boundary, pre_func, show_score, home_away, game_over

# Initiating Pygame and creating the game window along with establishing some of the png and framerate componenets.

pygame.init()
# pygame.mixer.init()
screen = pygame.display.set_mode((1530, 576))

pygame.display.set_caption("PBA Jam")
icon = pygame.image.load("files/png/icon.png")
pygame.display.set_icon(icon)

font = pygame.font.Font("files/font/pixel-love.ttf", 25)
font2 = pygame.font.Font("files/font/dogicapixel.ttf", 6)
font3 = pygame.font.Font("files/font/dogicapixelbold.ttf", 25)
font4 = pygame.font.Font("files/font/dogicapixel.ttf", 14)

fps = 60
clock = pygame.time.Clock()

court = pygame.image.load("files/png/Court.png").convert()

hoop = pygame.image.load("files/png/hoop.png").convert_alpha()
hoop_rect = hoop.get_rect(midtop=(217, 225))
hoop_rect2 = hoop.get_rect(midtop=(1312, 225))

# This holds the rect which will be used to detect if the player's shot is worth 2 or 3 points.

mid_range = pygame.image.load("files/png/2pnts.png").convert()
mid_range_rect = mid_range.get_rect(midtop=(1220, 345))

global p1_score
p1_score = 0
global p2_score
p2_score = 0

# When player 1 has the ball, the variable is true, when player 2 has the ball, it becomes false.

possession = True

# This will signifiy if the player is currently shooting a jumpshot or not.

jumper = False

# change_pos helps gives the illusion of a new possession by calling the game function with new possession, score, and jumper values


def change_pos(possession, p1_score, p2_score):
    possession = not possession
    pygame.time.delay(500)
    playball(possession, p1_score, p2_score, jumper)
    

def restart():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                playball(True, 0, 0, False)



# playball is the function that holds the code which runs PBA Jam. All the varibles before the while loop in the function are set so that everytime playball is called they start the same way.


def playball(possession, p1_score, p2_score, jumper):
    ph_x = 928
    ph_y = 328

    # This holds the player's jumposhot png

    moving_sprites = pygame.sprite.GroupSingle()
    player = Player(ph_x, ph_y, possession)
    moving_sprites.add(player)

    # Stores the rect that is in charge of assigning point value

    middy = pygame.sprite.Group()
    points_2 = Points(1220, 345)
    middy.add(points_2)

    # This holds frames and animation of the player with the ball.

    p1_spritesheet, player1, player2_d = p_soda(possession)

    player2_d_X_change = 0
    player2_d_Y_change = 0
    player2_d_rect = player2_d.get_rect(midbottom=(1090, 430))

    index = 0
    IMAGE_INTERVAL = 20
    last_update = 0

    player1_X = 928
    player1_Y = 325
    player1_X_change = 0
    player1_Y_change = 0

    jumping = False
    jump_height = 9
    min_jump_height = -1 * jump_height

    x = -10
    y = 0
    t_ime = 0
    power = 0
    angle = 0
    shoot = False

    ball = pygame.image.load("files/png/ball.png").convert_alpha()
    ball_rect = ball.get_rect(midtop=(x, y))

    pre_buck = False
    pre_swat = False

    game_active = True

    while True:
                
        if shoot:
            if ball_rect.x < 1400:
                t_ime += 0.05
                po = ballPath(x, y, power, angle, t_ime)
                ball_rect.x = po[0]
                ball_rect.y = po[1]
            else:
                shoot = False
                ball_rect.y = -100
                change_pos(possession, p1_score, p2_score)

        posX = hoop_rect2.x
        posY = hoop_rect2.y
        midpnt = midpoint(player1_X, player1_Y, posX, posY)
        line = [[player1_X, player1_Y], [midpnt[0], midpnt[1]]]

        # Here is how the movements of the players are controlled are established. If possesion = True then player 1 has the ball and can used their assigned controls to move around and score. if false, then player 2 has the ball and will use thier assigned controls to move their player and score.
        if game_active:
            if possession == True:
                player1_X, player1_Y, player1_X_change, player1_Y_change, player2_d_X_change, player2_d_Y_change, possession, jumping, moving_sprites, jumper, shoot, line, midpnt, x, y, t_ime, power, angle = poss_tru(
                    player1_X, player1_Y, player1_X_change, player1_Y_change,
                    player2_d_X_change, player2_d_Y_change, possession, jumping,
                    moving_sprites, jumper, shoot, line, midpnt, x, y, t_ime,
                    power, angle)
            else:
                player1_X, player1_Y, player1_X_change, player1_Y_change, player2_d_X_change, player2_d_Y_change, possession, jumping, moving_sprites, jumper, shoot, line, midpnt, x, y, t_ime, power, angle = poss_false(
                    player1_X, player1_Y, player1_X_change, player1_Y_change,
                    player2_d_X_change, player2_d_Y_change, possession, jumping,
                    moving_sprites, jumper, shoot, line, midpnt, x, y, t_ime,
                    power, angle)

        # Jumping in game is regulated in game by imitating the physics of gravity
        if jumping:

            player2_d_rect.y -= jump_height
            jump_height -= 1
            if jump_height <= min_jump_height:
                jumping = False
                jump_height = 8

        # This is used to manage the speed on the offensive player's dribbling animation

        if pygame.time.get_ticks() - last_update > IMAGE_INTERVAL:
            index = int((index + 1) % len(player1))
            last_update = pygame.time.get_ticks()

        player1_X += player1_X_change
        player1_Y += player1_Y_change
        player2_d_rect.x += player2_d_X_change
        player2_d_rect.y += player2_d_Y_change

        player1_Y = boundary(player1_Y, 469, 215)
        if not jumping:
            player2_d_rect.bottom = boundary(player2_d_rect.bottom, 573, 318)

        points = collision_sprites(moving_sprites.sprite, middy)
        swat = player2_d_rect.colliderect(ball_rect)
        buck = ball_rect.colliderect(hoop_rect2)

        # This regulates the point system so that points aren't added to the score every frame that the ball collides with the rim. Only if collide was false before it was true will points be added to the score.

        if (not pre_swat and swat) or ball_rect.x > 1409 or ball_rect.y > player1_Y + 64:
            change_pos(possession, p1_score, p2_score)
        elif not pre_buck and buck:
            # source = audio.play_file("files/sound/44.wav")
            p1_score, p2_score = bucket(p1_score, p2_score, points, possession)
            change_pos(possession, p1_score, p2_score)

        pre_buck, pre_swat = pre_func(pre_buck, buck, pre_swat, swat)

        # This is how the components are displayed on to the screen.

        if game_active:

        
            # source = audio.play_file("files/sound/bg.mp3", 1, True)
            middy.draw(screen)
            screen.blit(court, (0, 0))
            home_away(screen, font2)
            show_score(screen, font, p1_score, p2_score)
            if jumper == False:
                screen.blit(player1[index], (player1_X, player1_Y))
            if jumper == True:
                moving_sprites.draw(screen)
                moving_sprites.update()

            screen.blit(player2_d, player2_d_rect)
            screen.blit(ball, ball_rect)
            screen.blit(hoop, hoop_rect)
            screen.blit(hoop, hoop_rect2)

            if p1_score >= 21 or p2_score >= 21:
                game_active = False
        
        else:
            # source = audio.play_file("files/sound/end.mp3", 1, True)
            game_over(p1_score, p2_score, font3, font4, screen)
            restart()

        pygame.display.update()
        clock.tick(fps)

# The game is stored in the main function and when called main runs playball, hence running the game.


def main():
    hoop = True
    while hoop:
        playball(possession, p1_score, p2_score, jumper)
    pygame.quit()


if __name__ == "__main__":
    main()
