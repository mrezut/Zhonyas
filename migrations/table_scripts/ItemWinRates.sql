CREATE TABLE IF NOT EXISTS ItemWinRates (
    `item` VARCHAR(36) NOT NULL,
    'winRate' decimal(5,2),
    PRIMARY KEY(`item`)
);