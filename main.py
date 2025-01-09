import subprocess
import sqlite3
import customtkinter as ctk
from tkinter import messagebox


def style_widget(widget, **kwargs):
    """Apply styling to a widget."""
    for key, value in kwargs.items():
        widget.configure(**kwargs)

def reset_database():
    """Reset the database by executing the SQL commands from database.sql."""
    try:
        # Open and read the SQL file
        with open("database.sql", "r") as file:
            sql_script = file.read()

        # Connect to the SQLite database
        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()

        # Execute the SQL script
        cursor.executescript(sql_script)
        conn.commit()
        messagebox.showinfo("Reset Database", "Database reset successfully.")
    except FileNotFoundError:
        messagebox.showerror("Error", "The database.sql file was not found.")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Database error: {e}")
    finally:
        conn.close()




def show_main_menu():
    for widget in root.winfo_children():
        widget.destroy()

    # Title Label
    title_label = ctk.CTkLabel(root, text="DG Music Company", font=ctk.CTkFont(size=20, weight="bold"))
    title_label.pack(pady=20)

    # Login Button
    login_button = ctk.CTkButton(root, text="Login",fg_color="#5CB85C", command=show_login_screen, font=ctk.CTkFont(size=14))
    login_button.pack(pady=10)

    reset_db_button = ctk.CTkButton(
        root, text="Reset Database", fg_color="#FF6F61", command=reset_database, font=ctk.CTkFont(size=14)
    )
    reset_db_button.pack(pady=10)


def show_login_screen():
    for widget in root.winfo_children():
        widget.destroy()

    # Title Label
    title_label = ctk.CTkLabel(root, text="Login", font=ctk.CTkFont(size=20, weight="bold"))
    title_label.grid(row=0, column=0, columnspan=2, pady=20)

    # Username Label and Entry
    username_label = ctk.CTkLabel(root, text="Username:", font=ctk.CTkFont(size=14))
    username_label.grid(row=1, column=0, padx=10, pady=10)
    username_entry = ctk.CTkEntry(root, font=ctk.CTkFont(size=14))
    username_entry.grid(row=1, column=1, padx=10, pady=10)

    # Password Label and Entry
    password_label = ctk.CTkLabel(root, text="Password:", font=ctk.CTkFont(size=14))
    password_label.grid(row=2, column=0, padx=10, pady=10)
    password_entry = ctk.CTkEntry(root, show="*", font=ctk.CTkFont(size=14))
    password_entry.grid(row=2, column=1, padx=10, pady=10)

    def check_credentials():
        username = username_entry.get()
        password = password_entry.get()

        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()
        cursor.execute("SELECT UserID, bool_admin FROM User WHERE Username = ? AND Password = ?", (username, password))
        result = cursor.fetchone()
        conn.close()

        if result:
            user_id, is_admin = result
            if is_admin:
                root.destroy()  # Close the current window
                subprocess.run(["python", "admin.py"])  # Open admin.py
            else:
                root.destroy()  # Close the current window
                subprocess.run(["python", "user.py", str(user_id)])
        else:
            messagebox.showerror("Login", "Invalid username or password")

    # Login Button
    login_button = ctk.CTkButton(root, text="Login",fg_color="#5CB85C", command=check_credentials, font=ctk.CTkFont(size=14))
    login_button.grid(row=3, column=0, pady=20)

    # Back Button
    back_button = ctk.CTkButton(root, text="Back", command=show_main_menu, fg_color="#FF6F61", font=ctk.CTkFont(size=14))
    back_button.grid(row=3, column=1, pady=20)


if __name__ == "__main__":
    # Create the main window
    ctk.set_appearance_mode("System")  # Options: "System", "Light", "Dark"
    ctk.set_default_color_theme("blue")  # Options: "blue", "dark-blue", "green"

    root = ctk.CTk()
    root.configure(fg_color="#E3F2FD")
    root.title("Main Menu")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}")

    # Show the main menu
    show_main_menu()

    # Start the Tkinter event loop
    root.mainloop()