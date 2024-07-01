import tkinter as tk
from tkinter import messagebox, ttk
import pyperclip
import json
import os, platform
import string
import random
import webbrowser

class PasswordManager:
    def __init__(self, master):
        # Make main window
        self.master = master
        self.master.title("Password Manager")
        self.master.geometry("400x600")
        self.passwords = {}

        # Load passwords from file
        self.load_passwords()

        # Create Interface of main window
        self.frame = ttk.Frame(self.master)
        self.frame.pack(fill="both", expand=True)

        self.label = ttk.Label(self.frame, text="Login: ")
        self.label.pack(pady=10)

        self.entry = ttk.Entry(self.frame, width=40)
        self.entry.pack()

        self.label2 = ttk.Label(self.frame, text="Password: ")
        self.label2.pack(pady=10)

        self.entry2 = ttk.Entry(self.frame, width=40)
        self.entry2.pack()
        
        self.button_generate = ttk.Button(self.frame, text="Generate Password", command=self.generate_password)
        self.button_generate.pack(pady=10)

        self.use_symbols_var = tk.IntVar()
        self.use_symbols_checkbox = ttk.Checkbutton(self.frame, text="Use symbols", variable=self.use_symbols_var)
        self.use_symbols_checkbox.pack(pady=10)

        self.button = ttk.Button(self.frame, text="Add", command=self.add_password)
        self.button.pack(pady=10)

        # Create treeview for passwords
        self.treeview = ttk.Treeview(self.frame, columns=("Login", "Password"))
        self.treeview.pack(fill="both", expand=True)

        self.treeview.column("#0", width=0, stretch=tk.NO)
        self.treeview.column("Login", anchor=tk.W, width=200)
        self.treeview.column("Password", anchor=tk.W, width=200)

        self.treeview.heading("#0", text="", anchor=tk.W)
        self.treeview.heading("Login", text="Login", anchor=tk.W)
        self.treeview.heading("Password", text="Password", anchor=tk.W)

        # Update it
        self.update_treeview()

        # Create hotkeys
        self.treeview.bind("<Double-1>", self.treeview_item_click)  
        self.treeview.bind("<BackSpace>", self.delete_password)
        self.master.bind("<Return>", lambda event: self.add_password())
        if platform.system() == 'Darwin':  # macOS
            self.master.bind("<Command-e>", lambda event: self.edit_password_window())
        else:  # Windows, Linux
            self.master.bind("<Control-e>", lambda event: self.edit_password_window())

        # Create top menu bar
        self.menu = tk.Menu(self.master, tearoff=0)
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.help_menu = tk.Menu(self.menu, tearoff=0)
        self.master.config(menu=self.menu)
        
        # Password menu
        self.menu.add_cascade(label="Password", menu=self.file_menu)
        self.file_menu.add_command(label="Delete", command=self.delete_password)
        self.file_menu.add_command(label="Edit", command=self.edit_password_window)
        
        # Help menu
        self.menu.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="Dev's Github", command=lambda: webbrowser.open('https://github.com/fynjirby'))
        self.help_menu.add_command(label="About", command=lambda: self.about_window())

    # Make on click func
    def treeview_item_click(self, event):
        # Init Password and Website
        item = self.treeview.selection()[0]
        website = self.treeview.item(item, "values")[0]
        password = self.passwords[website]

        # Create window
        password_window = tk.Toplevel(self.master)
        password_window.title("Password")        
        password_window.geometry("170x300")

        # Create Interface for Password view window
        label_website = ttk.Label(password_window, text="Login: ")
        label_website.pack(pady=10)

        label_website_value = ttk.Label(password_window, text=website)
        label_website_value.pack(pady=10)

        label_password = ttk.Label(password_window, text="Password: ")
        label_password.pack(pady=10)

        label_password_value = ttk.Label(password_window, text=password)
        label_password_value.pack(pady=10)

        #Create copy password func
        def copy_password(event=None):
            pyperclip.copy(website + ' & ' + password)

        # Create copy button
        button_copy = ttk.Button(password_window, text="Copy", command=lambda event=None: copy_password(event))
        button_copy.pack(pady=10)
        label_copy = ttk.Label(password_window, text="Cmd + C | Ctrl + C")
        label_copy.pack(pady=10)
        if platform.system() == 'Darwin':
            password_window.bind("<Command-c>", copy_password)  # macOS
        else:
            password_window.bind("<Control-c>", copy_password)  # Windows, Linux
        button_edit = ttk.Button(password_window, text="Edit", command=lambda: self.edit_password_window())
        button_edit.pack(pady=0)

    # Create load passwords func
    def load_passwords(self):
        if os.path.exists("passwords.json"):
            with open("passwords.json", "r") as f:
                self.passwords = json.load(f)
        else:
            with open("passwords.json", "w") as f:
                json.dump({}, f)

    # Create save passwords func
    def save_passwords(self):
        with open("passwords.json", "w") as f:
            json.dump(self.passwords, f)

    # Create generate password func
    def generate_password(self):
        length = random.randint(8, 12)
        chars = string.ascii_letters + string.digits
        if self.use_symbols_var.get():
            chars += string.punctuation
        password = ''.join(random.choice(chars) for _ in range(length))
        self.entry2.delete(0, tk.END)
        self.entry2.insert(0, password)

    # Create add password func
    def add_password(self):
        website = self.entry.get()
        password = self.entry2.get()
        if website and password:  # Check if both fields are not empty
            self.passwords[website] = password
            self.entry.delete(0, tk.END)
            self.entry2.delete(0, tk.END)
            self.update_treeview()
            self.save_passwords()
        else:
            messagebox.showerror("Error", "Can't save empty password!")

    # Creeate edit password func
    def edit_password(self, event):
        item = self.treeview.selection()[0]
        website = self.treeview.item(item, "values")[0]
        password = self.treeview.item(item, "values")[1]
        self.entry.insert(0, website)
        self.entry2.insert(0, password)
        
    # Create edit password window
    def edit_password_window(self):
        selection = self.treeview.selection()
        if selection: # Check if selection choosed
            #Init password and website
            item = selection[0]
            website = self.treeview.item(item, "values")[0]
            password = self.passwords[website]

            # Create window
            edit_window = tk.Toplevel(self.master)
            edit_window.title("Edit Password")

            # Create interface
            label_website = ttk.Label(edit_window, text="Login: ")
            label_website.pack(pady=10)

            entry_website = ttk.Entry(edit_window, width=40)
            entry_website.insert(0, website)
            entry_website.pack()

            label_password = ttk.Label(edit_window, text="Password: ")
            label_password.pack(pady=10)

            entry_password = ttk.Entry(edit_window, width=40)
            entry_password.insert(0, password)
            entry_password.pack()
            
            # Create save changes func
            def save_changes(event=None):
                new_website = entry_website.get()
                new_password = entry_password.get()
                self.passwords[new_website] = new_password
                if new_website != website:
                    del self.passwords[website]
                self.update_treeview()
                self.save_passwords()
                edit_window.destroy()

            # Create save button
            button_save = ttk.Button(edit_window, text="Save", command=save_changes)
            button_save.pack(pady=10)
            edit_window.bind("<Return>", lambda event: save_changes())
        else:
            messagebox.showerror("Error", "No password selected")

    # Create delete password func
    def delete_password(self, event=None):
        selection = self.treeview.selection()
        if selection: # Check if selection choosed
            item = selection[0]
            website = self.treeview.item(item, "values")[0]
            del self.passwords[website]
            self.update_treeview()
            self.save_passwords()
        else:
            messagebox.showerror("Error", "No password selected")

    # Create update treeview func
    def update_treeview(self):
        self.treeview.delete(*self.treeview.get_children())
        for website, password in self.passwords.items():
            self.treeview.insert("", tk.END, values=(website, "*" * len(password)))

    # Create about window
    def about_window(self):
        about_window = tk.Toplevel(self.master)
        about_window.title("About")
        about_window.geometry("200x60")
        copyright = ttk.Label(about_window, text="Fynjirby 2024 ©")
        copyright.pack(pady=5)
        link = ttk.Label(about_window, text="Source code (click)")
        link.pack()
        link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/fynjirby/passmngr"))
        
# Just need :)
root = tk.Tk()
my_manager = PasswordManager(root)
root.mainloop()