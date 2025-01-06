import subprocess
import sqlite3
import tkinter as tk
from tkinter import ttk,messagebox

def style_widget(widget, **kwargs):
    """Apply styling to a widget."""
    for key, value in kwargs.items():
        widget[key] = value

def show_main_menu():
    for widget in root.winfo_children():
        widget.destroy()

    # Create and style the main menu buttons
    title_label = tk.Label(root, text="DG Music Company", font=("Helvetica", 16, "bold"), fg="blue")
    title_label.pack(pady=20)

    login_button = tk.Button(root, text="Login", command=show_login_screen)
    style_widget(login_button, font=("Helvetica", 12), bg="lightblue", relief="raised", padx=10, pady=5)
    login_button.pack(pady=10)


def show_login_screen():
    for widget in root.winfo_children():
        widget.destroy()

    # Create and style the login screen
    title_label = tk.Label(root, text="Login", font=("Helvetica", 16, "bold"), fg="blue")
    title_label.grid(row=0, column=0, columnspan=2, pady=20)

    username_label = tk.Label(root, text="Username:", font=("Helvetica", 12))
    username_label.grid(row=1, column=0, padx=10, pady=10)
    username_entry = tk.Entry(root, font=("Helvetica", 12))
    username_entry.grid(row=1, column=1, padx=10, pady=10)

    password_label = tk.Label(root, text="Password:", font=("Helvetica", 12))
    password_label.grid(row=2, column=0, padx=10, pady=10)
    password_entry = tk.Entry(root, show="*", font=("Helvetica", 12))
    password_entry.grid(row=2, column=1, padx=10, pady=10)

    def check_credentials():
        username = username_entry.get()
        password = password_entry.get()

        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()
        cursor.execute("SELECT UserID,bool_admin FROM User WHERE Username = ? AND Password = ?", (username, password))
        result = cursor.fetchone()
        conn.close()

        if result:
            user_id,is_admin = result
            if is_admin:
                root.destroy()  # Close the current window
                subprocess.run(["python", "admin.py"])  # Open musicdb6.py
            else:
                root.destroy()  # Close the current window
                subprocess.run(["python", "user.py", str(user_id)])
        else:
            messagebox.showerror("Login", "Invalid username or password")

    # Create and style the login and back buttons
    login_button = tk.Button(root, text="Login", command=check_credentials)
    style_widget(login_button, font=("Helvetica", 12), bg="lightblue", relief="raised", padx=10, pady=5)
    login_button.grid(row=3, column=0, pady=20)

    back_button = tk.Button(root, text="Back", command=show_main_menu)
    style_widget(back_button, font=("Helvetica", 12), bg="lightcoral", relief="raised", padx=10, pady=5)
    back_button.grid(row=3, column=1, pady=20)



if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    root.title("Main Menu")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}")

    # Show the main menu
    show_main_menu()

    # Start the Tkinter event loop
    root.mainloop()
