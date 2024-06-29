CREATE TABLE IF NOT EXISTS ChampionWinRates (
    `championName` VARCHAR(36) NOT NULL,
    `role` VARCHAR(36) NOT NULL,
    'winRate' decimal(5,2),
    PRIMARY KEY(`championName`, `role`)
);