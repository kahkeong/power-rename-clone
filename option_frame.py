import tkinter as tk


class OptionFrame(tk.LabelFrame):
    def __init__(self, item_list, parent_object, background):
        tk.LabelFrame.__init__(
            self,
            parent_object,
            text="Options",
            # background=background,
            relief=tk.GROOVE,
            borderwidth=5,
        )
        self.item_list = item_list
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

        ROW_PER_COLUMN = 6

        values = []
        for index, name in enumerate(self.alist):
            value = tk.IntVar()
            btn_new = tk.Checkbutton(
                master=self,
                text=name,
                variable=value,
                command=lambda: self.item_list.update_option(values, self.alist),
            )
            btn_new.grid(
                row=index % ROW_PER_COLUMN,
                column=(0 + (index // ROW_PER_COLUMN)),
                sticky="w",
            )
            values.append(value)
