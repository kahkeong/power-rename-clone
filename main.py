import tkinter as tk
from tkinter.constants import RIDGE
from preview_frame import PreviewFrame, ItemList
from bottom_frame import BottomFrame
from debug_frame import DebugFrame
from search_frame import SearchFrame
from option_frame import OptionFrame

from tkinter.filedialog import askopenfilename, asksaveasfilename
from typing import Text


window = tk.Tk()
window.title("PowerRename Clone")

window.columnconfigure(0, minsize=300, weight=1)
window.rowconfigure(2, minsize=300, weight=1)
print('hello')
# search frame
frame_search = SearchFrame(parentObject=window, background="green")

# option frame
frame_option = OptionFrame(parentObject=window, background="purple")

# preview frame
frame_preview = PreviewFrame(parentObject=window, background="brown")
item_list = ItemList(frame_preview, frame_preview.internal_frame)
item_list.populate()

# bottom bar frame
frame_bottom_bar = BottomFrame(parentObject=window, background="yellow")

# debug frame
frame_debug = DebugFrame(item_list=item_list, parentObject=window, background="gray")


window.mainloop()