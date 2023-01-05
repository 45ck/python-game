import sys, pygame, pygame.gfxdraw, math, os, random
from .sound import Sound
from .game_objects import Bullet, Ballon, Cannon
from .user_interface import UserInterface

# global settings for pygame 
frames_per_second = 50
window_height = 600
window_width = 1000

# change sound effect for when the player toggles/changes between burst-fire and single-fire mode
change_sound = Sound("change.mp3")

# shoot sound effect for when the player shoots the cannon
shoot_sound = Sound("cannon.mp3")

# sound for when game finishes
finish_sound = Sound("finish.mp3")

# sound for when game starts
begin_sound = Sound("begin.mp3")

def start(is_restart = False):
    if is_restart:
        has_started_game = True
        in_game = True
    else:
        in_game = True
        has_started_game = False

    #the total number of missed shots the player has missed.
    missedShots = 0

    # tell python we are starting
    pygame.init()
    pygame.font.init()
    
    global ballon_speed
    ballon_speed = 5

    clock = pygame.time.Clock()
    display = pygame.display.set_mode((window_width, window_height), 0)
    ui = UserInterface(display)

    #import background image
    relative_directory = os.path.dirname(os.path.realpath(__file__));
    backgroundImage = pygame.image.load(relative_directory + "\\assets\\background.png")
    backgroundImage = pygame.transform.scale(backgroundImage, (window_width, window_height))

    # set up the ballon game object
    global ballon
    ballon = Ballon((50, 10))
    ballon.color = (255, 0, 0)
    ballon.velocity = ballon_speed
    ballon.size = 22

    # setup the cannon game object
    global cannon
    cannon = Cannon((window_width-50, 550))
    cannon.color = (0, 0, 0)
    cannon.move_speed = 6
    cannon.use_constraints = True
    cannon.maximum_y = window_height
    cannon.minimum_y = 0

    # all active game objects are stored in this array so that they can be updated on each frame
    global active_game_objects
    active_game_objects = [cannon, ballon]

    # all bullets are stored in an array of bullets to keep track of them
    global bullets
    bullets = []

    # if this is true, the cannon will fire multiple bullets at once.
    multiple_bullets_mode = False
    bullets_shot_burst = 3  # total number of bullets shot when firing a semi-auto
    bullet_burst_delay_ms = 100   #the time between the burst firing of the bullet.
    bullet_stack = 0 #total number of bullets that are queued in stack for firing
    last_fire =  pygame.time.get_ticks() # the last time the cannon was fired (in game ticks)

    #settings for animated text at the end of the game.
    current_animated_text_size = 30
    animated_text_size_max = 40
    animated_text_size_min = 30
    animated_text_size_additive = 0.5   #the animation speed

    #this loop repeats for ever and is the main loop inside of the game.
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  #if the user closes the game, exit.
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                # make sure that we have fired all bullets that need to be fired and that the fire button (space key) is pressed.
                if event.key == pygame.K_SPACE and bullet_stack == 0:
                    amount_bullets_shots = 1

                    # so that the cannon can fire 1 or many bullets, there is a "bullet stack" in place
                    # this stack is there so that a delay between shots can be implemented 
                    if multiple_bullets_mode == True:
                        amount_bullets_shots = bullets_shot_burst
                    
                    # add bullets to firing stack
                    bullet_stack += amount_bullets_shots
                #if the player is in the start menu, than TAB is to start the game.
                if event.key == pygame.K_TAB and has_started_game == False:
                    in_game = True
                    has_started_game = True
                    begin_sound.play()
                # if player presses the tab key than restart the game.
                if event.key == pygame.K_TAB and in_game == False:
                    in_game = True
                    begin_sound.play()
                    start(True)
                # if the user presses E (toggle burst fire for cannon)
                if event.key == pygame.K_e:
                    multiple_bullets_mode = not multiple_bullets_mode #invert boolean to be opposite of whatever it is, 
                                                                      # EG: if it's true it will become false, and vice versa.
                    change_sound.play() #play change sound effect for changing from multi-bullet to single-bullet
        #display background image no matter if we are in the game or have completed the game.
        display.blit(backgroundImage, (0,0))
        
        # if we are in the start menu
        if has_started_game == False:
             ui.create_text("Shoot the Ballon!", (275, 150), 65)
             ui.create_text("Press TAB to start!", (310, 250), 45)
             ui.create_text("Press SPACE to shoot the cannon", (280, 310), 30)
             ui.create_text("Press E to switch between mutli-fire and single-fire mode.", (100, 350), 30)
        # if we are in the finish-game menu
        elif in_game == False:
            ui.create_text("Game Finished!", (300, 200), 65)
            # this will loop through and decrease or increase the size of the animated text to give it a zoom in and out animation effect.
            if current_animated_text_size > animated_text_size_max or current_animated_text_size < animated_text_size_min:
                animated_text_size_additive = -animated_text_size_additive  # invert text size
            current_animated_text_size += animated_text_size_additive
            ui.create_text("Press TAB to restart the game!", (300, 300), int(current_animated_text_size))
        # if we are in the game and not in any menus
        elif in_game:
            # render each active game object
            for game_obj in active_game_objects:
                game_obj.update(display)

            # this bounces the ballon and and down.
            if ballon.y >= window_height and ballon.velocity > 0:
                ballon.velocity = -5
            elif ballon.y <= 0 and ballon.velocity < 0:
                ballon.velocity = 5

            # this will make sure that the ballon is always been pushed.
            ballon.push_y()
            
            # controls the movement of the cannon.
            if pygame.key.get_pressed()[pygame.K_UP]:
                cannon.move_up()
            elif pygame.key.get_pressed()[pygame.K_DOWN]:
                cannon.move_down()
            
            #loop over each bullet and see if the bullet is in the radius of the ballon
            for bullet in bullets:
                x1, y1 = bullet.x, bullet.y
                x2, y2 = ballon.x, ballon.y
                distance = math.hypot(x1 - x2, y1 - y2)
                if distance <= ballon.size + 10: 
                    #if the bullet is in the radius of the ballon, then end the game.
                    in_game = False
                    finish_sound.play()
                if bullet.x <= 0:
                    #if the bullet is not in the radius of the ballon, than continue and add a missed shot to the total missed shots count
                    missedShots += 1
                    bullets.remove(bullet)
            
            time_now = pygame.time.get_ticks() 
            # if we can fire a bullet, and we have bullets to fire in the stack
            if time_now  - last_fire >= bullet_burst_delay_ms and bullet_stack > 0:
                last_fire = time_now 
                shoot_bullet()
                bullet_stack -= 1
            
        #update the window to show all changes that have been made since last update
        pygame.display.update()
        #delay so that frame rate is consistent
        clock.tick(frames_per_second)

# shoot the bullet from the gun in the game, 
# this will spawn in the bullet object and register it as an active game object
def shoot_bullet():
    bullet = Bullet((window_width-75, cannon.y)) 
    bullet.color = (30, 30, 30) 
    bullet.size = 5

    #bullet goes 10 times the speed of the ballon - since the bullet is going left it is decreasing in pixels, so it must be negative.
    bullet.velocity = -10 * ballon_speed   

    # we don't want the bullet to continue past the window, so we will stop the bullet at the border of the window.
    bullet.minimum_x = 0
    bullet.maximum_x = window_width
    bullet.minimum_y = 0
    bullet.maximum_y = window_height
    bullet.use_constraints = True
    
    #make sure the object is in the array of objects to render 
    active_game_objects.append(bullet)
    bullets.append(bullet)

    shoot_sound.play() # play sound effect for cannon
