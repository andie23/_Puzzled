from os import getenv
from pcache import Profile
from global_dictionary import PlayerGlobalData

def getPlayerId():
    return getPlayer().id

def getPlayerName():
    return getPlayer().name

def getPlayer():
    player = PlayerGlobalData()
    if not player.name:    
        user = getUser()
        profile = getProfile(user)
        player.name = profile.name
        player.id = profile.id
    return player

def getProfile(user):
    profile = Profile()
    profile.name = user
    if not profile.fetch():
        profile.add()
    return profile

def getUser():
    user = getenv('USERNAME')
    if not user:
        user = 'default'
    return user
