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
INSERT INTO User ("UserID", "username", "password", "bool_admin") VALUES ('1', 'dan', '1234', '0');
INSERT INTO User ("UserID", "username", "password", "bool_admin") VALUES ('2', 'benmckee', '1234', '0');
INSERT INTO User ("UserID", "username", "password", "bool_admin") VALUES ('3', 'daniel', '1234', '0');
INSERT INTO User ("UserID", "username", "password", "bool_admin") VALUES ('4', 'waynesermon', '1234', '0');
INSERT INTO User ("UserID", "username", "password", "bool_admin") VALUES ('5', 'drake', '1234', '0');
INSERT INTO User ("UserID", "username", "password", "bool_admin") VALUES ('6', 'kendrick', '1234', '0');
INSERT INTO User ("UserID", "username", "password", "bool_admin") VALUES ('7', 'sabrina', '1234', '0');
INSERT INTO User ("UserID", "username", "password", "bool_admin") VALUES ('8', 'weeknd', '1234', '0');
INSERT INTO User ("UserID", "username", "password", "bool_admin") VALUES ('9', 'admin', '1234', '1');
INSERT INTO User ("UserID", "username", "password", "bool_admin") VALUES ('10', 'woodkid', '1234', '0');

-- Inserts for table Admin
INSERT INTO Admin (AdminID, "UserID") VALUES ('1', '9');

-- Inserts for table Individual
INSERT INTO Individual ("IndividID", "First_Name", "Last_Name", "Country born", "Age", "Phone", "Email", "UserID", "ArtID") VALUES ('1', 'Dan', 'Reynolds', 'USA', '35', '1234567890', 'dan@yahoo.com', '1', '1');
INSERT INTO Individual ("IndividID", "First_Name", "Last_Name", "Country born", "Age", "Phone", "Email", "UserID", "ArtID") VALUES ('2', 'Wayne', 'Sermon', 'USA', '30', '0987654321', 'wayne_sermons@yahoo.com', '2', '1');
INSERT INTO Individual ("IndividID", "First_Name", "Last_Name", "Country born", "Age", "Phone", "Email", "UserID", "ArtID") VALUES ('3', 'Ben', 'McKee', 'USA', '30', '0987654321', 'ben_mckee@yahoo.com', '3', '1');
INSERT INTO Individual ("IndividID", "First_Name", "Last_Name", "Country born", "Age", "Phone", "Email", "UserID", "ArtID") VALUES ('4', 'Daniel', 'Platzman', 'USA', '30', '0987654321', 'daniel_platzman@yahoo.com', '4', '1');
INSERT INTO Individual ("IndividID", "First_Name", "Last_Name", "Country born", "Age", "Phone", "Email", "UserID", "ArtID") VALUES ('5', 'Aubrey', 'Graham', 'Canada', '30', '0987654321', 'drake@yahoo.com', '5', '2');
INSERT INTO Individual ("IndividID", "First_Name", "Last_Name", "Country born", "Age", "Phone", "Email", "UserID", "ArtID") VALUES ('6', 'Kendrick', 'Duckworth', 'USA', '30', '0987654321', 'kendrick@yahoo.com', '6', '3');
INSERT INTO Individual ("IndividID", "First_Name", "Last_Name", "Country born", "Age", "Phone", "Email", "UserID", "ArtID") VALUES ('7', 'Sabrina', 'Carpenter', 'USA', '30', '0987654321', 'sabrinacarpenter@yahoo.com', '7', '4');
INSERT INTO Individual ("IndividID", "First_Name", "Last_Name", "Country born", "Age", "Phone", "Email", "UserID", "ArtID") VALUES ('8', 'Abel', 'Tesfaye', 'Canada', '30', '0987654321', 'theweeknd@yahoo.com', '8', '5');
INSERT INTO Individual ("IndividID", "First_Name", "Last_Name", "Country born", "Age", "Phone", "Email", "UserID", "ArtID") VALUES ('9', 'Yoann', 'Lemoine', 'Poland', '30', '0987654321', 'woodkid@yahoo.com', '10', '6');

