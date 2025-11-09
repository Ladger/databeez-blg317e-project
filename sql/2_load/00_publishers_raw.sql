USE databeez_db;


LOAD DATA LOCAL INFILE '/Users/mertcankilinc/Documents/GitHub/databeez-blg317e-project/data/publishers.csv'
INTO TABLE Publishers_raw
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;