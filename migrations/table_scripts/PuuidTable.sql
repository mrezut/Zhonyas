CREATE TABLE IF NOT EXISTS Puuids (
    `id` VARCHAR(36) NOT NULL,
    `puuid` VARCHAR(80) NOT NULL,
    'dateRecorded' int,
    'dateLastUpdated' int,
    PRIMARY KEY(`id`)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_puuid on Puuids (puuid);