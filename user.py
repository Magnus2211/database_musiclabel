import customtkinter as ctk
from tkinter import ttk,messagebox
import sqlite3
import subprocess
import sys


def exit_to_main():
    """Exit to the main menu."""
    root.destroy()
    subprocess.run(["python", "main.py"])


def clear(widget):
    """Clear all child widgets from a parent widget."""
    for child in widget.winfo_children():
        child.destroy()


def show_main_screen():
    """Displays the main user screen with options."""
    clear(root)

    # Title Label
    title_label = ctk.CTkLabel(root, text="Hello "+ show_name(), font=ctk.CTkFont(size=20, weight="bold"))
    title_label.pack(pady=20)

    # My Profile Button
    profile_button = ctk.CTkButton(root, text="My Profile",fg_color="#0078D7", command=show_dashboard)
    profile_button.pack(pady=10)

    # Search Button
    search_button = ctk.CTkButton(root, text="Search for Artist",fg_color="#17A2B8", command=show_search_screen)
    search_button.pack(pady=10)

    # Top 5 by Genre Button
    top_5_button = ctk.CTkButton(root, text="Top 5 by Genre",fg_color="#6F42C1", command=show_top_5_screen)
    top_5_button.pack(pady=10)

    search_artist_button = ctk.CTkButton(root, text="Quick Search for Artist",fg_color="#28A745", command=quick_search_for_artist)
    search_artist_button.pack(pady=10)

    # Exit Button
    exit_button = ctk.CTkButton(root, text="Exit to Main", fg_color="#FFB300", command=exit_to_main)
    exit_button.pack(pady=20)

def show_name():
    """Used to display name of the logged user"""
    try:
        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()
        cursor.execute("SELECT First_name FROM Individual WHERE UserID = ?", (user_id,))
        name = cursor.fetchone()
        name = name[0]
        if not name:
            messagebox.showerror(title="Error", message="No associated artist found for the user.")
            return


    except sqlite3.Error as e:
        messagebox.showerror(title="Error", message=f"Database error: {e}")
    finally:
        conn.close()
    
    return name

def show_dashboard():
    """Displays the dashboard for the logged-in user's artist."""
    try:
        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()
        cursor.execute("SELECT ArtID FROM Individual WHERE UserID = ?", (user_id,))
        artist = cursor.fetchone()
        if not artist:
            messagebox.showerror(title="Error", message="No associated artist found for the user.")
            return

        art_id = artist[0]
        show_artist_dashboard(art_id)

    except sqlite3.Error as e:
        messagebox.showerror(title="Error", message=f"Database error: {e}")
    finally:
        conn.close()


def show_search_screen():
    """Displays the search screen for finding another artist."""
    clear(root)

    # Title Label
    title_label = ctk.CTkLabel(root, text="Search for Artist", font=ctk.CTkFont(size=20, weight="bold"))
    title_label.pack(pady=20)

    # Search Frame
    search_frame = ctk.CTkFrame(root)
    search_frame.pack(pady=10)

    search_label = ctk.CTkLabel(search_frame, text="Artist Nickname:")
    search_label.grid(row=0, column=0, padx=10, pady=5)

    search_entry = ctk.CTkEntry(search_frame, placeholder_text="Enter artist nickname")
    search_entry.grid(row=0, column=1, padx=10, pady=5)

    # Search Button
    def search_artist():
        artist_nickname = search_entry.get().strip()
        if not artist_nickname:
            messagebox.showerror(title="Error", message="Please enter an artist nickname.")
            return

        try:
            conn = sqlite3.connect("db.db")
            cursor = conn.cursor()
            cursor.execute("SELECT ArtID FROM Artist WHERE Nickname = ?", (artist_nickname,))
            artist = cursor.fetchone()
            if not artist:
                messagebox.showerror(title="Error", message="Artist not found.")
                return

            art_id = artist[0]
            show_artist_dashboard(art_id)

        except sqlite3.Error as e:
            messagebox.showerror(title="Error", message=f"Database error: {e}")
        finally:
            conn.close()

    search_button = ctk.CTkButton(search_frame, text="Search", command=search_artist)
    search_button.grid(row=0, column=2, padx=10, pady=5)

    # Back Button
    back_button = ctk.CTkButton(root, text="Back", fg_color="#FF6F61", command=show_main_screen)
    back_button.pack(pady=20)



