CREATE TABLE IF NOT EXISTS MatchId_Puuid_Bridge (
    `Id` VARCHAR(36) NOT NULL,
    `MatchId` VARCHAR(20) NOT NULL,
    `puuid` VARCHAR(80) NOT NULL,
    PRIMARY KEY(`Id`)
);

CREATE INDEX IF NOT EXISTS idx_MatchId_bridge on MatchId_Puuid_Bridge (MatchId);

CREATE INDEX IF NOT EXISTS idx_puuid_bridge on MatchId_Puuid_Bridge (puuid);

CREATE UNIQUE INDEX IF NOT EXISTS idx_MatchId_puuid_bridge on MatchId_Puuid_Bridge (MatchId, puuid);