import pygame
import random
import os

pygame.init()

pygame.mixer.init()

#Screen Window
screen_width = 1000
screen_height = 600
game_window = pygame.display.set_mode((screen_width,screen_height))


#Title
pygame.display.set_caption('Snake Game')

#Colors
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
cyan = (0,255,255)

# Clock
fps = 60
clock = pygame.time.Clock()

#Music
def background_music():
    pygame.mixer.music.load(os.path.join('assets','background.mp3'))
    pygame.mixer.music.play()

def game_over_music():
    # pygame.mixer.music.load('gameover.mp3')
    pygame.mixer.music.load(os.path.join('assets','gameover.mp3'))
    pygame.mixer.music.play()

#Background Image
# image = pygame.image.load('abc.jpg')
image = pygame.image.load(os.path.join('assets','abc.jpg'))
image = pygame.transform.scale(image, (screen_width, screen_height))

#Text Display on Screen
font = pygame.font.SysFont(None,55)
def text_on_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    game_window.blit(screen_text, [x,y])


def plot_snake(snake_list, size):
    for x, y in snake_list :
        pygame.draw.rect(game_window, black, [x, y, size, size])


def welcome_screen():
    exit_game = False
    while not exit_game:
        game_window.fill(white)
        game_window.blit(image, (0,0))
        text_on_screen('Welcome to Snakes', blue, 340, 210)
        text_on_screen('Press Space Bar to Continue', blue, 270, 260)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    background_music()
                    game_loop()

            pygame.display.update()
            clock.tick(fps)

def game_loop():

    # Game Specific  Variables
    exit_game = False
    game_over = False

    '''
    Here a Flag is taken for Snake entering the Boundary
     before entering the boundary Snake can Only move in Down Direction
     After Entering the Boundary the Game Starts
     '''
    #Before Entering the Boundary
    flag = False

    # Snake Variables
    snake_x = 100
    snake_y = 30
    size = 12
    velocity_x = 0
    velocity_y = 0
    velocity = 4
    brick_counter = 0#For creating brick

    # Food Variables
    # Food Size = Snake Size
    food_x = random.randrange(100, 900)
    food_y = random.randrange(100, 500)
    no_of_food_eaten = 0

    # Snake Size Increament Variables
    snake_list = []
    snake_length = 1

    #File DataBase for Hiscore Count
    #If Hiscore file doesnt exists then create a text document by name hiscore.txt
    if(not os.path.exists('hiscore.txt')):
        with open('hiscore.txt','w') as file:
            file.write('0')

    #Score Variables
    score = 0
    hiscore_on_file = 0

    #Check hiscore text from file
    with open('hiscore.txt', 'r') as file :
        highscore_on_file = file.read()


    while not exit_game:

        if game_over:
            with open('hiscore.txt', 'w') as file:
                file.write(str(highscore_on_file))

            game_window.fill(white)
            text_on_screen('Game Over!!!', red, 380,230)
            text_on_screen('Press Enter to Restart', red, 350,270)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        background_music()
                        game_loop()


        else:
            game_window.fill(white)

            if not flag:

                pygame.draw.line(game_window, black, (30, 60), (80, 60), 5)
                pygame.draw.line(game_window, black, (130, 60), (970, 60), 5)
                pygame.draw.line(game_window, black, (30, 60), (30, 570), 5)
                pygame.draw.line(game_window, black, (30, 570), (970, 570), 5)
                pygame.draw.line(game_window, black, (970, 60), (970, 570), 5)

                pygame.draw.rect(game_window, black, [snake_x, snake_y, size, size])

                text_on_screen('Press Down Key to Continue', green, 270, 230)
                text_on_screen('Food', cyan, 360, 310)
                text_on_screen('Poison', red, 360, 370)

                pygame.draw.rect(game_window, cyan, [270, 320, 15, 15])
                pygame.draw.rect(game_window, red, [270, 380, 15, 15])

                for event in pygame.event.get():

                    if event.type == pygame.QUIT:
                        exit_game = True

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_DOWN:
                            velocity_y = velocity
                            velocity_x = 0

                snake_x += velocity_x
                snake_y += velocity_y

            if snake_y > 60:
                flag = True

            if flag:
                for event in pygame.event.get():
                    # print(event)

                    if event.type == pygame.QUIT:
                        exit_game = True

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT:
                            velocity_x = velocity
                            velocity_y = 0
                        if event.key == pygame.K_LEFT:
                            velocity_x = -velocity
                            velocity_y = 0
                        if event.key == pygame.K_UP:
                            velocity_y = -velocity
                            velocity_x = 0
                        if event.key == pygame.K_DOWN:
                            velocity_y = velocity
                            velocity_x = 0
                        # Cheat Code
                        if event.key == pygame.K_q:
                            score += 10

                snake_x += velocity_x
                snake_y += velocity_y

                if snake_x < 30 or snake_x > 970 or snake_y < 60 or snake_y > 570 :
                    game_over = True
                    game_over_music()



                if abs(snake_x - food_x) < 10 and abs(snake_y - food_y) < 10:
                    score += 10
                    brick_counter += 1

                    food_x = random.randrange(50, 950)
                    food_y = random.randrange(80, 550)

                    brick_x = random.randrange(80, 550)
                    brick_y = random.randrange(80, 550)

                    snake_length += 5

                    no_of_food_eaten += 1
                    if no_of_food_eaten % 5 == 0 :
                        velocity += 1

                    if score > int(highscore_on_file) :
                        highscore_on_file = score
                # print(brick_counter)

                game_window.fill(white)
                text_on_screen('    Score: ' + str(score) + '   Hiscore: ' + str(highscore_on_file), green, 10, 15)

                head = []
                head.append(snake_x)
                head.append(snake_y)
                snake_list.append(head)

                if len(snake_list) > snake_length:
                    del snake_list[0]

                if head in snake_list[:-1]:
                    game_over = True
                    game_over_music()

                pygame.draw.line(game_window, black, (30,60),(970,60), 5)
                pygame.draw.line(game_window, black, (30,60),(30,570), 5)
                pygame.draw.line(game_window, black, (30,570),(970,570), 5)
                pygame.draw.line(game_window, black, (970,60),(970,570), 5)
                plot_snake(snake_list, size)
                pygame.draw.rect(game_window, cyan, [food_x, food_y, size, size])

                if brick_counter > 8:
                    if abs(brick_x - food_x) > 50 or abs(brick_y - food_y) > 50:
                        pygame.draw.rect(game_window, red , [brick_x, brick_y, 15, 15])
                        print(f'snake_x:{snake_x}')
                        print(f'brick_x:{brick_x}')
                        print(f'snake_y:{snake_y}')
                        print(f'brick_y:{brick_y}')
                        print(f'abs X:{abs(snake_x - brick_x)}')
                        print(f'abs Y:{abs(snake_y - brick_y)}')
                        if abs(snake_x - brick_x) < 10 and abs(snake_y - brick_y) < 10:
                            game_over = True
                            game_over_music()

        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
    # quit()

if __name__ == '__main__':
    welcome_screen()