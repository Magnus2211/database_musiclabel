import customtkinter as ctk
import subprocess
import admin_functions


def exit_to_main(root):
    root.destroy()
    subprocess.run(["python", "main.py"])


def create_admin_window():
    global root
    root = ctk.CTk()
    root.configure(fg_color="#E3F2FD")
    root.title("Admin Panel")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}")
    create_admin_main_menu(root) 
    root.mainloop()


def create_admin_main_menu(root):
    # Clear any existing widgets in the root
    for widget in root.winfo_children():
        widget.destroy()

    # Main menu buttons
    title_label = ctk.CTkLabel(root, text="Admin Panel", font=ctk.CTkFont(size=20, weight="bold"), text_color="#3A86FF")
    title_label.pack(pady=20)

    view_button = ctk.CTkButton(root, text="View",fg_color="#42A5F5", command=lambda: admin_functions.show_view_screen(root, create_admin_main_menu))
    view_button.pack(pady=10)

    best_selling_button = ctk.CTkButton(root, text="Best-Selling Format",fg_color="#26C6DA", command=admin_functions.show_best_selling_format)
    best_selling_button.pack(pady=10)

    top_active_artists_button = ctk.CTkButton(root, text="Top 5 Active Artists",fg_color="#AB47BC", command=admin_functions.show_top_active_artists)
    top_active_artists_button.pack(pady=10)

    profit_button = ctk.CTkButton(root, text="Profit",fg_color="#66BB6A", command=lambda: admin_functions.show_profit_screen(root, create_admin_main_menu))
    profit_button.pack(pady=10)

    insert_button = ctk.CTkButton(root, text="Insert",fg_color="#4CAF50", command=lambda: admin_functions.show_insert_screen(root, create_admin_main_menu))
    insert_button.pack(pady=10)

    associate_button = ctk.CTkButton(root, text="Associate",fg_color="#FF9800", command=lambda: admin_functions.show_associate_screen(root, create_admin_main_menu))
    associate_button.pack(pady=10)

    better_view_button = ctk.CTkButton(root, text="Better View",fg_color="#29B6F6", command=lambda: admin_functions.show_better_view(root, create_admin_main_menu))
    better_view_button.pack(pady=10)

    delete_button = ctk.CTkButton(root, text="Delete", fg_color="#E53935", command=lambda: admin_functions.show_delete_screen(root, create_admin_main_menu))
    delete_button.pack(pady=10)

    exit_button = ctk.CTkButton(root, text="Exit to Main Menu", fg_color="#FFB300", command=lambda: exit_to_main(root))
    exit_button.pack(pady=10)


if __name__ == "__main__":
    create_admin_window()