CREATE TABLE IF NOT EXISTS Puuids (
    `Id` VARCHAR(36) NOT NULL,
    `puuid` VARCHAR(80) NOT NULL,
    'date_recorded' int,
    'date_last_updated' int,
    PRIMARY KEY(`Id`)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_puuid on Puuids (puuid);
