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
        ON UPDATE CASCADE
);

DROP TABLE IF EXISTS "Individual";
CREATE TABLE IF NOT EXISTS "Individual" (
    "IndividID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "First_name" VARCHAR(25) DEFAULT '',
    "Last_name" VARCHAR(25) DEFAULT '',
    "Country born" VARCHAR(25) DEFAULT '',
    "Age" INTEGER DEFAULT 0,
    "Phone" VARCHAR(25) DEFAULT '',
    "Email" VARCHAR(25) DEFAULT '',
    "UserID" INTEGER NOT NULL,
    "ArtID" INTEGER NOT NULL,
    FOREIGN KEY ("UserID") REFERENCES "User" ("UserID")
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY ("ArtID") REFERENCES "Artist" ("ArtID")
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


DROP TABLE IF EXISTS "Project";
CREATE TABLE IF NOT EXISTS "Project" (
    "ProjectID" INTEGER NOT NULL,
    "Release_Date" DATE DEFAULT NULL,
    "ArtID" INTEGER NOT NULL,
    "GenreID" INTEGER NOT NULL,
    "Title" VARCHAR(50) DEFAULT '',
    PRIMARY KEY ("ProjectID"),
    FOREIGN KEY ("ArtID") REFERENCES "Artist" ("ArtID")
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY ("GenreID") REFERENCES "Genre" ("GenreID")
        ON DELETE CASCADE
        ON UPDATE CASCADE
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
        ON UPDATE CASCADE
);

DROP TABLE IF EXISTS "Is_part_of";
CREATE TABLE IF NOT EXISTS "Is_part_of" (
	"SongID" integer,
	"AlbID" integer,
	PRIMARY KEY ("SongID", "AlbID"),
	FOREIGN KEY ("SongID") REFERENCES "Song" ("SongID")
            ON DELETE CASCADE
            ON UPDATE CASCADE,
	FOREIGN KEY ("AlbID") REFERENCES "Album" ("AlbID")
            ON DELETE CASCADE
            ON UPDATE CASCADE
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
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY ("SongID") REFERENCES "Song" ("SongID")
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

DROP TABLE IF EXISTS "Album";
CREATE TABLE IF NOT EXISTS "Album" (
    "AlbID" INTEGER NOT NULL,
    "ProjectID" INTEGER NOT NULL,
    "Rating" FLOAT DEFAULT 0,
    PRIMARY KEY ("AlbID"),
    FOREIGN KEY ("ProjectID") REFERENCES "Project" ("ProjectID")
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


DROP TABLE IF EXISTS "Format";
CREATE TABLE IF NOT EXISTS "Format" (
    "FormID" INTEGER NOT NULL,
    "Description" VARCHAR(10) NOT NULL,
    PRIMARY KEY ("FormID")
);

DROP TABLE IF EXISTS "Vinyl";
CREATE TABLE IF NOT EXISTS "Vinyl" (
    "AlbID" INTEGER NOT NULL,
    "FormID" INTEGER NOT NULL,
    "Cost" FLOAT DEFAULT 0,
    "Sales" INTEGER DEFAULT 0,
    PRIMARY KEY ("AlbID","FormID"),
    FOREIGN KEY ("AlbID") REFERENCES "Album" ("AlbID")
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY ("FormID") REFERENCES "Format" ("FormID")
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

DROP TABLE IF EXISTS "CD";
CREATE TABLE IF NOT EXISTS "CD" (
    "AlbID" INTEGER NOT NULL,
    "FormID" INTEGER NOT NULL,
    "Cost" FLOAT DEFAULT 0,
    "Sales" INTEGER DEFAULT 0,
    PRIMARY KEY ("AlbID","FormID"),
    FOREIGN KEY ("AlbID") REFERENCES "Album" ("AlbID")
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY ("FormID") REFERENCES "Format" ("FormID")
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

DROP TABLE IF EXISTS "Digital";
CREATE TABLE IF NOT EXISTS "Digital" (
    "AlbID" INTEGER NOT NULL,
    "FormID" INTEGER NOT NULL,
    "Plays" INTEGER DEFAULT 0,
    PRIMARY KEY ("AlbID","FormID"),
    FOREIGN KEY ("AlbID") REFERENCES "Album" ("AlbID")
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY ("FormID") REFERENCES "Format" ("FormID")
        ON DELETE CASCADE
        ON UPDATE CASCADE
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
        ON UPDATE CASCADE
);

DROP TABLE IF EXISTS "Works_on";
CREATE TABLE IF NOT EXISTS "Works_on" (
    "ProjectID" INTEGER NOT NULL,
    "PartID" INTEGER NOT NULL,
    PRIMARY KEY ("ProjectID", "PartID"),
    FOREIGN KEY ("ProjectID") REFERENCES "Project" ("ProjectID")
        ON DELETE CASCADE
        ON UPDATE CASCADE
    FOREIGN KEY ("PartID") REFERENCES "Partner" ("PartID")
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

DROP TABLE IF EXISTS "Artist";
CREATE TABLE IF NOT EXISTS "Artist" (
    "ArtID" INTEGER NOT NULL,
    "Nickname" VARCHAR (50) NOT NULL,
    "Country they operate" VARCHAR (50) NOT NULL,
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
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY ("InstID") REFERENCES "Instrument" ("InstID")
        ON DELETE CASCADE
        ON UPDATE CASCADE
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
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY ("ProjectID") REFERENCES "Project" ("ProjectID")
        ON DELETE CASCADE
        ON UPDATE CASCADE
);




-- Insert into User
INSERT INTO "User" ("UserID", "username", "password", "bool_admin")
VALUES
(1, 'dan', '1234', FALSE),
(2, 'benmckee', '1234', FALSE),
(3, 'daniel', '1234', FALSE),
(4, 'waynesermon', '1234', FALSE),
(5, 'drake', '1234', FALSE),
(6, 'kendrick', '1234', FALSE),
(7, 'jcole', '1234', FALSE),
(8, 'weekend', '1234', FALSE),
(9, 'admin1', '1234', TRUE),
(10, 'admin2', '1234', TRUE);


-- Insert into Admin
INSERT INTO "Admin" ("AdminID", "UserID")
VALUES
(1, 9),
(2, 10);


-- Insert into Artist
INSERT INTO "Artist" ("ArtID", "Nickname", "Country they operate")
VALUES
(1, 'Imagine Dragons', 'USA'),
(2, 'Drake', 'Canada'),
(3, 'Kendrick Lamar', 'USA'),
(4, 'J. Cole', 'USA'),
(5, 'The Weekend', 'Canada');

-- Insert into Individual
INSERT INTO "Individual" ("IndividID", "First_name", "Last_name", "Country born", "Age", "Phone", "Email", "UserID",  "ArtID")
VALUES
(1, 'Dan', 'Reynolds', 'USA', 35, '1234567890', 'dan@yahoo.com', 1, 1),
(2, 'Wayne', 'Sermon', 'USA', 30, '0987654321', 'wayne_sermons@yahoo.com', 2, 1),
(3, 'Ben', 'McKee', 'USA', 30, '0987654321', 'ben_mckee@yahoo.com', 3, 1),
(4, 'Daniel', 'Platzman', 'USA', 30, '0987654321', 'daniel_platzman@yahoo.com', 4, 1),
(5, 'Aubrey', 'Graham', 'Canada', 30, '0987654321', 'drake@yahoo.com', 5, 2),
(6, 'Kendrick', 'Duckworth', 'USA', 30, '0987654321', 'kendrick@yahoo.com', 6, 3),
(7, 'Jermaine', 'Cole', 'USA', 30, '0987654321', 'jcole@yahoo.com', 7, 4),
(8, 'Abel', 'Tesfaye', 'Canada', 30, '0987654321', 'theweekend@yahoo.com', 8, 5);

-- Insert into Genre
INSERT INTO "Genre" ("GenreID", "Name")
VALUES
(1, 'Pop'),
(2, 'Rock'),
(3, 'Rap');

-- Insert into Project
INSERT INTO "Project" ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title")
VALUES
--imagine dragons
(1, '2024-03-01', 1, 2, 'LOOM (Album)'),
(2, '2024-03-01', 1, 2, 'Wake up (Song)'),
(3, '2024-03-01', 1, 2, 'Nice to Meet You (Song)'),
(4, '2024-03-01', 1, 2, 'Eyes Closed (Song)'),
(5, '2022-04-20', 1, 2, 'Mercury (Album)'),
(6, '2022-04-20', 1, 2, 'My Life (Song)'),
(7,'2022-04-20', 1, 2, 'Lonely (Song)'),
(8,'2022-04-20', 1, 2, 'Wrecked (Song)'),
--drake
(9,'2024-08-01', 2, 3, 'For All the Dogs (Album)'),
(10,'2024-08-01', 2, 3, 'Amen (Song)'),
(11,'2024-08-01', 2, 3, 'First Person Shooter (Song)'),
(12,'2024-08-10', 2, 3, 'First Person Shooter (Video)'),
(13,'2024-08-01', 2, 3, 'Tried Our Best (Song)'),
(14,'2022-03-25', 2, 3, 'Her Loss (Album)'),
(15,'2022-03-25', 2, 3, 'Rich Flex (Song)'),
(16,'2022-03-30', 2, 3, 'Rich Flex (Video)'),
(17,'2022-03-25', 2, 3, 'Major Distribution (Song)'),
(18,'2022-03-25', 2, 3, 'Broke Boys (Song)'),
--kendrick
(19,'2024-11-25', 3, 3, 'GNX (Album)'),
(20,'2024-11-25', 3, 3, 'reincarnated (Song)'),
(21,'2024-11-25', 3, 3, 'squabble up (Song)'),
(22,'2024-11-28', 3, 3, 'squabble up (Video)'),
(23,'2024-11-25', 3, 3, 'man at the garden (Song)'),
(24,'2024-11-25', 3, 3, 'wacced out murals (Song)'),
(25,'2017-02-11', 3, 3, 'DAMN (Album)'),
(26,'2017-02-11', 3, 3, 'DNA (Song)'),
(27,'2017-02-11', 3, 3, 'DNA (Video)'),
(28,'2017-02-11', 3, 3, 'Pride (Song)'),
(29,'2017-02-11', 3, 3, 'Pride (Video)'),
--ft drake
(30,'2012-04-16', 3, 3, 'Poetic Justice (Song)');



-- Insert into Release
INSERT INTO "Release" ("ArtID", "ProjectID")
VALUES
(1, 1),
(1, 2),
(1, 3),
(1, 4),
(1, 5),
(1, 6),
(1, 7),
(1, 8),
(2, 9),
(2,10),
(2,11),
(2,12),
(2,13),
(2,14),
(2,15),
(2,16),
(2,17),
(2,18),
(3,19),
(3,20),
(3,21),
(3,22),
(3,23),
(3,24),
(3,25),
(3,26),
(3,27),
(3,28),
(3,29),
(3,30),
(2,30);

-- Insert into Song
INSERT INTO "Song" ("SongID", "ProjectID", "Duration", "Rating", "Plays")
VALUES
(1, 2, 240, 1, 100),
(2, 3, 180, 2, 200),
(3, 4, 180, 3, 300),
(4, 6, 180, 4, 400),
(5, 7, 180, 5, 500),
(6, 8, 180, 1, 600),
--drake
(7, 10, 180, 2, 700),
(8, 11, 180, 3, 800),
(9, 13,180, 4, 900),
(10, 15,180, 5, 1000),
(11, 17,180, 1, 1100),
(12, 18,180, 1, 1100),
--kendrick
(13, 20,180, 1, 1100),
(14, 21,180, 1, 1100),
(15, 23,180, 1, 1100),
(16, 24,180, 1, 1100),
(17, 26,180, 1, 1100),
(18, 28,180, 1, 1100),
--solo
(19, 30,180, 1, 1100);

-- Insert into Video
INSERT INTO "Video" ("VideoID", "ProjectID", "SongID", "Rating", "Views")
VALUES
(1, 12, 8, 4.5, 2000),
(2, 16, 10, 4.0, 1500),
(3, 22, 14, 4.0, 1500),
(4, 27, 17, 4.0, 1500),
(5, 29, 18, 4.0, 1500);

-- Insert into Album
INSERT INTO "Album" ("AlbID", "ProjectID", "Rating")
VALUES
(1, 1, 1.5),
(2, 5, 2.0),
(3, 9, 3.0),
(4, 14, 4.0),
(5, 19, 4.5),
(6, 25, 5.0);

-- Insert into Format
INSERT INTO "Format" ("FormID","Description")
VALUES
(1,"Vinyl"), 
(2,"CD"), 
(3,"Digital");



INSERT INTO "Is_part_of" ("SongID","AlbID")
VALUES
(1,1),
(2,1),
(3,1),
(4,1),
(5,1),
(6,1),
(7,2),
(8,2),
(9,2),
(10,2),
(11,2),
(12,2),
(13,3),
(14,3),
(15,3),
(16,3),
(17,3),
(18,3);

-- Insert into Vinyl
INSERT INTO "Vinyl" ("AlbID","FormID", "Cost", "Sales")
VALUES
(1,1, 15, 500),
(2,1, 15, 500);

-- Insert into CD
INSERT INTO "CD" ("AlbID","FormID", "Cost", "Sales")
VALUES
(1,2, 5.0, 100),
(2,2, 5.0, 200),
(3,2, 5.0, 300),
(4,2, 5.0, 400),
(5,2, 5.0, 500),
(6,2, 15.0, 600);

-- Insert into Digital
INSERT INTO "Digital" ("AlbID","FormID", "Plays")
VALUES
(1,3, 10000),
(2,3, 10000),
(3,3, 10000),
(4,3, 10000),
(5,3, 10000),
(6,3, 10000);


-- Insert into Role
INSERT INTO "Role" ("RoleID", "Description")
VALUES
(1, 'Producer'),
(2, 'Composer'),
(3, 'Video Director'),
(4, 'Lyricist');

-- Insert into Partner
INSERT INTO "Partner" ("PartID", "RoleID", "First_name", "Last_name")
VALUES
(1, 1, 'Alice', 'Producer1'),
(2, 1, 'Bob', 'Producer2'),
(3, 2, 'Bob', 'Composer1'),
(4, 2, 'Bob', 'Composer2'),
(5, 3, 'Bob', 'Video Director1'),
(6, 3, 'Bob', 'Video Director2'),
(7, 4, 'Bob', 'Lyricist1'),
(8, 4, 'Bob', 'Lyricist2');

-- Insert into Works_on
INSERT INTO "Works_on" ("ProjectID", "PartID")
VALUES
(1, 1),
(2, 2);

-- Insert into Instrument
INSERT INTO "Instrument" ("InstID", "Name")
VALUES
(1, 'Vocals'),
(2, 'Piano'),
(3, 'Drums'),
(4, 'Guitar'),
(5, 'Base');

-- Insert into Plays
INSERT INTO "Plays" ("IndividID", "InstID")
VALUES
(1, 1),
(2, 2);


COMMIT
