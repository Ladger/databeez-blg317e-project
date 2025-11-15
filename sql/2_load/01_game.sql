-- Responsbility: Berk Özcan

INSERT INTO Game (
    `Name`,
    `Year`,
    `Rank`,
    Publisher_ID,
    Platform_ID,
    Genre_ID
)
SELECT
    r.`Name`,
    CAST(NULLIF(r.`Year`, 'N/A') AS UNSIGNED),
    r.`Rank`,
    p.Publisher_ID,
    pl.Platform_ID,
    g.Genre_ID
FROM
    vgsales_raw r
JOIN Publisher p ON r.Publisher = p.Publisher_Name
JOIN Platform pl ON r.Platform = pl.Platform_Name
JOIN Genre g ON r.Genre = g.Genre_Name;