-- Responsibility: Berk Özcan

USE databeez_db;

DROP TABLE IF EXISTS Game;

CREATE TABLE Game (
    Game_ID INT AUTO_INCREMENT PRIMARY KEY,
    `Name` VARCHAR(255),
    `Year` INT,
    `Rank` INT,

    Publisher_ID INT,
    Platform_ID INT,
    Genre_ID INT
);