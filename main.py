import tkinter as tk

class Direction:
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Cell:
    SPEED = 0.2

    def __init__(self, player_id, x, y, direction=Direction.UP):
        self.player_id = player_id
        self.x = x
        self.y = y
        self.completion = 0
        self.direction = direction
    
    def is_completed(self):
        return self.completion >= 1
    
    def step(self):
        if self.is_completed():
            return True
        if self.direction == Direction.UP:
            self.y += self.SPEED
        elif self.direction == Direction.RIGHT:
            self.x += self.SPEED
        elif self.direction == Direction.DOWN:
            self.y -= self.SPEED
        else:
            self.x -= self.SPEED
        self.completion += self.SPEED
        return False


class StaticCell:
    def __init__(self, player_id):
        self.player_id = player_id
        self.value = 0


class Grid:
    def __init__(self, size):
        self.size = size
        self.grid = [None] * (size ** 2)

    def put(self, player_id, x, y):
        cell = self.get(x, y)
        if not cell:
            cell = Cell(player_id)
            return
        cell.player_id = player_id
        if cell.value < 2:
            cell.value += 1
            return
        # split
        cell = None
        animation_list = []
        if y > 0:
            animation_list.append(Cell(x, y, Direction.UP))
        if x < (self.size - 1):
            animation_list.append(Cell(x, y, Direction.RIGHT))
        if y < (self.size - 1):
            animation_list.append(Cell(x, y, Direction.DOWN))
        if x > 0:
            animation_list.append(Cell(x, y, Direction.LEFT))
        return animation_list
    
    def apply(animation_list):
        new_animations = []
        for anim in animation_list:
            if anim.is_completed():
                new_animations += self.put(anim.player_id, anim.x, anim.y)
        return new_animations
        
    def get(self, x, y):
        return self.grid[x + y * self.size]


# class Game(tk.Frame):
#     def __init__(self, master):
#         super(Game, self).__init__(master)
#         self.width = 800
#         self.height = 600

#         self.canvas = tk.Canvas(self, bg="#101010", width=self.width, height=self.height)
#         self.canvas.pack()
#         self.pack()
    
#         self.setup_game()
#         self.canvas.focus_set()
#         # self.canvas.bind("<Button>", lambda _: self....)
    
#     def setup_game():
#         self.map = Map(5)


# def main():
#     pass

# if __name__ == "__main__":
#     main()