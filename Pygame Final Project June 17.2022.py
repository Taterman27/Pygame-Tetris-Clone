# Nathan Becker
# May 27 2022
# Final Project (Tetris)

# Enhancements - Everything added after the base gameplay
'''
Upcoming blocks display - right hand side of UI
 - Shows upcoming blocks

Holding blocks - left hand side of UI
 - Pressing shift holds the block and allows the player to swap to it whenever
 
Shuffling Music
 - Various NES tracks play
   1. Tetris - Theme A (Gameboy)
   2. Tetris - Theme B (Gameboy)
   3. Tetris - End Results (Gameboy)
   4. Dr. Mario - Fever (NES)
   5. Dr. Mario - Chill (NES)
   
Score Tracking
 - Tracks score based on how many lines have been cleared
 
Scrolling Background
 - Visual effect
 - Background is made of two layers
 
Animations
 - Animation for clearing lines and for hard dropping blocks
 - Highlights the line cleared or block placed

Highscore Saving
 - Writes the highscore to a file
 - Retrieves this high score from the file
'''

import pygame
from pygame import mixer
import math
import random
pygame.init()
mixer.init()
size = (640,880)
screen = pygame.display.set_mode(size)
font = pygame.font.SysFont('Impact', 30, False, False)
#===============DRAW HERE====================
#"Static" drawing code can go here:
RED = (255,0,0) # 0 - 255
PURPLE = (144,49,212)
BLUE = (0,100,255)
GREEN = (49,212,84)
YELLOW = (250,214,31)
CYAN = (0,255,255)
BLACK = (0,0,0)
ORANGE = (255,125,0)
WHITE = (255,255,255)
GREY = (100,100,100)

# Text
Rules1 = font.render("Controls", True, WHITE)
Rules2 = font.render("A - Left | D - Right | S - Soft Drop", True, WHITE)
Rules3 = font.render("W - Hard Drop | Left Arrow - Rotate Left", True, WHITE)
Rules4 = font.render("Right Arrow - Rotate Right | Shift - Hold", True, WHITE)
Rules5 = font.render("Score", True, WHITE)
Rules6 = font.render("Line clear - 100 points", True, WHITE)

# Music
current_song = random.randrange(0,5)
if current_song == 0:
    mixer.music.load('Music\\tetris-1.mp3')
if current_song == 1:
    mixer.music.load('Music\\tetris-2.mp3')
if current_song == 2:
    mixer.music.load('Music\\tetris-3.mp3')
if current_song == 3:
    mixer.music.load('Music\\tetris-4.mp3')
if current_song == 4:
    mixer.music.load('Music\\tetris-5.mp3')
mixer.music.play()
current_song = 0 # For music shuffle feature

Tetromino = pygame.image.load('Textures\Tetromino.png')
Empty_Tile = pygame.image.load('Textures\Empty Grid.png')

# .convert() improves performance by converting pixel formats once rather than every frame. Without it, the game is way more laggy
# Only needed on larger textures, like the background and UI
# Backgrounds
BackgroundLayer1 = pygame.image.load('Textures\Background-1.png').convert() 
BackgroundLayer2 = pygame.image.load('Textures\Background-2.png').convert_alpha()
BackgroundLayer3 = pygame.image.load('Textures\Background-3.png').convert_alpha() 

# Menu and UI
UI = pygame.image.load('Textures\\UI.png').convert_alpha() 
Logo = pygame.image.load('Textures\Logo.png').convert_alpha() 
Lose_Screen = pygame.image.load('Textures\\Lose_Screen.png').convert_alpha()
Menu = pygame.image.load('Textures\\Main Menu.png').convert_alpha() 
Menu = pygame.transform.scale(Menu, (640,880))
Logo = pygame.transform.scale(Logo, (609,261))

# Menu Buttons
Back_Button = pygame.image.load('Textures\\Back_button.png')
Play_Button = pygame.image.load('Textures\\Play_button.png')
Quit_Button = pygame.image.load('Textures\\Quit_button.png')
Rules_Button = pygame.image.load('Textures\\Rules_button.png')

# Menu Borders
Small_Border = pygame.image.load('Textures\\Small_Button_Border.png')
Border = pygame.image.load('Textures\\Button_Border.png')
Textbox_Border = pygame.image.load('Textures\\Textbox_Border.png')

# Upcoming block display
upcoming_block_Z = pygame.image.load('Textures\Z Block.png')
upcoming_block_Square = pygame.image.load('Textures\Square Block.png')
upcoming_block_S = pygame.image.load('Textures\S Block.png')
upcoming_block_T = pygame.image.load('Textures\T Block.png')
upcoming_block_L = pygame.image.load('Textures\L Block.png')
upcoming_block_J = pygame.image.load('Textures\J Block.png')
upcoming_block_Line = pygame.image.load('Textures\Line Block.png')
# Scaling the images
upcoming_block_Z = pygame.transform.scale(upcoming_block_Z, (60,40))
upcoming_block_Square = pygame.transform.scale(upcoming_block_Square, (40,40))
upcoming_block_S = pygame.transform.scale(upcoming_block_S, (60,40))
upcoming_block_T = pygame.transform.scale(upcoming_block_T, (60,40))
upcoming_block_L = pygame.transform.scale(upcoming_block_L, (60,40))
upcoming_block_J = pygame.transform.scale(upcoming_block_J, (60,40))
upcoming_block_Line = pygame.transform.scale(upcoming_block_Line, (80,20))

