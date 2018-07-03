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
            log.debug('Creating New connection to %s...', self.db)
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
            self.con.close
            self.conObj = None 

    def insert(self, table, data):
        query = genInsertStatement(table, data.keys())
        log.debug('Executing "%s" with data "%s"', query, data)
        self.con.execute(query, data)
        self.con.commit()
        self.closeCon()

    def update(self, table, data, conditions):
        query = genUpdateStatement(table, data.keys(), conditions) 
        log.debug('Executing "%s" with data "%s"', query, data)
        self.con.execute(query, data)
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

    def add(self, completedTime):
        self.insert(
            table=self.table,
            data={
                'player_id': self.playerID, 'challenge_name':self.challenge,
                'completed_time':completedTime,'created':curdatetime(),
                'modified':curdatetime()
            }
        )

    def edit(self, data):
        self.update(
            table=self.table,
            data=data,
            conditions={
                'where' : {
                    'player_id':self.playerID, 
                    'challenge_name':self.challenge
                }
            }
        )

    def editTime(self, completedTime):
        self.edit({'completed_time': completedTime}, self.challenge)
 
    def get(self):
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
    @property
    def timeCompleted(self):
        resultset = self.select(
           table=self.table,
           columns=['completed_time'],
           conditions={
               'where': {
                    'player_id':self.playerID, 
                    'challenge_name':self.challenge
                }
           } 
        )

        return resultset[0]['completed_time']
    
    def isset(self):
        resultset = self.select(
            table=self.table, 
            columns=['*'], 
            conditions={
                'where': {
                    'challenge': self.challenge,
                    'player_id': self.playerID
                }
            }
        )

        return False if not resultset else True

class Difficulty(Pcache):
    def __init__(self, pid, difficulty=None):
        super(Pcache, self).__init__()
        Pcache.__init__(self)
        self.table = 'difficulty'
        self.playerID = pid
        self.difficulty = difficulty

    def add(self):
        self.insert(
            table=self.table,
            data={'player_id':self.playerID,'difficulty':self.difficulty}
        )

    def edit(self):
        self.update(
            table=self.table,
            data={'difficulty':self.difficulty},
            conditions={
                'where':{ 'player_id':self.playerID }
            }
        )

    def get(self):
        resultset = self.select(
            table=self.table,
            columns=['difficulty'],
            conditions={
                'where': {'player_id':self.playerID}
            }
        )

        return '' if not resultset else resultset[0]['difficulty']
    
    def isset(self):
        resultset = self.select(
            table=self.table, 
            columns=['*'], 
            conditions={
                'where': {
                    'player_id': self.playerID
                }
            }
        )
        return False if not resultset else True

class Stats(Pcache):
    def __init__(self, pid, challenge=None):
        super(Pcache, self).__init__()
        Pcache.__init__(self)
        self.table = 'stats'
        self.playerID = pid

    def add(self, playCount, gameovers,
             wins, totalTime):

        self.insert(
            table=self.table,
            data={
                'player_id':self.playerID, 'challenge_name':self.challenge, 
                'play_count':playCount, 'gameovers':gameovers, 'wins':wins, 
                'total_time':totalTime, 'created':curdatetime(), 'modified':curdatetime()
            }
        )

    def edit(self, data):
        cols['modified'] = curdatetime()
        self.update(
            table=self.table,
            columns=data,
            conditions={
                'where' : {
                    'player_id':self.playerID, 
                    'challenge_name': self.challenge
                }
            }
        )

    def get(self):
        return self.select(
           table=self.table,
           columns=['*'],
           conditions={
               'where' : {
                    'player_id':self.playerID, 
                    'challenge_name': self.challenge
                }
           } 
        )
    
    def getAll(self):
        return self.select(
           table=self.table,
           cols=['*'],
           conditions={
               'where' : {
                    'player_id':self.playerID 
                }
           } 
        )
    
    def isset(self):
        resultset = self.select(
            table=self.table, 
            columns=['*'], 
            conditions={
                'where': {
                    'challenge': self.challenge,
                    'player_id': self.playerID
                }
            }
        )

        return False if not resultset else True

class Profile(Pcache):
    def __init__(self, pid=0, pname=0):
        super(Pcache, self).__init__()
        Pcache.__init__(self)
        self.table = 'profile'
        self.id = pid
        self.name = pname

    @property
    def username(self):
        return self.get('name')
    @property
    def userid(self):
        return self.get('id')

    @property
    def created(self):
        return self.get('created')

    @property
    def modified(self):
        return self.get('modified')

    def isNameExists(self):
        return self.isset('name', self.name)
    
    def isIdExists(self):
        return self.isset('id', self.id)  
    
    def add(self):
        self.insert(
            table=self.table,
            data={'name':self.name, 'created':curdatetime(),
                  'modified':curdatetime()}
        )
    
    def get(self, column):
        resultset = self.select(
            table=self.table, 
            columns=[column], 
            conditions={
                'where': {'id': self.id},
                'orWhere' : {'name': self.name}
            }
        )
        return resultset[0][column]

    def isset(self, col, val):
        resultset = self.select(
            table=self.table, 
            columns=['*'], 
            conditions={
                'where': {col: val}
            }
        )

        return False if not resultset else True
