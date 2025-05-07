"""Main file for the application.

Returns:
    None: N/A
"""
#src/main.py
# imports
import tkinter as tk
from tkinter.filedialog import askopenfile
from typing import Any, List, Dict
from utils.models import Receipt
from utils.platform import get_version, get_conf, update_conf
from utils.receipts import get_receipt_by_id, get_last_receipt # type: ignore
from pages import Overview, Editor


class Root(tk.Tk):
    """_summary_

    Args:
        tk (tk.Tk): _description_
    """
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        self.frames: Dict[str, tk.Frame] = {}
        self.receipts: List[Receipt] = []
        self.current_rid: int | None = get_conf()["lastReceipt"]
        self.current_receipt: Receipt | None = None

        self.setup()
        self.layout()

        self.bind("<Control-n>", self.new_receipt)
        self.bind("<Control-o>", self.open_receipt)
        self.bind("<Control-s>", self.save_current_receipt)
        self.bind("<Control-q>", self.quit)

        if self.current_rid is None:    # if no receipt ID was found in the config file...
            self.show_frame("overview")
        else:   # if there was...
            self.current_receipt = get_receipt_by_id(self.current_rid)
            self.refresh_editor()
            self.show_frame("editor")

    def setup(self) -> None:
        """Initial setup of the tkinter window"""

        self.title(f"Bill Splitter 9000 v{get_version()} - by Mc_Snurtle")
        self.geometry(f"400x600+{(self.winfo_screenwidth()//2)-200}+{(self.winfo_screenheight()//2)-300}")
        self.resizable(False, False)

    def layout(self) -> None:
        """Setup the layout for the window."""

        # menubar
        menubar: tk.Menu = tk.Menu(self, tearoff=False)
        self["menu"] = menubar
        filemenu: tk.Menu = tk.Menu(menubar, tearoff=False)
        filemenu.add_command(label="Save (Ctrl+S)", command=self.save_current_receipt)
        filemenu.add_command(label="Open (Ctrl+O)", command=self.open_receipt)
        filemenu.add_separator()
        filemenu.add_command(label="Create New (Ctrl+N)", command=self.new_receipt)
        navigationmenu: tk.Menu = tk.Menu(menubar, tearoff=False)
        navigationmenu.add_command(label="Overview", command=lambda: self.show_frame("overview"))
        menubar.add_cascade(menu=filemenu, label="Receipt")

        # receipt overview
        overview_frame: tk.Frame = Overview(master=self, edit_func=self.open_receipt, del_func=self.del_current_receipt)
        self.frames["overview"] = overview_frame

        # receipt editor
        editor_frame: tk.Frame = tk.Frame(self) # <== placeholder for the Editor page
        self.frames["editor"] = editor_frame
        # NOTE: this has been moved to `self.populate_editor` so lambdas can be used to pass in the functions relevant to the specific receipts.

    def show_frame(self, key: str) -> Dict[str, tk.Frame]:
        """Hides all frames and shows the specified frame.

        :param key: str, the name of the frame to pack as found in `Root.frames`.

        :return hidden_frames: Dict[str, tk.Frame], a dictionary of all the frames that were forcibly hidden during the showing of the specified frame.
        """

        print(f"SHOWING FRAME: {key}")
        _ = [frame.pack_forget() for frame in self.frames.values()]
        self.frames[key].pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        hidden_frames = self.frames.copy()
        hidden_frames.pop(key)
        return hidden_frames

    def open_receipt(self, callback: Any = None, rid: int | None = None) -> Receipt | None:
        """Opens the specified receipt in the Editor view, asks user with file dialog if no filename is specified.

        Args:
            rid (int | None, optional): The receipt ID of the receipt to load. Defaults to None.

        Returns:
            Receipt | None: The receipt that was loaded.
        """
        if rid is None:    # if no receipt ID was specified
            file: Any = askopenfile(mode="r", defaultextension=".json", initialdir="data/receipt", initialfile=f"data/receipts/{get_last_receipt()}.json") # ask the user to pick a file
            if file is None:    # if user cancelled operation
                return
            self.current_receipt = Receipt.from_file(file) # type: ignore
        else:   # if a receipt ID was specified
            self.current_receipt = get_receipt_by_id(rid=rid)
        print("Current receipt:", self.current_receipt.name)    # type: ignore
        update_conf("lastReceipt", self.current_receipt.id) # type: ignore
        self.refresh_editor()
        self.show_frame("editor")

    # NOTE: COMING SOON...
    def new_receipt(self, callback: Any = None) -> None:
        """_summary_"""
        return callback

    # NOTE: COMING SOON...
    def save_current_receipt(self, callback: Any = None) -> None:
        """_summary_"""
        return callback

    # NOTE: COMING SOON...
    def del_current_receipt(self, filename: str) -> str:
        """_summary_"""
        return filename

    def calc_current_receipt(self) -> None:
        """_summary_"""
        return

    def refresh_editor(self) -> None:
        """Updates the Editor view for the window with the relevant information if the `self.current_receipt` is set."""

        if self.current_receipt is not None:
            self.frames["editor"].pack_forget() # remove the old editor frame
            self.frames["editor"].destroy()
            self.frames["editor"] = Editor(master=self, receipt=self.current_receipt, save_func=self.save_current_receipt, del_func=self.del_current_receipt, calc_func=self.calc_current_receipt)
            
    def quit(self, callback: Any = None) -> None:
        """Quits the application."""
        self.destroy()
        self.quit()


if __name__ == "__main__":
    root = Root()
    root.mainloop()
