-- TABLE CREATION -Load for Genres Raw Table -- Zeynep Nur Genel
USE databeez_db;


LOAD DATA LOCAL INFILE 'D:/databeez-blg317e-project/data/genres.csv'
INTO TABLE Genre_Raw
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;