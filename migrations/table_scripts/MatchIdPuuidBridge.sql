CREATE TABLE IF NOT EXISTS MatchIdPuuidBridge (
    `id` VARCHAR(36) NOT NULL,
    `matchId` VARCHAR(20) NOT NULL,
    `puuid` VARCHAR(80) NOT NULL,
    PRIMARY KEY(`id`)
);

CREATE INDEX IF NOT EXISTS idx_matchIdBridge on MatchIdPuuidBridge (matchId);

CREATE INDEX IF NOT EXISTS idx_puuidBridge on MatchIdPuuidBridge (puuid);

CREATE UNIQUE INDEX IF NOT EXISTS idx_MatchIdPuuidBridge on MatchIdPuuidBridge (matchId, puuid);