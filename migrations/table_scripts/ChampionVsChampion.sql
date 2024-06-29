CREATE TABLE IF NOT EXISTS ChampionVsChampion (
    `id` VARCHAR(36) NOT NULL,
    `matchId` VARCHAR(20) NOT NULL,
    `championName` VARCHAR(30) NOT NULL,
    'role' VARCHAR(30) NOT NULL,
    `opposingRoleChampionName` VARCHAR(30) NOT NULL,
    `win` INTEGER NOT NULL,
    PRIMARY KEY(`id`)
);