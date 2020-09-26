import tkinter as tk
import ctypes
import neat
from games import MovingBall, Pong
from agents import RandomAgent, NeuralNetworkAgent
from utils.controls import Controls

ctypes.windll.shcore.SetProcessDpiAwareness(1)

class PopulationPerGen(neat.Population):

    def run1(self, fitness_function):

        self.reporters.start_generation(self.generation)

        # Evaluate all genomes using the user-provided function.
        fitness_function(list(self.population.items()), self.config)

    def run2(self):

        # Gather and report statistics.
        best = None
        for g in self.population.values():
            if g.fitness is None:
                raise RuntimeError("Fitness not assigned to genome {}".format(g.key))

            if best is None or g.fitness > best.fitness:
                best = g
        self.reporters.post_evaluate(self.config, self.population, self.species, best)

        # Track the best genome ever seen.
        if self.best_genome is None or best.fitness > self.best_genome.fitness:
            self.best_genome = best

        if not self.config.no_fitness_termination:
            # End if the fitness threshold is reached.
            fv = self.fitness_criterion(g.fitness for g in self.population.values())
            if fv >= self.config.fitness_threshold:
                self.reporters.found_solution(self.config, self.generation, best)

        # Create the next generation from the current generation.
        self.population = self.reproduction.reproduce(self.config, self.species,
                                                        self.config.pop_size, self.generation)

        # Check for complete extinction.
        if not self.species.species:
            self.reporters.complete_extinction()

            # If requested by the user, create a completely new population,
            # otherwise raise an exception.
            if self.config.reset_on_extinction:
                self.population = self.reproduction.create_new(self.config.genome_type,
                                                                self.config.genome_config,
                                                                self.config.pop_size)
            else:
                raise neat.CompleteExtinctionException()

        # Divide the new population into species.
        self.species.speciate(self.config, self.population, self.generation)

        self.reporters.end_generation(self.config, self.population, self.species)

        self.generation += 1

        return self.best_genome

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
        self.rows.set("5")
        self.cols = tk.StringVar()
        self.cols.set("7")
        self.scale = tk.IntVar()
        self.choice.set(0)
        self.random_seed = tk.StringVar()
        self.random_seed.set("0")
        self.num_gens = tk.StringVar()
        self.num_gens.set("100")
        self.games_per_gen = tk.StringVar()
        self.games_per_gen.set("10")
        

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
        self.controls.make_spinboxes({
            "Game Seed: " : self.random_seed}, min_val=-100, max_val=100)
        self.controls.make_gap(400)
        self.controls.make_button("Generate Game", self.generate)
        self.controls.make_spinboxes({
            "Generations Left To Run: " : self.num_gens,
            "Games per Generation: " : self.games_per_gen}, 
            min_val=1, max_val=999)
        
        self.controls.pack(fill=tk.Y, side=tk.LEFT)

        self.game_frame = tk.Frame(master=self)
        self.game_frame.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)
        self.game_frame.configure(background="black") #gray15
        
        self.games = []
        
        # Set up AI
        config = neat.Config(
            neat.DefaultGenome, neat.DefaultReproduction,
            neat.DefaultSpeciesSet, neat.DefaultStagnation,
            'config.txt')
        self.population = PopulationPerGen(config)
        self.population.add_reporter(neat.StdOutReporter(False))

        self.mainloop()

    def generate(self):
        
        self.gen_game()
        self.games_done = 0

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
                    self.games.append(MovingBall(self.game_frame, random_seed=int(self.random_seed.get())))
                    self.games[i*col+j].grid(row=i, column=j, sticky=tk.N+tk.S+tk.E+tk.W)
        
        self.update()
        
        for game in self.games:
            game.generate()

        self.update()

        # try:
        if self.choice.get() == 0:
            self.games[0].bind_keys()
        else:
            self.population.run1(self.fitness_function)
            # for game in self.games:
            #     RandomAgent(game).start()
        # except:
        #     print("Unable to connect input with the game.")
        #     print("The game likely finished or crashed before input connections were finished.")

        self.random_seed.set(int(self.random_seed.get())+1)

    def check_done(self):
        for agent in self.agents.values():
            if agent.winfo_exists():
                self.after(100, self.check_done)
                return

        if self.games_done == 0:
            for genome, _ in self.agents.items():
                genome.fitness = 0
        
        self.games_done += 1
        self.set_fitnesses()
        
        if self.games_done == int(self.games_per_gen.get()):
            self.population.run2()
            if self.num_gens.get() != '1':
                self.games_done = 0
                self.num_gens.set(str(int(self.num_gens.get())-1))

        if self.num_gens.get() != '1' or self.games_done != int(self.games_per_gen.get()):
            self.gen_game()

    def fitness_function(self, genomes, config):
        self.agents = {}

        for i, (_, genome) in enumerate(genomes):
            if i >= len(self.games):
                break
            network = neat.nn.FeedForwardNetwork.create(genome, config)
            agent = NeuralNetworkAgent(self.games[i], network)
            self.agents[genome] = agent
            agent.start()
        self.check_done()

    def set_fitnesses(self):
        for genome, agent in self.agents.items():
            genome.fitness += agent.get_score()
