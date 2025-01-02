import subprocess
import sqlite3
import tkinter as tk
from tkinter import messagebox

def style_widget(widget, **kwargs):
    """Apply styling to a widget."""
    for key, value in kwargs.items():
        widget[key] = value

def show_main_menu():
    for widget in root.winfo_children():
        widget.destroy()

    # Create and style the main menu buttons
    title_label = tk.Label(root, text="Welcome to the Application", font=("Helvetica", 16, "bold"), fg="blue")
    title_label.pack(pady=20)

    login_button = tk.Button(root, text="Login", command=show_login_screen)
    style_widget(login_button, font=("Helvetica", 12), bg="lightblue", relief="raised", padx=10, pady=5)
    login_button.pack(pady=10)

    register_button = tk.Button(root, text="Register", command=show_register_screen)
    style_widget(register_button, font=("Helvetica", 12), bg="lightgreen", relief="raised", padx=10, pady=5)
    register_button.pack(pady=10)

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
        cursor.execute("SELECT bool_admin FROM User WHERE Username = ? AND Password = ?", (username, password))
        result = cursor.fetchone()
        conn.close()

        if result:
            is_admin = result[0]
            if is_admin:
                root.destroy()  # Close the current window
                subprocess.run(["python", "admin.py"])  # Open musicdb6.py
            else:
                messagebox.showinfo("Login", "User logged in, but not an admin.") #ALLAKSE TO SE root.destroy()  # Close the current window
                                                                                #subprocess.run(["python", "admin.py"])
        else:
            messagebox.showerror("Login", "Invalid username or password")

    # Create and style the login and back buttons
    login_button = tk.Button(root, text="Login", command=check_credentials)
    style_widget(login_button, font=("Helvetica", 12), bg="lightblue", relief="raised", padx=10, pady=5)
    login_button.grid(row=3, column=0, pady=20)

    back_button = tk.Button(root, text="Back", command=show_main_menu)
    style_widget(back_button, font=("Helvetica", 12), bg="lightcoral", relief="raised", padx=10, pady=5)
    back_button.grid(row=3, column=1, pady=20)

