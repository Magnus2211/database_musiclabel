import sqlite3
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk,messagebox
from admin import create_admin_main_menu

def clear(root):
    """Used to clear any widgets from the root,when transitioning from one scene to another"""
    for widget in root.winfo_children():
        widget.destroy()

def connect_db():
    """Establish and return a connection to the database."""
    conn = sqlite3.connect("db.db")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

# Back button
def go_back(root, create_admin_main_menu):
    """Return to the main admin window."""
    clear(root)  #Clear all widgets from the current window
    create_admin_main_menu(root)  #Reload the admin main menu


def fetch_top_active_artists():
    """Shows the top 5 artists with the most releases(It counts every release,with no datetime filtering)/In a different version,would like to have added datetime search query"""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = """
        SELECT 
            Artist.Nickname AS artist_name,
            COUNT(Release.ProjectID) AS total_releases
        FROM 
            Artist
        JOIN 
            Release ON Artist.ArtID = Release.ArtID
        GROUP BY 
            Artist.Nickname
        ORDER BY 
            total_releases DESC
        LIMIT 5;
        """
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    #Error handling
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Failed to retrieve data: {e}")
        return []
    finally:
        conn.close()

def fetch_top_profitable_artists():
    """Retrieve the top 5 profitable artists from sales of album(It counts every album,with no datetime filtering)
        /In a different version,would like to have added datetime search query"""
    try:
        conn = connect_db()
        cursor = conn.cursor()

        """COALESCE used to turn NULL values to 0 so sum can be done (arithmetic values cant be added with NULL)
        Could have also done differently with 2 different queries
        1 that inner joins CD
        1 that inner joins Vinyl
        then add their respective results
        Instead of COALSCSE we could have used IFNULL (shown afterwards in different fetch query)""" 


        query = """
        SELECT 
            Artist.Nickname AS artist_name,
            SUM(COALESCE(Vinyl.Cost * Vinyl.Sales, 0) + COALESCE(CD.Cost * CD.Sales, 0)) AS total_profits
        FROM 
            Artist
        JOIN 
            Release ON Artist.ArtID = Release.ArtID
        JOIN 
            Project ON Release.ProjectID = Project.ProjectID
        JOIN 
            Album ON Project.ProjectID = Album.ProjectID
        LEFT JOIN 
            Vinyl ON Album.AlbID = Vinyl.AlbID
        LEFT JOIN 
            CD ON Album.AlbID = CD.AlbID
        GROUP BY 
            Artist.Nickname
        ORDER BY 
            total_profits DESC
        LIMIT 5;
        """
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    #Error handler
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Failed to retrieve data: {e}")
        return []
    finally:
        conn.close()

def fetch_artist_profit(artist_name):
    """Retrieve the total profit for a specific artist.Same logic as above fetch"""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = """
        SELECT 
            Artist.Nickname AS artist_name,
            SUM(COALESCE(Vinyl.Cost * Vinyl.Sales, 0) + COALESCE(CD.Cost * CD.Sales, 0)) AS total_profits
        FROM 
            Artist
        JOIN 
            Release ON Artist.ArtID = Release.ArtID
        JOIN 
            Project ON Release.ProjectID = Project.ProjectID
        JOIN 
            Album ON Project.ProjectID = Album.ProjectID
        LEFT JOIN 
            Vinyl ON Album.AlbID = Vinyl.AlbID
        LEFT JOIN 
            CD ON Album.AlbID = CD.AlbID
        WHERE 
            Artist.Nickname = ?
        GROUP BY 
            Artist.Nickname;
        """
        cursor.execute(query, (artist_name,))
        result = cursor.fetchone()
        return result
    #Error handler
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Failed to retrieve data: {e}")
        return None
    finally:
        conn.close()

def fetch_best_selling_format():
    try:
        conn = connect_db()
        cursor = conn.cursor()

        """Checks which format (CD or Vinyl) is most profitable in general from all albums of all artists.(No datetime filtering unfortunately)"""
        query = """
        SELECT 
            Format.Description AS format_type,
            IFNULL(SUM(CD.Sales), 0) + IFNULL(SUM(Vinyl.Sales), 0) AS total_sales
        FROM 
            Format
        LEFT JOIN 
            CD ON Format.FormID = CD.FormID
        LEFT JOIN 
            Vinyl ON Format.FormID = Vinyl.FormID
        GROUP BY 
            Format.Description
        ORDER BY 
            total_sales DESC
        LIMIT 1;
        """
        cursor.execute(query)
        result = cursor.fetchone()
        return result 
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Failed to retrieve data: {e}")
        return None
    finally:
        conn.close()


def fetch_table_names():
    """Retrieve the names of all tables in the database.Used for View function"""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = [row[0] for row in cursor.fetchall()]
        return tables
    #Error handler
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Failed to load table names: {e}")
        return []
    finally:
        conn.close()

def fetch_instruments():
    """Retrieve a list of available instruments from Instrument table.Used when inserting an Individual."""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT InstID, Name FROM Instrument")
        results = cursor.fetchall()
        # Ensure instruments are formatted as "InstID: Name dictionary"
        return [f"{inst_id}: {name}" for inst_id, name in results]
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Failed to fetch instruments: {e}")
        return []
    finally:
        conn.close()

def fetch_genres():
    """
    Retrieve all genres from the Genre table in a list.
    """
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT Name FROM Genre")
        genres = [row[0] for row in cursor.fetchall()]
        return genres
    except sqlite3.Error as e:
        raise Exception(f"Failed to fetch genres: {e}")
    finally:
        conn.close()

