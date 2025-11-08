USE databeez_db;


LOAD DATA LOCAL INFILE 'D:/databeez-blg317e-project/data/platforms.csv'
INTO TABLE Platform
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;