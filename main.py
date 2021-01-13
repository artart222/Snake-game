import pygame, random


pygame.init()
pygame.mixer.init()
font = pygame.font.SysFont(None, 70)
fps_clock = pygame.time.Clock()

winx, winy = 750, 900
gamex, gamey = 750, 750
#Difference between winx, winy and gamex, gamey is:
    #becuse game has score board i must to consider more height for scord board
    #and becuse of this i declure 4 variable
win = pygame.display.set_mode((winx, winy))


background = pygame.image.load("shapes/background.png")
food_image = pygame.image.load("shapes/food.png")
game_icon = pygame.image.load("shapes/icon.png")


pygame.display.set_icon(game_icon)
pygame.display.set_caption("snake game")


#bib list contains some sounds. This sounds use when player change direction of snake
bib_list = [pygame.mixer.Sound("sounds/bib1.wav"),
pygame.mixer.Sound("sounds/bib2.wav"), pygame.mixer.Sound("sounds/bib3.wav"),
pygame.mixer.Sound("sounds/bib4.wav")]

eating_sound = pygame.mixer.Sound("sounds/eating_sound.wav")
crash_sound = pygame.mixer.Sound("sounds/crash.wav")

#This is 2d array that would contains position of snake's body parts in x and y axis
#First index of list always is position of snake head in x and y axis
snake_body_parts_list = [[375, 375]]

#food_positions_list items is possible situations for food coordinates
food_positions_list = []


"""
contact checker function checking if player head make contact with food
if head contact food this function add one snake body part to snake_body_parts_list
"""
def contact_checker(food_position):
    #check for making contact with food
    if snake_body_parts_list[0] == food_position:
        food_positions_list = find_possible_position_of_food_position()
        food_position = food_positions_list[random.randrange(0, len(food_positions_list))]

        eating_sound.play()

        if key == "up":
            snake_body_parts_list.append([snake_body_parts_list[-1][-2], snake_body_parts_list[-1][-1] + 50])
        if key == "down":
            snake_body_parts_list.append([snake_body_parts_list[-1][-2], snake_body_parts_list[-1][-1] - 50])
        if key == "left":
            snake_body_parts_list.append([snake_body_parts_list[-1][-2] + 50, snake_body_parts_list[-1][-1]])
        if key == "right":
            snake_body_parts_list.append([snake_body_parts_list[-1][-2] - 50, snake_body_parts_list[-1][-1]])

    return food_position


def editor_of_snake_body_parts_list():
    for part in range(len(snake_body_parts_list) - 1, 0, -1):
        snake_body_parts_list[part][0] = snake_body_parts_list[part - 1][0]
        snake_body_parts_list[part][1] = snake_body_parts_list[part - 1][1]


def crash_work():
    crash_sound.play()
    return False


"""
crash check if player head go out of sceen or snake head contact with snake
body and if head go out of screen or snake head contact with snake body make
game running false
"""
def crash(running):
    if snake_body_parts_list[0][0] >= gamex:
        running = crash_work()
    elif snake_body_parts_list[0][0] <= gamex - gamex:
         running = crash_work()
    elif snake_body_parts_list[0][1] >= gamey:
        running = crash_work()
    elif snake_body_parts_list[0][1] <= gamey - gamey:
        running = crash_work()

    for first_part in range(len(snake_body_parts_list)):
        for second_part in range(first_part + 1, len(snake_body_parts_list)):
            if snake_body_parts_list[first_part] == snake_body_parts_list[second_part]:
                running = crash_work()

    return running


def snake_drawer():
    if running == True:
        pygame.draw.circle(win, (255, 255, 0), snake_body_parts_list[0], 25)
        #drawing snake body
        for part in range(1, len(snake_body_parts_list)):
            pygame.draw.circle(win, (0, 255, 255), snake_body_parts_list[part], 25)


def change_direction_of_snake(key, route1, route2):
    if key != route1 and key != route2:
        return route2, True


#This function will find possible positions of food and put positions in food_positions_list
def find_possible_position_of_food_position():
    food_positions_list = []
    #editing food_positions_list and adding all possible positions
    for xpos in range(gamex + 1):
      if xpos % 25 == 0 and xpos % 50 == 25:
          for ypos in range(gamey + 1):
              if ypos % 25 == 0 and ypos % 50 == 25:
                  food_positions_list.append([xpos, ypos])

    #removing all parts of snake from possible positions
    for part in snake_body_parts_list:
        if part in food_positions_list:
            food_positions_list.remove(part)

    return food_positions_list


food_positions_list = find_possible_position_of_food_position()
food_position = food_positions_list[random.randrange(0, len(food_positions_list))]


def score_board():
    #we can find number of food that snake eaten with finding len of snake
    #You must subscart score from one because len of snake_body_parts_list is at least 1
    score = (len(snake_body_parts_list) - 1) * 10
    score = "score: " + str(score)

    win.fill((125, 255, 125), (0, gamey, winx, winy))

    #draw score
    text = font.render(score, True, (255, 255, 255))
    win.blit(text, (20, winy - 50))

    #drawing the high score and editing the high score file
    with open("high score file.txt", "r") as f:
        lines = f.readlines()
        high_score = lines[0]
        high_score = high_score.strip("\n")
        if int(high_score) >= (len(snake_body_parts_list) - 1) * 10:
            score = "high score: " + high_score
            text = font.render(score, True, (255, 255, 255))
            win.blit(text, (300, winy - 50))
        elif (len(snake_body_parts_list) - 1) * 10 > int(high_score):
            lines[0] = str((len(snake_body_parts_list) - 1) * 10)
            with open("high score file.txt", "w") as f:
                f.writelines(lines)
            score = "high score: " + str((len(snake_body_parts_list) - 1) * 10)
            text = font.render(score, True, (255, 255, 255))
            win.blit(text, (300, winy - 50))


#the direction of the snake
key = ""
#the number of times the snake has changed direction
number_of_times_snake_changes_direction = 0
#snake's head contact with food
running = True
while running:
    fps_clock.tick(10)
    win.blit(background, (0, 0))
    score_board()


    win.blit(food_image , (food_position[0] - 25 , food_position[1] - 25))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        keyChange = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                try:
                    key , keyChange = change_direction_of_snake(key , "down" , "up")
                except TypeError:
                    pass
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                try:
                    key , keyChange = change_direction_of_snake(key , "up" , "down")
                except TypeError:
                    pass
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                try:
                    key , keyChange = change_direction_of_snake(key , "left" , "right")
                except TypeError:
                    pass
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                try:
                    key , keyChange = change_direction_of_snake(key , "right" , "left")
                except TypeError:
                    pass
            if keyChange == True:
                bib_list[number_of_times_snake_changes_direction % 4].play()
                number_of_times_snake_changes_direction += 1
            keyChange = False
            break


    editor_of_snake_body_parts_list()


    #change position of snake head
    if key == "up":
        snake_body_parts_list[0][1] -= 50
    if key == "down":
        snake_body_parts_list[0][1] += 50
    if key == "right":
        snake_body_parts_list[0][0] += 50
    if key == "left":
        snake_body_parts_list[0][0] -= 50


    running = crash(running)
    snake_drawer()
    food_position = contact_checker(food_position)


    pygame.display.update()


while pygame.mixer.get_busy():
    pass
pygame.mixer.quit()
pygame.quit()
