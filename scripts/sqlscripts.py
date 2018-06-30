TABLE_SETUP = '''
        CREATE TABLE `profile` (
            `id` INTEGER(7) NOT NULL,
            `name` VARCHAR(35) NOT NULL,
            `created` datetime NOT NULL,
            `modified` datetime NOT NULL,
            PRIMARY KEY (`id`)
        );

        CREATE TABLE `scores` (
            `id` INTEGER(7) NOT NULL AUTO_INCREMENT,
            `player_id` INTEGER(7) NOT NULL,
            `challenge_name` VARCHAR(125) NOT NULL,
            `complete_time` FLOAT NOT NULL,
            `created` datetime NOT NULL,
            `modified` datetime NOT NULL,
            PRIMARY KEY (`id`)
        );

        CREATE TABLE `difficulty` (
            `player_id` INTEGER(7) NOT NULL AUTO_INCREMENT,
            `difficulty` VARCHAR(25) NOT NULL
        );

        CREATE TABLE `stats` (
            `id` INTEGER(7) NOT NULL AUTO_INCREMENT,
            `player_id` INTEGER(7) NOT NULL,
            `challenge_name` VARCHAR(125) NOT NULL,
            `play_count` INTEGER(7) NOT NULL,
            `gameovers` INTEGER(7) NOT NULL,
            `wins` INTEGER(7) NOT NULL,
            `total_time` FLOAT NOT NULL,
            `created` datetime NOT NULL,
            `modified` datetime NOT NULL,
            PRIMARY KEY (`id`)
        );
'''

ADD_SCORE = '''
    insert 
    into scores(player_id, challenge_name, complete_time, created, modified)
    values (?, ?, ?, ?, ?)
'''

UPDATE_SCORE = '''
    update scores 
    set 
        complete_time = ?,
        modified = ?
    where 
    player_id = ?
'''

ADD_STAT = '''
    insert 
    into stats( 
        player_id, challenge_name, play_count, loses, 
        wins, total_time, created, modified)
    values (?, ?, ?, ?, ?, ?, ?, ?)
'''

UPDATE_STAT= '''
    update stats
    set 
        {0} = ?,
        modified = ?
    where 
        player_id = ? and challenge_name = ?
'''

GET_ALL = '''
    select * 
    from
         {0}
    where
         player_id = ?
'''

GET = '''
    select * 
    from 
        {0}
    where 
        player_id = ? and challenge_name = ?
'''

GET_PROF = '''
    select * from profile where name = ?
'''

ADD_PROF = '''
    insert into profile(name, created) values (?, ?)
'''

ADD_DIFF = '''
    insert into difficulty (player_id, difficulty) values (?, ?) 
'''

UPDATE_DIFF = '''
    update difficulty
    set difficulty = ?
    where player_id = ?
'''

GET_DIFF = '''
    select difficulty
    from difficulty 
    where player_id = ?
'''
