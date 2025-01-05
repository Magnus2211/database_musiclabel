import tkinter as tk
import subprocess
import admin_functions


def exit_to_main():
        root.destroy()
        subprocess.run(["python", "main.py"])

def create_admin_window():
    global root
    root = tk.Tk()
    root.title("Admin Panel")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}")


    # Main menu widgets
    title_label = tk.Label(root, text="Admin Panel", font=("Helvetica", 16, "bold"), fg="blue")
    title_label.pack(pady=20)

    view_button = tk.Button(root, text="View", font=("Helvetica", 12), bg="lightblue", relief="raised", command=lambda: admin_functions.show_view_screen(root, create_admin_window))
    view_button.pack(pady=10)

    best_selling_button = tk.Button(root, text="Best-Selling Format", font=("Helvetica", 12), bg="lightgreen", relief="raised", command=admin_functions.show_best_selling_format)
    best_selling_button.pack(pady=10)

    top_active_artists_button = tk.Button(root, text="Top 5 Active Artists", font=("Helvetica", 12), bg="lightyellow", relief="raised", command=admin_functions.show_top_active_artists)
    top_active_artists_button.pack(pady=10)

    profit_button = tk.Button(root, text="Profit", font=("Helvetica", 12), bg="lightyellow", relief="raised", command=lambda:admin_functions.show_profit_screen(root,create_admin_window))
    profit_button.pack(pady=10)

    insert_button = tk.Button(root, text="Insert", font=("Helvetica", 12), bg="lightblue", relief="raised", command=lambda: admin_functions.show_insert_screen(root, create_admin_window))
    insert_button.pack(pady=10)

    associate_button = tk.Button(root, text="Associate", font=("Helvetica", 12), bg="lightpink", relief="raised", command=lambda: admin_functions.show_associate_screen(root, create_admin_window))
    associate_button.pack(pady=10)

    better_view_button = tk.Button(root, text="Better View", font=("Helvetica", 12), bg="lightgreen", relief="raised", command=lambda: admin_functions.show_better_view(root, create_admin_window))
    better_view_button.pack(pady=10)

    delete_button = tk.Button(root, text="Delete", font=("Helvetica", 12), bg="red", relief="raised", command=lambda: admin_functions.show_delete_screen(root, create_admin_window))
    delete_button.pack(pady=10)


    exit_button = tk.Button(root, text="Exit to Main Menu", font=("Helvetica", 12), bg="orange", relief="raised", command=exit_to_main)
    exit_button.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    create_admin_window()