def show_artist_dashboard(art_id):
    """Displays the dashboard for a specific artist."""
    clear(root)

    # Title Frame
    title_frame = ctk.CTkFrame(root)
    title_frame.pack(pady=10, fill="x")

    # Title Label
    title_label = ctk.CTkLabel(
        title_frame, text="Artist Dashboard", font=ctk.CTkFont(size=20, weight="bold")
    )
    title_label.pack(side="left", padx=(10, 20))

    # Back Button
    back_button = ctk.CTkButton(title_frame, text="Back", fg_color="#FF6F61", command=show_main_screen)
    back_button.pack(side="left", padx=10)

    # Main Frame
    main_frame = ctk.CTkFrame(root)
    main_frame.pack(fill="both", expand=True)

    # Sidebar for categories
    sidebar = ttk.Treeview(main_frame, columns=("Count"), show="tree")
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

    # Treeview to display details
    details_tree = ttk.Treeview(content_frame, columns=("Details", "Genre"), show="tree")
    details_tree.column("#0", width=300, anchor="w")
    details_tree.heading("#0", text="Items")
    details_tree.column("Details", width=300, anchor="w")
    details_tree.heading("Details", text="Details")
    details_tree.column("Genre", width=200, anchor="center")
    details_tree.heading("Genre", text="Genre")
    details_tree.pack(fill="both", expand=True)

    # Add Scrollbar for details_tree
    scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=details_tree.yview)
    details_tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    try:
        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()

        # Fetch counts for categories
        cursor.execute(
            "SELECT COUNT(*) FROM Album JOIN Project ON Album.ProjectID = Project.ProjectID WHERE Project.ArtID = ?",
            (art_id,),
        )
        album_count = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM Song JOIN Project ON Song.ProjectID = Project.ProjectID WHERE Project.ArtID = ?",
            (art_id,),
        )
        song_count = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*) FROM Song
            LEFT JOIN Is_part_of ON Song.SongID = Is_part_of.SongID
            JOIN Project ON Song.ProjectID = Project.ProjectID
            WHERE Project.ArtID = ? AND Is_part_of.AlbID IS NULL
            """,
            (art_id,),
        )
        single_count = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM Video JOIN Project ON Video.ProjectID = Project.ProjectID WHERE Project.ArtID = ?",
            (art_id,),
        )
        video_count = cursor.fetchone()[0]

        # Populate sidebar
        sidebar.insert("", "end", "releases", text="Releases", values=(album_count + song_count + video_count))
        sidebar.insert("releases", "end", "albums", text="Albums", values=(album_count))
        sidebar.insert("releases", "end", "songs", text="Songs", values=(song_count))
        sidebar.insert("releases", "end", "singles", text="Singles", values=(single_count))
        sidebar.insert("releases", "end", "videos", text="Videos", values=(video_count))

    except sqlite3.Error as e:
        messagebox.showerror(title="Error", message=f"Database error: {e}")
    finally:
        conn.close()

    def load_details(category):
        """Load details based on the selected category."""
        # Clear existing details in the tree
        for item in details_tree.get_children():
            details_tree.delete(item)

        try:
            conn = sqlite3.connect("db.db")
            cursor = conn.cursor()

            if category == "albums":
                # Fetch albums for the artist
                cursor.execute(
                    """
                    SELECT Album.AlbID, Project.Title, Genre.Name
                    FROM Album
                    JOIN Project ON Album.ProjectID = Project.ProjectID
                    JOIN Genre ON Project.GenreID = Genre.GenreID
                    WHERE Project.ArtID = ?
                    """,
                    (art_id,),
                )
                albums = cursor.fetchall()
                print("Albums fetched:", albums)  # Debugging: Print fetched albums

                if not albums:
                    print("No albums found for ArtID:", art_id)  # Debugging: Notify if no albums found

                for album_id, album_title, genre in albums:
                    # Insert album details into the treeview
                    album_node = details_tree.insert("", "end", text=album_title, values=("", genre))
                    print(f"Album added: {album_title}, Genre: {genre}")  # Debugging: Confirm album added

                    # Fetch songs in the album
                    cursor.execute(
                        """
                        SELECT Project.Title, Song.Duration, Song.Rating, Song.Plays, Genre.Name
                        FROM Song
                        JOIN Project ON Song.ProjectID = Project.ProjectID
                        JOIN Is_part_of ON Song.SongID = Is_part_of.SongID
                        JOIN Genre ON Project.GenreID = Genre.GenreID
                        WHERE Is_part_of.AlbID = ?
                        """,
                        (album_id,),
                    )
                    songs = cursor.fetchall()
                    print(f"Songs in album {album_title}: {songs}")  # Debugging: Print songs for the album

                    for song_title, duration, rating, plays, song_genre in songs:
                        mins, secs = divmod(duration, 60)
                        song_details = f"Duration: {mins}:{secs:02d}, Rating: {rating}, Plays: {plays}"
                        details_tree.insert(album_node, "end", text=song_title, values=(song_details, song_genre))

            elif category == "singles":
                # Fetch singles
                cursor.execute(
                    """
                    SELECT Project.Title, Song.Duration, Song.Rating, Song.Plays, Genre.Name
                    FROM Song
                    LEFT JOIN Is_part_of ON Song.SongID = Is_part_of.SongID
                    JOIN Project ON Song.ProjectID = Project.ProjectID
                    JOIN Genre ON Project.GenreID = Genre.GenreID
                    WHERE Project.ArtID = ? AND Is_part_of.AlbID IS NULL
                    """,
                    (art_id,),
                )
                singles = cursor.fetchall()
                print("Singles fetched:", singles)  # Debugging: Print singles data

                for song_title, duration, rating, plays, genre in singles:
                    mins, secs = divmod(duration, 60)
                    song_details = f"Duration: {mins}:{secs:02d}, Rating: {rating}, Plays: {plays}"
                    details_tree.insert("", "end", text=song_title, values=(song_details, genre))

            elif category == "songs":
                # Fetch all songs
                cursor.execute(
                    """
                    SELECT Project.Title, Song.Duration, Song.Rating, Song.Plays, Genre.Name
                    FROM Song
                    JOIN Project ON Song.ProjectID = Project.ProjectID
                    JOIN Genre ON Project.GenreID = Genre.GenreID
                    WHERE Project.ArtID = ?
                    """,
                    (art_id,),
                )
                songs = cursor.fetchall()
                print("Songs fetched:", songs)  # Debugging: Print all songs

                for song_title, duration, rating, plays, genre in songs:
                    mins, secs = divmod(duration, 60)
                    song_details = f"Duration: {mins}:{secs:02d}, Rating: {rating}, Plays: {plays}"
                    details_tree.insert("", "end", text=song_title, values=(song_details, genre))

            elif category == "videos":
                # Fetch videos
                cursor.execute(
                    """
                    SELECT Project.Title, Video.Rating, Video.Views, Genre.Name
                    FROM Video
                    JOIN Project ON Video.ProjectID = Project.ProjectID
                    JOIN Genre ON Project.GenreID = Genre.GenreID
                    WHERE Project.ArtID = ?
                    """,
                    (art_id,),
                )
                videos = cursor.fetchall()
                print("Videos fetched:", videos)  # Debugging: Print videos data

                for video_title, rating, views, genre in videos:
                    video_details = f"Rating: {rating}, Views: {views}"
                    details_tree.insert("", "end", text=video_title, values=(video_details, genre))

        except sqlite3.Error as e:
            messagebox.showerror(title="Error", message=f"Database error: {e}")
        finally:
            conn.close()



    def on_sidebar_select(event):
        selected_item = sidebar.focus()
        if selected_item in ["albums", "songs", "singles", "videos"]:
            load_details(selected_item)

    sidebar.bind("<<TreeviewSelect>>", on_sidebar_select)






def show_top_5_screen():
    """Displays the screen to select a genre and view top 5 items in that genre."""
    clear(root)

    # Title Label
    title_label = ctk.CTkLabel(root, text="Top 5 by Genre", font=ctk.CTkFont(size=20, weight="bold"))
    title_label.pack(pady=20)

    # Genre Selection Frame
    genre_frame = ctk.CTkFrame(root)
    genre_frame.pack(pady=10)

    genre_label = ctk.CTkLabel(genre_frame, text="Select Genre:", font=ctk.CTkFont(size=14))
    genre_label.grid(row=0, column=0, padx=10, pady=5)

    genre_var = ctk.StringVar()
    genre_combobox = ctk.CTkComboBox(genre_frame, variable=genre_var, font=ctk.CTkFont(size=14))
    genre_combobox.grid(row=0, column=1, padx=10, pady=5)

    # Load genres from the database
    try:
        conn = sqlite3.connect("db.db")
        cursor = conn.cursor()
        cursor.execute("SELECT Name FROM Genre")
        genres = [row[0] for row in cursor.fetchall()]
        genre_combobox.configure(values=genres)
    except sqlite3.Error as e:
        messagebox.showerror(title="Error", message=f"Database error: {e}")
    finally:
        conn.close()

    # Content Frame for Treeviews
    content_frame = ctk.CTkFrame(root)
    content_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Sidebar for Categories
    sidebar = ttk.Treeview(content_frame, columns=("Count"), show="tree")
    sidebar.column("#0", width=200, anchor="w")
    sidebar.heading("#0", text="Categories")
    sidebar.column("Count", width=50, anchor="center")
    sidebar.heading("Count", text="Count")
    sidebar.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

    # Details Treeview
    details_tree = ttk.Treeview(content_frame, columns=("Details"), show="tree")
    details_tree.column("#0", width=300, anchor="w")
    details_tree.heading("#0", text="Items")
    details_tree.column("Details", width=400, anchor="w")
    details_tree.heading("Details", text="Details")
    details_tree.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    # Add Scrollbar for details_tree
    scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=details_tree.yview)
    details_tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=2, sticky="ns")

    # Configure grid weights
    content_frame.grid_rowconfigure(0, weight=1)
    content_frame.grid_columnconfigure(1, weight=1)

    def show_top_5():
        """Fetch and display the top 5 albums, songs, and videos for the selected genre."""
        genre = genre_var.get()
        if not genre:
            messagebox.showerror(title="Error", message="Please select a genre.")
            return

        # Clear existing data
        for item in details_tree.get_children():
            details_tree.delete(item)
        for item in sidebar.get_children():
            sidebar.delete(item)

        try:
            conn = sqlite3.connect("db.db")
            cursor = conn.cursor()

            # Fetch GenreID
            cursor.execute("SELECT GenreID FROM Genre WHERE Name = ?", (genre,))
            genre_id = cursor.fetchone()
            if not genre_id:
                messagebox.showerror(title="Error", message="Genre not found.")
                return

            genre_id = genre_id[0]

            # Top 5 Albums
            cursor.execute(
                """
                SELECT Project.Title, Album.Rating
                FROM Album
                JOIN Project ON Album.ProjectID = Project.ProjectID
                WHERE Project.GenreID = ?
                ORDER BY Album.Rating DESC
                LIMIT 5
                """,
                (genre_id,),
            )
            albums = cursor.fetchall()

            # Top 5 Songs
            cursor.execute(
                """
                SELECT Project.Title, Song.Duration, Song.Rating, Song.Plays
                FROM Song
                JOIN Project ON Song.ProjectID = Project.ProjectID
                WHERE Project.GenreID = ?
                ORDER BY Song.Rating DESC, Song.Plays DESC
                LIMIT 5
                """,
                (genre_id,),
            )
            songs = cursor.fetchall()

            # Top 5 Videos
            cursor.execute(
                """
                SELECT Project.Title, Video.Rating, Video.Views
                FROM Video
                JOIN Project ON Video.ProjectID = Project.ProjectID
                WHERE Project.GenreID = ?
                ORDER BY Video.Rating DESC, Video.Views DESC
                LIMIT 5
                """,
                (genre_id,),
            )
            videos = cursor.fetchall()

            # Populate Sidebar
            sidebar.insert("", "end", "top5", text="Top 5", open=True)
            sidebar.insert("top5", "end", "albums", text="Albums", values=(len(albums)))
            sidebar.insert("top5", "end", "songs", text="Songs", values=(len(songs)))
            sidebar.insert("top5", "end", "videos", text="Videos", values=(len(videos)))

            def load_category_details(category):
                """Load the details of the selected category."""
                for item in details_tree.get_children():
                    details_tree.delete(item)

                if category == "albums":
                    for album_title, rating in albums:
                        details_tree.insert("", "end", text=f"{album_title} ", values=(f"Rating: {rating}",))
                elif category == "songs":
                    for song_title, duration, rating, plays in songs:
                        mins, secs = divmod(duration, 60)
                        song_details = f"Duration: {mins}:{secs:02d}, Rating: {rating}, Plays: {plays}"
                        details_tree.insert("", "end", text=f"{song_title} ", values=(song_details,))
                elif category == "videos":
                    for video_title, rating, views in videos:
                        video_details = f"Rating: {rating}, Views: {views}"
                        details_tree.insert("", "end", text=f"{video_title} ", values=(video_details,))

            def on_sidebar_select(event):
                selected_item = sidebar.focus()
                if selected_item in ["albums", "songs", "videos"]:
                    load_category_details(selected_item)

            sidebar.bind("<<TreeviewSelect>>", on_sidebar_select)

        except sqlite3.Error as e:
            messagebox.showerror(title="Error", message=f"Database error: {e}")
        finally:
            conn.close()

    # Show Button
    show_button = ctk.CTkButton(genre_frame, text="Show Top 5", command=show_top_5)
    show_button.grid(row=0, column=2, padx=10, pady=5)

    # Back Button
    back_button = ctk.CTkButton(genre_frame, text="Back", fg_color="#FF6F61", command=show_main_screen)
    back_button.grid(row=0, column=3, padx=10, pady=5)




def quick_search_for_artist():
    def search_artist():
        artist_nickname = search_entry.get().strip()

        if not artist_nickname:
            messagebox.showerror(title="Error", message="Please enter an artist nickname.")
            return

        try:
            conn = sqlite3.connect("db.db")
            cursor = conn.cursor()

            # Query the artist and their data
            query = """
            SELECT 
                Artist.ArtID, 
                Artist.Nickname AS artist_name,
                -- Most Successful Song
                (SELECT Project.Title
                 FROM Release
                 JOIN Project ON Release.ProjectID = Project.ProjectID
                 JOIN Song ON Project.ProjectID = Song.ProjectID
                 WHERE Release.ArtID = Artist.ArtID
                 ORDER BY Song.Plays DESC
                 LIMIT 1) AS most_successful_song,
                (SELECT MAX(Song.Plays)
                 FROM Release
                 JOIN Project ON Release.ProjectID = Project.ProjectID
                 JOIN Song ON Project.ProjectID = Song.ProjectID
                 WHERE Release.ArtID = Artist.ArtID) AS song_plays,
                -- Most Successful Video
                (SELECT Project.Title
                 FROM Release
                 JOIN Project ON Release.ProjectID = Project.ProjectID
                 JOIN Video ON Project.ProjectID = Video.ProjectID
                 WHERE Release.ArtID = Artist.ArtID
                 ORDER BY Video.Views DESC
                 LIMIT 1) AS most_successful_video,
                (SELECT MAX(Video.Views)
                 FROM Release
                 JOIN Project ON Release.ProjectID = Project.ProjectID
                 JOIN Video ON Project.ProjectID = Video.ProjectID
                 WHERE Release.ArtID = Artist.ArtID) AS video_views,
                -- Most Successful Album
                (SELECT Project.Title
                 FROM Release
                 JOIN Project ON Release.ProjectID = Project.ProjectID
                 JOIN Album ON Project.ProjectID = Album.ProjectID
                 LEFT JOIN CD ON Album.AlbID = CD.AlbID
                 LEFT JOIN Vinyl ON Album.AlbID = Vinyl.AlbID
                 WHERE Release.ArtID = Artist.ArtID
                 ORDER BY COALESCE(CD.Sales, 0) + COALESCE(Vinyl.Sales, 0) DESC
                 LIMIT 1) AS most_successful_album,
                (SELECT MAX(COALESCE(CD.Sales, 0) + COALESCE(Vinyl.Sales, 0))
                 FROM Release
                 JOIN Project ON Release.ProjectID = Project.ProjectID
                 JOIN Album ON Project.ProjectID = Album.ProjectID
                 LEFT JOIN CD ON Album.AlbID = CD.AlbID
                 LEFT JOIN Vinyl ON Album.AlbID = Vinyl.AlbID
                 WHERE Release.ArtID = Artist.ArtID) AS album_sales
            FROM 
                Artist
            WHERE Artist.Nickname = ?;
            """

            cursor.execute(query, (artist_nickname,))
            artist_data = cursor.fetchone()

            if not artist_data:
                messagebox.showerror(title="Error", message="Artist not found.")
                return

            art_id, artist_name, song, song_plays, video, video_views, album, album_sales = artist_data

            # Fetch individuals linked to the same ArtistID
            individuals_query = """
            SELECT First_name, Last_name, Email, Phone 
            FROM Individual 
            WHERE ArtID = ?;
            """

            cursor.execute(individuals_query, (art_id,))
            individuals = cursor.fetchall()

        finally:
            conn.close()

        # Clear the current window
        clear(root)

        # Display artist data
        artist_label = ctk.CTkLabel(root, text=f"Artist: {artist_name}", font=ctk.CTkFont(size=16, weight="bold"))
        artist_label.pack(pady=10)

        if song:
            song_label = ctk.CTkLabel(root, text=f"Most Successful Song: {song} ({song_plays} plays)")
            song_label.pack(pady=5)
        
        if video:
            video_label = ctk.CTkLabel(root, text=f"Most Successful Video: {video} ({video_views} views)")
            video_label.pack(pady=5)

        if album:
            album_label = ctk.CTkLabel(root, text=f"Most Successful Album: {album} ({album_sales} sales)")
            album_label.pack(pady=5)

        # Display individuals linked to the artist
        individuals_label = ctk.CTkLabel(root, text="Associated Individuals:", font=ctk.CTkFont(size=14, weight="bold"))
        individuals_label.pack(pady=10)

        for first_name, last_name, email, phone in individuals:
            individual_info = f"{first_name} {last_name} | Email: {email} | Phone: {phone}"
            individual_label = ctk.CTkLabel(root, text=individual_info)
            individual_label.pack(pady=2)

        # Back button
        back_button = ctk.CTkButton(root, text="Back", fg_color="#FF6F61", command=quick_search_for_artist)
        back_button.pack(pady=20)

    # Search bar UI
    clear(root)

    search_label = ctk.CTkLabel(root, text="Search Artist", font=ctk.CTkFont(size=16, weight="bold"))
    search_label.pack(pady=20)

    search_entry = ctk.CTkEntry(root, placeholder_text="Enter artist nickname")
    search_entry.pack(pady=10)

    search_button = ctk.CTkButton(root, text="Search", command=search_artist)
    search_button.pack(pady=10)

    back_button = ctk.CTkButton(root, text="Back", fg_color="#FF6F61", command=show_main_screen)
    back_button.pack(pady=20)






# Main Application
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: No UserID provided.")
        sys.exit(1)
    try:
        user_id = int(sys.argv[1])
    except ValueError:
        print("Error: Invalid UserID provided.")
        sys.exit(1)

    # Initialize CustomTkinter root
    root = ctk.CTk()
    root.configure(fg_color="#E3F2FD")
    root.title("User Dashboard")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}")
    show_main_screen()
    root.mainloop()