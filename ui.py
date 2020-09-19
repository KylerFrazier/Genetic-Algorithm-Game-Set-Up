import tkinter as tk
import ctypes
from games import MovingBall
from agents import RandomAgent
from utils.controls import Controls

ctypes.windll.shcore.SetProcessDpiAwareness(1)

class UserInterface(tk.Tk):

    def __init__(self):
        
        super().__init__()

        self.title("Brick Breaker Menu")
        self.configure(background="black")
        self.state("zoomed")
        
        self.controls = Controls(master=self)

        self.choice = tk.IntVar()
        self.choice.set(0)
        self.rows = tk.StringVar()
        self.rows.set("7")
        self.cols = tk.StringVar()
        self.cols.set("8")
        self.scale = tk.IntVar()
        self.choice.set(0)

        self.controls.make_gap(50)
        self.controls.make_label("Genetic Algorithm\nGame Controls", 25)
        self.controls.make_gap(50)
        self.controls.make_radio_buttons(self.choice, ["User", "A.I."])
        self.controls.make_gap(50)
        self.controls.make_spinboxes({
            "Number of Rows: " : self.rows, 
            "Number of Columns: " : self.cols})
        self.controls.make_gap(50)
        self.controls.make_radio_buttons(self.scale, ["Scalable", "Fixed"])
        self.controls.make_gap(50)
        self.controls.make_button("Generate Game", self.gen_game)
        
        self.controls.pack(fill=tk.Y, side=tk.LEFT)

        self.game_frame = tk.Frame(master=self)
        self.game_frame.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)
        self.game_frame.configure(background="black") #gray15
        
        self.random_seed = 0
        self.games = []
        
        self.mainloop()

    def gen_game(self):

        for game in self.games:
            if game.winfo_exists():
                game.bind_keys(False)
                game.destroy()

        scalable = True if self.scale.get() == 0 else False

        self.games = []
        if self.choice.get() == 0:
            self.games.append(MovingBall(self.game_frame))
            self.games[0].pack(fill=tk.BOTH if scalable else tk.NONE, expand=True)
        else:
            rows=int(self.rows.get())
            col=int(self.cols.get())
            for i in range(rows):
                tk.Grid.rowconfigure(self.game_frame, i, weight=1 if scalable else 0)
                for j in range(col):
                    tk.Grid.columnconfigure(self.game_frame, j, weight=1 if scalable else 0)
                    self.games.append(MovingBall(self.game_frame, random_seed=self.random_seed))
                    self.games[i*col+j].grid(row=i, column=j, sticky=tk.N+tk.S+tk.E+tk.W)
        
        self.update()
        
        for game in self.games:
            game.generate()

        self.update()

        try:
            if self.choice.get() == 0:
                self.games[0].bind_keys()
            else:
                for game in self.games:
                    RandomAgent(game).start()
        except:
            print("Unable to connect input with the game.")
            print("The game likely finished or crashed before input connections were finished.")

        self.random_seed += 1
