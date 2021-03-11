from os import read
import tkinter as tk
import logging.config
from item_list import ItemList
from preview_frame import PreviewFrame
from bottom_frame import BottomFrame
from search_frame import SearchFrame
from option_frame import OptionFrame
import pathlib
import sys

logging.config.fileConfig(fname="logging.conf")


def read_input():
    arg_list = sys.argv
    path_object = None
    hint = "input must be an absolute path to the directory that you would like to run this program"

    try:
        if len(arg_list) == 1:
            raise AssertionError(f"no input is provided, {hint}")
        else:
            path = str(arg_list[1])
            path_object = pathlib.Path(path)

            if not (path_object.exists() and path_object.is_dir()):
                path_object = None
                raise IndexError("")

    except AssertionError as error:
        logging.debug(error)
    except:
        logging.debug(f"invalid input: {arg_list[1]}, {hint}")

    return path_object


def run(path_object):
    window = tk.Tk()
    window.title("PowerRename Clone")

    window.columnconfigure(0, minsize=300, weight=1)
    window.rowconfigure(2, minsize=300, weight=1)

    item_list = ItemList(path_object)
    # search frame
    frame_search = SearchFrame(item_list=item_list, parent_object=window)

    # option frame
    frame_option = OptionFrame(item_list=item_list, parent_object=window)

    # preview frame
    frame_preview = PreviewFrame(item_list=item_list, parent_object=window)

    # bottom bar frame
    frame_bottom_bar = BottomFrame(item_list=item_list, parent_object=window)

    item_list.canvas_frame = frame_preview.internal_frame
    item_list.scroll_bar_frame = frame_preview
    item_list.bottom_frame = frame_bottom_bar
    frame_bottom_bar.item_list = item_list

    item_list.get_items()
    window.mainloop()


def main():
    path_object = read_input()
    if path_object:
        run(path_object)


if __name__ == "__main__":
    main()