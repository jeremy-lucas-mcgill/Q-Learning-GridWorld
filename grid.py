import numpy as np
class Grid:
    def __init__(self,rows, cols, move_reward) -> None:
        self.rows = rows
        self.cols = cols
        self.grid = np.full((rows,cols), ".",dtype='<U3')
        self.move_reward = move_reward
        self.player_pos = None
        self.player_start_pos = None
        self.terminal_dict = {}
        self.wall_pos = []
        self.player_reward = 0
        self.updateGrid()
    def player_action_and_reward(self,direction):
        new_pos = self.player_pos
        if (direction == 0):
            new_pos = (new_pos[0] - 1,new_pos[1])
        elif (direction == 1):
             new_pos = (new_pos[0],new_pos[1] + 1)
        elif (direction == 2):
             new_pos = (new_pos[0] + 1,new_pos[1])
        elif (direction == 3):
             new_pos = (new_pos[0],new_pos[1] - 1)

        if (0 <= new_pos[0] < self.rows and 0 <= new_pos[1] < self.cols and not self.grid[new_pos] == "#"):
            self.player_pos = new_pos
        new_state = self.player_pos
        reward = self.move_reward + self.terminal_dict[new_state] if new_state in self.terminal_dict else self.move_reward
        self.player_reward += reward
        self.updateGrid()
        return new_state, reward
    def updateGrid(self):
        self.grid = np.full((self.rows,self.cols), ".",dtype='<U3')
        if self.wall_pos is not None:
            self.wall_pos = [pos for pos in self.wall_pos if pos[0] < self.rows and pos[1] < self.cols]
            for pos in self.wall_pos:
                self.grid[pos] = "#"
        if self.terminal_dict is not None:
            self.terminal_dict = {pos: val for pos, val in self.terminal_dict.items() if pos[0] < self.rows and pos[1] < self.cols}
            for pos in self.terminal_dict.keys():
                self.grid[pos] = self.terminal_dict[pos]
        if self.player_pos is not None:
            if self.player_pos[0] < self.rows and self.player_pos[1] < self.cols:
                self.grid[self.player_pos] = "&"
            else:
                self.player_pos = None
    def reset(self):
        self.player_pos = self.player_start_pos
        self.player_reward = 0
        self.updateGrid()
    def addWallPos(self,pos):
        if not pos in self.wall_pos:
            self.wall_pos.append(pos)
    def removeWallPos(self,pos):
        if pos in self.wall_pos:
            self.wall_pos.remove(pos)
    def addTerminalPos(self,pos,value):
        self.terminal_dict[pos] = value
    def removeTerminalPos(self,pos):
       del self.terminal_dict[pos]
    def addPlayerPos(self,pos):
        self.player_pos = pos
        self.player_start_pos = pos
    def removePlayerPos(self):
        self.player_pos = None
    def removeAtPosition(self,pos):
        if pos in self.wall_pos:
            self.removeWallPos(pos)
        elif pos in self.terminal_dict.keys():
            self.removeTerminalPos(pos)
        elif pos == self.player_pos:
            self.removePlayerPos()
    def placeAtPosition(self,pos, character):
        if self.is_int(character):
            self.addTerminalPos(pos,int(character))
        elif character == "&":
            self.addPlayerPos(pos)
        elif character == "#":
            self.addWallPos(pos)
    def is_int(self,s):
        try:
            int(s)
            return True
        except ValueError:
            return False  
    def __str__(self) -> str:
        return str(str(self.grid))
    
        