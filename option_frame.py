import tkinter as tk


class OptionFrame(tk.LabelFrame):
    def __init__(self, parentObject, background):
        tk.LabelFrame.__init__(
            self,
            parentObject,
            text="Options",
            # background=background,
            relief=tk.GROOVE,
            borderwidth=5,
        )
        self.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        self.alist = [
            "Use Regular Expressions",
            "Match All Occurences",
            "Case Sensitive",
            "Enumerate Items",
            "Item name Only",
            "Item Extension Only",
            "Exclude Folders",
            "Exclude Files",
            "Exclude Subfolder Items",
            "Make Uppercase",
            "Make Lowercase",
            "Make Titlecase",
        ]

        values = []
        for index, name in enumerate(self.alist[:6]):
            value = tk.IntVar()
            btn_new = tk.Checkbutton(master=self, text=name, variable=value)
            btn_new.grid(row=index + 1, column=0, sticky="w")
            values.append(value)

        for index, name in enumerate(self.alist[6:]):
            value = tk.IntVar()
            btn_new = tk.Checkbutton(master=self, text=name, variable=value)
            btn_new.grid(row=index + 1, column=1, sticky="w")
            values.append(value)