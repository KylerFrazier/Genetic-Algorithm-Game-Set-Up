import tkinter as tk
class GameCanvas(tk.Canvas):

    def __init__(self, master=None, cnf={}, width=1280, height=720, fps=25, **kw):
        
        kw["width"] = width
        kw["height"] = height
        super().__init__(master, cnf, **kw)

        self.configure(
            background="gray15",
            highlightbackground="green",
            highlightthickness=5
        )

        self.update_frame_time(fps)

    def vw(self, percentage=1):

        return percentage*self.winfo_width()/100

    def vh(self, percentage=1):

        return percentage*self.winfo_height()/100
    
    def update_frame_time(self, fps=25):

        self.frame_time = 0 if fps == 0 else int(1000/fps)
        return self.frame_time

    def get_bindings(self) -> dict:
        
        return {}

    def bind_keys(self, bind=True):
        
        for action, function in self.get_bindings().items():
            if bind:
                self.winfo_toplevel().bind(action, function)
            else:
                self.winfo_toplevel().unbind(action)

    def update(self):

        return 0

    def animate(self):

        if self.frame_time != 0:
            try:
                score = self.update()
            except tk.TclError:
                self.destroy()
        
        if score == None:
            self.after(self.frame_time, self.animate)
        else:
            self.bind_keys(False)
            self.destroy()
            return score
