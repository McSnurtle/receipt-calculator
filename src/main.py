#src/main.py
# imports
import tkinter as tk
from tkinter.filedialog import askopenfile
from typing import Any, List, Dict, IO
from utils.models import Receipt
from utils.platform import get_version, get_conf
from utils.receipts import get_last_receipt, get_receipts, get_receipt
from pages import Overview, Editor

# vars
pass


class Root(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.frames: Dict[str, tk.Frame] = {}
        self.receipts: List[Receipt] = []
        self.current_receipt: Receipt | None = None

        self.setup()
        self.layout()
        
        # DEBUG
        self.show_frame("overview")
        
    def setup(self) -> None:
        """Initial setup of the tkinter window"""

        self.title(f"Bill Splitter 9000 v{get_version()} - by Mc_Snurtle")
        self.geometry(f"400x600+{(self.winfo_screenwidth()//2)-200}+{(self.winfo_screenheight()//2)-300}")
        self.resizable(False, False)

        self.current_receipt: Receipt | None = get_conf()["lastReceipt"]

    def layout(self) -> None:
        """Setup the layout for the window."""

        # menubar
        menubar: tk.Menu = tk.Menu(self, tearoff=False)
        self["menu"] = menubar
        filemenu: tk.Menu = tk.Menu(menubar, tearoff=False)
        filemenu.add_command(label="Save (Ctrl+S)", command=self.save_receipt)
        filemenu.add_command(label="Open (Ctrl+O)", command=self.open_receipt)
        filemenu.add_separator()
        filemenu.add_command(label="Create New (Ctrl+N)", command=self.new_receipt)
        menubar.add_cascade(menu=filemenu, label="Receipt")

        # receipt overview
        overview_frame: tk.Frame = Overview(self, edit_func=self.open_receipt, del_func=self.del_receipt)
        self.frames["overview"] = overview_frame

        # receipt editor
        editor_frame: tk.Frame = Editor(self, self.current_receipt)
        self.frames["editor"] = editor_frame

    def show_frame(self, key: str) -> Dict[str, tk.Frame]:
        """Hides all frames and shows the specified frame.
        
        :param key: str, the name of the frame to pack as found in `Root.frames`.

        :return hidden_frames: Dict[str, tk.Frame], a dictionary of all the frames that were forcibly hidden during the showing of the specified frame.
        """

        print(f"SHOWING FRAME: {key}")
        [frame.pack_forget() for frame in self.frames.values()]
        self.frames[key].pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        return self.frames.copy().pop(key)

    def save_receipt(self, callback: Any = None) -> Receipt:
        pass
    
    def open_receipt(self, filename: str | None = None) -> Receipt:
        if filename is None:    # if not filename was selected
            file: IO[Any] = askopenfile(mode="r", defaultextension=".json") # ask the user to pick a file
            if file is None:    # if user cancelled operation
                return
            self.current_receipt = Receipt.from_file(file)
        else:
            self.current_receipt = get_receipt(filename)
        self.populate_editor()
        self.show_frame("editor")
    
    def new_receipt(self, callback: Any = None) -> Receipt:
        pass
    
    def del_receipt(self, filename: str) -> str:
        return filename
            
    def populate_editor(self) -> None:
        self.frames["editor"] = Editor(self.current_receipt)
    
    
if __name__ == "__main__":
    root = Root()
    root.mainloop()
    