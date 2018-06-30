CREATE TABLE `profile` (
    `id` INTEGER(7) NOT NULL,
    `name` VARCHAR(35) NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE `scores` (
    `id` INTEGER(7) NOT NULL,
    `playerID` INTEGER(7) NOT NULL,
    `challengeName` VARCHAR(125) NOT NULL,
    `completeTime` FLOAT NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE `difficulty` (
    `playerID` INTEGER(7) NOT NULL,
    `difficulty` VARCHAR(25) NOT NULL
);

CREATE TABLE `stats` (
    `id` INTEGER(7) NOT NULL,
    `playerID` INTEGER(7) NOT NULL,
    `challengeName` VARCHAR(125) NOT NULL,
    `playCount` INTEGER(7) NOT NULL,
    `gameovers` INTEGER(7) NOT NULL,
    `wins` INTEGER(7) NOT NULL,
    `totalTime` FLOAT NOT NULL,
    PRIMARY KEY (`id`)
);