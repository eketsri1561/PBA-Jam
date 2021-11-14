import pygame
from gameplay_functions import collision_sprites, ball_path, midpoint, bucket,\
    Player, Points, p_soda, boundary, pre_func, show_score, home_away, \
    game_over, swish_sound, main_menu, GameConstants, offensive_player

# Initiating Pygame and creating the game window along with establishing
# some of the png and framerate components.

pygame.init()
pygame.mixer.init()
SCREEN = pygame.display.set_mode((1530, 576))

pygame.display.set_caption("PBA Jam")
ICON = pygame.image.load("files/png/icon.png")
pygame.display.set_icon(ICON)

FPS = 60
CLOCK = pygame.time.Clock()

pygame.mixer.music.load("files/sound/bg.wav")
pygame.mixer.music.play(-1)

P1_SCORE = 0
P2_SCORE = 0

# When player 1 has the ball, the variable is true, when player 2 has the
# ball, it becomes false.

POSSESSION = True

# This will signify if the player is currently shooting a jumpshot or not.

JUMPER = False


def change_pos(possession, p1_score, p2_score, p1_i, p2_i):
    """Runs playball() with updated values.

    Args:
        possession: A boolean representing who has the ball.
        p1_score: Integer representing how many points player 1 has scored.
        p2_score: Integer representing how many points player 2 has scored.
        p1_i: Integer representing player 1's character.
        p2_i: Integer representing player 2's character.

    Returns:
        None
    """
    possession = not possession
    pygame.time.delay(500)
    playball(possession, p1_score, p2_score, False, p1_i, p2_i)


def restart():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                main()


