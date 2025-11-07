-- Responsibility: Berk Özcan

USE databeez_db;

DROP TABLE IF EXISTS Game;
CREATE TABLE Game (
    Game_ID INT AUTO_INCREMENT PRIMARY KEY,
    `Name` VARCHAR(255),
    `Year` INT,
    `Rank` INT,

    Publisher_ID INT NOT NULL,
    Platform_ID INT NOT NULL,
    Genre_ID INT NOT NULL,

    FOREIGN KEY (Publisher_ID) REFERENCES Publisher(Publisher_ID),
    FOREIGN KEY (Platform_ID) REFERENCES Platform(Platform_ID),
    FOREIGN KEY (Genre_ID) REFERENCES Genre(Genre_ID)
);