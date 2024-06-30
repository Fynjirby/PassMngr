import tkinter as tk
from tkinter import messagebox, ttk
import pyperclip
import json
import os, platform

class PasswordManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Password Manager")
        self.master.geometry("400x500")
        self.passwords = {}

        # Load passwords from file
        self.load_passwords()

        self.frame = ttk.Frame(self.master)
        self.frame.pack(fill="both", expand=True)

        self.label = ttk.Label(self.frame, text="Website: ")
        self.label.pack(pady=10)

        self.entry = ttk.Entry(self.frame, width=40)
        self.entry.pack()

        self.label2 = ttk.Label(self.frame, text="Password: ")
        self.label2.pack(pady=10)

        self.entry2 = ttk.Entry(self.frame, width=40, show="*")
        self.entry2.pack()

        self.button = ttk.Button(self.frame, text="Add", command=self.add_password)
        self.button.pack(pady=10)

        self.treeview = ttk.Treeview(self.frame, columns=("Website", "Password"))
        self.treeview.pack(fill="both", expand=True)

        self.treeview.column("#0", width=0, stretch=tk.NO)
        self.treeview.column("Website", anchor=tk.W, width=200)
        self.treeview.column("Password", anchor=tk.W, width=200)

        self.treeview.heading("#0", text="", anchor=tk.W)
        self.treeview.heading("Website", text="Website", anchor=tk.W)
        self.treeview.heading("Password", text="Password", anchor=tk.W)

        self.update_treeview()

        self.treeview.bind("<BackSpace>", self.delete_password)
        self.master.bind("<Return>", lambda event: self.add_password())
        if platform.system() == 'Darwin':  # macOS
            self.master.bind("<Command-e>", lambda event: self.edit_password_window())
        else:  # Windows, Linux
            self.master.bind("<Control-e>", lambda event: self.edit_password_window())


        self.menu = tk.Menu(self.master, tearoff=0)
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label="Delete", command=self.delete_password)
        self.file_menu.add_command(label="Edit", command=self.edit_password_window)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.master.config(menu=self.menu)

    def load_passwords(self):
        if os.path.exists("passwords.json"):
            with open("passwords.json", "r") as f:
                self.passwords = json.load(f)
        else:
            with open("passwords.json", "w") as f:
                json.dump({}, f)

    def save_passwords(self):
        with open("passwords.json", "w") as f:
            json.dump(self.passwords, f)

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

    def edit_password(self, event):
        item = self.treeview.selection()[0]
        website = self.treeview.item(item, "values")[0]
        password = self.treeview.item(item, "values")[1]
        self.entry.insert(0, website)
        self.entry2.insert(0, password)

    def edit_password_window(self):
        selection = self.treeview.selection()
        if selection:
            item = selection[0]
            website = self.treeview.item(item, "values")[0]
            password = self.treeview.item(item, "values")[1]

            edit_window = tk.Toplevel(self.master)
            edit_window.title("Edit Password")

            label_website = ttk.Label(edit_window, text="Website: ")
            label_website.pack(pady=10)

            entry_website = ttk.Entry(edit_window, width=40)
            entry_website.insert(0, website)
            entry_website.pack()

            label_password = ttk.Label(edit_window, text="Password: ")
            label_password.pack(pady=10)

            entry_password = ttk.Entry(edit_window, width=40)
            entry_password.insert(0, password)
            entry_password.pack()

            def save_changes():
                new_website = entry_website.get()
                new_password = entry_password.get()
                self.passwords[new_website] = new_password
                if new_website != website:
                    del self.passwords[website]
                self.update_treeview()
                self.save_passwords()  # Save passwords after editing
                edit_window.destroy()

            button_save = ttk.Button(edit_window, text="Save", command=save_changes)
            button_save.pack(pady=10)

        else:
            messagebox.showerror("Error", "No password selected")
                
    def delete_password(self, event=None):
        selection = self.treeview.selection()
        if selection:
            item = selection[0]
            website = self.treeview.item(item, "values")[0]
            del self.passwords[website]
            self.update_treeview()
            self.save_passwords()
        else:
            messagebox.showerror("Error", "No password selected")

    def update_treeview(self):
        self.treeview.delete(*self.treeview.get_children())
        for website, password in self.passwords.items():
            self.treeview.insert("", tk.END, values=(website, password))
root = tk.Tk()
my_manager = PasswordManager(root)
root.mainloop()