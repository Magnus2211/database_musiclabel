BEGIN TRANSACTION;

DROP TABLE IF EXISTS "User";
CREATE TABLE IF NOT EXISTS "User" (
    "UserID" INTEGER NOT NULL,
    "username" VARCHAR(20) NOT NULL,
    "password" VARCHAR(20) NOT NULL,
    "bool_admin" BOOLEAN NOT NULL,
    PRIMARY KEY ("UserID")
);

DROP TABLE IF EXISTS "Admin";
CREATE TABLE IF NOT EXISTS "Admin" (
    "AdminID" INTEGER NOT NULL,
    "UserID" INTEGER NOT NULL,
    PRIMARY KEY ("AdminID"),
    FOREIGN KEY ("UserID") REFERENCES "User" ("UserID")
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS "Individual";
CREATE TABLE IF NOT EXISTS "Individual" (
    "IndividID" INTEGER,
    "First_name" VARCHAR(25) DEFAULT '',
    "Last_name" VARCHAR(25) DEFAULT '',
    "Country" VARCHAR(25) DEFAULT '',
    "Age" INTEGER DEFAULT 0,
    "Phone" VARCHAR(25) DEFAULT '',
    "Email" VARCHAR(25) DEFAULT '',
    "UserID" INTEGER NOT NULL,
    "ContID" INTEGER NOT NULL,
    "ArtID" INTEGER NOT NULL,
    PRIMARY KEY ("IndividID"),
    FOREIGN KEY ("UserID") REFERENCES "User" ("UserID")
        ON DELETE CASCADE,
    FOREIGN KEY ("ContID") REFERENCES "Contract" ("ContID")
        ON DELETE CASCADE,
    FOREIGN KEY ("ArtID") REFERENCES "Artist" ("ArtID")
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS "Contract";
CREATE TABLE IF NOT EXISTS "Contract" (
    "ContID" INTEGER NOT NULL,
    "Start_Date" DATE DEFAULT NULL,
    "End_Date" DATE DEFAULT NULL,
    "Salary" FLOAT DEFAULT 0,
    PRIMARY KEY ("ContID")
);

DROP TABLE IF EXISTS "Project";
CREATE TABLE IF NOT EXISTS "Project" (
    "ProjectID" INTEGER NOT NULL,
    "Release_Date" DATE DEFAULT NULL,
    "ArtistID" INTEGER NOT NULL,
    "GenreID" INTEGER NOT NULL,
    "Title" VARCHAR(50) DEFAULT '',
    PRIMARY KEY ("ProjectID"),
    FOREIGN KEY ("ArtistID") REFERENCES "Artist" ("ArtID")
        ON DELETE CASCADE,
    FOREIGN KEY ("GenreID") REFERENCES "Genre" ("GenreID")
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS "Song";
CREATE TABLE IF NOT EXISTS "Song" (
    "SongID" INTEGER NOT NULL,
    "ProjectID" INTEGER NOT NULL,
    "Duration" INTEGER DEFAULT 0,
    "Rating" FLOAT DEFAULT 0,
    "Plays" INTEGER DEFAULT 0,
    PRIMARY KEY ("SongID"),
    FOREIGN KEY ("ProjectID") REFERENCES "Project" ("ProjectID")
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS "Video";
CREATE TABLE IF NOT EXISTS "Video" (
    "VideoID" INTEGER NOT NULL,
    "ProjectID" INTEGER NOT NULL,
    "SongID" INTEGER NOT NULL,
    "Rating" FLOAT DEFAULT 0,
    "Views" INTEGER DEFAULT 0,
    PRIMARY KEY ("VideoID"),
    FOREIGN KEY ("ProjectID") REFERENCES "Project" ("ProjectID")
        ON DELETE CASCADE,
    FOREIGN KEY ("SongID") REFERENCES "Song" ("SongID")
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS "Album";
CREATE TABLE IF NOT EXISTS "Album" (
    "AlbID" INTEGER NOT NULL,
    "ProjectID" INTEGER NOT NULL,
    "Rating" FLOAT DEFAULT 0,
    PRIMARY KEY ("AlbID"),
    FOREIGN KEY ("ProjectID") REFERENCES "Project" ("ProjectID")
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS "Releases_As";
CREATE TABLE IF NOT EXISTS "Releases_As" (
    "AlbID" INTEGER NOT NULL,
    "FormID" INTEGER NOT NULL,
    PRIMARY KEY ("AlbID", "FormID"),
    FOREIGN KEY ("AlbID") REFERENCES "Album" ("AlbID")
        ON DELETE CASCADE,
    FOREIGN KEY ("FormID") REFERENCES "Format" ("FormID")
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS "Format";
CREATE TABLE IF NOT EXISTS "Format" (
    "FormID" INTEGER NOT NULL,
    PRIMARY KEY ("FormID")
);

DROP TABLE IF EXISTS "Vinyl";
CREATE TABLE IF NOT EXISTS "Vinyl" (
    "FormID" INTEGER NOT NULL,
    "Cost" FLOAT DEFAULT 0,
    "Sales" INTEGER DEFAULT 0,
    PRIMARY KEY ("FormID"),
    FOREIGN KEY ("FormID") REFERENCES "Format" ("FormID")
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS "CD";
CREATE TABLE IF NOT EXISTS "CD" (
    "FormID" INTEGER NOT NULL,
    "Cost" FLOAT DEFAULT 0,
    "Sales" INTEGER DEFAULT 0,
    PRIMARY KEY ("FormID"),
    FOREIGN KEY ("FormID") REFERENCES "Format" ("FormID")
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS "Digital";
CREATE TABLE IF NOT EXISTS "Digital" (
    "FormID" INTEGER NOT NULL,
    "Plays" INTEGER DEFAULT 0,
    PRIMARY KEY ("FormID"),
    FOREIGN KEY ("FormID") REFERENCES "Format" ("FormID")
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS "Is_part_of";
CREATE TABLE IF NOT EXISTS "Is_part_of" (
    "SongID" INTEGER NOT NULL,
    "AlbID" INTEGER NOT NULL,
    PRIMARY KEY ("SongID", "AlbID"),
    FOREIGN KEY ("SongID") REFERENCES "Song" ("SongID")
        ON DELETE CASCADE,
    FOREIGN KEY ("AlbID") REFERENCES "Album" ("AlbID")
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS "Partner";
CREATE TABLE IF NOT EXISTS "Partner" (
    "PartID" INTEGER NOT NULL,
    "RoleID" INTEGER NOT NULL,
    "First_name" VARCHAR(25) DEFAULT '',
    "Last_name" VARCHAR(25) DEFAULT '',
    PRIMARY KEY ("PartID"),
    FOREIGN KEY ("RoleID") REFERENCES "Role" ("RoleID")
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS "Works_on";
CREATE TABLE IF NOT EXISTS "Works_on" (
    "ProjectID" INTEGER NOT NULL,
    "PartID" INTEGER NOT NULL,
    PRIMARY KEY ("ProjectID", "PartID"),
    FOREIGN KEY ("ProjectID") REFERENCES "Project" ("ProjectID")
        ON DELETE CASCADE,
    FOREIGN KEY ("PartID") REFERENCES "Partner" ("PartID")
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS "Artist";
CREATE TABLE IF NOT EXISTS "Artist" (
    "ArtID" INTEGER NOT NULL,
    "Nickname" VARCHAR (50) NOT NULL,
    "Country" VARCHAR (50) NOT NULL,
    PRIMARY KEY ("ArtID")
);

DROP TABLE IF EXISTS "Role";
CREATE TABLE IF NOT EXISTS "Role" (
    "RoleID" INTEGER NOT NULL,
    "Description" VARCHAR(50) NOT NULL,
    PRIMARY KEY ("RoleID")
);

DROP TABLE IF EXISTS "Genre";
CREATE TABLE IF NOT EXISTS "Genre" (
    "GenreID" INTEGER NOT NULL,
    "Name" VARCHAR(50) NOT NULL,
    PRIMARY KEY ("GenreID")
);

DROP TABLE IF EXISTS "Plays";
CREATE TABLE IF NOT EXISTS "Plays" (
    "IndividID" INTEGER NOT NULL,
    "InstID" INTEGER NOT NULL,
    PRIMARY KEY ("IndividID", "InstID"),
    FOREIGN KEY ("IndividID") REFERENCES "Individual" ("IndividID")
        ON DELETE CASCADE,
    FOREIGN KEY ("InstID") REFERENCES "Instrument" ("InstID")
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS "Instrument";
CREATE TABLE IF NOT EXISTS "Instrument" (
    "InstID" INTEGER NOT NULL,
    "Name" VARCHAR(50) NOT NULL,
    PRIMARY KEY ("InstID")
);

DROP TABLE IF EXISTS "Release";
CREATE TABLE IF NOT EXISTS "Release" (
    "ArtID" INTEGER NOT NULL,
    "ProjectID" INTEGER NOT NULL,
    PRIMARY KEY ("ArtID", "ProjectID"),
    FOREIGN KEY ("ArtID") REFERENCES "Artist" ("ArtID")
        ON DELETE CASCADE,
    FOREIGN KEY ("ProjectID") REFERENCES "Project" ("ProjectID")
        ON DELETE CASCADE
);




-- Insert into User
INSERT INTO "User" ("UserID", "username", "password", "bool_admin")
VALUES
(1, 'user1', 'password1', FALSE),
(2, 'admin1', 'password2', TRUE);

-- Insert into Admin
INSERT INTO "Admin" ("AdminID", "UserID")
VALUES
(1, 2);

-- Insert into Contract
INSERT INTO "Contract" ("ContID", "Start_Date", "End_Date", "Salary")
VALUES
(1, '2024-01-01', '2024-12-31', 50000),
(2, '2024-06-01', '2025-05-31', 60000);

-- Insert into Artist
INSERT INTO "Artist" ("ArtID", "Nickname", "Country")
VALUES
(1, 'Artist1', 'USA'),
(2, 'Artist2', 'Canada');

-- Insert into Individual
INSERT INTO "Individual" ("IndividID", "First_name", "Last_name", "Country", "Age", "Phone", "Email", "UserID", "ContID", "ArtID")
VALUES
(1, 'John', 'Doe', 'USA', 25, '1234567890', 'johndoe@example.com', 1, 1, 1),
(2, 'Jane', 'Smith', 'Canada', 30, '0987654321', 'janesmith@example.com', 2, 2, 2);

-- Insert into Genre
INSERT INTO "Genre" ("GenreID", "Name")
VALUES
(1, 'Pop'),
(2, 'Rock');

-- Insert into Project
INSERT INTO "Project" ("ProjectID", "Release_Date", "ArtistID", "GenreID", "Title")
VALUES
(1, '2024-03-01', 1, 1, 'Album1'),
(2, '2024-08-01', 2, 2, 'Album2');

-- Insert into Song
INSERT INTO "Song" ("SongID", "ProjectID", "Duration", "Rating", "Plays")
VALUES
(1, 1, 240, 4.5, 1000),
(2, 2, 180, 4.0, 800);

-- Insert into Video
INSERT INTO "Video" ("VideoID", "ProjectID", "SongID", "Rating", "Views")
VALUES
(1, 1, 1, 4.5, 2000),
(2, 2, 2, 4.0, 1500);

-- Insert into Album
INSERT INTO "Album" ("AlbID", "ProjectID", "Rating")
VALUES
(1, 1, 4.5),
(2, 2, 4.0);

-- Insert into Format
INSERT INTO "Format" ("FormID")
VALUES
(1), (2), (3);

-- Insert into Releases_As
INSERT INTO "Releases_As" ("AlbID", "FormID")
VALUES
(1, 1),
(2, 2);

-- Insert into Vinyl
INSERT INTO "Vinyl" ("FormID", "Cost", "Sales")
VALUES
(1, 30.5, 500);

-- Insert into CD
INSERT INTO "CD" ("FormID", "Cost", "Sales")
VALUES
(2, 15.0, 800);

-- Insert into Digital
INSERT INTO "Digital" ("FormID", "Plays")
VALUES
(3, 10000);

-- Insert into Is_part_of
INSERT INTO "Is_part_of" ("SongID", "AlbID")
VALUES
(1, 1),
(2, 2);

-- Insert into Role
INSERT INTO "Role" ("RoleID", "Description")
VALUES
(1, 'Producer'),
(2, 'Composer');

-- Insert into Partner
INSERT INTO "Partner" ("PartID", "RoleID", "First_name", "Last_name")
VALUES
(1, 1, 'Alice', 'Johnson'),
(2, 2, 'Bob', 'Williams');

-- Insert into Works_on
INSERT INTO "Works_on" ("ProjectID", "PartID")
VALUES
(1, 1),
(2, 2);

-- Insert into Instrument
INSERT INTO "Instrument" ("InstID", "Name")
VALUES
(1, 'Guitar'),
(2, 'Piano');

-- Insert into Plays
INSERT INTO "Plays" ("IndividID", "InstID")
VALUES
(1, 1),
(2, 2);

-- Insert into Release
INSERT INTO "Release" ("ArtID", "ProjectID")
VALUES
(1, 1),
(2, 2);


COMMIT
