from agent import Agent
from grid import Grid
class Game:
    def __init__(self,width,length, move_reward):
        self.agent = Agent(True,1,0.9,0.5)
        self.grid = Grid(width, length, move_reward)
        self.current_training_step = 0
        self.current_training_episode = 0
        self.current_training_max_steps = 0
        self.current_training_episodes = 0
        self.current_run_step = 0
        self.current_run_episode = 0
        self.current_run_max_steps = 0
        self.current_run_episodes = 0
        self.current_run_path = []
        self.start_agent_exploration_rate = self.agent.exploration_rate
    def start_train(self, num_episodes, max_steps):
        self.current_training_episodes = num_episodes
        self.current_training_max_steps = max_steps
        self.current_training_step = 0
        self.current_training_episode = 0
        self.grid.reset()
    def train_step(self):
        if (self.current_training_episode < self.current_training_episodes):
            if (self.current_training_step < self.current_training_max_steps):
                self.current_training_step += 1
                state = self.grid.player_pos
                is_terminal = state in self.grid.terminal_dict.keys()
                if is_terminal:
                    self.grid.reset()
                    self.current_training_episode += 1
                    self.current_training_step = 0
                else:
                    action = self.agent.takeActionFromPosition(state)
                    new_state, reward = self.grid.player_action_and_reward(action)
                    self.agent.updateQValue(state,action,new_state,reward,is_terminal)
            else:
                self.current_training_episode += 1
                self.current_training_step = 0
            return True
        else:
            self.grid.reset()
            return False
    def start_run(self,episodes,max_steps):
        self.current_run_episodes = episodes
        self.current_run_max_steps = max_steps
        self.current_run_step = 0
        self.current_run_episode = 0
        self.agent.exploration_rate = 0
        self.grid.reset()
    def run_path_step(self):
        if self.current_run_episode < self.current_run_episodes:
            if self.current_run_step < self.current_run_max_steps:
                self.current_run_step += 1
                is_terminal = self.grid.player_pos in self.grid.terminal_dict.keys()
                if is_terminal:
                    self.grid.reset()
                    self.current_run_path = []
                    self.current_run_episode += 1
                    self.current_run_step = 0
                else:
                    action = self.agent.takeActionFromPosition(self.grid.player_pos)
                    _ , _ = self.grid.player_action_and_reward(action)
                    self.current_run_path.append(action)
            else:
                self.grid.reset()
                self.current_run_path = []
                self.current_run_episode += 1
                self.current_run_step = 0
            return True
        else:
            self.agent.exploration_rate = self.start_agent_exploration_rate
            self.grid.reset()
            return False