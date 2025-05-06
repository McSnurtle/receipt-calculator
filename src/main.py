#src/main.py
# imports
import os
import json
import tkinter as tk
from typing import Any, List, Dict
from utils.models import Receipt
from utils.ui import ReceiptPreview, ScrollableFrame
from utils.platform import popup, get_receipts

# vars
pass


class Root(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.frames: Dict[str, tk.Frame] = {}
        self.receipts: List[Receipt] = []

        self.setup()
        self.layout()
        
        # DEBUG
        self.show_frame("overview")
        
    def setup(self) -> None:
        """Initial setup of the tkinter window"""

        self.title("Bill Splitter 9000 - by Mc_Snurtle")
        self.geometry(f"400x600+{(self.winfo_screenwidth()//2)-200}+{(self.winfo_screenheight()//2)-300}")
        self.resizable = False

        self.fetch_receipts()

    def layout(self) -> None:
        """Setup the layout for the window."""

        # receipt overview
        overview_frame: tk.Frame = tk.Frame(self)
        self.frames["overview"] = overview_frame
        title_label: tk.Label = tk.Label(overview_frame, text="Receipts", font=("Helvetica", 24))
        title_label.pack(side=tk.TOP, padx=5, pady=5, anchor=tk.NW)
        receipt_list_frame: tk.Frame = ScrollableFrame(parent=overview_frame)
        receipt_list_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True, side=tk.BOTTOM, anchor=tk.S)
        for receipt in get_receipts():
            receipt_frame: tk.Frame = ReceiptPreview(receipt=receipt, edit_func=lambda r=receipt.name: print(f"Clicked {r}!"), del_func=lambda r=receipt.name: print(f"Deleting {r}!"), master=receipt_list_frame.viewPort)
            receipt_frame.pack(padx=10, pady=10, side=tk.TOP, anchor=tk.N, fill=tk.X, expand=True)

        # receipt creator
        
        # receipt editor
    
    def show_frame(self, key: str) -> Dict[str, tk.Frame]:
        """Hides all frames and shows the specified frame.
        
        :param key: str, the name of the frame to pack as found in `Root.frames`.

        :return hidden_frames: Dict[str, tk.Frame], a dictionary of all the frames that were forcibly hidden during the showing of the specified frame.
        """

        [frame.pack_forget() for frame in self.frames.values()]
        self.frames[key].pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        return self.frames.copy().pop(key)
    
    def fetch_receipts(self) -> List[Receipt]:
        receipts: List[Receipt] = get_receipts()
    
    
if __name__ == "__main__":
    root = Root()
    root.mainloop()
    