#--------PROFIT
def show_profit_screen(root, create_admin_main_menu):
    """Display the profit analysis screen."""

    #Clearing previous widgets
    clear(root)

    # Title label
    profit_label = ctk.CTkLabel(root, text="Profit Analysis", font=ctk.CTkFont(size=20, weight="bold"))
    profit_label.pack(pady=20)

    # Search bar
    search_label = ctk.CTkLabel(root, text="Search for Artist's Total Profit", font=ctk.CTkFont(size=14))
    search_label.pack(pady=10)
    search_entry = ctk.CTkEntry(root, font=ctk.CTkFont(size=14))
    search_entry.pack(pady=10)

    def search_artist_profit():
        """Find and display the total profit for the entered artist name."""
        artist_name = search_entry.get().strip()
        if not artist_name:
            messagebox.showerror("Error", "Please enter an artist's name.")
            return

        # Using the above fetch_profit function
        result = fetch_artist_profit(artist_name)

        if result:
            total_profit = result[1]
            messagebox.showinfo(
                "Artist's Total Profit",
                f"Total profit for {artist_name} is ${total_profit:.2f}."
            )
        else:
            messagebox.showerror("Artist's Total Profit", f"No profit data found for {artist_name}.Artist doesn't exist in the database.")

    search_button = ctk.CTkButton(root, text="Search", fg_color="#1E90FF", text_color="black", command=search_artist_profit)
    search_button.pack(pady=10)

    # Display Top 5 Profitable Artists
    def show_top_profitable_artists():
        """Display the top 5 profitable artists based on total profits."""
        results = fetch_top_profitable_artists()
        if results:
            #Creates a list of formatted strings that contains the Artist Nickname and the profilts from his Albums
            artist_list = "\n".join([f"{i+1}. {artist} - {profits:.2f} $" for i, (artist, profits) in enumerate(results)])
            messagebox.showinfo(
                "Top 5 Profitable Artists",
                f"The top 5 profitable artists are:\n\n{artist_list}"
            )
        else:
            messagebox.showinfo("Top 5 Profitable Artists", "No profit data available.")

    top_profitable_button = ctk.CTkButton(root, text="Top 5 Profitable Artists", fg_color="lightgreen", text_color="black", command=show_top_profitable_artists)
    top_profitable_button.pack(pady=20)

    # Back button
    back_button = ctk.CTkButton(root, text="Back", fg_color="#FF6F61", text_color="black", command=lambda: go_back(root, create_admin_main_menu))
    back_button.pack(pady=10)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#BEST SELLING FORMAT
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def show_best_selling_format():
    """Display the best-selling format based on total sales from all Albums from all Artists."""
    result=fetch_best_selling_format()
    if result:
        format_type, total_sales = result
        messagebox.showinfo(
            "Best-Selling Format",
            f"The best-selling format is '{format_type}' with total sales of {total_sales}."
        )
    else:
        messagebox.showinfo("Best-Selling Format", "No sales data available.")


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#TOP 5 ACTIVE ARTISTS
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def show_top_active_artists():
    """Display the top 5 active artists based on the number of releases."""
    results = fetch_top_active_artists()
    if results:
        artist_list = "\n".join([f"{i+1}. {artist} - {releases} releases" for i, (artist, releases) in enumerate(results)])
        messagebox.showinfo(
            "Top 5 Active Artists",
            f"The top 5 active artists are:\n\n{artist_list}"
        )
    else:
        messagebox.showinfo("Top 5 Active Artists", "No artist release data available.")


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#VIEW FUNCTION
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def show_view_screen(root, create_admin_main_menu):
    """Display the screen to view table contents."""
    clear(root)

    # Title label
    view_label = ctk.CTkLabel(root, text="View Table Contents", font=ctk.CTkFont(size=20, weight="bold"))
    view_label.pack(pady=20)

    # Dropdown to select the table
    table_var = tk.StringVar()
    table_dropdown = ttk.Combobox(root, textvariable=table_var, state="readonly", font=("Helvetica", 12))
    table_dropdown.pack(pady=10)

    # Frame for Treeview (data display)
    tree_frame = ctk.CTkFrame(root)
    tree_frame.pack(fill="both", expand=True, pady=10)

    # Treeview widget for data
    data_tree = ttk.Treeview(tree_frame, show="headings")
    data_tree.pack(fill="both", expand=True)

    # Scrollbar for Treeview
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=data_tree.yview)
    scrollbar.pack(side="right", fill="y")
    data_tree.configure(yscroll=scrollbar.set)

    # Frame for Back button
    button_frame = ctk.CTkFrame(root)
    button_frame.pack(fill="x", pady=10)

    back_button = ctk.CTkButton(button_frame, text="Back", fg_color="#FF6F61", command=lambda: go_back(root, create_admin_main_menu))
    back_button.pack(pady=10)

    def load_table_names():
        """Load all table names of the music label database into the dropdown."""
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
            tables = [row[0] for row in cursor.fetchall()]
            table_dropdown['values'] = tables
            if tables:
                table_var.set(tables[0])  # Setting a default value on the combobox
                load_table_data()  # Automatically load data for the first table
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to load table names: {e}")
        finally:
            conn.close()

    def load_table_data(event=None):
        """Load data from the selected table of the combobox into the Treeview Frame."""
        table_name = table_var.get()
        if not table_name:
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()

            # Fetch column names and data from selected table,extracting them into a list
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [col[1] for col in cursor.fetchall()]
            if not columns:
                messagebox.showerror("Error", f"No columns found in the table '{table_name}'.")
                return

            # Configure Treeview columns
            data_tree["columns"] = columns
            data_tree.delete(*data_tree.get_children())  # Clear existing rows in the Treeview

            #Centering each column
            for col in columns:
                data_tree.heading(col, text=col)
                data_tree.column(col, anchor="center", width=150)

            # Fetch table data
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            if not rows:
                messagebox.showinfo("Info", f"No data found in the table '{table_name}'.")
                return

            for row in rows:
                data_tree.insert("", "end", values=row)

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")
        finally:
            conn.close()

    #Bind the table dropdown selection event
    table_dropdown.bind("<<ComboboxSelected>>", load_table_data)

    #Load table names initially
    load_table_names()




#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#INSERT SCREEN WITH COMBOBOX
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def show_insert_screen(root, create_admin_main_menu):
    """Display the insert screen main window with combobox values Individual,Project and Partner."""
    clear(root)

    # Title label
    insert_label = ctk.CTkLabel(root, text="Insert Data", font=ctk.CTkFont(size=20, weight="bold"))
    insert_label.pack(pady=20)

    # Combobox for selecting the table
    table_label = ctk.CTkLabel(root, text="Select Table:", font=ctk.CTkFont(size=14))
    table_label.pack(pady=10)

    table_var = ctk.StringVar()
    table_combobox = ctk.CTkComboBox(root, variable=table_var, values=["Individual", "Project", "Partner"], font=ctk.CTkFont(size=14))
    table_combobox.pack(pady=10)

    # Function to handle Insert based on selection
    def handle_insert():
        selected_table = table_var.get()
        if not selected_table:
            ctk.CTkMessagebox(title="Error", message="Please select a table to insert data into.", icon="error")
            return

        if selected_table == "Individual":
            show_individual_insert_form(root)
        elif selected_table == "Project":
            show_project_insert_form(root)
        elif selected_table == "Partner":
            show_partner_insert_form(root)
        else:
            ctk.CTkMessagebox(title="Error", message="Invalid selection.", icon="error")

    #Insert button
    insert_button = ctk.CTkButton(root, text="Insert", command=handle_insert, fg_color="green")
    insert_button.pack(pady=20)

    #Back button
    back_button = ctk.CTkButton(root, text="Back", command=lambda: go_back(root, create_admin_main_menu), fg_color="#FF6F61")
    back_button.pack(pady=10)



