-- Responsibility: Mertcan Kilinc

USE databeez_db;

INSERT INTO Platform (
    Platform_Name, 
    Manufacturer, 
    Release_Year)

SELECT
    t.Platform_Name, 
    t.Manufacturer, 
    t.Release_Year
FROM    
    platfroms_raw t;
