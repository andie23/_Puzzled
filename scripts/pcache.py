##############################################################
# Author: Andrew Mfune
# Date: 02/07/2018
# Description: This module contains modules for accessing data
#              kept in the Pcache aka the database. The 
#              master class is Pcache from which other classes 
#              (named after their tables) inherit from.
##############################################################

import sqlite3
from utils import getDBPath, isPathExists, curdatetime
from logger import logger
from sqlscripts import *
from pyqueryutils import *
from os import unlink
log = logger()

class Pcache:
    def __init__(self):
        self.db = getDBPath()
        self.conObj = None
        if not isPathExists(self.db):
            self._setupCache()

    @property
    def con(self):
        if self.conObj is None:
            log.debug('Openning Cache: %s...', self.db)
            con = sqlite3.connect(self.db)
            con.row_factory = sqlite3.Row
            self.conObj = con
            return con
        return self.conObj

    @property
    def cur(self):
        return self.con.cursor()

    def closeCon(self):
        if self.conObj:
            self.con.close()
            self.conObj = None 
            log.debug('Cache Closed!')

    def insert(self, table, data):
        query = genInsertStatement(table, data.keys())
        log.debug('Executing "%s" with data "%s"', query, data)
        self.con.execute(query, data)
        self.con.commit()
        self.closeCon()

    def edit(self, table, data, conditions):
        query = genUpdateStatement(table, data.keys(), conditions) 
        where = conditions['where']

        if 'orWhere' in conditions:
            where.update(conditions['orWhere'])
        data.update(where)

        log.debug('Executing "%s" with data "%s"', query, data)
        self.con.execute(query, data)
        self.con.commit()
        self.closeCon()

    def select(self, table, columns=['*'], conditions={}):
        query = genSelectStatement(table, columns, conditions)
        cur = self.cur
        
        if conditions: 
            where = conditions['where']
            orWhere = {} if 'orWhere' not in conditions else conditions['orWhere']
            where.update(orWhere)
            log.debug('Executing "%s" with "%s"', query, where)
            cur.execute(query, where)
        else:
            log.debug('Executing "%s"', query)
            cur.execute(query)

        resultset = cur.fetchall()

        return resultset

    def _setupCache(self):
        log.debug('Creating cache file: %s', self.db)
        try:
            self.con.executescript(TABLE_SETUP)
            self.con.commit()
            self.closeCon()
        except Exception as error:
            log.debug('Error Creating cache file: %s', error)
            unlink(self.db)
            

class Scores(Pcache):
    def __init__(self, pid, challenge=None):
        super(Pcache, self).__init__()
        Pcache.__init__(self)
        self.table = 'scores'
        self.playerID = pid
        self.challenge = challenge
        self.timeCompleted = 0.0
        self.overallScore = 0
        self.moves = 0
        self.streaks = 0

    def add(self):
        self.insert(
            table=self.table,
            data={
                'player_id': self.playerID, 
                'challenge_name': self.challenge,
                'moves': self.moves, 
                'completed_time': self.timeCompleted,
                'streaks': self.streaks,
                'overall_score' : self.overallScore,
                'created': curdatetime(),
                'modified': curdatetime()
            }
        )

    def update(self):
        self.edit(
            table=self.table,
            data={
                'player_id': self.playerID, 
                'challenge_name': self.challenge,
                'moves': self.moves, 
                'completed_time': self.timeCompleted,
                'streaks': self.streaks,
                'overall_score' : self.overallScore,
                'modified': curdatetime()
            },
            conditions={
                'where' : {
                    'player_id':self.playerID, 
                    'challenge_name':self.challenge
                }
            }
        )

    def getResultset(self):
        return self.select(
           table=self.table,
           columns=['*'],
           conditions={
               'where' : {
                    'player_id':self.playerID, 
                    'challenge_name':self.challenge
                }
           } 
        )

    def fetch(self):
        resultset = self.getResultset()
        if resultset:
            resultset = resultset[0]
            self.timeCompleted = resultset['completed_time']
            self.moves = resultset['moves']
            self.streaks = resultset['streaks']
            self.overallScore = resultset['overall_score']
            return True
        return False

    def isset(self):
        return False if not self.getResultset() else True

class Stats(Pcache):
    def __init__(self, pid, challenge=None):
        super(Pcache, self).__init__()
        Pcache.__init__(self)
        self.table = 'stats'
        self.playerID = pid
        self.challenge = challenge
        self.playCount = 0
        self.totalTime = 0.0
        self.wins = 0
        self.loses = 0

    def add(self):
        self.insert(
            table=self.table,
            data={
                'player_id':self.playerID, 
                'challenge_name':self.challenge, 
                'play_count': self.playCount, 
                'loses': self.loses, 
                'wins': self.wins, 
                'total_time': self.totalTime, 
                'created':curdatetime(), 
                'modified':curdatetime()
            }
        )

    def update(self):
        self.edit(
            table=self.table,
            data={
                'player_id':self.playerID, 
                'challenge_name':self.challenge, 
                'play_count': self.playCount, 
                'loses': self.loses, 
                'wins': self.wins, 
                'total_time': self.totalTime,
                'modified':curdatetime() 
            },
            conditions={
                'where' : {
                    'player_id':self.playerID, 
                    'challenge_name': self.challenge
                }
            }
        )
    def getResultset(self):
        return self.select(
           table=self.table,
           columns=['*'],
           conditions={
               'where' : {
                    'player_id':self.playerID, 
                    'challenge_name':self.challenge
                }
           } 
        )

    def fetch(self):
        resultset = self.getResultset()
        if resultset:
            resultset = resultset[0]
            self.wins = resultset['wins']
            self.loses = resultset['loses']
            self.playCount = resultset['play_count']
            self.totalTime = resultset['total_time']
            return True
        return False
   
    def isset(self):
        return False if not self.getResultset() else True

class Profile(Pcache):
    def __init__(self, pid=0):
        super(Pcache, self).__init__()
        Pcache.__init__(self)
        self.table = 'profile'
        self.id = pid
        self.name = ''
 
    def add(self):
        self.insert(
            table=self.table,
            data={
                'name':self.name, 
                'created':curdatetime(),
                'modified':curdatetime()
            }
        )
    
    def getResultset(self):
        return self.select(
            table=self.table, 
            columns=['*'], 
            conditions={
                'where': {'id': self.id},
                'orWhere' : {'name': self.name}
            }
        )

    def fetch(self):
        resultset = self.getResultset()
        if resultset:
            resultset = resultset[0]
            self.id = resultset['id']
            self.name = resultset['name']
            return True
        return False

    def isset(self):
        return False if not self.getResultset() else True