# Icons
icon_red = pygame.image.load('Textures\Red.png')
icon_green = pygame.image.load('Textures\Green.png')
icon_yellow = pygame.image.load('Textures\Yellow.png')
icon_purple = pygame.image.load('Textures\Purple.png')
icon_blue = pygame.image.load('Textures\Blue.png')
icon_orange = pygame.image.load('Textures\Orange.png')
icon_cyan = pygame.image.load('Textures\Cyan.png')

playgrid = [] # Stores state of all tiles (0 is empty, 1 is a placed tile, and 2 is an active tile)
colour = [] # Stores colour of all tiles
for i in range(0,220): # Adds 210 rows to both lists
    colour.append(WHITE)
    playgrid.append(0)
buttons = False # Input variables
middleClicked = False
rightClicked = False
leftClicked = False
UP = False
DOWN = False
RIGHT = False
LEFT = False
ROTATE_L = False
ROTATE_R = False
shift = False
mpos = pygame.mouse.get_pos() # Mouse position
mouse_x = mpos[0]
mouse_y = mpos[1]
background_x = 0 # Scrolling Background effect
Flip_layers = False # Decides if a background layer should be moved to the other side of the screen, for seamless scrolling
speed = 1 # How fast the time increases
time = 0 # Frame counter, changed by speed variable. When over 60, the block falls and the time is set to 0
repeat_lr = 0 # A timer that counts down, when it reaches 0, the movement input will repeat. It is also set to 0 when a key is released, so inputs won't be ignored and won't happen every frame
repeat_down = 0 # A similar timer to repeat_lr, but for the drop key    
animation_timer = 0 # Timer used by all animations
hard_drop_animation = False # If true, the hard-drop animation is played
hard_drop_animation_initiated = False # Hard drop animation. Block snaps to bottom and immedietly gets placed
line_clear_animation_initiated = False
line_clear_animation = False
debug = False
hold = -1
animated_tiles = []
animated_tile_colour = []
upcoming_blocks = random.sample(range(7), 7)
block_bag = random.sample(range(7), 7) # After initial list of upcoming blocks is generated, a separate list is generated. This list will only randomize if its empty, and will only contain one of each block type. The first block in the "bag" will be put at the end of upcoming_blocks when a new block is needed
pygame.display.set_caption('Tetris')
pygame.display.set_icon(icon_red)
score = 0
file = open("Highscores.txt", 'a') # Creates the file if it doesn't exist, otherwise does nothing
file.close()
file = open("Highscores.txt", 'r') # Opens the file in read mode
if file.read() == "": # Checks if the file is empty, and sets the highscore to 0
    highscore = 0
else:
    file.seek(0) # Starts reading the file from the start again
    highscore = int(file.read()) # Sets the highscore to the first line of the file
