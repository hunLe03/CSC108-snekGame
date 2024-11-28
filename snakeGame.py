from tkinter import *
import random

# Constants
score = 0

GAME_WIDTH = 1000
GAME_HEIGHT = 600
SPEED = 75
SPACE_SIZE = 50
INITIAL_BODY_PARTS = score + 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#121212"


class SnakeAndFood:
    def __init__(self):
        # Initialize the main window
        self.snek = Tk()
        self.snek.title("Snake Game")
        self.snek.resizable(False, False)

        self.direction = "right"

        # Label for the score
        self.score_frame = Frame(self.snek, bg="grey", height=40)
        self.score_frame.pack(fill=X)
        self.label = Label(
            self.score_frame,
            text=f"Score: {score}",
            font=("consolas", 20),
            bg="grey",
            fg="white",
        )
        self.label.pack(anchor=W, padx=10)

        # Game canvas
        self.canvas = Canvas(
            self.snek, bg=BACKGROUND_COLOR, width=GAME_WIDTH, height=GAME_HEIGHT
        )
        self.canvas.pack()

        # Center the window
        self.snek.update_idletasks()
        window_width = self.snek.winfo_width()
        window_height = self.snek.winfo_height()
        screen_width = self.snek.winfo_screenwidth()
        screen_height = self.snek.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.snek.geometry(f"{window_width}x{window_height}+{x}+{0}")

        # Initialize snake and food
        self.snake = self.init_snake()
        self.food = self.init_food(self.snake)

        # Bind arrow keys for direction change
        self.snek.bind("<Left>", lambda event: self.change_direction("left"))
        self.snek.bind("<Right>", lambda event: self.change_direction("right"))
        self.snek.bind("<Up>", lambda event: self.change_direction("up"))
        self.snek.bind("<Down>", lambda event: self.change_direction("down"))

        # Start the game loop
        self.next_turn()

    def init_snake(self):
        body_size = INITIAL_BODY_PARTS
        coordinates = []
        squares = []

        for i in range(body_size):
            coordinates.append([0, (GAME_HEIGHT / 2)])

        for x, y in coordinates:
            square = self.canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake"
            )
            squares.append(square)

        return {"coordinates": coordinates, "squares": squares}

    def init_food(self, snake):
        while True:
            x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
            if [x, y] not in snake["coordinates"]:
                break

        self.canvas.create_oval(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food"
        )
        return {"coordinates": [x, y]}

    def change_direction(self, new_direction):
        print("THis executed")
        # Prevent reversing direction
        opposites = {"left": "right", "right": "left", "up": "down", "down": "up"}
        if new_direction != opposites.get(self.direction):
            self.direction = new_direction

    def next_turn(self):
        x, y = self.snake["coordinates"][0]
        global score

        # Move the snake in the current direction
        if self.direction == "up":
            y -= SPACE_SIZE
        elif self.direction == "down":
            y += SPACE_SIZE
        elif self.direction == "left":
            x -= SPACE_SIZE
        elif self.direction == "right":
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

        # Add the new head position
        self.snake["coordinates"].insert(0, [x, y])

        # Draw the new head
        square = self.canvas.create_rectangle(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR
        )
        self.snake["squares"].insert(0, square)

        # Check if the snake eats the food
        if [x, y] == self.food["coordinates"]:
            score += 1
            self.label.config(text=f"Score: {score}")
            self.canvas.delete("food")
            self.food = self.init_food(self.snake)
        else:
            # Remove the last part of the snake's body
            del self.snake["coordinates"][-1]
            self.canvas.delete(self.snake["squares"][-1])
            del self.snake["squares"][-1]

        # Check for collisions
        if self.check_collision():
            self.game_over()
        else:
            self.snek.after(SPEED, self.next_turn)

    def check_collision(self):
        x, y = self.snake["coordinates"][0]
        if [x, y] in self.snake["coordinates"][1:]:
            return True
        return False

    def game_over(self):
        self.canvas.delete("all")
        self.canvas.create_text(
            GAME_WIDTH // 2,
            GAME_HEIGHT // 2,
            font=("consolas", 50),
            text="Game Over!",
            fill="red",
            tag="gameover",
        )

    def mainloop(self):
        self.snek.mainloop()


