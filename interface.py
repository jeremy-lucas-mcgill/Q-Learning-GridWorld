import pygame
from pygame_components import *
from game import Game

pygame.init()

#constants
width = 1000
height = 800
grid_width = 8
grid_height = 8
#screen
screen = pygame.display.set_mode((width,height))
#display items
interface_title = Title((50,5),(500,40),BLUE_LIGHT, 3, "Grid World", 30, BLACK)
parameters_title = Title((600,50), (350,50), BLUE_LIGHT, 3,"Parameters", 30, BLACK)
info_text = Title((50,575), (500,50), BLUE_LIGHT,3,"INFO", 30,BLACK)
training_button = Button((50,650), (150,50),GREEN,GREEN_DARK,GREEN_LIGHT,3,"TRAIN", 30,BLACK)
run_button = Button((225,650), (150,50), YELLOW,YELLOW_DARK,YELLOW_LIGHT,3,"RUN", 30,BLACK)
stop_button = Button((400,650), (150,50), RED,RED_DARK,RED_LIGHT,3,"STOP", 30, BLACK)
width_title = Title((600,125), (165,50), BLUE_LIGHT, 3, "Change Grid Width", 23, BLACK)
height_title = Title((785,125), (165,50), BLUE_LIGHT, 3, "Change Grid Height", 23, BLACK)
increase_width_button = Button((600,180), (75,50), GREEN, GREEN_DARK, GREEN_LIGHT,3, "+",40, BLACK)
decrease_width_button = Button((690,180), (75,50), RED, RED_DARK, RED_LIGHT,3, "-",40, BLACK)
increase_height_button = Button((785,180), (75,50), GREEN, GREEN_DARK, GREEN_LIGHT,3, "+",40, BLACK)
decrease_height_button = Button((875,180), (75,50), RED, RED_DARK, RED_LIGHT,3, "-",40, BLACK)
player_button = Button((600,275), (150,50), BLUE,BLUE_DARK, BLUE_LIGHT,3, "PLAYER",30, BLACK)
wall_button = Button((800,275), (150,50), GRAY, GRAY_DARK, GRAY_LIGHT,3, "WALL",30, BLACK)
green_button = Button((600,350), (150,50), GREEN, GREEN_DARK, GREEN_LIGHT,3, "POSITIVE TERMINAL",20, BLACK)
red_button = Button((800,350), (150,50), RED, RED_DARK, RED_LIGHT,3, "NEGATIVE TERMINAL",20, BLACK)
#lists
texts = [interface_title,parameters_title, info_text,width_title,height_title]
buttons = [training_button,stop_button,run_button,increase_width_button,decrease_width_button,
           increase_height_button, decrease_height_button,player_button,wall_button,green_button,red_button]
#grid and gameplay handling
game = Game(grid_width,grid_height,-1)
character = None
is_training = False
is_running = False
stop = False

def increase_width():
    global game
    game.grid.rows += 1
    game.grid.updateGrid()
def decrease_width():
    global game
    if (game.grid.rows - 1 > 0):
        game.grid.rows -= 1
        game.grid.updateGrid()
def increase_height():
    global game
    game.grid.cols += 1
    game.grid.updateGrid()
def decrease_height():
    global game
    if game.grid.cols - 1 > 0:
        game.grid.cols -= 1
        game.grid.updateGrid()
def set_character(char):
    global character
    character = char
def checkCharacter(mouse_clicks):
    global character
    left, middle,right = mouse_clicks
    if right == 1:
        character = None
def CheckPlayer(mouse_clicks):
    global character
    if "&" in game.grid.grid and character == "&":
        character = None
def startTraining():
    global is_training
    is_training = True
    game.start_train(200,100)
def startRunning():
    global is_running
    is_running = True
    game.start_run(1,100)
def stop_sim():
    global stop
    stop = not stop
#run loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for button in buttons:
            button.handle_event(event)
    #get mouse position
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicks = pygame.mouse.get_pressed()
    #grid 
    grid_display = GridDisplay(screen, (50,50), (550,550),game.grid,game.agent)
    #handle button presses
    if (not is_training and not is_running):
        if training_button.button_clicked and game.grid.player_pos is not None:
            startTraining()
        if run_button.button_clicked and game.grid.player_pos is not None:
            startRunning()
        if increase_width_button.button_clicked:
            increase_width()
        if decrease_width_button.button_clicked:
            decrease_width()
        if increase_height_button.button_clicked:
            increase_height()
        if decrease_height_button.button_clicked:
            decrease_height()
        if player_button.button_clicked:
            set_character("&")
        if wall_button.button_clicked:
            set_character("#")
        if green_button.button_clicked:
            set_character(str(2 * game.grid.rows if game.grid.rows > game.grid.cols else 2 * game.grid.cols))
        if red_button.button_clicked:
            set_character(str(-2 * game.grid.rows if game.grid.rows > game.grid.cols else -2 * game.grid.cols))
        checkCharacter(mouse_clicks)
        CheckPlayer(mouse_clicks)
        result = grid_display.detectMouseOnGrid(mouse_clicks, mouse_pos)
        if result:
            grid_pos_x,grid_pos_y, num = result
            grid_display.placeOnGrid(character,grid_pos_x,grid_pos_y, num)
    #controls
    if stop_button.button_clicked:
        stop_sim()
    if (is_training and not is_running):
        if not stop:
            is_training = game.train_step()
            pygame.time.delay(1)
    if (is_running and not is_training):
        if not stop:
            is_running = game.run_path_step()
            pygame.time.delay(100)

    #draw interface
    screen.fill(WHITE)
    grid_display.drawCells()
    grid_display.drawGrid()
    for text in texts:
        text.draw(screen)
    for button in buttons:
        button.updateAndDraw(screen, mouse_pos)
    pygame.display.flip()
pygame.quit()