#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#INSERT INDIVIDUAL
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def show_individual_insert_form(root):
    """Form to insert data into the Individual table."""
    clear(root)

    # Title label
    title_label = ctk.CTkLabel(root, text="Insert New Individual", font=ctk.CTkFont(size=20, weight="bold"))
    title_label.pack(pady=20)

    # Main form frame
    form_frame = ctk.CTkFrame(root)
    form_frame.pack(pady=10)

    # Form fields
    fields = ["Username", "Password", "First Name", "Last Name", "Country Born", "Age", "Phone", "Email"]
    entries = {}

    # Create a grid layout for the fields
    for row, field in enumerate(fields):
        label = ctk.CTkLabel(form_frame, text=f"{field}:", font=ctk.CTkFont(size=14))
        label.grid(row=row, column=0, sticky="w", padx=10, pady=5)
        entry = ctk.CTkEntry(form_frame, font=ctk.CTkFont(size=14))
        if field == "Password":
            entry.configure(show="*")
        entry.grid(row=row, column=1, padx=10, pady=5)
        entries[field] = entry

    # Instrument association
    instrument_label = ctk.CTkLabel(root, text="Associate Instruments (optional):", font=ctk.CTkFont(size=14))
    instrument_label.pack(pady=10)
    instrument_frame = ctk.CTkFrame(root)
    instrument_frame.pack(pady=10)

    instrument_var = ctk.StringVar()
    instrument_combobox = ctk.CTkComboBox(instrument_frame, variable=instrument_var, font=ctk.CTkFont(size=14))
    instrument_combobox.grid(row=0, column=0, padx=5)

    try:
        instruments = fetch_instruments()
        instrument_combobox.configure(values=instruments)
    except Exception as e:
        ctk.CTkMessagebox(title="Error", message=f"Failed to load instruments: {e}")

    selected_instruments = []

    def add_instrument():
        instrument = instrument_var.get()
        if not instrument:
            ctk.CTkMessagebox(title="Error", message="Please select an instrument.")
            return

        if ":" not in instrument:
            ctk.CTkMessagebox(title="Error", message="Invalid instrument format.")
            return

        if instrument not in selected_instruments:
            selected_instruments.append(instrument)
            instrument_listbox.insert("end", instrument)

    add_button = ctk.CTkButton(instrument_frame, text="Add", command=add_instrument, fg_color="green")
    add_button.grid(row=0, column=1, padx=5)

    instrument_listbox = tk.Listbox(root, font=("Helvetica", 12), height=5)
    instrument_listbox.pack(pady=10)

    def remove_instrument():
        selected = instrument_listbox.curselection()
        if selected:
            selected_instruments.remove(instrument_listbox.get(selected[0]))
            instrument_listbox.delete(selected)

    remove_button = ctk.CTkButton(root, text="Remove Selected", command=remove_instrument, fg_color="red")
    remove_button.pack(pady=5)

    # Artist association options
    association_var = ctk.StringVar(value="No")
    association_label = ctk.CTkLabel(root, text="Associated with another artist?", font=ctk.CTkFont(size=14))
    association_label.pack(pady=10)

    association_frame = ctk.CTkFrame(root)
    association_frame.pack(pady=5)

    association_yes = ctk.CTkRadioButton(association_frame, text="Yes", variable=association_var, value="Yes")
    association_yes.grid(row=0, column=0, padx=10)

    association_no = ctk.CTkRadioButton(association_frame, text="No", variable=association_var, value="No")
    association_no.grid(row=0, column=1, padx=10)

    artist_frame = ctk.CTkFrame(root)
    artist_frame.pack(pady=10)

    def update_artist_fields(*args):
        for widget in artist_frame.winfo_children():
            widget.destroy()

        if association_var.get() == "Yes":
            artist_nickname_label = ctk.CTkLabel(artist_frame, text="Artist Nickname:", font=ctk.CTkFont(size=14))
            artist_nickname_label.pack(pady=5)
            artist_nickname_entry = ctk.CTkEntry(artist_frame, font=ctk.CTkFont(size=14))
            artist_nickname_entry.pack(pady=5)
            entries["Artist Nickname"] = artist_nickname_entry
        else:
            nickname_label = ctk.CTkLabel(artist_frame, text="New Artist Nickname:", font=ctk.CTkFont(size=14))
            nickname_label.pack(pady=5)
            nickname_entry = ctk.CTkEntry(artist_frame, font=ctk.CTkFont(size=14))
            nickname_entry.pack(pady=5)
            entries["New Artist Nickname"] = nickname_entry

            country_base_label = ctk.CTkLabel(artist_frame, text="Country Base:", font=ctk.CTkFont(size=14))
            country_base_label.pack(pady=5)
            country_base_entry = ctk.CTkEntry(artist_frame, font=ctk.CTkFont(size=14))
            country_base_entry.pack(pady=5)
            entries["Country Base"] = country_base_entry

    association_var.trace_add("write", update_artist_fields)
    update_artist_fields()

    # Save button
    def save_individual():
        # Dynamically update the entries dictionary based on the current association option
        if association_var.get() == "Yes":
            # Only include fields relevant for association with an existing artist
            required_fields = {
                "Username": entries["Username"],
                "Password": entries["Password"],
                "First Name": entries["First Name"],
                "Last Name": entries["Last Name"],
                "Country Born": entries["Country Born"],
                "Age": entries["Age"],
                "Phone": entries["Phone"],
                "Email": entries["Email"],
                "Artist Nickname": entries["Artist Nickname"]
            }
        else:
            # Include additional fields for creating a new artist
            required_fields = {
                "Username": entries["Username"],
                "Password": entries["Password"],
                "First Name": entries["First Name"],
                "Last Name": entries["Last Name"],
                "Country Born": entries["Country Born"],
                "Age": entries["Age"],
                "Phone": entries["Phone"],
                "Email": entries["Email"],
                "New Artist Nickname": entries["New Artist Nickname"],
                "Country Base": entries["Country Base"]
            }

        try:
            # Collect data from active fields
            data = {field: entry.get().strip() for field, entry in required_fields.items()}

            # Validate required fields
            if any(not value for value in data.values()):
                messagebox.showerror("Error", "All required fields must be filled out.")
                return

            username = data["Username"]
            password = data["Password"]
            associated_artist = association_var.get() == "Yes"

            conn = connect_db()
            cursor = conn.cursor()

            # Check if username already exists
            cursor.execute("SELECT * FROM User WHERE Username = ?", (username,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Username already exists.")
                return

            # Insert into User table
            cursor.execute(
                "INSERT INTO User (Username, Password, bool_admin) VALUES (?, ?, ?)",
                (username, password, False),
            )
            user_id = cursor.lastrowid

            # Handle artist association
            if associated_artist:
                artist_nickname = data["Artist Nickname"]
                cursor.execute("SELECT ArtID FROM Artist WHERE Nickname = ?", (artist_nickname,))
                artist = cursor.fetchone()
                if not artist:
                    messagebox.showerror("Error", "Artist with this nickname does not exist.")
                    return
                art_id = artist[0]
            else:
                new_nickname = data["New Artist Nickname"]
                country_base = data["Country Base"]
                cursor.execute(
                    "INSERT INTO Artist (Nickname, [Country they operate]) VALUES (?, ?)",
                    (new_nickname, country_base),
                )
                art_id = cursor.lastrowid

            # Insert into Individual table
            cursor.execute(
                """
                INSERT INTO Individual (UserID, First_name, Last_name, [Country born], Age, Phone, Email, ArtID)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (user_id, data["First Name"], data["Last Name"], data["Country Born"], data["Age"], data["Phone"], data["Email"], art_id),
            )
            individ_id = cursor.lastrowid

            
            for instrument in selected_instruments:
                try:
                    inst_id = int(instrument.split(":")[0])  # Extract InstID
                    cursor.execute(
                        """
                        INSERT INTO Plays (IndividID, InstID)
                        VALUES (?, ?)
                        """,
                        (individ_id, inst_id),
                    )
                except ValueError:
                    messagebox.showerror("Error", f"Invalid instrument format: {instrument}")
                    return


            conn.commit()
            messagebox.showinfo("Success", "Individual added successfully.")
            show_insert_screen(root,create_admin_main_menu)

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to insert data: {e}")
        finally:
            conn.close()

    save_button = ctk.CTkButton(root, text="Save", command=save_individual, fg_color="#26A69A")
    save_button.pack(pady=20)

    back_button = ctk.CTkButton(root, text="Back", command=lambda: show_insert_screen(root, create_admin_main_menu), fg_color="#FF6F61")
    back_button.pack(pady=10)


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#INSERT PROJECT
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def show_project_insert_form(root):
    """Form to insert data into the Project table."""
    clear(root)

    # Title label
    title_label = ctk.CTkLabel(root, text="Insert New Project", font=ctk.CTkFont(size=20, weight="bold"))
    title_label.pack(pady=20)

    # Form fields
    fields = ["Artist Nickname", "Title"]
    entries = {}

    for field in fields:
        label = ctk.CTkLabel(root, text=f"{field}:", font=ctk.CTkFont(size=14))
        label.pack(pady=5)
        entry = ctk.CTkEntry(root, font=ctk.CTkFont(size=14))
        entry.pack(pady=5)
        entries[field] = entry

    # Combobox for Genre
    genre_label = ctk.CTkLabel(root, text="Genre:", font=ctk.CTkFont(size=14))
    genre_label.pack(pady=5)
    genre_var = ctk.StringVar()
    genre_combobox = ctk.CTkComboBox(root, variable=genre_var, font=ctk.CTkFont(size=14))
    genre_combobox.pack(pady=5)

    # Load genres from database
    try:
        genres = fetch_genres()
        genre_combobox.configure(values=genres)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load genres: {e}")

    # Release Date
    release_date_label = ctk.CTkLabel(root, text="Release Date (YYYY-MM-DD):", font=ctk.CTkFont(size=14))
    release_date_label.pack(pady=5)
    release_date_entry = ctk.CTkEntry(root, font=ctk.CTkFont(size=14))
    release_date_entry.pack(pady=5)

    # Radiobuttons for project type
    project_type_var = ctk.StringVar(value="Song")
    project_type_label = ctk.CTkLabel(root, text="Project Type:", font=ctk.CTkFont(size=14))
    project_type_label.pack(pady=10)

    project_types = ["Album", "Song", "Video"]
    for project_type in project_types:
        rb = ctk.CTkRadioButton(root, text=project_type, variable=project_type_var, value=project_type)
        rb.pack(pady=5)

    # Dynamic frame for additional fields based on project type
    dynamic_frame = ctk.CTkFrame(root)
    dynamic_frame.pack(pady=10)

    formats = {"Vinyl": tk.IntVar(), "CD": tk.IntVar(), "Digital": tk.IntVar()}
    price_entry_vinyl = None
    price_entry_cd = None
    album_assoc_var = tk.StringVar(value="No")  # Added for Song association

    def update_dynamic_fields(*args):
        nonlocal price_entry_vinyl, price_entry_cd

        # Clear existing fields
        for widget in dynamic_frame.winfo_children():
            widget.destroy()

        project_type = project_type_var.get()
        if project_type == "Album":
            # Format checkboxes
            format_label = ctk.CTkLabel(dynamic_frame, text="Available Formats:", font=ctk.CTkFont(size=14))
            format_label.pack(pady=5)

            for fmt in formats:
                cb = ctk.CTkCheckBox(dynamic_frame, text=fmt, variable=formats[fmt])
                cb.pack(pady=5)

            # Price entry for Vinyl and CD
            price_label_vinyl = ctk.CTkLabel(dynamic_frame, text="Vinyl Price:", font=ctk.CTkFont(size=14))
            price_entry_vinyl = ctk.CTkEntry(dynamic_frame, font=ctk.CTkFont(size=14))

            price_label_cd = ctk.CTkLabel(dynamic_frame, text="CD Price:", font=ctk.CTkFont(size=14))
            price_entry_cd = ctk.CTkEntry(dynamic_frame, font=ctk.CTkFont(size=14))

            def toggle_price():
                # Show or hide price fields based on the selected format
                if formats["Vinyl"].get():
                    price_label_vinyl.pack(pady=5)
                    price_entry_vinyl.pack(pady=5)
                else:
                    price_label_vinyl.pack_forget()
                    price_entry_vinyl.pack_forget()

                if formats["CD"].get():
                    price_label_cd.pack(pady=5)
                    price_entry_cd.pack(pady=5)
                else:
                    price_label_cd.pack_forget()
                    price_entry_cd.pack_forget()

            formats["Vinyl"].trace_add("write", lambda *args: toggle_price())
            formats["CD"].trace_add("write", lambda *args: toggle_price())
            toggle_price()

        elif project_type == "Song":
            # Radiobutton for album association
            album_assoc_label = ctk.CTkLabel(dynamic_frame, text="Belongs to an Album?", font=ctk.CTkFont(size=14))
            album_assoc_label.pack(pady=5)
            album_assoc_rb_yes = ctk.CTkRadioButton(dynamic_frame, text="Yes", variable=album_assoc_var, value="Yes")
            album_assoc_rb_yes.pack(pady=5)
            album_assoc_rb_no = ctk.CTkRadioButton(dynamic_frame, text="No", variable=album_assoc_var, value="No")
            album_assoc_rb_no.pack(pady=5)

            # Album name field
            album_name_label = ctk.CTkLabel(dynamic_frame, text="Album Name:", font=ctk.CTkFont(size=14))
            album_name_entry = ctk.CTkEntry(dynamic_frame, font=ctk.CTkFont(size=14))

            def update_album_name(*args):
                if album_assoc_var.get() == "Yes":
                    album_name_label.pack(pady=5)
                    album_name_entry.pack(pady=5)
                else:
                    album_name_label.pack_forget()
                    album_name_entry.pack_forget()

            album_assoc_var.trace_add("write", lambda *args: update_album_name())
            update_album_name()

            # Song duration field
            song_duration_label = ctk.CTkLabel(dynamic_frame, text="Song Duration (seconds):", font=ctk.CTkFont(size=14))
            song_duration_label.pack(pady=5)
            song_duration_entry = ctk.CTkEntry(dynamic_frame, font=ctk.CTkFont(size=14))
            song_duration_entry.pack(pady=5)
            entries["Song Duration"] = song_duration_entry

        elif project_type == "Video":
            # Duration field for Video
            duration_label = ctk.CTkLabel(dynamic_frame, text="Duration (seconds):", font=ctk.CTkFont(size=14))
            duration_label.pack(pady=5)
            duration_entry = ctk.CTkEntry(dynamic_frame, font=ctk.CTkFont(size=14))
            duration_entry.pack(pady=5)
            entries["Duration"] = duration_entry

    project_type_var.trace_add("write", update_dynamic_fields)
    update_dynamic_fields()


    def save_project():
        data = {field: entry.get().strip() for field, entry in entries.items() if entry.winfo_exists()}
        data["Genre"] = genre_var.get()
        data["Release Date"] = release_date_entry.get().strip()

        if any(not value for value in data.values()):
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        project_type = project_type_var.get()
        data["Title"] += f" ({project_type})"  # Append project type to the title

        try:
            conn = connect_db()
            cursor = conn.cursor()

            # Fetch ArtID from Artist table
            cursor.execute("SELECT ArtID FROM Artist WHERE Nickname = ?", (data["Artist Nickname"],))
            artist = cursor.fetchone()
            if not artist:
                messagebox.showerror("Error", "Artist nickname not found. Please ensure the artist exists.")
                return
            art_id = artist[0]

            # Fetch GenreID from Genre table
            cursor.execute("SELECT GenreID FROM Genre WHERE Name = ?", (data["Genre"],))
            genre = cursor.fetchone()
            if not genre:
                messagebox.showerror("Error", "Genre not found. Please ensure the genre exists.")
                return
            genre_id = genre[0]

            # Insert into Project table
            cursor.execute(
                "INSERT INTO Project (ArtID, Title, GenreID, Release_Date) VALUES (?, ?, ?, ?)",
                (art_id, data["Title"], genre_id, data["Release Date"]),
            )
            project_id = cursor.lastrowid

            # Insert into Release table
            cursor.execute(
                "INSERT INTO Release (ArtID, ProjectID) VALUES (?, ?)",
                (art_id, project_id)
            )

            # Handle Song
            if project_type == "Song":
                song_duration = entries["Song Duration"].get().strip()
                if not song_duration.isdigit():
                    messagebox.showerror("Error", "Song duration must be a valid number.")
                    return

                cursor.execute("INSERT INTO Song (ProjectID, Duration) VALUES (?, ?)", (project_id, int(song_duration)))
                song_id = cursor.lastrowid

                # Handle album association
                if "Album Name" in entries and "Album Name" in data:
                    cursor.execute(
                        """
                        SELECT Album.AlbID
                        FROM Album
                        JOIN Project ON Album.ProjectID = Project.ProjectID
                        WHERE Project.ArtID = ? AND Project.Title = ?
                        """,
                        (art_id, data["Album Name"]),
                    )
                    album = cursor.fetchone()
                    if not album:
                        messagebox.showerror("Error", f"Album '{data['Album Name']}' does not belong to the specified artist.")
                        return
                    album_id = album[0]
                    cursor.execute("INSERT INTO Is_part_of (SongID, AlbID) VALUES (?, ?)", (song_id, album_id))

                messagebox.showinfo("Success", "Project and Song added successfully.")

            # Handle Album
            elif project_type == "Album":
                cursor.execute("INSERT INTO Album (ProjectID) VALUES (?)", (project_id,))
                album_id = cursor.lastrowid

                # Insert formats and price
                if formats["Vinyl"].get():
                    vinyl_price = price_entry_vinyl.get().strip()
                    if not vinyl_price.isdigit():
                        messagebox.showerror("Error", "Vinyl price must be a valid number.")
                        return
                    cursor.execute("INSERT INTO Vinyl (AlbID, FormID, Cost) VALUES (?, ?, ?)", (album_id, 1, float(vinyl_price)))

                if formats["CD"].get():
                    cd_price = price_entry_cd.get().strip()
                    if not cd_price.isdigit():
                        messagebox.showerror("Error", "CD price must be a valid number.")
                        return
                    cursor.execute("INSERT INTO CD (AlbID, FormID, Cost) VALUES (?, ?, ?)", (album_id, 2, float(cd_price)))

                if formats["Digital"].get():
                    cursor.execute("INSERT INTO Digital (AlbID, FormID) VALUES (?, ?)", (album_id, 3))

                messagebox.showinfo("Success", "Project and Album added successfully.")

            elif project_type == "Video":
                duration = entries["Duration"].get().strip()
                if not duration.isdigit():
                    messagebox.showerror("Error", "Duration must be a valid number.")
                    return

                cursor.execute("INSERT INTO Video (ProjectID, Duration) VALUES (?, ?)", (project_id, int(duration)))
                messagebox.showinfo("Success", "Project and Video added successfully.")

            conn.commit()
        except sqlite3.Error as e:
            print(f"Database error occurred: {e}")
            messagebox.showerror("Error", f"Failed to insert project: {e}")
        finally:
            conn.close()

    save_button = ctk.CTkButton(root, text="Save", fg_color="#26A69A", command=save_project)
    save_button.pack(pady=20)

    # Back button
    back_button = ctk.CTkButton(root, text="Back", fg_color="#FF6F61", command=lambda: show_insert_screen(root, create_admin_main_menu))
    back_button.pack(pady=10)


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#INSERT PARTNER
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def show_partner_insert_form(root):
    """Form to insert data into the Partner table."""
    clear(root)

    # Title label
    title_label = ctk.CTkLabel(root, text="Insert Into Partner", font=ctk.CTkFont(size=20, weight="bold"), text_color="blue")
    title_label.pack(pady=20)

    # Form fields for Partner
    fields = ["First Name", "Last Name"]
    entries = {}

    for idx, field in enumerate(fields):
        label = ctk.CTkLabel(root, text=f"{field}:", font=ctk.CTkFont(size=14))
        label.pack(pady=5)
        entry = ctk.CTkEntry(root, font=ctk.CTkFont(size=14))
        entry.pack(pady=5)
        entries[field] = entry

    # Combobox for selecting Role
    role_var = ctk.StringVar()
    role_label = ctk.CTkLabel(root, text="Role:", font=ctk.CTkFont(size=14))
    role_label.pack(pady=5)

    role_combobox = ctk.CTkComboBox(root, variable=role_var, font=ctk.CTkFont(size=14), state="readonly")
    role_combobox.pack(pady=5)

    # Load roles into the combobox
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT RoleID, Description FROM Role")  # Adjust table/column names if needed
        roles = cursor.fetchall()
        if roles:
            role_combobox.configure(values=[f"{role[0]}: {role[1]}" for role in roles])  # Format: RoleID: RoleName
        else:
            messagebox.showerror("Error", "No roles found in the database.")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Failed to load roles: {e}")
    finally:
        conn.close()

    # Save button
    def save_partner():
        data = {field: entry.get().strip() for field, entry in entries.items()}
        selected_role = role_var.get()

        if any(not value for value in data.values()) or not selected_role:
            messagebox.showerror("Error", "All fields must be filled out, including Role.")
            return

        try:
            # Extract RoleID from the selected combobox value
            role_id = int(selected_role.split(":")[0])

            conn = connect_db()
            cursor = conn.cursor()
            query = "INSERT INTO Partner (RoleID, First_name, Last_name) VALUES (?, ?, ?)"
            cursor.execute(query, (role_id, data["First Name"], data["Last Name"]))
            conn.commit()
            messagebox.showinfo("Success", "Data inserted successfully.")
            show_insert_screen(root, create_admin_main_menu)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to insert data: {e}")
        except ValueError:
            messagebox.showerror("Error", "Invalid role selection format.")
        finally:
            conn.close()

    save_button = ctk.CTkButton(root, text="Save", font=ctk.CTkFont(size=14), fg_color="#26A69A", command=save_partner)
    save_button.pack(pady=20)

    # Back button
    back_button = ctk.CTkButton(root, text="Back", font=ctk.CTkFont(size=14), fg_color="#FF6F61", command=lambda: show_insert_screen(root, create_admin_main_menu))
    back_button.pack(pady=10)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#ASSOCIATE FUNCTION
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def show_associate_screen(root, create_admin_main_menu):
    """
    Display the associate screen with combobox options to associate a song with an album, 
    a partner with a project, or a video with a song.
    """
    clear(root)

    # Title label
    associate_label = ctk.CTkLabel(root, text="Associate Data", font=ctk.CTkFont(size=20, weight="bold"), text_color="blue")
    associate_label.pack(pady=20)

    # Combobox for selecting association type
    associate_type_label = ctk.CTkLabel(root, text="Select Association Type:", font=ctk.CTkFont(size=14))
    associate_type_label.pack(pady=10)
    associate_var = ctk.StringVar()
    associate_combobox = ctk.CTkComboBox(root, variable=associate_var, state="readonly", font=ctk.CTkFont(size=14))
    associate_combobox.configure(values=["Song to Album", "Partner to Project", "Video to Song"])
    associate_combobox.pack(pady=10)

    # Dynamic frame for input fields
    dynamic_frame = ctk.CTkFrame(root)
    dynamic_frame.pack(pady=20)

    def update_dynamic_fields(*args):
        for widget in dynamic_frame.winfo_children():
            widget.destroy()

        association_type = associate_var.get()

        if association_type == "Song to Album":
            # Song to Album fields
            song_label = ctk.CTkLabel(dynamic_frame, text="Song Title:", font=ctk.CTkFont(size=14))
            song_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
            song_entry = ctk.CTkEntry(dynamic_frame, font=ctk.CTkFont(size=14))
            song_entry.grid(row=0, column=1, padx=10, pady=5)

            album_label = ctk.CTkLabel(dynamic_frame, text="Album Title:", font=ctk.CTkFont(size=14))
            album_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
            album_entry = ctk.CTkEntry(dynamic_frame, font=ctk.CTkFont(size=14))
            album_entry.grid(row=1, column=1, padx=10, pady=5)

            def associate_song_album():
                song_title = song_entry.get().strip()
                album_title = album_entry.get().strip()

                if not song_title or not album_title:
                    messagebox.showerror("Error", "Please fill in both Song Title and Album Title.")
                    return

                try:
                    conn = connect_db()
                    cursor = conn.cursor()

                    # Fetch the album ID based on the album title
                    cursor.execute("""
                        SELECT Album.AlbID, Project.ArtID
                        FROM Album
                        JOIN Project ON Album.ProjectID = Project.ProjectID
                        WHERE Project.Title = ?
                    """, (album_title,))
                    album = cursor.fetchone()

                    if not album:
                        messagebox.showerror("Error", "Album not found.")
                        return

                    album_id, album_art_id = album

                    # Fetch the song ID based on the song title
                    cursor.execute("""
                        SELECT Song.SongID, Project.ArtID
                        FROM Song
                        JOIN Project ON Song.ProjectID = Project.ProjectID
                        WHERE Project.Title = ?
                    """, (song_title,))
                    song = cursor.fetchone()

                    if not song:
                        messagebox.showerror("Error", "Song not found.")
                        return

                    song_id, song_art_id = song

                    # Ensure the song and album belong to the same artist
                    if album_art_id != song_art_id:
                        messagebox.showerror("Error", "Song and Album do not belong to the same artist.")
                        return

                    # Insert association into Is_part_of table
                    cursor.execute("INSERT INTO Is_part_of (SongID, AlbID) VALUES (?, ?)", (song_id, album_id))
                    conn.commit()
                    messagebox.showinfo("Success", "Song associated with Album successfully.")
                except sqlite3.Error as e:
                    messagebox.showerror("Database Error", f"Error: {e}")
                finally:
                    conn.close()

            associate_button = ctk.CTkButton(dynamic_frame, text="Associate", font=ctk.CTkFont(size=14), fg_color="#5CB85C", command=associate_song_album)
            associate_button.grid(row=2, column=0, columnspan=2, pady=10)

        elif association_type == "Partner to Project":
            # Partner to Project fields
            partner_label = ctk.CTkLabel(dynamic_frame, text="Partner ID:", font=ctk.CTkFont(size=14))
            partner_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
            partner_entry = ctk.CTkEntry(dynamic_frame, font=ctk.CTkFont(size=14))
            partner_entry.grid(row=0, column=1, padx=10, pady=5)

            project_label = ctk.CTkLabel(dynamic_frame, text="Project Title:", font=ctk.CTkFont(size=14))
            project_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
            project_entry = ctk.CTkEntry(dynamic_frame, font=ctk.CTkFont(size=14))
            project_entry.grid(row=1, column=1, padx=10, pady=5)

            def associate_partner_project():
                partner_id = partner_entry.get().strip()
                project_title = project_entry.get().strip()

                if not partner_id or not project_title:
                    messagebox.showerror("Error", "Please fill in both Partner ID and Project Title.")
                    return

                try:
                    partner_id = int(partner_id)
                except ValueError:
                    messagebox.showerror("Error", "Partner ID must be a valid integer.")
                    return

                try:
                    conn = connect_db()
                    cursor = conn.cursor()

                    # Fetch the project ID based on the project title
                    cursor.execute("SELECT ProjectID FROM Project WHERE Title = ?", (project_title,))
                    project = cursor.fetchone()

                    if not project:
                        messagebox.showerror("Error", "Project not found.")
                        return

                    project_id = project[0]

                    # Insert association into Works_on table
                    cursor.execute("INSERT INTO Works_on (ProjectID, PartID) VALUES (?, ?)", (project_id, partner_id))
                    conn.commit()
                    messagebox.showinfo("Success", "Partner associated with Project successfully.")
                except sqlite3.Error as e:
                    messagebox.showerror("Database Error", f"Error: {e}")
                finally:
                    conn.close()

            associate_button = ctk.CTkButton(dynamic_frame, text="Associate", font=ctk.CTkFont(size=14), fg_color="#5CB85C", command=associate_partner_project)
            associate_button.grid(row=2, column=0, columnspan=2, pady=10)

        elif association_type == "Video to Song":
            # Video to Song fields
            video_label = ctk.CTkLabel(dynamic_frame, text="Video Title:", font=ctk.CTkFont(size=14))
            video_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
            video_entry = ctk.CTkEntry(dynamic_frame, font=ctk.CTkFont(size=14))
            video_entry.grid(row=0, column=1, padx=10, pady=5)

            song_label = ctk.CTkLabel(dynamic_frame, text="Song Title:", font=ctk.CTkFont(size=14))
            song_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
            song_entry = ctk.CTkEntry(dynamic_frame, font=ctk.CTkFont(size=14))
            song_entry.grid(row=1, column=1, padx=10, pady=5)

            def associate_video_song():
                video_title = video_entry.get().strip()
                song_title = song_entry.get().strip()

                if not video_title or not song_title:
                    messagebox.showerror("Error", "Please fill in both Video Title and Song Title.")
                    return

                try:
                    conn = connect_db()
                    cursor = conn.cursor()

                    # Fetch the video ID and artist ID based on the video title
                    cursor.execute("""
                        SELECT Video.VideoID, Project.ArtID
                        FROM Video
                        JOIN Project ON Video.ProjectID = Project.ProjectID
                        WHERE Project.Title = ?
                    """, (video_title,))
                    video = cursor.fetchone()

                    if not video:
                        messagebox.showerror("Error", "Video not found.")
                        return

                    video_id, video_art_id = video

                    # Fetch the song ID and artist ID based on the song title
                    cursor.execute("""
                        SELECT Song.SongID, Project.ArtID
                        FROM Song
                        JOIN Project ON Song.ProjectID = Project.ProjectID
                        WHERE Project.Title = ?
                    """, (song_title,))
                    song = cursor.fetchone()

                    if not song:
                        messagebox.showerror("Error", "Song not found.")
                        return

                    song_id, song_art_id = song

                    # Ensure the video and song belong to the same artist
                    if video_art_id != song_art_id:
                        messagebox.showerror("Error", "Video and Song do not belong to the same artist.")
                        return

                    # Update the SongID in the Video table
                    cursor.execute("UPDATE Video SET SongID = ? WHERE VideoID = ?", (song_id, video_id))
                    conn.commit()
                    messagebox.showinfo("Success", "Video associated with Song successfully.")
                except sqlite3.Error as e:
                    messagebox.showerror("Database Error", f"Error: {e}")
                finally:
                    conn.close()

            associate_button = ctk.CTkButton(dynamic_frame, text="Associate", font=ctk.CTkFont(size=14), fg_color="#5CB85C", command=associate_video_song)
            associate_button.grid(row=2, column=0, columnspan=2, pady=10)

    associate_var.trace_add("write", update_dynamic_fields)

    # Back button
    back_button = ctk.CTkButton(root, text="Back", font=ctk.CTkFont(size=14), fg_color="#FF6F61", command=lambda: go_back(root, create_admin_main_menu))
    back_button.pack(pady=10)




#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#BETTER VIEW
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def show_better_view(root, create_admin_main_menu):
    """Show a better view with releases categorized into Albums, Songs, Singles, and Videos."""
    # Clear the window
    clear(root)

    # Title Frame
    title_frame = ctk.CTkFrame(root)
    title_frame.pack(fill="x", pady=10)

    # Title Label
    title_label = ctk.CTkLabel(
        title_frame, text="Better View", font=ctk.CTkFont(size=20, weight="bold"), text_color="blue"
    )
    title_label.pack(side="left", padx=10)

    # Back Button
    back_button = ctk.CTkButton(title_frame, text="Back", fg_color="#FF6F61", command=lambda: go_back(root, create_admin_main_menu))
    back_button.pack(side="right", padx=10)

    # Main Frame
    main_frame = ctk.CTkFrame(root)
    main_frame.pack(fill="both", expand=True)

    # Sidebar for categories
    sidebar = ttk.Treeview(main_frame, columns=("Count"), show="tree", height=20)
    sidebar.column("#0", width=200, anchor="w")
    sidebar.heading("#0", text="Categories")
    sidebar.column("Count", width=50, anchor="center")
    sidebar.heading("Count", text="Count")
    sidebar.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

    # Content Area
    content_frame = ctk.CTkFrame(main_frame)
    content_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    main_frame.grid_rowconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)

    # Treeview for displaying details
    details_tree = ttk.Treeview(content_frame, columns=("Type", "Artist", "Genre", "Details"), show="tree headings", height=20)
    details_tree.column("#0", width=300, anchor="w")
    details_tree.heading("#0", text="Releases")
    details_tree.column("Type", width=100, anchor="center")
    details_tree.heading("Type", text="Type")
    details_tree.column("Artist", width=150, anchor="center")
    details_tree.heading("Artist", text="Artist")
    details_tree.column("Genre", width=100, anchor="center")
    details_tree.heading("Genre", text="Genre")
    details_tree.column("Details", width=300, anchor="w")
    details_tree.heading("Details", text="Details")
    details_tree.pack(fill="both", expand=True)

    # Scrollbar for details_tree
    scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=details_tree.yview)
    details_tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Database connection and data fetching
    try:
        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()

        # Fetch counts for categories
        cursor.execute("SELECT COUNT(*) FROM Album")
        album_count = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*) 
            FROM Song 
            WHERE ProjectID IN (SELECT ProjectID FROM Project)
        """)
        song_count = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*) 
            FROM Song 
            WHERE SongID NOT IN (
                SELECT SongID 
                FROM Is_part_of
            ) 
            AND ProjectID IN (
                SELECT ProjectID 
                FROM Project
            )
        """)
        single_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM Video")
        video_count = cursor.fetchone()[0]

        # Populate sidebar
        sidebar.insert("", "end", "releases", text="Releases", values=(album_count + song_count + single_count + video_count))
        sidebar.insert("releases", "end", "albums", text="Albums", values=(album_count))
        sidebar.insert("releases", "end", "songs", text="Songs", values=(song_count))
        sidebar.insert("releases", "end", "singles", text="Singles", values=(single_count))
        sidebar.insert("releases", "end", "videos", text="Videos", values=(video_count))

    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Database error: {e}")
    finally:
        conn.close()

    def load_details(category):
        """Load details based on the selected category."""
        # Clear the details tree before populating
        for item in details_tree.get_children():
            details_tree.delete(item)

        try:
            conn = sqlite3.connect("db.db")
            cursor = conn.cursor()

            if category == "albums":
                # Fetch albums and their songs
                cursor.execute("""
                    SELECT 
                        Album.AlbID, 
                        Project.Title AS AlbumTitle, 
                        Artist.Nickname AS Artist, 
                        Genre.Name AS Genre
                    FROM Album
                    JOIN Project ON Album.ProjectID = Project.ProjectID
                    JOIN Artist ON Project.ArtID = Artist.ArtID
                    JOIN Genre ON Project.GenreID = Genre.GenreID
                """)
                albums = cursor.fetchall()

                for album_id, album_title, artist, genre in albums:
                    album_node = details_tree.insert("", "end", text=f"{album_title}", values=("Album", artist, genre, ""))

                    # Fetch songs in the album
                    cursor.execute("""
                        SELECT 
                            Project.Title AS SongTitle, 
                            Song.Duration, 
                            Song.Rating, 
                            Song.Plays
                        FROM Song
                        JOIN Project ON Song.ProjectID = Project.ProjectID
                        JOIN Is_part_of ON Song.SongID = Is_part_of.SongID
                        WHERE Is_part_of.AlbID = ?
                    """, (album_id,))
                    songs = cursor.fetchall()

                    for song_title, duration, rating, plays in songs:
                        mins, secs = divmod(duration, 60)
                        song_details = f"Duration: {mins}:{secs:02d}, Rating: {rating}, Plays: {plays}"
                        details_tree.insert(album_node, "end", text=f"{song_title}", values=("Song", artist, "", song_details))

            elif category == "songs":
                # Fetch all songs
                cursor.execute("""
                    SELECT 
                        Project.Title AS SongTitle, 
                        Artist.Nickname AS Artist, 
                        Genre.Name AS Genre, 
                        Song.Duration, 
                        Song.Rating, 
                        Song.Plays
                    FROM Song
                    JOIN Project ON Song.ProjectID = Project.ProjectID
                    JOIN Artist ON Project.ArtID = Artist.ArtID
                    JOIN Genre ON Project.GenreID = Genre.GenreID
                """)
                songs = cursor.fetchall()

                for song_title, artist, genre, duration, rating, plays in songs:
                    mins, secs = divmod(duration, 60)
                    song_details = f"Duration: {mins}:{secs:02d}, Rating: {rating}, Plays: {plays}"
                    details_tree.insert("", "end", text=f"{song_title}", values=("Song", artist, genre, song_details))

            elif category == "singles":
                # Fetch singles
                cursor.execute("""
                    SELECT 
                        Project.Title AS SingleTitle, 
                        Artist.Nickname AS Artist, 
                        Genre.Name AS Genre, 
                        Song.Duration, 
                        Song.Rating, 
                        Song.Plays
                    FROM Song
                    JOIN Project ON Song.ProjectID = Project.ProjectID
                    JOIN Artist ON Project.ArtID = Artist.ArtID
                    JOIN Genre ON Project.GenreID = Genre.GenreID
                    LEFT JOIN Is_part_of ON Song.SongID = Is_part_of.SongID
                    WHERE Is_part_of.SongID IS NULL
                """)
                singles = cursor.fetchall()

                for single_title, artist, genre, duration, rating, plays in singles:
                    mins, secs = divmod(duration, 60)
                    single_details = f"Duration: {mins}:{secs:02d}, Rating: {rating}, Plays: {plays}"
                    details_tree.insert("", "end", text=f"{single_title}", values=("Single", artist, genre, single_details))

            elif category == "videos":
                # Fetch videos
                cursor.execute("""
                    SELECT 
                        Project.Title AS VideoTitle, 
                        Artist.Nickname AS Artist, 
                        Genre.Name AS Genre, 
                        Video.Rating, 
                        Video.Views
                    FROM Video
                    JOIN Project ON Video.ProjectID = Project.ProjectID
                    JOIN Artist ON Project.ArtID = Artist.ArtID
                    JOIN Genre ON Project.GenreID = Genre.GenreID
                """)
                videos = cursor.fetchall()

                for video_title, artist, genre, rating, views in videos:
                    video_details = f"Rating: {rating}, Views: {views}"
                    details_tree.insert("", "end", text=f"{video_title}", values=("Video", artist, genre, video_details))

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")
        finally:
            conn.close()

    def on_sidebar_select(event):
        """Handle sidebar selection and load corresponding details."""
        selected_item = sidebar.focus()
        if selected_item in ["albums", "songs", "singles", "videos"]:
            load_details(selected_item)

    sidebar.bind("<<TreeviewSelect>>", on_sidebar_select)








#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#DELETE FUNCTION
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def show_delete_screen(root, create_admin_main_menu):
    """Display the delete screen with options to delete an Individual, Project, or Partner."""
    clear(root)  # Clear existing widgets on the screen

    # Title Frame
    title_frame = ctk.CTkFrame(root)
    title_frame.pack(fill="x", pady=10)

    # Title Label
    delete_label = ctk.CTkLabel(title_frame, text="Delete Records", font=ctk.CTkFont(size=20, weight="bold"), text_color="blue")
    delete_label.pack(side="left", padx=10)

    # Back Button
    back_button = ctk.CTkButton(title_frame, text="Back", fg_color="#FF6F61", command=lambda: go_back(root, create_admin_main_menu))
    back_button.pack(side="right", padx=10)

    # Combobox for selecting the delete option
    delete_type_label = ctk.CTkLabel(root, text="Select Record Type to Delete:", font=ctk.CTkFont(size=14))
    delete_type_label.pack(pady=10)

    delete_var = ctk.StringVar()
    delete_combobox = ctk.CTkComboBox(root, variable=delete_var, values=["Individual", "Project", "Partner"], font=ctk.CTkFont(size=14))
    delete_combobox.pack(pady=10)

    # Frame for dynamic input fields
    dynamic_frame = ctk.CTkFrame(root)
    dynamic_frame.pack(pady=20)

    def update_dynamic_fields(*args):
        """Update input fields dynamically based on the selected delete option."""
        for widget in dynamic_frame.winfo_children():
            widget.destroy()

        delete_type = delete_var.get()

        if delete_type == "Individual":
            # Individual deletion
            id_label = ctk.CTkLabel(dynamic_frame, text="Enter Individual ID:", font=ctk.CTkFont(size=14))
            id_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
            id_entry = ctk.CTkEntry(dynamic_frame, font=ctk.CTkFont(size=14))
            id_entry.grid(row=0, column=1, padx=10, pady=5)

            def delete_individual():
                individ_id = id_entry.get().strip()
                if not individ_id.isdigit():
                    messagebox.showerror("Error", "Please enter a valid Individual ID.")
                    return

                try:
                    conn = sqlite3.connect("db.db")
                    cursor = conn.cursor()

                    # Check if the individual exists
                    cursor.execute("SELECT * FROM Individual WHERE IndividID = ?", (int(individ_id),))
                    individual = cursor.fetchone()
                    if not individual:
                        messagebox.showerror("Error", "Individual not found.")
                        return

                    # Proceed with deletion
                    cursor.execute("DELETE FROM Individual WHERE IndividID = ?", (int(individ_id),))
                    conn.commit()
                    messagebox.showinfo("Success", "Individual deleted successfully.")
                except sqlite3.Error as e:
                    messagebox.showerror("Error", f"Database error: {e}")
                finally:
                    conn.close()

            delete_button = ctk.CTkButton(dynamic_frame, text="Delete", fg_color="#E53935", command=delete_individual)
            delete_button.grid(row=1, column=0, columnspan=2, pady=10)

        elif delete_type == "Project":
            # Project deletion
            title_label = ctk.CTkLabel(dynamic_frame, text="Enter Project Title:", font=ctk.CTkFont(size=14))
            title_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
            title_entry = ctk.CTkEntry(dynamic_frame, font=ctk.CTkFont(size=14))
            title_entry.grid(row=0, column=1, padx=10, pady=5)

            def delete_project():
                project_title = title_entry.get().strip()
                if not project_title:
                    messagebox.showerror("Error", "Please enter a valid Project Title.")
                    return

                try:
                    conn = sqlite3.connect("db.db")
                    cursor = conn.cursor()

                    # Check if the project exists
                    cursor.execute("SELECT ProjectID FROM Project WHERE Title = ?", (project_title,))
                    project = cursor.fetchone()
                    if not project:
                        messagebox.showerror("Error", "Project not found.")
                        return

                    project_id = project[0]

                    # Proceed with deletion
                    cursor.execute("DELETE FROM Project WHERE ProjectID = ?", (project_id,))
                    conn.commit()
                    messagebox.showinfo("Success", "Project deleted successfully.")
                except sqlite3.Error as e:
                    messagebox.showerror("Error", f"Database error: {e}")
                finally:
                    conn.close()

            delete_button = ctk.CTkButton(
                dynamic_frame, text="Delete", fg_color="red", command=delete_project
            )
            delete_button.grid(row=1, column=0, columnspan=2, pady=10)

        elif delete_type == "Partner":
            # Partner deletion
            id_label = ctk.CTkLabel(dynamic_frame, text="Enter Partner ID:", font=ctk.CTkFont(size=14))
            id_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
            id_entry = ctk.CTkEntry(dynamic_frame, font=ctk.CTkFont(size=14))
            id_entry.grid(row=0, column=1, padx=10, pady=5)

            def delete_partner():
                partner_id = id_entry.get().strip()
                if not partner_id.isdigit():
                    messagebox.showerror("Error", "Please enter a valid Partner ID.")
                    return

                try:
                    conn = sqlite3.connect("db.db")
                    cursor = conn.cursor()

                    # Check if the partner exists
                    cursor.execute("SELECT * FROM Partner WHERE PartID = ?", (int(partner_id),))
                    partner = cursor.fetchone()
                    if not partner:
                        messagebox.showerror("Error", "Partner not found.")
                        return

                    # Proceed with deletion
                    cursor.execute("DELETE FROM Partner WHERE PartID = ?", (int(partner_id),))
                    conn.commit()
                    messagebox.showinfo("Success", "Partner deleted successfully.")
                except sqlite3.Error as e:
                    messagebox.showerror("Error", f"Database error: {e}")
                finally:
                    conn.close()

            delete_button = ctk.CTkButton(dynamic_frame, text="Delete", fg_color="#FF0000", command=delete_partner)
            delete_button.grid(row=1, column=0, columnspan=2, pady=10)

    # Trace changes in combobox selection
    delete_var.trace_add("write", update_dynamic_fields)
