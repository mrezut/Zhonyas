CREATE TABLE IF NOT EXISTS ItemWR (
    `Id` VARCHAR(36) NOT NULL,
    `ItemName` VARCHAR(80) NOT NULL,
    `MatchId` VARCHAR(20) NOT NULL,
    `ChampionName` VARCHAR(30) NOT NULL,
    'Role' VARCHAR(30) NOT NULL,
    `OpposingRoleChampionName` VARCHAR(30) NOT NULL,
    `Win` INTEGER NOT NULL,
    PRIMARY KEY('Id')
);

CREATE INDEX IF NOT EXISTS idx_MatchId on ItemWR (MatchId);

CREATE UNIQUE INDEX IF NOT EXISTS idx_UniqueItemWR on ItemWR (MatchId, ChampionName, ItemName);
