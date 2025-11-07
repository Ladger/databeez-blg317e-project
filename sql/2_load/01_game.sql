-- Responsbility: Berk Özcan

-- Foreign Key implementation will be Week 7 change when all tables are present with data

ALTER TABLE Game
MODIFY COLUMN Publisher_ID INT NULL,
MODIFY COLUMN Platform_ID  INT NULL,
MODIFY COLUMN Genre_ID     INT NULL;

-- If the entry is "N/A" we are returning NULL for that cell
INSERT INTO Game (`Name`, `Year`, `Rank`)
SELECT
    `Name`,
    CAST(NULLIF(`Year`, 'N/A') AS UNSIGNED),
    `Rank`
FROM
    vgsales_raw;