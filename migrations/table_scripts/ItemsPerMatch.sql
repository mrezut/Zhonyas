CREATE TABLE IF NOT EXISTS ItemsPerMatch (
    `id` VARCHAR(36) NOT NULL,
    `itemName` VARCHAR(80) NOT NULL,
    `matchId` VARCHAR(20) NOT NULL,
    `championName` VARCHAR(30) NOT NULL,
    'role' VARCHAR(30) NOT NULL,
    `opposingRoleChampionName` VARCHAR(30) NOT NULL,
    `win` INTEGER NOT NULL,
    'item_count' INTEGER NOT NULL,
    PRIMARY KEY('id')
);

CREATE INDEX IF NOT EXISTS idx_MatchId on ItemsPerMatch (MatchId);

CREATE UNIQUE INDEX IF NOT EXISTS idx_UniqueItemsPerMatch on ItemsPerMatch (matchId, championName, itemName);