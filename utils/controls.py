import tkinter as tk, tkinter.font

class Controls(tk.Frame):

    def __init__(self, master=None, cnf={}, **kw):
        
        super().__init__(master, cnf, **kw)

        self.color = "white"
        self.background = "gray15"
        self.button_background = "gray25"
        self.hover = "gray55"
        self.button_selected = "#555777777"
        self.border = "gray"
        self.font_family = "Times New Roman"
        self.padx = 20
        self.pady = 5

        self.configure(
            background=self.background, 
            highlightbackground=self.border, 
            highlightthickness=5
        )

    def make_gap(self, height=50):

        gap = tk.Frame(master=self, height=height, background=self.background)
        gap.grid()

    def make_label(self, text="", size=14):

        font = tk.font.Font(family=self.font_family, size=size)
        label = tk.Label(
            master=self, 
            foreground=self.color,
            background=self.background,
            font=font,
            text=text,
        )
        label.grid(padx=self.padx, pady=self.pady)
        return label

    def make_radio_buttons(self, var=1, choices=[], size=14):

        font = tk.font.Font(family=self.font_family, size=size)
        radiobuttons = []
        button_grid = tk.Frame(master=self, background=self.background)
        for i, choice in enumerate(choices):
            rbutton = tk.Radiobutton(
                master=button_grid,
                text=choice,
                font=font,
                foreground=self.color,
                background=self.button_background,
                activebackground=self.hover,
                activeforeground=self.color,
                selectcolor=self.button_selected,
                indicatoron=0,
                borderwidth=0,
                width=8,
                variable=var,
                value=i
            )
            rbutton.grid(row=0, column=i, padx=5)
            radiobuttons.append(rbutton)
        button_grid.grid(padx=self.padx, pady=self.pady)
        return radiobuttons

    def make_button(self, text="", function=lambda : None, size=14, ):

        font = tk.font.Font(family=self.font_family, size=size)
        button = tk.Button(
            master=self,
            foreground=self.color,
            background=self.button_background,
            activebackground=self.hover,
            activeforeground=self.color,
            font=font,
            text=text,
            pady=10,
            padx=10,
            borderwidth=0
        )
        button.grid(padx=self.padx, pady=self.pady)
        button.bind("<Button-1>", lambda _, *args, **kwargs : function(*args, **kwargs ))
        return button

    def make_spinboxes(self, text_and_vars={}, min_val=1, max_val=100, size=14):
        
        labels_and_spinboxes = tk.Frame(
            master=self, 
            background=self.background,
        )
        font = tk.font.Font(family=self.font_family, size=size)

        spinboxes = []
        for i, text in enumerate(text_and_vars):
            label = tk.Label(
                master=labels_and_spinboxes, 
                foreground=self.color,
                background=self.background,
                font=font,
                text=text,
            )
            label.grid(padx=self.padx, pady=self.pady, row=i, column=0, sticky=tk.W)
            spinbox = tk.Spinbox(
                master=labels_and_spinboxes,
                font=font,
                foreground=self.color,
                background=self.button_background,
                readonlybackground=self.button_background,
                buttonbackground=self.hover,
                activebackground=self.hover,
                borderwidth=0,
                width=4,
                from_=min_val,
                to=max_val,
                state="readonly",
                textvariable=text_and_vars[text]
            )
            spinbox.grid(padx=self.padx, pady=self.pady, row=i, column=1, sticky=tk.E)
            spinboxes.append(spinbox)
        labels_and_spinboxes.grid()
        return tuple(spinboxes)

    def make_option_menu(self, var="", options=[], function=lambda : None, size=14, ):

        font = tk.font.Font(family=self.font_family, size=size)
        option_menu = tk.OptionMenu(self, var, *options, command=function)
        option_menu.configure(
            indicatoron=0,
            foreground=self.color,
            background=self.button_background,
            activebackground=self.hover,
            activeforeground=self.color,
            font=font,
            pady=25,
            padx=25,
            borderwidth=0
        )
        option_menu.grid(padx=self.padx, pady=self.pady)
        return option_menu