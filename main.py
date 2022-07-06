import tkinter as tk

class Direction:
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class Cell:
    SPEED = 0.01

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
            self.x = round(self.x)
            self.y = round(self.y)
            return True
        if self.direction == Direction.UP:
            self.y -= self.SPEED
        elif self.direction == Direction.RIGHT:
            self.x += self.SPEED
        elif self.direction == Direction.DOWN:
            self.y += self.SPEED
        else:
            self.x -= self.SPEED
        self.completion += self.SPEED
        self.x = round(self.x, 6)
        self.y = round(self.y, 6)
        return False


class StaticCell:
    def __init__(self, player_id, value=0):
        self.player_id = player_id
        self.value = value


class Grid:
    def __init__(self, size):
        self.size = size
        self.grid = [None] * (size ** 2)

    def put(self, player_id, x, y):
        cell = self.get(x, y)
        if not cell:
            self.set(x, y, StaticCell(player_id))
            return []
        if cell.value < 2:
            self.set(x, y, StaticCell(player_id, cell.value + 1))
            return []
        # split
        self.set(x, y, None)
        animation_list = []
        if y > 0:
            animation_list.append(Cell(player_id, x, y, Direction.UP))
        if x < (self.size - 1):
            animation_list.append(Cell(player_id, x, y, Direction.RIGHT))
        if y < (self.size - 1):
            animation_list.append(Cell(player_id, x, y, Direction.DOWN))
        if x > 0:
            animation_list.append(Cell(player_id, x, y, Direction.LEFT))
        return animation_list
    
    def apply(self, animation_list):
        new_animations = []
        for anim in animation_list:
            if anim.is_completed():
                new_animations += self.put(anim.player_id, anim.x, anim.y)
        return new_animations
        
    def get(self, x, y):
        return self.grid[int(x) + int(y) * self.size]
    
    def set(self, x, y, value):
        self.grid[int(x) + int(y) * self.size] = value

class Game(tk.Frame):
    SIZE = 600
    MAP_SIZE = 5
    CELL_SIZE_PERCENT = 0.86
    PLAYER_SIZE_PERCENT = 0.80
    DOT_SIZE_PERCENT = 0.16

    def __init__(self, master):
        super(Game, self).__init__(master)
        self.width = self.height = self.SIZE
        
        self.canvas = tk.Canvas(self, bg="#dddddd", width=self.width, height=self.height)
        self.canvas.pack()
        self.pack()

        self.setup_game()
        self.draw_map()
        self.draw_static()
        self.canvas.focus_set()
        self.canvas.bind("<Button-1>", self.mouse_click)
    
    def setup_metricks(self):
        self.slot_size = self.SIZE / self.MAP_SIZE
        self.cell_size = self.slot_size * self.CELL_SIZE_PERCENT
        self.cell_space = (self.slot_size - self.cell_size) / 2
        self.player_size = self.cell_size * self.PLAYER_SIZE_PERCENT
        self.dot_rad = self.player_size * self.DOT_SIZE_PERCENT / 2
    
    def setup_game(self):
        self.map = Grid(self.MAP_SIZE)
        self.setup_metricks()
        # manually set players
        self.map.set(1, 1, StaticCell(0, value=2))
        self.map.set(self.MAP_SIZE - 1, self.MAP_SIZE - 1, StaticCell(1))
        self.player_turn = 0
        self.animations = []

    def mouse_click(self, event):
        if self.animations:
            return

        x = event.x // self.slot_size
        xrem = event.x % self.slot_size
        y = event.y // self.slot_size
        yrem = event.y % self.slot_size
        # check for slot-space zone
        if  xrem < self.cell_space or xrem > self.cell_size or \
            yrem < self.cell_space or yrem > self.cell_size:
            return
        
        cell = self.map.get(x, y)
        if cell and cell.player_id != self.player_turn:
            return
        self.animations = self.map.put(self.player_turn, x, y)
        self.player_turn = (self.player_turn + 1) % 2
        self.game_loop()

    def game_loop(self):
        flag = False
        for anim in self.animations:
            flag |= anim.step()
        
        # if anims and they're done
        if flag:
            self.animations = self.map.apply(self.animations)
        
        # update screen
        self.draw()

        # check for wins
        if not self.animations:
            pass
            # TODO: check for a winner
        else:
            self.after(10, self.game_loop)
    
    def draw(self):
        self.canvas.delete("tmp")
        self.draw_static()
        self.draw_moving()

    def draw_map(self):
        for y in range(self.MAP_SIZE):
            for x in range(self.MAP_SIZE):
                xx = x * self.slot_size + self.cell_space
                yy = y * self.slot_size + self.cell_space
                self.canvas.create_rectangle(xx, yy, xx + self.cell_size, yy + self.cell_size, fill="#aaaaaa")
        
    def draw_static(self):
        # draw static cells
        for y in range(self.MAP_SIZE):
            for x in range(self.MAP_SIZE):
                cell = self.map.get(x, y)
                if not cell:
                    continue
                xx = x * self.slot_size + self.cell_space
                yy = y * self.slot_size + self.cell_space
                color = "#ee1010"
                if cell.player_id == 1:
                    color = "#1010ee"
                self.draw_player(xx, yy, color, cell.value)
    
    def draw_player(self, x, y, color, value=0):
        # args - coords of the cell (not slot)
        player_space = (self.cell_size - self.player_size) / 2
        xx = x + player_space
        yy = y + player_space
        self.canvas.create_rectangle(xx, yy, xx + self.player_size, yy + self.player_size, fill=color, tags="tmp")
        # dots
        if value == 0:
            # center
            self.draw_circle(xx + self.player_size / 2, yy + self.player_size / 2, self.dot_rad)
        elif value == 1:
            dot_space = (self.player_size - self.dot_rad * 4) / 3
            # left
            self.draw_circle(xx + dot_space + self.dot_rad, yy + self.player_size / 2, self.dot_rad)
            # right
            self.draw_circle(xx + dot_space * 2 + self.dot_rad * 3, yy + self.player_size / 2, self.dot_rad)
        else:
            dot_space = (self.player_size - self.dot_rad * 4) / 3
            # up
            self.draw_circle(xx + self.player_size / 2, yy + dot_space + self.dot_rad, self.dot_rad)
            # left
            self.draw_circle(xx + dot_space + self.dot_rad, yy + self.player_size - dot_space - self.dot_rad, self.dot_rad)
            # right
            self.draw_circle(xx + self.player_size - dot_space - self.dot_rad, yy + self.player_size - dot_space - self.dot_rad, self.dot_rad)
    
    def draw_circle(self, x, y, rad, fill="#eeeeee"):
        self.canvas.create_oval(x - rad, y - rad, x + rad, y + rad, fill=fill, tags="tmp")

    def draw_moving(self):
        for anim in self.animations:
            x = anim.x * self.slot_size + self.cell_space
            y = anim.y * self.slot_size + self.cell_space
            color = "#ee1010"
            if anim.player_id == 1:
                color = "#1010ee"
            self.draw_player(x, y, color)



def main():
    root = tk.Tk()
    root.title("Clonium")
    game = Game(root)
    game.mainloop()

if __name__ == "__main__":
    main()