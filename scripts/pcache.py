import sqlite3
from utils import getDBPath, isPathExists, curdatetime
from logger import logger
from sqlscripts import *

log = logger()

class Pcache:
    def __init__(self):
        self.db = getDBPath()

        if not isPathExists(db):
            log.debug('Creating cache file...')
            self._setupCache()

    @property
    def con(self):
        log.debug('connecting to %s...', db)
        return sqlite3.connect(db)
    
    @property
    def cur(self):
        return self.con.cursor()

    def execadd(self, query, values):
        log.debug('Executing query %s with values %s', query, values)
        self.cur.execute(query, values)
        self.cur.commit()

    def _setupCache(self):
        self.cur.executescript(TABLE_SETUP)
        self.cur.commit()

class Scores(Pcache):
    def __init__(self):
        super(Pcache, self).__init__()

    def add(self, pid, chname, comptime):
        self.execadd(ADD_SCORE, (
                pid, chname, comptime, 
                curdatetime, curdatetime
            ))

    def update(self, pid, chname, completeTime):
        self.execadd(UPDATE_SCORE, (
            pid, chname, 
            completeTime, 
            curdatetime
            ))

    def get(self, pid, challenge):
        query = GET.format('scores')
        self.cur.execute(query, (pid, challenge))
        return self.cur.fetchone()

    def getAll(self, pid):
        query = GET.format('scores')
        self.cur.execute(query, (pid))
        return self.cur.fetchall()

class Difficulty(Pcache):
    def __init__(self):
        super(Pcache, self).__init__()

    def add(self, pid, difficulty):
        self.execadd(ADD_DIFF, (pid, difficulty))

    def update(self, pid, difficulty):
        self.execadd(UPDATE_DIFF, (pid, difficulty))

    def get(self, pid):
        self.cur.execute(GET_DIFF, (pid))
        return self.cur.fetchone()

class Stats(Pcache):
    def __init__(self):
        super(Pcache, self).__init__()

    def add(self, pid, chname, pcount, loses,
            wins, total_time):
        self.execadd(ADD_STAT, (
            pid, chname, pcount, loses,
            wins, total_time, curdatetime, curdatetime
        ))

    def update(self, pid, chname, field, fvalue):
        query = UPDATE_STAT.format(field)
        self.execadd(UPDATE_STAT, (
            fvalue, curdatetime, pid, chname
            ))

    def get(self, pid, challenge):
        self.cur.execute(GET_STAT, (pid, challenge))
        return self.cur.fetchone()

    def getAll(self, pid):
        self.cur.execute(GET_ALL_STAT, (pid))
        return self.cur.fetchall()

class Profile(Pcache):
    def __init__(self):
        super(Pcache, self).__init__()

    def add(self, name):
        self.execadd(ADD_PROF, (name))

    def get(self, name):
        self.cur.execute(GET_PROF, (name, curdatetime))
        return self.cur.fetchone()