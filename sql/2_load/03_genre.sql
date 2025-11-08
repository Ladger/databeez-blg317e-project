-- Responsibility: Zeynep Nur Genel
-- Loading data to Genre Table --
USE databeez_db;

INSERT INTO Genre (
    Genre_Name, 
    Description, 
    Example_Game)

SELECT
    t.Genre_Name, 
    t.Description, 
    t.Example_Game
FROM    
    genre_raw t;