class GUI:
    def __init__(self):
        # Highlight: Create the main window
        self.root = Tk()
        self.root.title("Snake Game Menu")
        self.root.resizable(False, False)

        self.root.update_idletasks()
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f"{400}x{400}+{x}+{0}")

        # Highlight: Main menu screen
        self.main_menu()

    def main_menu(self):
        """Main menu screen with buttons to navigate."""
        self.clear_window()

        # Title Label
        Label(
            self.root,
            text="Snake Game",
            font=("Consolas", 24, "bold"),
            fg="white",
            bg=BACKGROUND_COLOR,
            pady=20,
        ).pack(fill=X)

        # Start Button
        Button(
            self.root,
            text="Start Game",
            font=("Consolas", 14),
            command=self.start_game,
            width=20,
        ).pack(pady=10)

        # Change Speed Button
        Button(
            self.root,
            text="Change Speed",
            font=("Consolas", 14),
            command=self.change_speed,
            width=20,
        ).pack(pady=10)

        # Change Map Button
        Button(
            self.root,
            text="Change Map",
            font=("Consolas", 14),
            command=self.change_map,
            width=20,
        ).pack(pady=10)

        # Exit Button
        Button(
            self.root,
            text="Exit",
            font=("Consolas", 14),
            command=self.root.quit,
            width=20,
        ).pack(pady=10)

    def clear_window(self):
        """Clears all widgets from the root window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def start_game(self):
        """Starts the Snake game."""
        self.root.destroy()
        snake_game = SnakeAndFood()
        snake_game.mainloop()

    def change_speed(self):
        """Displays speed settings."""
        self.clear_window()

        self.current_speed_var = StringVar()
        self.current_speed_var.set(
            f"Select Speed\nCurrent Speed: {self.get_speed_text(SPEED)}"
        )

        Label(
            self.root,
            textvariable=self.current_speed_var,
            font=("Consolas", 18),
            bg=BACKGROUND_COLOR,
            fg="white",
        ).pack(pady=20)

        speeds = [150, 100, 75, 50]
        text = ""
        for speed in speeds:
            if speed == 150:
                text = "Easy"
            elif speed == 100:
                text = "Medium"
            elif speed == 75:
                text = "Hard"
            elif speed == 50:
                text = "Very Hard"
            Button(
                self.root,
                text=f"Speed: {text}",
                font=("Consolas", 14),
                command=lambda s=speed: self.set_speed(s),
                width=20,
            ).pack(pady=5)

        Button(
            self.root,
            text="Back to Menu",
            font=("Consolas", 14),
            command=self.main_menu,
            width=20,
        ).pack(pady=20)

    def set_speed(self, speed):
        """Sets the game speed."""
        global SPEED
        SPEED = speed

        self.current_speed_var.set(
            f"Select Speed\nCurrent Speed: {self.get_speed_text(SPEED)}"
        )

    def get_speed_text(self, speed):
        """Converts speed value to descriptive text."""
        if speed == 150:
            return "Easy"
        elif speed == 100:
            return "Medium"
        elif speed == 75:
            return "Hard"
        elif speed == 50:
            return "Very Hard"
        return "Unknown"

    def change_map(self):
        """Displays map settings."""
        self.clear_window()

        Label(
            self.root,
            text="Select Map",
            font=("Consolas", 18),
            bg=BACKGROUND_COLOR,
            fg="white",
        ).pack(pady=20)

        maps = ["Classic", "Obstacles", "Maze"]
        for map_option in maps:
            Button(
                self.root,
                text=f"Map: {map_option}",
                font=("Consolas", 14),
                command=lambda m=map_option: self.set_map(m),
                width=20,
            ).pack(pady=5)

        Button(
            self.root,
            text="Back to Menu",
            font=("Consolas", 14),
            command=self.main_menu,
            width=20,
        ).pack(pady=20)

    def set_map(self, map_name):
        """Sets the map."""
        print(f"Map selected: {map_name}")  # Replace with map functionality
        self.main_menu()

    def mainloop(self):
        self.root.mainloop()


class Obstacles:
    pass


# Run the game
if __name__ == "__main__":
    gui = GUI()
    gui.mainloop()