def playball(possession, p1_score, p2_score, jumper, p1_i, p2_i):
    """Holds the main part of the PBA Jam program.

    Args:
        possession: A boolean representing who has the ball.
        p1_score: Integer representing how many points player 1 has scored.
        p2_score: Integer representing how many points player 2 has scored.
        jumper: A boolean representing shooting state.
        p1_i: Integer representing player 1's character.
        p2_i: Integer representing player 2's character.

    Returns:
        None
    """
    gc = GameConstants(928, 328, 0, 0, 0, 20, 0, 928, 325, 0, 0, False, 9,
                       -10, 0, 0, 0, 0, False, False, False, True)

    court = pygame.image.load("files/png/Court.png").convert()

    hoop = pygame.image.load("files/png/hoop.png").convert_alpha()
    hoop_rect = hoop.get_rect(midtop=(217, 225))
    hoop_rect2 = hoop.get_rect(midtop=(1312, 225))

    # This holds the player's jumpshot png

    moving_sprites = pygame.sprite.GroupSingle()
    player = Player(gc.ph_x, gc.ph_y, possession, p1_i, p2_i)
    moving_sprites.add(player)

    # Stores the rect that is in charge of assigning point value

    middy = pygame.sprite.Group()
    points_2 = Points(1220, 345)
    middy.add(points_2)

    # This holds frames and animation of the player with the ball.

    p1_spritesheet, player1, player2_d = p_soda(possession, p1_i, p2_i)
    player2_d_rect = player2_d.get_rect(midbottom=(1090, 430))

    min_jump_height = -1 * gc.jump_height

    ball = pygame.image.load("files/png/ball.png").convert_alpha()
    ball_rect = ball.get_rect(midtop=(gc.x, gc.y))

    while True:

        if gc.shoot:
            if ball_rect.x < 1400:
                gc.t_ime += 0.05
                po = ball_path(gc.x, gc.y, gc.power, gc.angle, gc.t_ime)
                ball_rect.x = po[0]
                ball_rect.y = po[1]
            else:
                gc.shoot = False
                ball_rect.y = -100
                change_pos(possession, p1_score, p2_score, p1_i, p2_i)

        pos_x = hoop_rect2.x
        pos_y = hoop_rect2.y
        midpnt = midpoint(gc.player1_x, gc.player1_y, pos_x, pos_y)
        line = [[gc.player1_x, gc.player1_y], [midpnt[0], midpnt[1]]]

        # Here is how the movements of the players are controlled are
        # established. If possession = True then player 1 has the ball and
        # can used their assigned controls to move around and score. if
        # false, then player 2 has the ball and will use their assigned
        # controls to move their player and score.
        if gc.game_active:
            (gc.player1_x, gc.player1_y, gc.player1_x_change,
             gc.player1_y_change, gc.player2_d_x_change, gc.player2_d_y_change,
             possession, gc.jumping, moving_sprites, jumper, gc.shoot, line,
             midpnt, gc.x, gc.y, gc.t_ime, gc.power, gc.angle, p1_i,
             p2_i) = offensive_player(
                gc.player1_x, gc.player1_y, gc.player1_x_change,
                gc.player1_y_change, gc.player2_d_x_change,
                gc.player2_d_y_change, possession, gc.jumping, moving_sprites,
                jumper, gc.shoot, line, midpnt, gc.x,
                gc.y, gc.t_ime, gc.power, gc.angle, p1_i, p2_i)

        # Jumping in game is regulated in game by imitating the physics of
        # gravity
        if gc.jumping:
            player2_d_rect.y -= gc.jump_height
            gc.jump_height -= 1
            if gc.jump_height <= min_jump_height:
                gc.jumping = False
                gc.jump_height = 8

        # This is used to manage the speed on the offensive player's
        # dribbling animation

        if pygame.time.get_ticks() - gc.last_update > gc.image_interval:
            gc.index = int((gc.index + 1) % len(player1))
            gc.last_update = pygame.time.get_ticks()

        gc.player1_x += gc.player1_x_change
        gc.player1_y += gc.player1_y_change
        player2_d_rect.x += gc.player2_d_x_change
        player2_d_rect.y += gc.player2_d_y_change
        gc.player1_y = boundary(gc.player1_y, 469, 215)

        if not gc.jumping:
            player2_d_rect.bottom = boundary(player2_d_rect.bottom, 573, 318)

        points = collision_sprites(moving_sprites.sprite, middy)
        swat = player2_d_rect.colliderect(ball_rect)
        buck = ball_rect.colliderect(hoop_rect2)

        # This regulates the point system so that points aren't added to the
        # score every frame that the ball collides with the rim. Only if
        # collide was false before it was true will points be added to the
        # score.

        if (not gc.pre_swat and swat) or ball_rect.x > 1409 or ball_rect.y > \
                gc.player1_y + 64:
            change_pos(possession, p1_score, p2_score, p1_i, p2_i)
        elif not gc.pre_buck and buck:
            swish_sound()
            p1_score, p2_score = bucket(p1_score, p2_score, points, possession)
            change_pos(possession, p1_score, p2_score, p1_i, p2_i)

        gc.pre_buck, gc.pre_swat = pre_func(gc.pre_buck, buck, gc.pre_swat,
                                            swat)

        # This is how the components are displayed on to the screen.

        if gc.game_active:
            middy.draw(SCREEN)
            SCREEN.blit(court, (0, 0))
            home_away(SCREEN)
            show_score(SCREEN, p1_score, p2_score)

            if not jumper:
                SCREEN.blit(player1[gc.index], (gc.player1_x, gc.player1_y))
            else:
                moving_sprites.draw(SCREEN)
                moving_sprites.update()

            SCREEN.blit(player2_d, player2_d_rect)
            SCREEN.blit(ball, ball_rect)
            SCREEN.blit(hoop, hoop_rect)
            SCREEN.blit(hoop, hoop_rect2)

            if p1_score >= 21 or p2_score >= 21:
                gc.game_active = False

        else:
            game_over(p1_score, p2_score, SCREEN)
            restart()

        pygame.display.update()
        CLOCK.tick(FPS)


# The game is stored in the main function and when called main runs
# playball, hence running the game.

def main():
    play = False
    if not play:
        p1_i, p2_i = main_menu(SCREEN, CLOCK)
        play = True
    while play:
        playball(POSSESSION, P1_SCORE, P2_SCORE, JUMPER, p1_i, p2_i)
    pygame.quit()


if __name__ == "__main__":
    main()
