from tkinter import *
import random


score = 10
direction = "right"

GAME_WIDTH = 700
GAME_HEIGHT = 600
SPEED = 75
SPACE_SIZE = 50
BODY_PARTS = score + 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#121212"


class Snake:
    def __init__(self):
        self.bodySize = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, (GAME_HEIGHT / 2)])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake"
            )
            self.squares.append(square)


class Food:
    def __init__(self):
        x = random.randint(0, int(GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, int(GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food"
        )


def nextTurn(snake, food):
    x, y = snake.coordinates[0]
    snake

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR
    )

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score

        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()

    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if checkCollision(snake):
        gameover()

    else:
        snek.after(SPEED, nextTurn, snake, food)


def changeDirection(newDirection=None):
    global direction

    if newDirection is None:
        snek.bind("<Left>", lambda event: changeDirection("left"))
        snek.bind("<Right>", lambda event: changeDirection("right"))
        snek.bind("<Up>", lambda event: changeDirection("up"))
        snek.bind("<Down>", lambda event: changeDirection("down"))
        return

    opposites = {"left": "right", "right": "left", "up": "down", "down": "up"}
    if newDirection != opposites.get(direction):
        direction = newDirection


def checkCollision(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for bodyPart in snake.coordinates[1:]:
        if x == bodyPart[0] and y == bodyPart[1]:
            print("Game Over")
            return True


def gameover():
    canvas.delete(ALL)
    canvas.create_text(
        canvas.winfo_width() / 2,
        canvas.winfo_height() / 2,
        font=("consolas", 70),
        text="Game Over!",
        fill="red",
        tag="gameover",
    )
    pass


snek = Tk()
snek.title("sneks")
snek.resizable(False, False)

label = Label(snek, text="Score:{}".format(score), font=("consolas", 40))
label.pack()


# ----------------------------------------------------------------
# GUI settings
# ----------------------------------------------------------------

canvas = Canvas(snek, bg=BACKGROUND_COLOR, width=GAME_WIDTH, height=GAME_HEIGHT)
canvas.pack()

snek.update()

windowHeight = snek.winfo_height()
windowWidth = snek.winfo_width()
screenHeight = snek.winfo_screenheight()
screenWidth = snek.winfo_screenwidth()

x = int((screenWidth / 2) - (windowWidth / 2))
y = int((screenHeight / 2) - (windowHeight / 2))

snek.geometry(f"{windowWidth}x{windowHeight}+{x}+{0}")


# snek.bind("<Left>", lambda event: changeDirection("left"))
# snek.bind("<Right>", lambda event: changeDirection("right"))
# snek.bind("<Up>", lambda event: changeDirection("up"))
# snek.bind("<Down>", lambda event: changeDirection("down"))

snake = Snake()
food = Food()
changeDirection()
nextTurn(snake, food)

snek.mainloop()
