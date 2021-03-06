import tkinter as tk
import pathlib
import logging

logging.basicConfig(level=logging.DEBUG)


class ItemList(object):
    def __init__(self):
        self.check_button_list = []
        self.lbl_renamed_list = []
        self.path_object_list = []
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
        Update the list of items that are showing at the renamed column based on the selected options, the searched value and replace with value
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

            # first, there are some options which determine whether a name is eligible to be renamed
            # after we go through all the filter options, if the filtered name is not empty, then we can proceed to determine the renamed name of the original name

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

    def display_widgets(self):
        # for item
        for index, (check_button, lbl_renamed) in enumerate(
            zip(self.check_button_list, self.lbl_renamed_list)
        ):
            _, level = self.path_object_list[index]

            check_button.grid(
                # +1 to exclude the first row which contain the columns name
                row=index + 1,
                column=0,
                ipadx=(20 * level,),
                pady=1,
                sticky="w",
            )
            lbl_renamed.grid(
                row=index + 1,
                column=1,
                sticky="w",
            )

    def create_widgets(self):
        """Create all widgets from the populated path objects list that we have gotten"""

        for path_object, _ in self.path_object_list:
            # used to represent value of checkbox , 1 or 0, set default to selected
            int_var = tk.IntVar(value=1)
            check_button = tk.Checkbutton(
                self.canvas_frame,
                text=path_object.name,
                variable=int_var,
                bg="yellow",
                command=self.check_button_callback(len(self.check_button_list)),
            )
            # set int_var as attribute of check_button
            check_button.val = int_var

            lbl_renamed = tk.Label(self.canvas_frame, text="", bg="green")

            self.check_button_list.append(check_button)
            self.lbl_renamed_list.append(lbl_renamed)

    def option_make_uppercase(self, value):
        return value.upper()

    def option_make_lowercase(self, value):
        return value.lower()

    def option_make_titlecase(self, value):
        return value.titlecase()

    def option_item_name_(self, pathlib_object):
        return pathlib_object.stem

    def option_item_extension(self, pathlib_object):
        return pathlib_object.suffix

    def option_enumerate_item(self, pathlib_object, index):
        """
        Appends a numeric suffix to file names that were modified in the operation. For example: test.jpg -> test (1).jpg
        """

        # if item name is test.tar.gz, it should be renamed to test (1).tar.gz instead of test.tar (1).gz
        path_suffixes = pathlib_object.suffixes
        value = f"pathlib_object.stem ({index})" + "".join(path_suffixes)
        return value

    def update_option(self, options, rules):
        print(f"update option: {options}")
        for index, option in enumerate(options):
            if option.get():
                print(rules[index])

    def get_items(self):
        self.__get_items(
            pathlib.Path("C:/Users/kahkeong/Desktop/Code/power-rename-clone/test"), 0
        )
        self.create_widgets()
        self.display_widgets()
        self.update_selected_count()
        self.update_renaming_count()
        # ensure the UI is updated
        self.canvas_frame.update_idletasks()
        self.scroll_bar_frame.on_canvas_configure(None)

    def __get_items(self, path, level):
        """
        Starting from root, get_items go into sub folders and retrieve the pathlib object that represent each of the folders and files.
        By default, process the folders first before files

        Keyword arguments:
        path - path object of a folder
        level - level of this folder starting from root
        """
        dir_path_objects = [x for x in path.iterdir() if x.is_dir()]
        for dir_path_object in dir_path_objects:
            self.path_object_list.append((dir_path_object, level))
            new_path = pathlib.Path(f"{dir_path_object.resolve()}")
            self.__get_items(new_path, level + 1)

        file_path_objects = [x for x in path.iterdir() if x.is_file()]
        for file_path_object in file_path_objects:
            self.path_object_list.append((file_path_object, level))