-- Inserts for table Project
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('1', '2024-03-01', '1', '2', 'LOOM (Album)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('2', '2024-03-01', '1', '2', 'Wake up (Song)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('3', '2024-03-01', '1', '2', 'Nice to Meet You (Song)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('4', '2024-03-01', '1', '2', 'Eyes Closed (Song)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('5', '2022-04-20', '1', '2', 'Mercury (Album)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('6', '2022-04-20', '1', '2', 'My Life (Song)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('7', '2022-04-20', '1', '2', 'Lonely (Song)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('8', '2022-04-20', '1', '2', 'Wrecked (Song)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('9', '2024-08-01', '2', '3', 'For All the Dogs (Album)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('10', '2024-08-01', '2', '3', 'Amen (Song)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('11', '2024-08-01', '2', '3', 'First Person Shooter (Song)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('12', '2024-08-10', '2', '3', 'First Person Shooter (Video)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('13', '2024-08-01', '2', '3', 'Tried Our Best (Song)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('14', '2022-03-25', '2', '3', 'Her Loss (Album)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('15', '2022-03-25', '2', '3', 'Rich Flex (Song)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('16', '2022-03-30', '2', '3', 'Rich Flex (Video)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('17', '2022-03-25', '2', '3', 'Major Distribution (Song)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('18', '2022-03-25', '2', '3', 'Broke Boys (Song)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('19', '2024-11-25', '3', '3', 'GNX (Album)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('20', '2024-11-25', '3', '3', 'reincarnated (Song)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('21', '2024-11-25', '3', '3', 'squabble up (Song)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('22', '2024-11-28', '3', '3', 'squabble up (Video)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('23', '2024-11-25', '3', '3', 'man at the garden (Song)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('24', '2024-11-25', '3', '3', 'wacced out murals (Song)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('25', '2017-02-11', '3', '3', 'DAMN (Album)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('26', '2017-02-11', '3', '3', 'DNA (Song)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('27', '2017-02-11', '3', '3', 'DNA (Video)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('28', '2017-02-11', '3', '3', 'Pride (Song)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('29', '2017-02-11', '3', '3', 'Pride (Video)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('30', '2012-04-16', '3', '3', 'Poetic Justice (Song)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('31', '2022-05-15', '4', '1', 'Singular Act I (Album)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('32', '2022-05-15', '4', '1', 'Almost Love (Song)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('33', '2022-05-15', '4', '1', 'Almost Love (Video)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('34', '2022-05-15', '4', '1', 'Hold Tight (Song)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('35', '2022-05-15', '4', '1', 'Singular Act II (Album)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('36', '2022-05-15', '4', '1', 'In My Bed (Song)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('37', '2022-05-15', '4', '1', 'Pushing 20 (Song)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('38', '2022-05-15', '4', '1', 'Tell Em (Song)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('39', '2022-05-15', '4', '1', 'Tell Em (Video)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('40', '2020-05-20', '5', '1', 'After Hours (Album)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('41', '2020-05-20', '5', '1', 'Alone Again (Song)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('42', '2020-05-20', '5', '1', 'Too Late (Song)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('43', '2020-05-20', '5', '1', 'Snowchild (Song)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('44', '2020-05-20', '5', '1', 'Snowchild (Video)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('45', '2022-11-20', '5', '1', 'DawnFM (Album)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('46', '2022-11-20', '5', '1', 'Take My Breath (Song)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('47', '2022-11-20', '5', '1', 'Take My Breath (Video)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('48', '2022-11-20', '5', '1', 'Out of Time (Song)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('49', '2022-11-20', '5', '1', 'Best Friends (Song)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('50', '2020-03-30', '6', '2', 'S16 (Album)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('51', '2020-03-30', '6', '2', 'Goliath (Song))');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('52', '2020-03-30', '6', '2', 'Enemy (Song)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('53', '2020-03-30', '6', '2', 'Shift (Song)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('54', '2013-07-15', '6', '2', 'The Golden "Age" (Album)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('55', '2013-07-15', '6', '2', 'The Golden "Age" (Song)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('56', '2013-07-15', '6', '2', 'I Love You (Song)');
INSERT INTO Project ("ProjectID", "Release_Date", "ArtID", "GenreID", "Title") VALUES ('57', '2013-07-15', '6', '2', 'Shadows (Song)');

-- Inserts for table Song
INSERT INTO Song ("SongID", "ProjectID", "Duration", "Rating", "Plays") VALUES ('1', '2', '240', '1.0', '100');
INSERT INTO Song ("SongID", "ProjectID", "Duration", "Rating", "Plays") VALUES ('2', '3', '180', '2.0', '200');
INSERT INTO Song ("SongID", "ProjectID", "Duration", "Rating", "Plays") VALUES ('3', '4', '180', '3.0', '300');
INSERT INTO Song ("SongID", "ProjectID", "Duration", "Rating", "Plays") VALUES ('4', '6', '180', '4.0', '400');
INSERT INTO Song ("SongID", "ProjectID", "Duration", "Rating", "Plays") VALUES ('5', '7', '180', '5.0', '500');
INSERT INTO Song ("SongID", "ProjectID", "Duration", "Rating", "Plays") VALUES ('6', '8', '180', '1.0', '600');
INSERT INTO Song ("SongID", "ProjectID", "Duration", "Rating", "Plays") VALUES ('7', '10', '180', '2.0', '700');
INSERT INTO Song ("SongID", "ProjectID", "Duration", "Rating", "Plays") VALUES ('8', '11', '180', '3.0', '800');
INSERT INTO Song ("SongID", "ProjectID", "Duration", "Rating", "Plays") VALUES ('9', '13', '180', '4.0', '900');
INSERT INTO Song ("SongID", "ProjectID", "Duration", "Rating", "Plays") VALUES ('10', '15', '180', '5.0', '1000');
INSERT INTO Song ("SongID", "ProjectID", "Duration", "Rating", "Plays") VALUES ('11', '17', '180', '1.0', '1100');
INSERT INTO Song ("SongID", "ProjectID", "Duration", "Rating", "Plays") VALUES ('12', '18', '180', '1.0', '1100');
INSERT INTO Song ("SongID", "ProjectID", "Duration", "Rating", "Plays") VALUES ('13', '20', '180', '1.0', '1100');
INSERT INTO Song ("SongID", "ProjectID", "Duration", "Rating", "Plays") VALUES ('14', '21', '180', '1.0', '1100');
INSERT INTO Song ("SongID", "ProjectID", "Duration", "Rating", "Plays") VALUES ('15', '23', '180', '1.0', '1100');
INSERT INTO Song ("SongID", "ProjectID", "Duration", "Rating", "Plays") VALUES ('16', '24', '180', '1.0', '1100');
INSERT INTO Song ("SongID", "ProjectID", "Duration", "Rating", "Plays") VALUES ('17', '26', '180', '1.0', '1100');
INSERT INTO Song ("SongID", "ProjectID", "Duration", "Rating", "Plays") VALUES ('18', '28', '180', '1.0', '1100');
INSERT INTO Song ("SongID", "ProjectID", "Duration", "Rating", "Plays") VALUES ('19', '30', '180', '1.0', '1100');
INSERT INTO Song ("SongID", "ProjectID", "Duration", "Rating", "Plays") VALUES ('20', '32', '180', '1.0', '1100');
INSERT INTO Song ("SongID", "ProjectID", "Duration", "Rating", "Plays") VALUES ('21', '34', '180', '1.0', '1100');
INSERT INTO Song ("SongID", "ProjectID", "Duration", "Rating", "Plays") VALUES ('22', '36', '180', '1.0', '1100');
INSERT INTO Song ("SongID", "ProjectID", "Duration", "Rating", "Plays") VALUES ('23', '37', '180', '1.0', '1100');
INSERT INTO Song ("SongID", "ProjectID", "Duration", "Rating", "Plays") VALUES ('24', '38', '180', '1.0', '1100');
INSERT INTO Song ("SongID", "ProjectID", "Duration", "Rating", "Plays") VALUES ('25', '41', '180', '1.0', '1100');
INSERT INTO Song ("SongID", "ProjectID", "Duration", "Rating", "Plays") VALUES ('26', '42', '180', '1.0', '1100');
INSERT INTO Song ("SongID", "ProjectID", "Duration", "Rating", "Plays") VALUES ('27', '43', '180', '1.0', '1100');
INSERT INTO Song ("SongID", "ProjectID", "Duration", "Rating", "Plays") VALUES ('28', '46', '180', '1.0', '1100');
INSERT INTO Song ("SongID", "ProjectID", "Duration", "Rating", "Plays") VALUES ('29', '48', '180', '1.0', '1100');
INSERT INTO Song ("SongID", "ProjectID", "Duration", "Rating", "Plays") VALUES ('30', '49', '180', '1.0', '1100');
INSERT INTO Song ("SongID", "ProjectID", "Duration", "Rating", "Plays") VALUES ('31', '51', '180', '1.0', '1100');
INSERT INTO Song ("SongID", "ProjectID", "Duration", "Rating", "Plays") VALUES ('32', '52', '180', '1.0', '1100');
INSERT INTO Song ("SongID", "ProjectID", "Duration", "Rating", "Plays") VALUES ('33', '53', '180', '1.0', '1100');
INSERT INTO Song ("SongID", "ProjectID", "Duration", "Rating", "Plays") VALUES ('34', '55', '180', '1.0', '1100');
INSERT INTO Song ("SongID", "ProjectID", "Duration", "Rating", "Plays") VALUES ('35', '56', '180', '1.0', '1100');
INSERT INTO Song ("SongID", "ProjectID", "Duration", "Rating", "Plays") VALUES ('36', '57', '180', '1.0', '1100');

-- Inserts for table Is_part_of
INSERT INTO Is_part_of ("SongID", "AlbID") VALUES ('1', '1');
INSERT INTO Is_part_of ("SongID", "AlbID") VALUES ('2', '1');
INSERT INTO Is_part_of ("SongID", "AlbID") VALUES ('3', '1');
INSERT INTO Is_part_of ("SongID", "AlbID") VALUES ('4', '2');
INSERT INTO Is_part_of ("SongID", "AlbID") VALUES ('5', '2');
INSERT INTO Is_part_of ("SongID", "AlbID") VALUES ('6', '2');
INSERT INTO Is_part_of ("SongID", "AlbID") VALUES ('7', '3');
INSERT INTO Is_part_of ("SongID", "AlbID") VALUES ('8', '3');
INSERT INTO Is_part_of ("SongID", "AlbID") VALUES ('9', '3');
INSERT INTO Is_part_of ("SongID", "AlbID") VALUES ('10', '4');
INSERT INTO Is_part_of ("SongID", "AlbID") VALUES ('11', '4');
INSERT INTO Is_part_of ("SongID", "AlbID") VALUES ('12', '4');
INSERT INTO Is_part_of ("SongID", "AlbID") VALUES ('13', '5');
INSERT INTO Is_part_of ("SongID", "AlbID") VALUES ('14', '5');
INSERT INTO Is_part_of ("SongID", "AlbID") VALUES ('15', '5');
INSERT INTO Is_part_of ("SongID", "AlbID") VALUES ('16', '5');
INSERT INTO Is_part_of ("SongID", "AlbID") VALUES ('17', '6');
INSERT INTO Is_part_of ("SongID", "AlbID") VALUES ('18', '6');
INSERT INTO Is_part_of ("SongID", "AlbID") VALUES ('20', '7');
INSERT INTO Is_part_of ("SongID", "AlbID") VALUES ('21', '7');
INSERT INTO Is_part_of ("SongID", "AlbID") VALUES ('22', '8');
INSERT INTO Is_part_of ("SongID", "AlbID") VALUES ('23', '8');
INSERT INTO Is_part_of ("SongID", "AlbID") VALUES ('24', '8');
INSERT INTO Is_part_of ("SongID", "AlbID") VALUES ('25', '9');
INSERT INTO Is_part_of ("SongID", "AlbID") VALUES ('26', '9');
INSERT INTO Is_part_of ("SongID", "AlbID") VALUES ('27', '9');
INSERT INTO Is_part_of ("SongID", "AlbID") VALUES ('28', '10');
INSERT INTO Is_part_of ("SongID", "AlbID") VALUES ('29', '10');
INSERT INTO Is_part_of ("SongID", "AlbID") VALUES ('30', '10');
INSERT INTO Is_part_of ("SongID", "AlbID") VALUES ('31', '11');
INSERT INTO Is_part_of ("SongID", "AlbID") VALUES ('32', '11');
INSERT INTO Is_part_of ("SongID", "AlbID") VALUES ('33', '11');
INSERT INTO Is_part_of ("SongID", "AlbID") VALUES ('34', '12');
INSERT INTO Is_part_of ("SongID", "AlbID") VALUES ('35', '12');
INSERT INTO Is_part_of ("SongID", "AlbID") VALUES ('36', '12');

-- Inserts for table Video
INSERT INTO Video ("VideoID", "ProjectID", "SongID", "Rating", "Views", "Duration") VALUES ('1', '12', '8', '4.5', '2000', '0');
INSERT INTO Video ("VideoID", "ProjectID", "SongID", "Rating", "Views", "Duration") VALUES ('2', '16', '10', '4.0', '1500', '0');
INSERT INTO Video ("VideoID", "ProjectID", "SongID", "Rating", "Views", "Duration") VALUES ('3', '22', '14', '4.0', '1500', '0');
INSERT INTO Video ("VideoID", "ProjectID", "SongID", "Rating", "Views", "Duration") VALUES ('4', '27', '17', '4.0', '1500', '0');
INSERT INTO Video ("VideoID", "ProjectID", "SongID", "Rating", "Views", "Duration") VALUES ('5', '29', '18', '4.0', '1500', '0');
INSERT INTO Video ("VideoID", "ProjectID", "SongID", "Rating", "Views", "Duration") VALUES ('6', '33', '20', '4.0', '1500', '0');
INSERT INTO Video ("VideoID", "ProjectID", "SongID", "Rating", "Views", "Duration") VALUES ('7', '39', '24', '4.0', '1500', '0');
INSERT INTO Video ("VideoID", "ProjectID", "SongID", "Rating", "Views", "Duration") VALUES ('8', '44', '27', '4.0', '1500', '0');
INSERT INTO Video ("VideoID", "ProjectID", "SongID", "Rating", "Views", "Duration") VALUES ('9', '47', '28', '4.0', '1500', '0');

-- Inserts for table Album
INSERT INTO Album ("AlbID", "ProjectID", "Rating") VALUES ('1', '1', '1.5');
INSERT INTO Album ("AlbID", "ProjectID", "Rating") VALUES ('2', '5', '2.0');
INSERT INTO Album ("AlbID", "ProjectID", "Rating") VALUES ('3', '9', '3.0');
INSERT INTO Album ("AlbID", "ProjectID", "Rating") VALUES ('4', '14', '4.0');
INSERT INTO Album ("AlbID", "ProjectID", "Rating") VALUES ('5', '19', '4.5');
INSERT INTO Album ("AlbID", "ProjectID", "Rating") VALUES ('6', '25', '5.0');
INSERT INTO Album ("AlbID", "ProjectID", "Rating") VALUES ('7', '31', '5.0');
INSERT INTO Album ("AlbID", "ProjectID", "Rating") VALUES ('8', '35', '5.0');
INSERT INTO Album ("AlbID", "ProjectID", "Rating") VALUES ('9', '40', '5.0');
INSERT INTO Album ("AlbID", "ProjectID", "Rating") VALUES ('10', '45', '5.0');
INSERT INTO Album ("AlbID", "ProjectID", "Rating") VALUES ('11', '50', '5.0');
INSERT INTO Album ("AlbID", "ProjectID", "Rating") VALUES ('12', '54', '5.0');

-- Inserts for table Format
INSERT INTO Format ("FormID", "Description") VALUES ('1', 'Vinyl');
INSERT INTO Format ("FormID", "Description") VALUES ('2', 'CD');
INSERT INTO Format ("FormID", "Description") VALUES ('3', 'Digital');

-- Inserts for table Vinyl
INSERT INTO Vinyl ("AlbID", "FormID", "Cost", "Sales") VALUES ('1', '1', '15.0', '500');
INSERT INTO Vinyl ("AlbID", "FormID", "Cost", "Sales") VALUES ('2', '1', '15.0', '500');

-- Inserts for table CD
INSERT INTO CD ("AlbID", "FormID", "Cost", "Sales") VALUES ('1', '2', '5.0', '100');
INSERT INTO CD ("AlbID", "FormID", "Cost", "Sales") VALUES ('2', '2', '5.0', '200');
INSERT INTO CD ("AlbID", "FormID", "Cost", "Sales") VALUES ('3', '2', '5.0', '300');
INSERT INTO CD ("AlbID", "FormID", "Cost", "Sales") VALUES ('4', '2', '5.0', '400');
INSERT INTO CD ("AlbID", "FormID", "Cost", "Sales") VALUES ('5', '2', '5.0', '500');
INSERT INTO CD ("AlbID", "FormID", "Cost", "Sales") VALUES ('6', '2', '15.0', '600');

-- Inserts for table Digital
INSERT INTO Digital ("AlbID", "FormID", "Plays") VALUES ('1', '3', '10000');
INSERT INTO Digital ("AlbID", "FormID", "Plays") VALUES ('2', '3', '10000');
INSERT INTO Digital ("AlbID", "FormID", "Plays") VALUES ('3', '3', '10000');
INSERT INTO Digital ("AlbID", "FormID", "Plays") VALUES ('4', '3', '10000');
INSERT INTO Digital ("AlbID", "FormID", "Plays") VALUES ('5', '3', '10000');
INSERT INTO Digital ("AlbID", "FormID", "Plays") VALUES ('6', '3', '10000');

-- Inserts for table Partner
INSERT INTO Partner ("PartID", "RoleID", "First_Name", "Last_Name") VALUES ('1', '1', 'Alice', 'Producer1');
INSERT INTO Partner ("PartID", "RoleID", "First_Name", "Last_Name") VALUES ('2', '1', 'Bob', 'Producer2');
INSERT INTO Partner ("PartID", "RoleID", "First_Name", "Last_Name") VALUES ('3', '2', 'Bob', 'Composer1');
INSERT INTO Partner ("PartID", "RoleID", "First_Name", "Last_Name") VALUES ('4', '2', 'Bob', 'Composer2');
INSERT INTO Partner ("PartID", "RoleID", "First_Name", "Last_Name") VALUES ('5', '3', 'Bob', 'Video Director1');
INSERT INTO Partner ("PartID", "RoleID", "First_Name", "Last_Name") VALUES ('6', '3', 'Bob', 'Video Director2');
INSERT INTO Partner ("PartID", "RoleID", "First_Name", "Last_Name") VALUES ('7', '4', 'Bob', 'Lyricist1');
INSERT INTO Partner ("PartID", "RoleID", "First_Name", "Last_Name") VALUES ('8', '4', 'Bob', 'Lyricist2');

-- Inserts for table Works_on
INSERT INTO Works_on ("ProjectID", "PartID") VALUES ('1', '1');
INSERT INTO Works_on ("ProjectID", "PartID") VALUES ('2', '2');

-- Inserts for table Artist
INSERT INTO Artist ("ArtID", "Nickname", "Country they operate") VALUES ('1', 'Imagine Dragons', 'USA');
INSERT INTO Artist ("ArtID", "Nickname", "Country they operate") VALUES ('2', 'Drake', 'Canada');
INSERT INTO Artist ("ArtID", "Nickname", "Country they operate") VALUES ('3', 'Kendrick Lamar', 'USA');
INSERT INTO Artist ("ArtID", "Nickname", "Country they operate") VALUES ('4', 'Sabrina Carpenter', 'USA');
INSERT INTO Artist ("ArtID", "Nickname", "Country they operate") VALUES ('5', 'The Weeknd', 'Canada');
INSERT INTO Artist ("ArtID","Nickname", "Country they operate") VALUES ('6', 'Woodkid', 'France');

-- Inserts for table Role
INSERT INTO Role ("RoleID", "Description") VALUES ('1', 'Producer');
INSERT INTO Role ("RoleID", "Description") VALUES ('2', 'Composer');
INSERT INTO Role ("RoleID", "Description") VALUES ('3', 'Video Director');
INSERT INTO Role ("RoleID", "Description") VALUES ('4', 'Lyricist');

-- Inserts for table Genre
INSERT INTO Genre ("GenreID", "Name") VALUES ('1', 'Pop');
INSERT INTO Genre ("GenreID", "Name") VALUES ('2', 'Rock');
INSERT INTO Genre ("GenreID", "Name") VALUES ('3', 'Rap');

-- Inserts for table "Plays"
INSERT INTO "Plays" ("IndividID", "InstID") VALUES ('1', '1');
INSERT INTO "Plays" ("IndividID", "InstID") VALUES ('2', '2');

-- Inserts for table Instrument
INSERT INTO Instrument ("InstID", "Name") VALUES ('1', 'Vocals');
INSERT INTO Instrument ("InstID", "Name") VALUES ('2', 'Piano');
INSERT INTO Instrument ("InstID", "Name") VALUES ('3', 'Drums');
INSERT INTO Instrument ("InstID", "Name") VALUES ('4', 'Guitar');
INSERT INTO Instrument ("InstID", "Name") VALUES ('5', 'Base');

-- Inserts for table Release
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('1', '1');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('1', '2');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('1', '3');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('1', '4');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('1', '5');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('1', '6');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('1', '7');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('1', '8');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('2', '9');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('2', '10');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('2', '11');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('2', '12');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('2', '13');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('2', '14');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('2', '15');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('2', '16');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('2', '17');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('2', '18');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('3', '19');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('3', '20');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('3', '21');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('3', '22');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('3', '23');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('3', '24');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('3', '25');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('3', '26');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('3', '27');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('3', '28');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('3', '29');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('3', '30');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('2', '30');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('4', '31');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('4', '32');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('4', '33');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('4', '34');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('4', '35');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('4', '36');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('4', '37');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('4', '38');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('4', '39');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('5', '40');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('5', '41');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('5', '42');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('5', '43');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('5', '44');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('5', '45');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('5', '46');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('5', '47');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('5', '48');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('5', '49');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('6', '50');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('6', '51');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('6', '52');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('6', '53');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('6', '54');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('6', '55');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('6', '56');
INSERT INTO Release ("ArtID", "ProjectID") VALUES ('6', '57');

COMMIT