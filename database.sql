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
        ON UPDATE CASCADE,
    UNIQUE ("ArtID", "Title")
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
    "SongID" INTEGER DEFAULT NULL,
    "Rating" FLOAT DEFAULT 0,
    "Views" INTEGER DEFAULT 0,
    "Duration" INTEGER DEFAULT 0,
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
(7, 'sabrina', '1234', FALSE),
(8, 'weeknd', '1234', FALSE),
(9, 'admin', '1234', TRUE),
(10,'woodkid','1234',FALSE);



-- Insert into Admin
INSERT INTO "Admin" ("AdminID", "UserID")
VALUES
(1, 9);



-- Insert into Artist
INSERT INTO "Artist" ("ArtID", "Nickname", "Country they operate")
VALUES
(1, 'Imagine Dragons', 'USA'),
(2, 'Drake', 'Canada'),
(3, 'Kendrick Lamar', 'USA'),
(4, 'Sabrina Carpenter', 'USA'),
(5, 'The Weeknd', 'Canada'),
(6, 'Woodkid', 'France');

-- Insert into Individual
INSERT INTO "Individual" ("IndividID", "First_name", "Last_name", "Country born", "Age", "Phone", "Email", "UserID",  "ArtID")
VALUES
(1, 'Dan', 'Reynolds', 'USA', 35, '1234567890', 'dan@yahoo.com', 1, 1),
(2, 'Wayne', 'Sermon', 'USA', 30, '0987654321', 'wayne_sermons@yahoo.com', 2, 1),
(3, 'Ben', 'McKee', 'USA', 30, '0987654321', 'ben_mckee@yahoo.com', 3, 1),
(4, 'Daniel', 'Platzman', 'USA', 30, '0987654321', 'daniel_platzman@yahoo.com', 4, 1),
(5, 'Aubrey', 'Graham', 'Canada', 30, '0987654321', 'drake@yahoo.com', 5, 2),
(6, 'Kendrick', 'Duckworth', 'USA', 30, '0987654321', 'kendrick@yahoo.com', 6, 3),
(7, 'Sabrina', 'Carpenter', 'USA', 30, '0987654321', 'sabrinacarpenter@yahoo.com', 7, 4),
(8, 'Abel', 'Tesfaye', 'Canada', 30, '0987654321', 'theweeknd@yahoo.com', 8, 5),
(9, 'Yoann', 'Lemoine', 'Poland', 30, '0987654321', 'woodkid@yahoo.com', 10, 6);

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
(30,'2012-04-16', 3, 3, 'Poetic Justice (Song)'),
--sabrina
(31,'2022-05-15', 4, 1, 'Singular Act I (Album)'),
(32,'2022-05-15', 4, 1, 'Almost Love (Song)'),
(33,'2022-05-15', 4, 1, 'Almost Love (Video)'),
(34,'2022-05-15', 4, 1, 'Hold Tight (Song)'),
(35,'2022-05-15', 4, 1, 'Singular Act II (Album)'),
(36,'2022-05-15', 4, 1, 'In My Bed (Song)'),
(37,'2022-05-15', 4, 1, 'Pushing 20 (Song)'),
(38,'2022-05-15', 4, 1, 'Tell Em (Song)'),
(39,'2022-05-15', 4, 1, 'Tell Em (Video)'),
--weeknd
(40,'2020-05-20',5, 1, 'After Hours (Album)'),
(41,'2020-05-20',5, 1, 'Alone Again (Song)'),
(42,'2020-05-20',5, 1, 'Too Late (Song)'),
(43,'2020-05-20',5, 1, 'Snowchild (Song)'),
(44,'2020-05-20',5, 1, 'Snowchild (Video)'),
(45,'2022-11-20',5, 1, 'DawnFM (Album)'),
(46,'2022-11-20',5, 1, 'Take My Breath (Song)'),
(47,'2022-11-20',5, 1, 'Take My Breath (Video)'),
(48,'2022-11-20',5, 1, 'Out of Time (Song)'),
(49,'2022-11-20',5, 1, 'Best Friends (Song)'),
--woodkid
(50,'2020-03-30',6, 2, 'S16 (Album)'),
(51,'2020-03-30',6, 2, 'Goliath (Song))'),
(52,'2020-03-30',6, 2, 'Enemy (Song)'),
(53,'2020-03-30',6, 2, 'Shift (Song)'),
(54,'2013-07-15',6, 2, 'The Golden Age (Album)'),
(55,'2013-07-15',6, 2, 'The Golden Age (Song)'),
(56,'2013-07-15',6, 2, 'I Love You (Song)'),
(57,'2013-07-15',6, 2, 'Shadows (Song)');



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
--basically poetic song has kendrick ft drake
(3,30),
(2,30),
--
(4,31),
(4,32),
(4,33),
(4,34),
(4,35),
(4,36),
(4,37),
(4,38),
(4,39),
(5,40),
(5,41),
(5,42),
(5,43),
(5,44),
(5,45),
(5,46),
(5,47),
(5,48),
(5,49),
(6,50),
(6,51),
(6,52),
(6,53),
(6,54),
(6,55),
(6,56),
(6,57);



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
--ft drake
(19, 30,180, 1, 1100),
--sabrina
(20, 32,180, 1, 1100),
(21, 34,180, 1, 1100),
(22, 36,180, 1, 1100),
(23, 37,180, 1, 1100),
(24, 38,180, 1, 1100),
--weeknd
(25, 41,180, 1, 1100),
(26, 42,180, 1, 1100),
(27, 43,180, 1, 1100),
(28, 46,180, 1, 1100),
(29, 48,180, 1, 1100),
(30, 49,180, 1, 1100),
--woodkid
(31, 51,180, 1, 1100),
(32, 52,180, 1, 1100),
(33, 53,180, 1, 1100),
(34, 55,180, 1, 1100),
(35, 56,180, 1, 1100),
(36, 57,180, 1, 1100);

-- Insert into Video
INSERT INTO "Video" ("VideoID", "ProjectID", "SongID", "Rating", "Views","Duration")
VALUES
(1, 12, 8, 4.5, 2000,0),
(2, 16, 10, 4.0, 1500,0),
(3, 22, 14, 4.0, 1500,0),
(4, 27, 17, 4.0, 1500,0),
(5, 29, 18, 4.0, 1500,0),
(6, 33, 20, 4.0, 1500,0),
(7, 39, 24, 4.0, 1500,0),
(8, 44, 27, 4.0, 1500,0),
(9, 47, 28, 4.0, 1500,0);

-- Insert into Album
INSERT INTO "Album" ("AlbID", "ProjectID", "Rating")
VALUES
(1, 1, 1.5),
(2, 5, 2.0),
(3, 9, 3.0),
(4, 14, 4.0),
(5, 19, 4.5),
(6, 25, 5.0),
(7, 31, 5.0),
(8, 35, 5.0),
(9, 40, 5.0),
(10, 45, 5.0),
(11, 50, 5.0),
(12, 54, 5.0);

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
(4,2),
(5,2),
(6,2),
(7,3),
(8,3),
(9,3),
(10,4),
(11,4),
(12,4),
(13,5),
(14,5),
(15,5),
(16,5),
(17,6),
(18,6),
(20,7),
(21,7),
(22,8),
(23,8),
(24,8),
(25,9),
(26,9),
(27,9),
(28,10),
(29,10),
(30,10),
(31,11),
(32,11),
(33,11),
(34,12),
(35,12),
(36,12);


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
