TABLE_SETUP = '''
        CREATE TABLE `profile` (
            `id` INTEGER PRIMARY KEY AUTOINCREMENT,
            `name` VARCHAR(35) NOT NULL,
            `created` datetime NOT NULL,
            `modified` datetime NOT NULL
        );

        CREATE TABLE `scores` (
            `id` INTEGER PRIMARY KEY AUTOINCREMENT,
            `player_id` INTEGER(7) NOT NULL,
            `challenge_name` VARCHAR(125) NOT NULL,
            `completed_time` FLOAT NOT NULL,
            `created` datetime NOT NULL,
            `modified` datetime NOT NULL
        );

        CREATE TABLE `difficulty` (
            `id` INTEGER PRIMARY KEY AUTOINCREMENT,
            `player_id` INTEGER(7) NOT NULL,
            `difficulty` VARCHAR(25) NOT NULL
        );

        CREATE TABLE `stats` (
            `id` INTEGER PRIMARY KEY AUTOINCREMENT,
            `player_id` INTEGER(7) NOT NULL,
            `challenge_name` VARCHAR(125) NOT NULL,
            `play_count` INTEGER(7) NOT NULL,
            `gameovers` INTEGER(7) NOT NULL,
            `wins` INTEGER(7) NOT NULL,
            `total_time` FLOAT NOT NULL,
            `created` datetime NOT NULL,
            `modified` datetime NOT NULL
        );
'''
