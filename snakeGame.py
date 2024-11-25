from tkinter import *
import random


score = 0
direction = "right"

GAME_WIDTH = 1050
GAME_HEIGHT = 630
SPEED =  
SPACE_SIZE = 35
BODY_PARTS = score + 3
SNAKE_COLOR = "#00FF00"
# HEAD_COLOR = "#00FFFF"
FOOD_COLOR = "#FF0000"
OBS_COLOR = "#f2f2f2"
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
    def __init__(self, snake):
        self.create_food(snake)

    def create_food(self, snake):
        # x, y = snake.coordinates[0]

        while True:
            x = random.randint(0, int(GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
            y = random.randint(0, int(GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
            # print("food = " + str([int(x / SPACE_SIZE), int(y / SPACE_SIZE)]))
            # Check if the new food coordinates are not on the snake's body

            onSnake = False
            for coord in snake.coordinates:
                if coord == (x, y):
                    onSnake = True
                    break

            if onSnake == False:
                self.coordinates = [x, y]
                break

                # Create the food on the canvas
        canvas.create_oval(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food"
        )


def nextTurn(snake, food):
    x, y = snake.coordinates[0]
    # print(snake.coordinates[0])

    # Move the snake in the current direction
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    # Wrap around the screen borders
    if x < 0:
        x = GAME_WIDTH - SPACE_SIZE
    elif x >= GAME_WIDTH:
        x = 0
    if y < 0:
        y = GAME_HEIGHT - SPACE_SIZE
    elif y >= GAME_HEIGHT:
        y = 0

    # Insert new coordinates at the beginning of the snake's body
    snake.coordinates.insert(0, (x, y))

    # Draw the new head
    square = canvas.create_rectangle(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR
    )
    snake.squares.insert(0, square)

    # Check if the snake has eaten the food
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food(snake)  # Create new food, avoiding snake's body
    else:
        # If no food is eaten, remove the tail
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if checkCollision(snake):
        gameover()
    else:
        snek.after(SPEED, nextTurn, snake, food)
    # snek.after(SPEED, nextTurn, snake, food)


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
# Obstackes
# ----------------------------------------------------------------
def createObstacleObj(x, y):
    square = canvas.create_rectangle(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=OBS_COLOR, tag="obstacle"
    )
    pass


# ----------------------------------------------------------------
# Lvl 1
# ----------------------------------------------------------------
# def createLvl1():
#     for i in range(0, int(GAME_HEIGHT / SPACE_SIZE)):
#         a = 0
#         createObstacleObj(0, a + i)
#         a += SPACE_SIZE
#     # createObstacleObj(1, 2)
#     # createObstacleObj(1, 3)
#     # createObstacleObj(1, 4)
#     pass


# ----------------------------------------------------------------
# Lvl 2
# ----------------------------------------------------------------
def createLvl2():
    pass


# ----------------------------------------------------------------
# Lvl 3
# ----------------------------------------------------------------
def createLvl3():
    pass


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

snake = Snake()
food = Food(snake)
changeDirection()
nextTurn(snake, food)

snek.mainloop()
