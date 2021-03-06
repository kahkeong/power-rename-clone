import tkinter as tk
from item_list import ItemList
from preview_frame import PreviewFrame
from bottom_frame import BottomFrame
from debug_frame import DebugFrame
from search_frame import SearchFrame
from option_frame import OptionFrame


window = tk.Tk()
window.title("PowerRename Clone")

window.columnconfigure(0, minsize=300, weight=1)
window.rowconfigure(2, minsize=300, weight=1)
print("hello")


item_list = ItemList()
# search frame
frame_search = SearchFrame(
    item_list=item_list, parent_object=window, background="green"
)

# option frame
frame_option = OptionFrame(
    item_list=item_list, parent_object=window, background="purple"
)

# preview frame

frame_preview = PreviewFrame(
    item_list=item_list, parent_object=window, background="brown"
)
item_list.canvas_frame = frame_preview.internal_frame
item_list.scroll_bar_frame = frame_preview

# bottom bar frame
frame_bottom_bar = BottomFrame(parent_object=window, background="yellow")

item_list.lbl_items_selected = frame_bottom_bar.lbl_items_selected
item_list.lbl_items_renaming = frame_bottom_bar.lbl_items_renaming

# debug frame
frame_debug = DebugFrame(item_list=item_list, parent_object=window, background="gray")

item_list.get_items()
window.mainloop()