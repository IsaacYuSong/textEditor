import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Text Editor")

        # Create a sidebar
        self.sidebar = tk.Frame(root, width=200, bg="gray")
        self.sidebar.pack(expand="no", fill="y", side="left")

        self.tree = ttk.Treeview(self.sidebar)
        self.tree.pack(expand="yes", fill="both")

        # Configure the treeview columns
        self.tree["columns"] = ("Name", "Type")
        self.tree.column("#0", width=0, stretch="no")
        self.tree.column("Name", anchor="w", width=150)
        self.tree.column("Type", anchor="w", width=50)

        # Define column headings
        self.tree.heading("#0", text="", anchor="w")
        self.tree.heading("Name", text="Name", anchor="w")
        self.tree.heading("Type", text="Type", anchor="w")

        # Create a text widget
        self.text_widget = tk.Text(root, wrap="word", undo=True, foreground="white", background="black", insertbackground="white", selectbackground="blue")
        self.text_widget.pack(expand="yes", fill="both")

        # Create a menu bar
        self.menu_bar = tk.Menu(root)
        self.root.config(menu=self.menu_bar)

        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Open Folder", command=self.open_folder)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.destroy)

        # Edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=self.text_widget.edit_undo)
        self.edit_menu.add_command(label="Redo", command=self.text_widget.edit_redo)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=self.cut_text)
        self.edit_menu.add_command(label="Copy", command=self.copy_text)
        self.edit_menu.add_command(label="Paste", command=self.paste_text)

        # View menu
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)
        self.view_menu.add_checkbutton(label="Dark Mode", command=self.toggle_dark_mode)

        # Tools menu
        self.tools_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Tools", menu=self.tools_menu)
        self.tools_menu.add_command(label="Word Count", command=self.get_word_count)

        self.dark_mode = False

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.text_widget.delete(1.0, tk.END)
                self.text_widget.insert(tk.END, content)

    def open_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            # Clear existing items in the treeview
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Insert folder items into the treeview
            self.insert_folder_items("", folder_path)

    def insert_folder_items(self, parent, path):
        items = os.listdir(path)
        for item in items:
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                # Insert folder item
                self.tree.insert(parent, "end", text=item, values=("Folder",))
                # Recursively insert items in the folder
                self.insert_folder_items(item, item_path)
            elif os.path.isfile(item_path):
                # Insert file item
                self.tree.insert(parent, "end", text=item, values=("File",))

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                content = self.text_widget.get(1.0, tk.END)
                file.write(content)

    def cut_text(self):
        self.text_widget.event_generate("<<Cut>>")

    def copy_text(self):
        self.text_widget.event_generate("<<Copy>>")

    def paste_text(self):
        self.text_widget.event_generate("<<Paste>>")

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.text_widget.config(foreground="white", background="black", insertbackground="white", selectbackground="blue")
        else:
            self.text_widget.config(foreground="black", background="white", insertbackground="black", selectbackground="blue")

    def get_word_count(self):
        content = self.text_widget.get(1.0, tk.END)
        words = content.split()
        word_count = len(words)
        messagebox.showinfo("Word Count", f"Total words: {word_count}")

if __name__ == "__main__":
    root = tk.Tk()
    text_editor = TextEditor(root)
    root.mainloop()