file.close() # Closes the file
HighscoreDisplay = font.render(str(highscore), True, WHITE)
move_down = False # Variable that overrides the automatic block dropping, and moves the block down when the player hits S
swap_cooldown = False # Variable that stores whether or not a new block has been created since the last block was held. If not, a swap doesn't happen
ticks_on_ground = 0 # Variable that counts how many attempts have been made to place a block, a block will only place if 3 attempts are made.
lose = False
write_highscore = False # Variable to tell whether or not the highscore needs to be updated
#===============END DRAWING==================
done = False
clock = pygame.time.Clock()
title = True
rules = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                UP = True
            if event.key == pygame.K_s:
                DOWN = True
            if event.key == pygame.K_d:
                RIGHT = True
            if event.key == pygame.K_a:
                LEFT = True
            if event.key == pygame.K_RIGHT:
                ROTATE_R = True
            if event.key == pygame.K_LEFT:
                ROTATE_L = True
            if event.key == pygame.K_l:
                debug = True            
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                shift = True            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                UP = False
            if event.key == pygame.K_a:
                LEFT = False
                repeat = 0
            if event.key == pygame.K_s:
                DOWN = False
            if event.key == pygame.K_d:
                RIGHT = False
                repeat = 0
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                shift = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            buttons = pygame.mouse.get_pressed()
            if buttons[0] == True:
                leftClicked = True
            if buttons[1] == True:
                middleClicked = True
                title = False
            if buttons[2] == True:
                rightClicked = True
        if event.type == pygame.MOUSEBUTTONUP:
            buttons = pygame.mouse.get_pressed()
            if buttons[0] == False:
                leftClicked = False
            if buttons[1] == False:
                middleClicked = False
            if buttons[2] == False:
                rightClicked = False
    # Shuffle Music
    if not pygame.mixer.music.get_busy():
        current_song = random.randrange(0,5)
        if current_song == 0:
            mixer.music.load('Music\\tetris-1.mp3')
        if current_song == 1:
            mixer.music.load('Music\\tetris-2.mp3')
        if current_song == 2:
            mixer.music.load('Music\\tetris-3.mp3')
        if current_song == 3:
            mixer.music.load('Music\\tetris-4.mp3')
        if current_song == 4:
            mixer.music.load('Music\\tetris-5.mp3')
        mixer.music.play()
    
    # Mouse Position
    mpos = pygame.mouse.get_pos()
    mouse_x = mpos[0]
    mouse_y = mpos[1]
    if title:
        screen.blit(Logo, [15,100])
        if title and not rules and not lose:
            if mouse_x > 40 and mouse_x < 600 and mouse_y > 500 and mouse_y < 580: # Play Button
                pygame.draw.rect(screen,WHITE,[48,508,544,66])
                if leftClicked:
                    title = False
            else:
                pygame.draw.rect(screen,GREY,[48,508,544,66])
            screen.blit(Border, [40,500])
            screen.blit(Play_Button, [40,500])
            if mouse_x > 40 and mouse_x < 600 and mouse_y > 600 and mouse_y < 680: # Rules Button
                pygame.draw.rect(screen,RED,[48,608,544,66])
                if leftClicked:
                    rules = True
            else:
                pygame.draw.rect(screen,GREY,[48,608,544,66])
            screen.blit(Border, [40,600])   
            screen.blit(Rules_Button, [40,600])
            if mouse_x > 160 and mouse_x < 480 and mouse_y > 700 and mouse_y < 780: # Quit Button
                pygame.draw.rect(screen,RED,[168,708,304,64])
                if leftClicked:
                    done = True
            else:
                pygame.draw.rect(screen,GREY,[168,708,304,64])
            screen.blit(Small_Border,[160,700])
            screen.blit(Quit_Button, [160,700])
            
            # Main Menu Highscore Display
            pygame.draw.rect(screen,GREY,[168,828,304,64])
            HighscoreText = font.render("Highscore:", True, WHITE)
            screen.blit(HighscoreText,[220,840])
            screen.blit(HighscoreDisplay,[360,840])
            screen.blit(Small_Border,[160,820])
        elif rules:
            pygame.draw.rect(screen,GREY,[40,400,560,300])
            screen.blit(Rules1, [40,400])
            screen.blit(Rules2, [60,450])
            screen.blit(Rules3, [60,500])
            screen.blit(Rules4, [60,550])
            screen.blit(Rules5, [60,600])
            screen.blit(Rules6, [60,650])
            if mouse_x > 160 and mouse_x < 500 and mouse_y > 720 and mouse_y < 800:
                pygame.draw.rect(screen,RED,[168,728,304,64])
                if leftClicked:
                    rules = False
                    leftClicked = False # Prevents the user from clicking the quit button afterwards
            else:
                pygame.draw.rect(screen,GREY,[168,728,304,64])
            screen.blit(Back_Button,[160,720])
            screen.blit(Small_Border,[160,720])
            screen.blit(Textbox_Border,[28,388])
        elif lose:
            if write_highscore:
                file = open("Highscores.txt", 'w') # Opens the file in write mode
                file.write(str(highscore)) # Writes the highscore to the file
                file.close() # Closes the file
            pygame.draw.rect(screen,GREY,[40,400,560,300])
            LoseScoreDisplay = font.render(str(last_score), True, WHITE)
            HighscoreDisplay = font.render(str(highscore), True, WHITE)
            screen.blit(LoseScoreDisplay, [105,655])
            screen.blit(HighscoreDisplay, [105,553])
            if mouse_x > 160 and mouse_x < 500 and mouse_y > 720 and mouse_y < 800:
                pygame.draw.rect(screen,RED,[168,728,304,64])
                if leftClicked:
                    lose = False
                    leftClicked = False # Prevents the user from clicking the quit button afterwards
            else:
                pygame.draw.rect(screen,GREY,[168,728,304,64]) 
            screen.blit(Back_Button,[160,720])
            screen.blit(Small_Border,[160,720])
            screen.blit(Lose_Screen,[0,0])
            screen.blit(Textbox_Border,[28,388])
        # Resets all game variables if on the title screen
        playgrid = [] # Stores state of all tiles (0 is empty, 1 is a placed tile, and 2 is an active tile)
        colour = [] # Stores colour of all tiles
        for i in range(0,220): # Adds 210 rows to both lists
            colour.append(WHITE)
            playgrid.append(0)
        score = 0
        speed = 1 
        time = 0 
        repeat_lr = 0
        repeat_down = 0
        animation_timer = 0 
        hard_drop_animation = False 
        hard_drop_animation_initiated = False
        line_clear_animation_initiated = False
        line_clear_animation = False
        animated_tiles = []
        animated_tile_colour = []
        upcoming_blocks = random.sample(range(7), 7)
        block_bag = random.sample(range(7), 7)
        hold = -1
        block_swapped = False
        move_down = False
        ticks_on_ground = 0
    else:
        if debug and leftClicked:
            colour[((mouse_x-120)//40)+(10*((mouse_y-40)//40))] = RED
            playgrid[((mouse_x-120)//40)+(10*((mouse_y-40)//40))] = 1
        # Hold mechanic
        if shift and hold == -1 and not swap_cooldown: 
            hold = block_type
            used_block = upcoming_blocks[0]
            upcoming_blocks = upcoming_blocks[1:]
            block_swapped = True
            swap_cooldown = True
        elif shift and hold != -1 and not swap_cooldown:
            used_block = hold
            hold = block_type
            block_swapped = True
            swap_cooldown = True
        # Blocks, generate shape
        if len(upcoming_blocks) < 7:
            upcoming_blocks.append(block_bag[0])
            block_bag = block_bag[1:]
        if len(block_bag) == 1:
            block_bag = random.sample(range(7), 7)
        if playgrid.count(2) == 0:
            swap_cooldown = False
            if playgrid[3:7].count(1) < 1 and playgrid[13:17].count(1) < 1:
                if upcoming_blocks[0] == 0:
                    block_pos = [3,4,14,15] # Goes from furthest left to furthest right
                    block_type = 0 # Z Block 
                    block_colour = RED
                    pygame.display.set_icon(icon_red)
                if upcoming_blocks[0] == 1:
                    block_pos = [4,5,14,15]
                    block_type = 1 # Square Block
                    block_colour = YELLOW
                    pygame.display.set_icon(icon_yellow)
                if upcoming_blocks[0] == 2:
                    block_pos = [13,14,4,5] 
                    block_type = 2 # S Block
                    block_colour = GREEN
                    pygame.display.set_icon(icon_green)
                if upcoming_blocks[0] == 3:
                    block_pos = [13,14,4,15] 
                    block_type = 3 # T Block
                    block_colour = PURPLE
                    pygame.display.set_icon(icon_purple)
                if upcoming_blocks[0] == 4:
                    block_pos = [13,14,15,5]
                    block_type = 4 # Orange L Block
                    block_colour = ORANGE
                    pygame.display.set_icon(icon_orange)
                if upcoming_blocks[0] == 5:
                    block_pos = [3,13,14,15]
                    block_type = 5 # Blue L Block
                    block_colour = BLUE
                    pygame.display.set_icon(icon_blue)
                if upcoming_blocks[0] == 6:
                    block_pos = [13,14,15,16]
                    block_type = 6 # Line Block
                    block_colour = CYAN
                    pygame.display.set_icon(icon_cyan)
                block_swapped = False
                upcoming_blocks = upcoming_blocks[1:]
                block_rotation = 0 # 0-1 or 0-3 depending on block
                block_row = 0
                First = block_pos[0]%10 # The first block must be the furthest to the left for collision detection
                Last = block_pos[-1]%10
                shift = False
            else:
                # The player loses if they reach the top of the screen
                if score > highscore:
                    highscore = score
                lose = True
                last_score = score
                write_highscore = True
                title = True              
        elif block_swapped:
            if playgrid[3:7].count(1) < 1 and playgrid[13:17].count(1) < 1:
                if used_block == 0:
                    block_pos = [3,4,14,15] # Goes from furthest left to furthest right
                    block_type = 0 # Z Block 
                    block_colour = RED
                    pygame.display.set_icon(icon_red)
                if used_block == 1:
                    block_pos = [4,5,14,15]
                    block_type = 1 # Square Block
                    block_colour = YELLOW
                    pygame.display.set_icon(icon_yellow)
                if used_block == 2:
                    block_pos = [13,14,4,5] 
                    block_type = 2 # S Block
                    block_colour = GREEN
                    pygame.display.set_icon(icon_green)
                if used_block == 3:
                    block_pos = [13,14,4,15] 
                    block_type = 3 # T Block
                    block_colour = PURPLE
                    pygame.display.set_icon(icon_purple)
                if used_block == 4:
                    block_pos = [13,14,15,5]
                    block_type = 4 # Orange L Block
                    block_colour = ORANGE
                    pygame.display.set_icon(icon_orange)
                if used_block == 5:
                    block_pos = [3,13,14,15]
                    block_type = 5 # Blue L Block
                    block_colour = BLUE
                    pygame.display.set_icon(icon_blue)
                if used_block == 6:
                    block_pos = [13,14,15,16]
                    block_type = 6 # Line Block
                    block_colour = CYAN
                    pygame.display.set_icon(icon_cyan)
                block_swapped = False
                block_rotation = 0 # 0-1 or 0-3 depending on block
                block_row = 0
                First = block_pos[0]%10 # The first block must be the furthest to the left for collision detection
                Last = block_pos[-1]%10
                shift = False            
            else:
                # The player loses if they reach the top of the screen
                if score > highscore:
                    highscore = score
                lose = True
                last_score = score
                write_highscore = True
                title = True
        # Player movement
        # Block movement handeled here
        if ROTATE_R or ROTATE_L:
            nudge_failed = False
            lowest = 0
            if ROTATE_R:
                block_change_1 = 0 # Stores the movement changes of each block
                block_change_2 = 0 
                block_change_3 = 0
                block_change_4 = 0      
                previous_rotation = block_rotation
                # Add this if block goes off right side of screen when rotating - and block_pos[-1]%10 != 9 
                # Add this if block goes off left side of screen when rotating - and block_pos[0]%10 != 0
                if block_type == 0 and block_rotation == 0: # Z block rotations
                    block_change_1 = 10
                    block_change_2 = 19
                    block_change_3 = -10
                    block_change_4 = -1
                    block_rotation = 1
                elif block_type == 0 and block_rotation == 1 and block_pos[-1]%10 != 9:
                    block_change_1 = -10
                    block_change_2 = -19
                    block_change_3 = 10
                    block_change_4 = 1
                    block_rotation = 0
                elif block_type == 2 and block_rotation == 0: # S block rotations
                    block_change_1 = -9 
                    block_change_3 = 11
                    block_change_4 = 20
                    block_rotation = 1
                elif block_type == 2 and block_rotation == 1 and block_pos[-1]%10 != 1:
                    block_change_1 = 9 
                    block_change_3 = -11
                    block_change_4 = -20
                    block_rotation = 0
                elif block_type == 3 and block_rotation == 0: # T block rotations
                    block_change_1 = 11
                    block_rotation = 1
                elif block_type == 3 and block_rotation == 1 and block_pos[0]%10 != 0:
                    block_change_1 = -11
                    block_change_3 = 20
                    block_rotation = 2
                elif block_type == 3 and block_rotation == 2:
                    block_change_4 = -11
                    block_rotation = 3
                elif block_type == 3 and block_rotation == 3 and block_pos[-1]%10 != 9:
                    block_change_3 = -20
                    block_change_4 = 11
                    block_rotation = 0
                elif block_type == 4 and block_rotation == 0: # Orange L block rotations
                    block_change_1 = -9
                    block_change_3 = 9
                    block_change_4 = 20
                    block_rotation = 1
                elif block_type == 4 and block_rotation == 1 and block_pos[0]%10 != 0:
                    block_change_1 = 9
                    block_change_3 = -1
                    block_change_4 = -10
                    block_rotation = 2
                elif block_type == 4 and block_rotation == 2:
                    block_change_1 = -10
                    block_change_3 = -19
                    block_change_4 = 9
                    block_rotation = 3
                elif block_type == 4 and block_rotation == 3 and block_pos[-1]%10 != 9 :
                    block_change_1 = 10
                    block_change_3 = 11
                    block_change_4 = -19
                    block_rotation = 0
                elif block_type == 5 and block_rotation == 0: # Blue L block rotations
                    block_change_1 = 1
                    block_change_2 = 11
                    block_change_4 = -10
                    block_rotation = 1
                elif block_type == 5 and block_rotation == 1 and block_pos[0]%10 != 0:
                    block_change_1 = 9
                    block_change_2 = 1
                    block_change_4 = 10
                    block_rotation = 2
                elif block_type == 5 and block_rotation == 2:
                    block_change_1 = 10
                    block_change_2 = -1
                    block_change_4 = -11
                    block_rotation = 3
                elif block_type == 5 and block_rotation == 3 and block_pos[-1]%10 != 9 :
                    block_change_1 = -20
                    block_change_2 = -11
                    block_change_4 = 11
                    block_rotation = 0
                elif block_type == 6 and block_rotation == 0: # Line block rotations
                    block_change_1 = 12
                    block_change_2 = 21
                    block_change_3 = -10
                    block_change_4 = -1
                    block_rotation = 1
                elif block_type == 6 and block_rotation == 1 and block_pos[-1]%10 != 9 and block_pos[0]%10 > 1:
                    block_change_1 = -2
                    block_change_2 = -11
                    block_change_3 = 20
                    block_change_4 = 11
                    block_rotation = 2
                elif block_type == 6 and block_rotation == 2:
                    block_change_1 = 11
                    block_change_3 = -11
                    block_change_4 = -22
                    block_rotation = 3
                elif block_type == 6 and block_rotation == 3 and block_pos[-1]%10 != 0 and block_pos[0]%10 < 8:
                    block_change_1 = -21
                    block_change_2 = -10
                    block_change_3 = 1
                    block_change_4 = 12
                    block_rotation = 0
            elif ROTATE_L: # Counter clockwise rotations
                block_change_1 = 0 # Stores the movement changes of each block
                block_change_2 = 0 
                block_change_3 = 0
                block_change_4 = 0      
                previous_rotation = block_rotation
                # Add this if block goes off right side of screen when rotating - and block_pos[-1]%10 != 9 
                # Add this if block goes off left side of screen when rotating - and block_pos[0]%10 != 0
                if block_type == 0 and block_rotation == 0: # Z block rotations
                    block_change_1 = 10
                    block_change_2 = 19
                    block_change_3 = -10
                    block_change_4 = -1
                    block_rotation = 1
                elif block_type == 0 and block_rotation == 1 and block_pos[-1]%10 != 9:
                    block_change_1 = -10
                    block_change_2 = -19
                    block_change_3 = 10
                    block_change_4 = 1
                    block_rotation = 0
                elif block_type == 2 and block_rotation == 0: # S block rotations
                    block_change_1 = -9 
                    block_change_3 = 11
                    block_change_4 = 20
                    block_rotation = 1
                elif block_type == 2 and block_rotation == 1 and block_pos[-1]%10 != 1:
                    block_change_1 = 9 
                    block_change_3 = -11
                    block_change_4 = -20
                    block_rotation = 0
                elif block_type == 3 and block_rotation == 0: # T block rotations
                    block_change_3 = 20
                    block_change_4 = -11
                    block_rotation = 3
                elif block_type == 3 and block_rotation == 3 and block_pos[-1]%10 != 9:
                    block_change_4 = 11
                    block_rotation = 2
                elif block_type == 3 and block_rotation == 2:
                    block_change_3 = -20
                    block_change_1 = 11
                    block_rotation = 1
                elif block_type == 3 and block_rotation == 1 and block_pos[0]%10 != 0:
                    block_change_1 = -11
                    block_rotation = 0
                elif block_type == 4 and block_rotation == 0: # Orange L block rotations
                    block_change_1 = -10
                    block_change_3 = -11
                    block_change_4 = 19
                    block_rotation = 3
                elif block_type == 4 and block_rotation == 3 and block_pos[-1]%10 != 9:
                    block_change_1 = 10
                    block_change_3 = 19
                    block_change_4 = -9
                    block_rotation = 2
                elif block_type == 4 and block_rotation == 2:
                    block_change_1 = -9
                    block_change_3 = 1
                    block_change_4 = 10
                    block_rotation = 1
                elif block_type == 4 and block_rotation == 1 and block_pos[0]%10 != 0:
                    block_change_1 = 9
                    block_change_3 = -9
                    block_change_4 = -20
                    block_rotation = 0
                elif block_type == 5 and block_rotation == 0: # Blue L block rotations
                    block_change_1 = 20
                    block_change_2 = 11
                    block_change_4 = -11
                    block_rotation = 3
                elif block_type == 5 and block_rotation == 3 and block_pos[-1]%10 != 9:
                    block_change_1 = -10
                    block_change_2 = 1
                    block_change_4 = 11
                    block_rotation = 2
                elif block_type == 5 and block_rotation == 2:
                    block_change_1 = -9
                    block_change_2 = -1
                    block_change_4 = -10
                    block_rotation = 1
                elif block_type == 5 and block_rotation == 1 and block_pos[-1]%10 != 0:
                    block_change_1 = -1
                    block_change_2 = -11
                    block_change_4 = 10
                    block_rotation = 0
                elif block_type == 6 and block_rotation == 0: # Line block rotations 
                    block_change_1 = 21
                    block_change_2 = 10
                    block_change_3 = -1
                    block_change_4 = -12
                    block_rotation = 3
                elif block_type == 6 and block_rotation == 3 and block_pos[-1]%10 != 0 and block_pos[0]%10 < 8: 
                    block_change_1 = -11
                    block_change_3 = 11
                    block_change_4 = 22
                    block_rotation = 2
                elif block_type == 6 and block_rotation == 2:
                    block_change_1 = 2
                    block_change_2 = 11
                    block_change_3 = -20
                    block_change_4 = -11
                    block_rotation = 1
                elif block_type == 6 and block_rotation == 1 and block_pos[-1]%10 != 9 and block_pos[0]%10 > 1:
                    block_change_1 = -12
                    block_change_2 = -21
                    block_change_3 = 10
                    block_change_4 = 1
                    block_rotation = 0           
            block_pos[0] += block_change_1
            block_pos[1] += block_change_2
            block_pos[2] += block_change_3
            block_pos[3] += block_change_4    
            for i in range(4):
                if block_pos[i]+(block_row*10) > lowest:
                    lowest = block_pos[i]+(block_row*10)
            if lowest > 200:
                block_row -= 1 # "Nudges" the block upwards if a rotation places it out of the screen
                if lowest > 210:
                    block_row -= 1
                if playgrid[block_pos[0]+(block_row*10)] == 1 or playgrid[block_pos[1]+(block_row*10)] == 1 or playgrid[block_pos[2]+(block_row*10)] == 1 or playgrid[block_pos[3]+(block_row*10)] == 1: # Checks if the block collides with anything after a "nudge" is attempted, and reverses the nudge if this happens
                    block_row += 1
                    nudge_failed = True
            if playgrid[block_pos[0]+(block_row*10)] == 1 or playgrid[block_pos[1]+(block_row*10)] == 1 or playgrid[block_pos[2]+(block_row*10)] == 1 or playgrid[block_pos[3]+(block_row*10)] == 1 or nudge_failed: # Checks if the block overlaps existing blocks, and reverses the rotation if this happens
                block_pos[0] -= block_change_1
                block_pos[1] -= block_change_2
                block_pos[2] -= block_change_3
                block_pos[3] -= block_change_4 
                block_rotation = previous_rotation
            First = block_pos[0]%10
            Last = block_pos[-1]%10     
        if LEFT and repeat_lr == 0:
            repeat_lr = 5
            clear = 0
            for i in range(4):
                if playgrid[block_pos[i]-1+(block_row*10)] != 1:
                    clear += 1
            if First != 0 and clear == 4:  
                for i in range(4):
                    block_pos[i] -= 1
        if RIGHT and repeat_lr == 0:
            repeat_lr = 5
            clear = 0
            if block_pos[-1]+(block_row*10)+1 < 200:
                for i in range(4):
                    if playgrid[block_pos[i]+1+(block_row*10)] != 1:
                        clear += 1
            if Last != 9 and clear == 4:
                for i in range(4):
                    block_pos[i] += 1                    
        if DOWN and repeat_down == 0:
            repeat_down = 5
            move_down = True      
        First = block_pos[0]%10
        Last = block_pos[-1]%10
        if repeat_lr > 0:
            repeat_lr -= 1
        if repeat_down > 0:
            repeat_down -= 1            
        # Clears Active block
        for i in range(200):
            if playgrid[i] == 2:
                playgrid[i] = 0
                colour[i] = WHITE
        # Game movement (falling) + updating Playgrid
        speed = 1+(score/1000) # Slowly increases the speed as more lines are cleared
        time += speed
        if time > 30 or move_down:
            move_down = False
            below = []
            lowest = 0
            for i in range(4):
                below.append(block_pos[i]+10+(block_row*10))
            for i in range(4):
                if below[i] > lowest:
                    lowest = below[i]
            if lowest < 200:
                if playgrid[below[0]] == 1 or playgrid[below[1]] == 1 or playgrid[below[2]] == 1 or playgrid[below[3]] == 1: # Detects blocks below
                    if ticks_on_ground == 4: # Makes the block attempt to land 3 times before actually placing, to allow last second movement to happen
                        for i in range(4):
                            playgrid[block_pos[i]+block_row*10] = 1
                            colour[block_pos[i]+block_row*10] = block_colour
                    else:
                        ticks_on_ground += 1 # Counts how long the block has been on the ground, counts in attempts to place
                        for i in range(4):
                            playgrid[block_pos[i]+block_row*10] = 2
                            colour[block_pos[i]+block_row*10] = block_colour                        
                else:
                    block_row += 1
                    for i in range(4): # Moves shape if there is no blocks below
                        playgrid[block_pos[i]+block_row*10] = 2
                        colour[block_pos[i]+block_row*10] = block_colour
                    ticks_on_ground = 0 # If the block 
            elif ticks_on_ground == 4:
                for i in range(4): # Places blocks
                    playgrid[block_pos[i]+block_row*10] = 1
                    colour[block_pos[i]+block_row*10] = block_colour
            else:
                ticks_on_ground += 1 
                for i in range(4): # Re adds blocks at the old position
                    playgrid[block_pos[i]+block_row*10] = 2
                    colour[block_pos[i]+block_row*10] = block_colour
        else:
            for i in range(4): # Re adds blocks at the old position if everything else fails
                playgrid[block_pos[i]+block_row*10] = 2
                colour[block_pos[i]+block_row*10] = block_colour

        # Modulus 10 would help with block length
        # Blocks should keep track of previous spot so it can be cleared
        
        # Timer
        if time > 30:
            time = 0
        if UP: # Hard drop mechanic. Block snaps to bottom and immedietly gets placed
            hard_drop_finished = False
            below = []
            lowest = 0
            while not hard_drop_finished:
                for i in range(200):
                    if playgrid[i] == 2:
                        playgrid[i] = 0
                        colour[i] = WHITE
                below = []
                lowest = 0
                for i in range(4):
                    below.append(block_pos[i]+10+(block_row*10))
                for i in range(4):
                    if below[i] > lowest:
                        lowest = below[i]
                if lowest < 200:
                    if playgrid[below[0]] == 1 or playgrid[below[1]] == 1 or playgrid[below[2]] == 1 or playgrid[below[3]] == 1: # Detects blocks below
                        for i in range(4):
                            playgrid[block_pos[i]+block_row*10] = 1
                            colour[block_pos[i]+block_row*10] = block_colour
                            hard_drop_animation_initiated = True # Starts the hard drop animation over, cancels any existing animation
                            hard_drop_finished = True
                    else:
                        block_row += 1
                        for i in range(4): # Moves shape if there is no blocks below
                            playgrid[block_pos[i]+block_row*10] = 2
                            colour[block_pos[i]+block_row*10] = block_colour
                else:
                    for i in range(4): # Places blocks
                        playgrid[block_pos[i]+block_row*10] = 1
                        colour[block_pos[i]+block_row*10] = block_colour
                        hard_drop_animation_initiated = True # Starts the hard drop animation over, cancels any existing animation
                        hard_drop_finished = True
                UP = False    
        
        # Checks for lines
        number_cleared = 0
        for i in range(0,20):
            if playgrid[i*10:i*10+10].count(1) == 10: # Checks if a line is all 1
                for o in range(0,10):
                    playgrid[o+i*10] = 0
                    colour[o+i*10] = WHITE
                    line_cleared = i*10+o+1 # Last position of last line cleared (if line 10 is cleared, this will equal 100)
                number_cleared += 1
                line_clear_animation_initiated = True
                playgrid_copy = [] # Makes changes to the playgrid, but uses info from playgrid
                colour_copy = [] # same as playgrid_copy
                for i in range(210): # Makes the copies 200 entries long = to the originals
                    playgrid_copy.append(0)
                    colour_copy.append(WHITE)
                for i in range(line_cleared):
                    playgrid_copy[i+10] = playgrid[i]
                    colour_copy[i+10] = colour[i]
                for i in range(line_cleared, 200):
                    colour_copy[i] = colour[i]
                    playgrid_copy[i] = playgrid[i]
                playgrid_copy = playgrid_copy[:200]
                colour_copy = colour_copy[:200]
                playgrid = playgrid_copy
                colour = colour_copy
        score += number_cleared*100 # Adds line cleared to score * 100 
        # UI
        screen.blit(UI, [0,0])    
        
        # Animations
        if line_clear_animation_initiated:
            line_clear_animation_initiated = False
            hard_drop_animation_initiated = False
            hard_drop_animation = False
            animation_timer = 30
            line_clear_animation = True
            animated_tiles = number_cleared
            animated_row = (line_cleared//10)# Gives the first row that has been cleared
            animated_r = 225
            animated_g = 223
            animated_b = 133
        elif hard_drop_animation_initiated and not line_clear_animation:
            hard_drop_animation_initiated = False
            line_clear_animation_initiated = False
            animation_timer = 30 # length of animation
            animated_tiles = block_pos # copies the block position before a new one is created
            animated_row = block_row
            animated_r = 225
            animated_g = 223
            animated_b = 133
            hard_drop_animation = True
        if animation_timer != 0:
            animation_timer -= 1
        if animation_timer == 0:
            hard_drop_animation = False
            line_clear_animation = False
        
        # Draw Screen Grid
        for i in range(0,20):
            for o in range(0,10):
                if colour[o+(i*10)] == WHITE:
                    screen.blit(Empty_Tile, [o*40+120, i*40+40])
                else:
                    pygame.draw.rect(screen, colour[o+(i*10)], [o*40+120, i*40+40, 40, 40])
                    screen.blit(Tetromino, [o*40+120, i*40+40])
        if animation_timer !=  0 and line_clear_animation:
            animated_r += 1
            animated_g += 1        
            animated_b += 3       
            animated_tile_colour = (animated_r,animated_g,animated_b) 
            for i in range(animated_tiles): # draws animated tiles
                for o in range(10):
                    pygame.draw.rect(screen, animated_tile_colour, [o*40+120, (animated_row-i)*40, 40, 40])
        elif animation_timer !=  0 and hard_drop_animation:
            animated_r += 1
            animated_g += 1        
            animated_b += 3       
            animated_tile_colour = (animated_r,animated_g,animated_b) 
            for i in range(len(animated_tiles)): # draws animated tiles
                pygame.draw.rect(screen, animated_tile_colour, [(animated_tiles[i]%10)*40+120, ((animated_row+animated_tiles[i]//10)*40+40), 40, 40])
        # Upcoming Blocks Display
        for i in range(len(upcoming_blocks)):
            if upcoming_blocks[i] == 0:
                screen.blit(upcoming_block_Z, [550, 100+(i*80)])
            if upcoming_blocks[i] == 1:
                screen.blit(upcoming_block_Square, [560, 100+(i*80)])
            if upcoming_blocks[i] == 2:
                screen.blit(upcoming_block_S, [550, 100+(i*80)])         
            if upcoming_blocks[i] == 3:
                screen.blit(upcoming_block_T, [550, 100+(i*80)])
            if upcoming_blocks[i] == 4:
                screen.blit(upcoming_block_L, [550, 100+(i*80)])
            if upcoming_blocks[i] == 5:
                screen.blit(upcoming_block_J, [550, 100+(i*80)])         
            if upcoming_blocks[i] == 6:
                screen.blit(upcoming_block_Line, [540, 100+(i*80)])
        # Held Block Display
        if hold == 0:
            screen.blit(upcoming_block_Z, [35, 120])
        if hold == 1:
            screen.blit(upcoming_block_Square, [45, 120])
        if hold == 2:
            screen.blit(upcoming_block_S, [35, 120])         
        if hold == 3:
            screen.blit(upcoming_block_T, [35, 120])
        if hold == 4:
            screen.blit(upcoming_block_L, [35, 120])
        if hold == 5:
            screen.blit(upcoming_block_J, [35, 120])         
        if hold == 6:
            screen.blit(upcoming_block_Line, [25, 120])        
        ScoreDisplay = font.render(str(score), True, WHITE)
        screen.blit(ScoreDisplay, [540,680])
    
    pygame.display.flip()
    
    # Background
    background_x += 0.5
    screen.blit(BackgroundLayer1, [0,0])
    if Flip_layers: # Draws the layers with layer 2 on the left and layer 3 on the right
        screen.blit(BackgroundLayer2, [background_x,0])
        screen.blit(BackgroundLayer3, [background_x-640,0])
    else: # Draws the layers with layer 3 on the left and layer 2 on the right
        screen.blit(BackgroundLayer2, [background_x-640,0])
        screen.blit(BackgroundLayer3, [background_x,0])
    if background_x > 640:
        background_x = 0
        if Flip_layers:
            Flip_layers = False
        else:
            Flip_layers = True        
    
    ROTATE_L = False
    ROTATE_R = False
    clock.tick(60)
pygame.draw.rect(screen, BLACK, [0,0,640,880])
pygame.quit()