import tkinter as tk
import pathlib


class ItemList(object):
    def __init__(self):
        self.check_button_list = []
        self.lbl_renamed_list = []
        self.search = ""
        self.replace = ""
        self.show_all = True

        # reference to objects from other classes assigned at main.py
        self.canvas_frame = None
        self.scroll_bar_frame = None
        self.lbl_items_selected = None
        self.lbl_items_renaming = None

    def update_renamed(self):
        """
        Update the list of items that are showing at the Renamed column
        """
        for check_button, label in zip(self.check_button_list, self.lbl_renamed_list):
            item_name = check_button["text"]

            # is selected and search keyword appear in item name
            if check_button.val.get() and self.search in item_name:
                new_name = item_name.replace(self.search, self.replace)
                label.config(text=new_name)
                pass
            else:
                label.config(text="")

    def update_search(self, value):
        """
        Update the search keyword. As search keyword is updated, the previously items that are eligible to be renamed might not longer be valid.
        So we need the update the appropriate components.
        """
        self.search = value
        self.update_renamed()
        self.update_renaming_count()

    def update_replace(self, value):
        """
        Update the renamed item value. Since no other components will be affected, we just update the renamed value.
        """
        self.replace = value
        self.update_renamed()

    def update_filter(self):
        """
        Trigger to show all selected items or show only items that will be renamed
        """
        self.show_all = not self.show_all
        for check_button, label in zip(self.check_button_list, self.lbl_renamed_list):
            if self.show_all:
                check_button.grid()
                label.grid()
            else:
                # not checked
                if not check_button.val.get():
                    # grid will hide the widget but the widget will still remember the positions, calling grid() on the widget will show them again
                    check_button.grid_remove()
                    label.grid_remove()

        self.update_renaming_count()

    def update_selected_count(self):
        total = 0
        for check_button in self.check_button_list:
            if check_button.val.get():
                total += 1

        self.lbl_items_selected.config(text=f"Items Selected: {total}")

    def update_renaming_count(self):
        total = 0
        for label in self.lbl_renamed_list:
            if label["text"] != "":
                total += 1

        print(f"Renaming count: {total}")
        self.lbl_items_renaming.config(text=f"Item Renaming: {total}")

    def check_button_callback(self, index):
        """Auxiliary function to encapsulate the index value with the callback function """

        def callback():
            check_button = self.check_button_list[index]
            label = self.lbl_renamed_list[index]
            print(check_button, index)

            # check item
            if check_button.val.get():
                label.grid()
                pass
            # uncheck item
            else:
                label.grid_remove()

            # TODO: can make bottom operations to O(1)
            self.update_renamed()
            self.update_selected_count()
            self.update_renaming_count()

        return callback

    def add_item(self, text, level):
        """Add new item to canvas frame """
        # used to represent value of checkbox , 1 or 0, set default to selected
        int_var = tk.IntVar(value=1)

        original = tk.Checkbutton(
            self.canvas_frame,
            text=text,
            variable=int_var,
            bg="yellow",
            command=self.check_button_callback(len(self.check_button_list)),
        )
        # set int_var as attribute of original
        original.val = int_var

        original.grid(
            # +1 to exclude the first row which contain the columns name
            row=len(self.check_button_list) + 1,
            column=0,
            ipadx=(20 * level,),
            pady=1,
            sticky="w",
        )

        renamed = tk.Label(self.canvas_frame, text="", bg="green")
        renamed.grid(
            row=len(self.lbl_renamed_list) + 1,
            column=1,
            sticky="w",
        )

        self.check_button_list.append(original)
        self.lbl_renamed_list.append(renamed)

    def get_items(self):
        self.__get_items(
            pathlib.Path("C:/Users/kahkeong/Desktop/Code/power-rename-clone/test"), 0
        )

        self.update_selected_count()
        self.update_renaming_count()
        # ensure the UI is updated
        self.canvas_frame.update_idletasks()
        self.scroll_bar_frame.on_canvas_configure(None)

    def __get_items(self, path, level):
        """
        Starting from root, get_itemsly go into sub folders and get the folders and files name.
        By default, process the folders first before files

        Keyword arguments:
        path - path to a folder
        level - level of this folder starting from root
        """
        dir_list = [x for x in path.iterdir() if x.is_dir()]
        for dir in dir_list:
            self.add_item(str(dir.name), level)
            new_path = pathlib.Path(f"{dir.resolve()}")
            self.__get_items(new_path, level + 1)

        file_list = [x for x in path.iterdir() if x.is_file()]
        for file in file_list:
            self.add_item(str(file.name), level)