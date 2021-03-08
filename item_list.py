import tkinter as tk
import pathlib
import logging
import re


class ItemList(object):
    def __init__(self):
        self.check_button_list = []
        self.lbl_renamed_list = []
        self.path_object_list = []
        self.selected_options = []
        self.search = ""
        self.replace = ""
        self.show_checked_only = False
        self.show_renamed_only = False

        # reference to objects from other classes assigned at main.py
        self.canvas_frame = None
        self.scroll_bar_frame = None
        self.lbl_items_selected = None
        self.lbl_items_renaming = None

    def update_renamed(self):
        """
        Update the list of items that are showing at the renamed column based on the selected options, the searched value and replace with value
        """
        enumerate_index = 1

        for (path_object, level), check_button, label in zip(
            self.path_object_list, self.check_button_list, self.lbl_renamed_list
        ):
            skip = False
            match = True
            item_name = check_button["text"]
            new_name = item_name

            # We do filter according to below sequential code, if an item is filtered out, it means it is not eligible to be renamed
            # Then, we check whether the file/dir match the "search" input, if there is no match, means there is nothing to rename for this file/dir

            # user did not select this file/dir to rename
            if not check_button.val.get():
                skip = True

            # path_object match one of the following statements so should not be renamed
            if "Exclude Folders" in self.selected_options and path_object.is_dir():
                skip = True
            elif "Exclude Files" in self.selected_options and path_object.is_file():
                skip = True
            elif "Exclude Subfolder Items" in self.selected_options and level >= 1:
                skip = True

            if skip:
                logging.info(f"file name: {item_name} is skipped")
                label.config(text="")
                continue

            # the scope of the name that shall be renamed
            if "Item Name Only" in self.selected_options:
                new_name = path_object.stem
            elif "Item Extension Only" in self.selected_options:
                new_name = path_object.suffix

            # built-in "in" function is case sensitive by default
            if "Case Sensitive" in self.selected_options:
                if self.search in new_name:
                    match = True
                    # by default, build in function "replace" will replace all occurences
                    if "Match All Occurences" in self.selected_options:
                        new_name = new_name.replace(self.search, self.replace)
                    else:
                        new_name = new_name.replace(self.search, self.replace, 1)
            else:
                # since regex is not enabled, escape all special characters
                search_name = re.escape(self.search)
                if re.search(search_name, new_name, flags=re.IGNORECASE):
                    match = True
                    if "Match All Occurences" in self.selected_options:
                        new_name = re.sub(
                            search_name, self.replace, new_name, flags=re.IGNORECASE
                        )
                    else:
                        new_name = re.sub(
                            search_name, self.replace, new_name, 1, flags=re.IGNORECASE
                        )

            if not match:
                logging.info("file name: {item_name} has no match for search input")

            # Note, even if there are no matches, if any one of the case change options match, we will still rename the original name
            if "Make Uppercase" in self.selected_options:
                if new_name != new_name.upper():
                    new_name = new_name.upper()
            elif "Make Lowercase" in self.selected_options:
                if new_name != new_name.lower():
                    new_name = new_name.lower()
            elif "Make Titlecase" in self.selected_options:
                old_path = path_object
                # titlecase should have no effect on item extension
                if old_path.stem != new_name.title():
                    new_name = new_name.title()

            # if one of the following options are valid, means we actually edited either the name (stem) or the extension path,
            # so we need to add back the name (stem) or the extension
            if "Item Name Only" in self.selected_options:
                new_name = new_name + path_object.suffix
            elif "Item Extension Only" in self.selected_options:
                new_name = path_object.stem + new_name

            if "Enumerate Items" in self.selected_options:
                # only apply to name that will be renamed
                if new_name != item_name:
                    # making the new_name as Path object just to get the stem and suffix more easily
                    new_path = pathlib.Path(new_name)

                    # special consideration for name start with "." like ".gitignore", path_instance.stem() return ".gitignore" instead of empty
                    if new_path.stem[0] == ".":
                        new_name = f"({enumerate_index}){new_name}"
                    else:
                        new_name = (
                            f"{new_path.stem} ({enumerate_index}){new_path.suffix}"
                        )
                    enumerate_index += 1

            if new_name != item_name:
                logging.info(
                    f"old name: {item_name} will be renamed to new name: {new_name}"
                )
                label.config(text=new_name)
            else:
                label.config(text="")

    def update_search(self, value):
        """
        Update the search keyword. As search keyword is updated, the previously items that are eligible to be renamed might not longer be valid.
        So we need the update the appropriate components.
        """
        self.search = value
        self.update_renamed()
        self.update_display_widgets()
        self.update_renaming_count()

    def update_replace(self, value):
        """
        Update the replace value. Since no other components will be affected, we just need to update the renamed column.
        """
        self.replace = value
        self.update_renamed()

    def update_selected_count(self):
        """
        Update the selected count UI at bottom left corner
        """
        total = 0
        for check_button in self.check_button_list:
            if check_button.val.get():
                total += 1

        self.lbl_items_selected.config(text=f"Items Selected: {total}")
        logging.info(f"Selected count: {total}")

    def update_renaming_count(self):
        """
        Update the renaming count UI at bottom left corner
        """
        total = 0
        for label in self.lbl_renamed_list:
            if label["text"] != "":
                total += 1

        self.lbl_items_renaming.config(text=f"Item Renaming: {total}")
        logging.info(f"Renaming count: {total}")

    def check_button_callback(self, index):
        """Callback for each check button in the original column """

        check_button = self.check_button_list[index]
        logging.info(f"button, {check_button['text']} clicked")

        self.update_renamed()
        self.update_display_widgets()
        self.update_selected_count()
        self.update_renaming_count()

    def update_show_renamed_only(self):
        """
        Trigger to show all selected items or show only items that will be renamed
        """
        logging.info("called")
        # only one of them can be True at any time
        self.show_renamed_only = not self.show_renamed_only
        self.show_checked_only = False
        self.update_display_widgets()
        self.update_renaming_count()

    def update_show_checked_only(self):
        """
        Trigger to show all items or show only checked items
        """
        logging.info("called")
        # only one of them can be True at any time
        self.show_checked_only = not self.show_checked_only
        self.show_renamed_only = False
        self.update_display_widgets()

    def update_display_widgets(self):
        """Display the items in both original and renamed columns"""
        logging.info("called")

        # clear everything on the grid
        for _, (check_button, lbl_renamed, path_object) in enumerate(
            zip(self.check_button_list, self.lbl_renamed_list, self.path_object_list)
        ):
            check_button.grid_forget()
            lbl_renamed.grid_forget()

        # populate the grid
        line = 0
        for check_button, lbl_renamed, path_object in zip(
            self.check_button_list, self.lbl_renamed_list, self.path_object_list
        ):
            # show checked rows only
            if self.show_checked_only and not check_button.val.get():
                continue
            # show rows that will be renamed only
            elif self.show_renamed_only and not lbl_renamed["text"]:
                continue

            _, level = path_object

            check_button.grid(
                # +1 to exclude the first row which contain the columns name
                row=line + 1,
                column=0,
                # more left padding for file in inner directories
                ipadx=(20 * level,),
                pady=1,
                sticky="w",
            )
            lbl_renamed.grid(
                row=line + 1,
                column=1,
                sticky="w",
            )
            line += 1

    def create_widgets(self):
        """Create all widgets from the populated path objects list that we have gotten"""

        for index, (path_object, _) in enumerate(self.path_object_list):
            # used to represent value of checkbox, 1 or 0, set default to 1
            int_var = tk.IntVar(value=1)
            check_button = tk.Checkbutton(
                self.canvas_frame,
                text=path_object.name,
                variable=int_var,
                bg="yellow",
                command=lambda index=index: self.check_button_callback(index),
            )
            # set int_var as attribute of check_button
            check_button.val = int_var

            lbl_renamed = tk.Label(self.canvas_frame, text="", bg="green")

            self.check_button_list.append(check_button)
            self.lbl_renamed_list.append(lbl_renamed)

    def update_options(self, options):
        """
        Update the options that are selected
        """
        logging.info("called")
        self.selected_options = options
        self.update_renamed()
        self.update_display_widgets()
        self.update_renaming_count()

    def get_items(self):
        """
        Populate the UI with initial state of the program, i.e. all file/folder names in the directory of where this program was runned
        """
        self._get_items(
            pathlib.Path("C:/Users/kahkeong/Desktop/CKK/From work/multi-docker-master"),
            0,
        )
        self.create_widgets()
        self.update_display_widgets()
        self.update_selected_count()
        self.update_renaming_count()
        # ensure the UI is updated
        self.canvas_frame.update_idletasks()
        self.scroll_bar_frame.on_canvas_configure(None)

    def _get_items(self, path, level):
        """
        Starting from root, get_items go into sub folders and retrieve the pathlib object that represent each of the folders and files.
        By default, process the folders first before files

        Keyword arguments:
        path - path object of a folder
        level - level of this folder starting from the directory of where this program was runned
        """
        dir_path_objects = [x for x in path.iterdir() if x.is_dir()]
        for dir_path_object in dir_path_objects:
            self.path_object_list.append((dir_path_object, level))
            new_path = pathlib.Path(f"{dir_path_object.resolve()}")
            self._get_items(new_path, level + 1)

        file_path_objects = [x for x in path.iterdir() if x.is_file()]
        for file_path_object in file_path_objects:
            self.path_object_list.append((file_path_object, level))