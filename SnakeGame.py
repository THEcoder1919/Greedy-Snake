from tkinter import  *
import random
import time
import pygame
import sys
import os

def resource_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    return filename

pygame.mixer.init()
game_over_sound = pygame.mixer.Sound(resource_path("mixkit-arcade-retro-game-over-213.wav"))
eat_sound = pygame.mixer.Sound(resource_path("mixkit-retro-game-notification-212.wav"))
restart_sound = pygame.mixer.Sound(resource_path("mixkit-retro-arcade-racer-start-218.wav"))

GAME_WIDTH = 400
GAME_HEIGHT = 400
SPEED = 100
SPACE_SIZE = 30
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
DOLLAR_COLOR = "#00FF00"
BACKGROUND_COLOR = "#000000"

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Dollar:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        # pyright: ignore [reportArgumentType]
        canvas.create_text(x + SPACE_SIZE // 2, y + SPACE_SIZE // 2, text="$", fill=DOLLAR_COLOR, font=("Consolas", -SPACE_SIZE), tag="dollar")

def next_turn(snake, dollar):
    global SPEED
    x, y = snake.coordinates[0]

    if direction == "down":
        y += SPACE_SIZE
    elif direction == "up":
        y -= SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == dollar.coordinates[0] and y == dollar.coordinates[1]:
        global score
        score += 1
        eat_sound.play()  
        label.config(text="Score:" + str(score))
        canvas.delete("dollar")
        dollar = Dollar()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, dollar)

    
def change_direction(new_direction):
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction
        
def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH:
        return True
    if y < 0 or y >= GAME_HEIGHT:
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False

def game_over():
    game_over_sound.play()
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2 - 40,  font=('consolas', 40), text="GAME OVER :(", fill="red")
    restart_btn = Button(window, text="Play Again?", font=("Consolas", 20), bg="black", fg="lime", command=restart)
    canvas.create_window(canvas.winfo_width()/2, canvas.winfo_height()/2 + 40, window=restart_btn)

def restart():
    global score, direction
    restart_sound.play(maxtime=1300)
    score = 0
    direction = 'down'
    label.config(text="Score:0")
    canvas.delete(ALL)
    snake = Snake()
    dollar = Dollar()
    next_turn(snake, dollar)

window = Tk()
window.configure(background = BACKGROUND_COLOR)
window.title("Greedy Snake")

score = 0
direction = 'down'

label = Label(window, text = "Score:" + str(score), font = ("Consolas", 40), bg="black", fg="lime")
label.pack()

canvas = Canvas(window, bg = BACKGROUND_COLOR, height = GAME_HEIGHT, width = GAME_WIDTH)
canvas.pack()

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
dollar = Dollar()
next_turn(snake, dollar)
window.update()
window.mainloop()
