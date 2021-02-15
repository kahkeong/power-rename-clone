import tkinter as tk


class OptionFrame(tk.Frame):
    def __init__(self, parentObject, background):
        tk.Frame.__init__(
            self, parentObject, background=background, relief=tk.RIDGE, borderwidth=10
        )
        self.grid(row=1, column=0, sticky="ew")
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

        self.lbl_options = tk.Label(master=self, text="Options")
        self.lbl_options.grid(row=0, column=0, columnspan=2, sticky="w")

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