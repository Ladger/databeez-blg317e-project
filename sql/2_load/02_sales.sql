-- Responsibility: Zeynep Kocabıyık
-- STEP 2: LOADING DATA - Sales Table

USE DatabeeZ_db;

-- vgsales_raw tablosundan Sales verilerini çekme
INSERT INTO Sales (
    Game_ID, 
    NA_Sales, 
    EU_Sales, 
    JP_Sales, 
    Other_Sales, 
    Global_Sales
)
SELECT
    -- Game tablosunda zaten INSERT INTO yapıldığı için
    -- Satır sırasının aynı kalması koşuluyla Game_ID'leri otomatik olarak eşleştirebiliriz.
    -- Bu, vgsales_raw'daki her satırın Game tablosunda aynı sıradaki satırla eşleştiği varsayımına dayanır.
    g.Game_ID,
    r.NA_Sales,
    r.EU_Sales,
    r.JP_Sales,
    r.Other_Sales,
    r.Global_Sales
FROM
    vgsales_raw r
JOIN
    Game g ON r.`Name` = g.`Name` AND r.`Rank` = g.`Rank`;

-- Not: JOIN işlemi, en güvenilir yoldur ve Rank ve Name kombinasyonunu kullanarak
-- vgsales_raw'daki verileri Game tablosundaki doğru Game_ID ile eşleştirir.