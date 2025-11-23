-- Responsibility: Mertcan Kilinc


USE DatabeeZ_db;


INSERT INTO Publisher (
    Publisher_Name, 
    Country, 
    Year_Established)

SELECT
    t.Publisher_Name, 
    t.Country, 
    t.Year_Established
FROM    
    publisher_raw t;