def show_register_screen():
    global first_name_entry, last_name_entry, country_born_entry, age_entry, phone_entry, email_entry
    global nickname_entry, country_base_entry, associated_artist_var  # Declare these as global

    for widget in root.winfo_children():
        widget.destroy()

    # Create and style the register screen
    title_label = tk.Label(root, text="Register", font=("Helvetica", 16, "bold"), fg="blue")
    title_label.grid(row=0, column=0, columnspan=2, pady=20)

    username_label = tk.Label(root, text="Username:", font=("Helvetica", 12))
    username_label.grid(row=1, column=0, padx=10, pady=10)
    username_entry = tk.Entry(root, font=("Helvetica", 12))
    username_entry.grid(row=1, column=1, padx=10, pady=10)

    password_label = tk.Label(root, text="Password:", font=("Helvetica", 12))
    password_label.grid(row=2, column=0, padx=10, pady=10)
    password_entry = tk.Entry(root, show="*", font=("Helvetica", 12))
    password_entry.grid(row=2, column=1, padx=10, pady=10)

    admin_var = tk.StringVar(value="Yes")

    admin_label = tk.Label(root, text="Is the user an admin?", font=("Helvetica", 12))
    admin_label.grid(row=3, column=0, columnspan=2, pady=10)

    admin_yes = tk.Radiobutton(root, text="Yes", variable=admin_var, value="Yes", font=("Helvetica", 12))
    admin_yes.grid(row=4, column=0, padx=10, pady=5)

    admin_no = tk.Radiobutton(root, text="No", variable=admin_var, value="No", font=("Helvetica", 12))
    admin_no.grid(row=4, column=1, padx=10, pady=5)

    additional_fields_frame = tk.Frame(root)

    def show_individual_fields():
        global first_name_entry, last_name_entry, country_born_entry, age_entry, phone_entry, email_entry
        global nickname_entry, country_base_entry, associated_artist_var  # Declare as global

        for widget in additional_fields_frame.winfo_children():
            widget.destroy()

        first_name_label = tk.Label(additional_fields_frame, text="First Name:", font=("Helvetica", 12))
        first_name_label.grid(row=0, column=0, padx=10, pady=5)
        first_name_entry = tk.Entry(additional_fields_frame, font=("Helvetica", 12))
        first_name_entry.grid(row=0, column=1, padx=10, pady=5)

        last_name_label = tk.Label(additional_fields_frame, text="Last Name:", font=("Helvetica", 12))
        last_name_label.grid(row=1, column=0, padx=10, pady=5)
        last_name_entry = tk.Entry(additional_fields_frame, font=("Helvetica", 12))
        last_name_entry.grid(row=1, column=1, padx=10, pady=5)

        country_born_label = tk.Label(additional_fields_frame, text="Country Born:", font=("Helvetica", 12))
        country_born_label.grid(row=2, column=0, padx=10, pady=5)
        country_born_entry = tk.Entry(additional_fields_frame, font=("Helvetica", 12))
        country_born_entry.grid(row=2, column=1, padx=10, pady=5)

        age_label = tk.Label(additional_fields_frame, text="Age:", font=("Helvetica", 12))
        age_label.grid(row=3, column=0, padx=10, pady=5)
        age_entry = tk.Entry(additional_fields_frame, font=("Helvetica", 12))
        age_entry.grid(row=3, column=1, padx=10, pady=5)

        phone_label = tk.Label(additional_fields_frame, text="Phone:", font=("Helvetica", 12))
        phone_label.grid(row=4, column=0, padx=10, pady=5)
        phone_entry = tk.Entry(additional_fields_frame, font=("Helvetica", 12))
        phone_entry.grid(row=4, column=1, padx=10, pady=5)

        email_label = tk.Label(additional_fields_frame, text="Email:", font=("Helvetica", 12))
        email_label.grid(row=5, column=0, padx=10, pady=5)
        email_entry = tk.Entry(additional_fields_frame, font=("Helvetica", 12))
        email_entry.grid(row=5, column=1, padx=10, pady=5)

        associated_artist_var = tk.StringVar(value="No")  # Define associated_artist_var
        associated_artist_label = tk.Label(additional_fields_frame, text="Associated with another artist?", font=("Helvetica", 12))
        associated_artist_label.grid(row=6, column=0, columnspan=2, pady=10)

        associated_artist_yes = tk.Radiobutton(additional_fields_frame, text="Yes", variable=associated_artist_var, value="Yes", font=("Helvetica", 12))
        associated_artist_yes.grid(row=7, column=0, padx=10, pady=5)

        associated_artist_no = tk.Radiobutton(additional_fields_frame, text="No", variable=associated_artist_var, value="No", font=("Helvetica", 12))
        associated_artist_no.grid(row=7, column=1, padx=10, pady=5)

        def handle_association():
            global nickname_entry, country_base_entry  # Declare as global
            for widget in additional_fields_frame.winfo_children():
                if widget.grid_info().get('row') >= 8:
                    widget.destroy()

            if associated_artist_var.get() == "Yes":
                nickname_label = tk.Label(additional_fields_frame, text="Nickname:", font=("Helvetica", 12))
                nickname_label.grid(row=8, column=0, padx=10, pady=5)
                nickname_entry = tk.Entry(additional_fields_frame, font=("Helvetica", 12))
                nickname_entry.grid(row=8, column=1, padx=10, pady=5)
            else:
                nickname_label = tk.Label(additional_fields_frame, text="Nickname:", font=("Helvetica", 12))
                nickname_label.grid(row=8, column=0, padx=10, pady=5)
                nickname_entry = tk.Entry(additional_fields_frame, font=("Helvetica", 12))
                nickname_entry.grid(row=8, column=1, padx=10, pady=5)

                country_base_label = tk.Label(additional_fields_frame, text="Country Base:", font=("Helvetica", 12))
                country_base_label.grid(row=9, column=0, padx=10, pady=5)
                country_base_entry = tk.Entry(additional_fields_frame, font=("Helvetica", 12))
                country_base_entry.grid(row=9, column=1, padx=10, pady=5)

        associated_artist_var.trace_add("write", lambda *args: handle_association())
        handle_association()

    def handle_admin_change(*args):
        if admin_var.get() == "No":
            additional_fields_frame.grid(row=5, column=0, columnspan=2, pady=10)
            show_individual_fields()
        else:
            for widget in additional_fields_frame.winfo_children():
                widget.destroy()
            additional_fields_frame.grid_forget()

    admin_var.trace_add("write", handle_admin_change)
    additional_fields_frame.grid(row=5, column=0, columnspan=2, pady=10)

    def register_user():
        username = username_entry.get()
        password = password_entry.get()
        is_admin = admin_var.get() == "Yes"

        if not username or not password:
            messagebox.showerror("Register", "Please fill out all required fields.")
            return

        try:
            conn = sqlite3.connect("db.db", timeout=5)
            cursor = conn.cursor()

            # Check if username already exists
            cursor.execute("SELECT * FROM User WHERE Username = ?", (username,))
            if cursor.fetchone():
                messagebox.showerror("Register", "Username already exists.")
                return

            # Insert into User table
            cursor.execute("INSERT INTO User (Username, Password, bool_admin) VALUES (?, ?, ?)", (username, password, is_admin))
            user_id = cursor.lastrowid

            if is_admin:
                # Insert into Admin table
                cursor.execute("INSERT INTO Admin (UserID) VALUES (?)", (user_id,))
            else:
                # Individual details
                first_name = first_name_entry.get()
                last_name = last_name_entry.get()
                country_born = country_born_entry.get()
                age = age_entry.get()
                phone = phone_entry.get()
                email = email_entry.get()

                if not all([first_name, last_name, country_born, age, phone, email]):
                    messagebox.showerror("Register", "Please fill out all individual details.")
                    return

                associated_artist = associated_artist_var.get()
                art_id = None

                if associated_artist == "Yes":
                    # Associate with an existing artist
                    nickname = nickname_entry.get()
                    cursor.execute("SELECT ArtID FROM Artist WHERE Nickname = ?", (nickname,))
                    artist = cursor.fetchone()
                    if artist:
                        art_id = artist[0]
                    else:
                        messagebox.showerror("Register", "Artist with this nickname not found.")
                        conn.rollback()
                        return
                else:
                    # Create a new artist and associate
                    nickname = nickname_entry.get()
                    country_base = country_base_entry.get()
                    if not nickname or not country_base:
                        messagebox.showerror("Register", "Please fill out all artist details.")
                        return

                    # Insert into Artist table
                    cursor.execute("INSERT INTO Artist (Nickname, [Country they operate]) VALUES (?, ?)", (nickname, country_base))
                    art_id = cursor.lastrowid

                # Insert into Individual table with the determined ArtID
                cursor.execute(
                    """INSERT INTO Individual (UserID, First_name, Last_name, [Country born], Age, Phone, Email, ArtID)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (user_id, first_name, last_name, country_born, age, phone, email, art_id),
                )

            conn.commit()
            messagebox.showinfo("Register", "Registration successful!")
        except sqlite3.Error as e:
            messagebox.showerror("Register", f"Database error: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # Create and style the register and back buttons
    register_button = tk.Button(root, text="Register", command=register_user)
    style_widget(register_button, font=("Helvetica", 12), bg="lightgreen", relief="raised", padx=10, pady=5)
    register_button.grid(row=6, column=0, pady=20)

    back_button = tk.Button(root, text="Back", command=show_main_menu)
    style_widget(back_button, font=("Helvetica", 12), bg="lightcoral", relief="raised", padx=10, pady=5)
    back_button.grid(row=6, column=1, pady=20)

# Create the main window
root = tk.Tk()
root.title("Main Menu")
root.geometry("800x800")  # Adjusted window size

# Show the main menu
show_main_menu()

# Start the Tkinter event loop
root.mainloop()

