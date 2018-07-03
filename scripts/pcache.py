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

    def insert(self, table, columns, values):
        query = genInsertStatement(table, columns)
        log.debug('Executing insert statement: %s with values %s', query, values)
        self.con.execute(query, tuple(values))
        self.con.commit()
        self.closeCon()

    def update(self, table, columns, conditions):
        colnames = columns.keys()
        colvalues = columns.values()
        query = genUpdateStatement(table, colnames, conditions) 
        log.debug('Executing update statement: %s with values %s', query, colvalues)
        self.con.execute(query, tuple(colvalues))
        self.closeCon()

    def select(self, table, columns=['*'], conditions={}):
        query = genSelectStatement(table, columns, conditions)
        cur = self.cur
        
        if conditions:
            values = []
            whereValues = conditions['where'].values()
            orWhereValues = [] if 'orWhere' not in conditions else conditions['orWhere'].values()

            values.extend(whereValues)
            values.extend(orWhereValues)

            log.debug('Executing select "%s" with "%s"', query, values)
            cur.execute(query, tuple(values))
        else:
            log.debug('Executing select "%s"', query)
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
    def __init__(self, playerID):
        super(Pcache, self).__init__()
        Pcache.__init__(self)
        self.table = 'scores'
        self.playerID = playerID

    def add(self, challenge, completedTime):
        self.insert(
            table=self.table, 
            columns=['player_id', 'challenge_name', 
                     'completed_time', 'created', 'modified'],
            values=[self.playerID, challenge, completedTime,
                     curdatetime(), curdatetime()]
        )

    def edit(self, cols, challenge):
        self.update(
            table=self.table,
            columns=cols,
            conditions={
                'where' : {
                    'player_id':self.playerID, 
                    'challenge_name':challenge
                }
            }
        )

    def editTime(self, completedTime, challenge):
        self.edit({'completed_time': completedTime}, challenge)
 
    def get(self, challenge):
        return self.select(
           table=self.table,
           columns=['*'],
           conditions={
               'where' : {
                    'player_id':self.playerID, 
                    'challenge_name':challenge
                }
           } 
        )

    def getCompletedTime(self, challenge):
        resultset = self.select(
           table=self.table,
           columns=['completed_time'],
           conditions={
               'where' : {
                    'player_id':self.playerID, 
                    'challenge_name':challenge
                }
           } 
        )

        return resultset[0]['completed_time']
    
    def isset(self, challenge):
        resultset = self.select(
            table=self.table, 
            columns=['*'], 
            conditions={
                'where': {
                    'challenge':challenge,
                    'player_id': self.playerID
                }
            }
        )

        return False if not resultset else True

class Difficulty(Pcache):
    def __init__(self, playerID):
        super(Pcache, self).__init__()
        Pcache.__init__(self)
        self.table = 'difficulty'
        self.playerID = playerID

    def add(self, difficulty):
        self.insert(
            table=self.table,
            columns=['player_id', 'difficulty'],
            values=[self.playerID, difficulty]
        )

    def edit(self, difficulty):
        self.update(
            table=self.table,
            columns={'difficulty':difficulty},
            conditions={
                'where':{ 'player_id':self.playerID }
            }
        )

    def get(self):
        resultset = self.select(
            table=self.table,
            cols=['difficulty'],
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
    def __init__(self, playerID):
        super(Pcache, self).__init__()
        Pcache.__init__(self)
        self.table = 'stats'
        self.playerID = playerID

    def add(self, challenge, playCount, gameovers,
             wins, totalTime):
        
        self.insert(
            table=self.table,
            columns=['player_id', 'challenge_name', 'play_count',
                     'gameovers', 'wins', 'total_time', 'created', 'modified'],
            values=[self.playerID, challenge, playCount, gameovers,
                    wins, totalTime, curdatetime(), curdatetime()]   
        )

    def edit(self, cols, challenge):
        cols['modified'] = curdatetime()
        self.update(
            table=self.table,
            columns=cols,
            conditions={
                'where' : {
                    'player_id':self.playerID, 
                    'challenge_name':challenge
                }
            }
        )

    def get(self, challenge):
        return self.select(
           table=self.table,
           cols=['*'],
           conditions={
               'where' : {
                    'player_id':self.playerID, 
                    'challenge_name':challenge
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
    
    def isset(self, challenge):
        resultset = self.select(
            table=self.table, 
            columns=['*'], 
            conditions={
                'where': {
                    'challenge':challenge,
                    'player_id': self.playerID
                }
            }
        )

        return False if not resultset else True


class Profile(Pcache):
    def __init__(self):
        super(Pcache, self).__init__()
        Pcache.__init__(self)
        self.table = 'profile'
        
    def add(self, username):
        self.insert(
            table=self.table,
            columns=['name', 'created', 'modified'], 
            values=[username, curdatetime(), curdatetime()]
        )

    def getUsername(self, playerID):
        resultset = self.select(
            table=self.table, 
            columns=['name'], 
            conditions={
                'where': {'id': playerID}
            }
        )

        return resultset[0]['name']

    def getID(self, username):
        resultset = self.select(
            table=self.table, 
            columns=['id'], 
            conditions={
                'where': {'name': username}
            }
        )

        return resultset[0]['id']

    def isUsernameExists(self, username):
        return self.isset('name', username)
    
    def isIdExists(self, pid):
        return self.isset('id', pid)

    def isset(self, col, val):
        resultset = self.select(
            table=self.table, 
            columns=['*'], 
            conditions={
                'where': {col: val}
            }
        )

        return False if not resultset else True
