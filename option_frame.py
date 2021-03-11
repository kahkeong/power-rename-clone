import tkinter as tk
import logging


class OptionFrame(tk.LabelFrame):
    def __init__(self, item_list, parent_object):
        tk.LabelFrame.__init__(
            self,
            parent_object,
            text="Options",
            relief=tk.GROOVE,
            borderwidth=5,
        )
        self.item_list = item_list
        self.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        self.buttons = {}
        self.alist = [
            "Use Regular Expressions",
            "Match All Occurences",
            "Case Sensitive",
            "Enumerate Items",
            "Item Name Only",
            "Item Extension Only",
            "Exclude Folders",
            "Exclude Files",
            "Exclude Subfolder Items",
            "Make Uppercase",
            "Make Lowercase",
            "Make Titlecase",
        ]
        self.selected_options = set()
        self.case_change_options = set(
            [
                "Make Uppercase",
                "Make Lowercase",
                "Make Titlecase",
            ]
        )
        self.item_name_or_extension_options = set(
            ["Item Name Only", "Item Extension Only"]
        )

        ROW_PER_COLUMN = 6

        values = []
        for index, option in enumerate(self.alist):
            value = tk.IntVar()
            btn_new = tk.Checkbutton(
                master=self,
                text=option,
                variable=value,
                command=lambda option=option: self.update_options(option),
            )
            # quick hack as somehow, we cannot access variable via following syntax "btn_new.variable"
            btn_new.val = value

            btn_new.grid(
                row=index % ROW_PER_COLUMN,
                column=(0 + (index // ROW_PER_COLUMN)),
                sticky="w",
            )
            values.append(value)
            self.buttons[option] = btn_new

    def update_options(self, option):
        is_option_enabled = option in self.selected_options

        # only one of them can be enabled at any point of time
        if option in self.item_name_or_extension_options:
            self.selected_options -= self.item_name_or_extension_options
            for item in self.item_name_or_extension_options:
                self.buttons[item].val.set(0)

            # disable it since previously, it was enabled
            if is_option_enabled:
                self.buttons[option].val.set(0)
            # enable it
            else:
                self.buttons[option].val.set(1)
                self.selected_options.add(option)

        # only one of them can be enabled at any point of time
        elif option in self.case_change_options:
            self.selected_options -= self.case_change_options
            for item in self.case_change_options:
                self.buttons[item].val.set(0)

            # disable it since previously, it was enabled
            if is_option_enabled:
                self.buttons[option].val.set(0)
            # enable it
            else:
                self.buttons[option].val.set(1)
                self.selected_options.add(option)

        elif option in self.selected_options:
            self.selected_options.remove(option)
        else:
            self.selected_options.add(option)

        logging.debug(
            f"newly selected option: {option}, enabled options: {self.selected_options}"
        )

        self.item_list.update_options(self.selected_options)
