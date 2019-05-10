from os import getenv
from pcache import Profile

def getPlayer():
    user = getUser()
    addProfileIfNotExist(user)
    return user

def addProfileInDbIfNotExist(user):
    profile = Profile()
    profile.name = user
    if not profile.fetch():
        profile.add()

def getUser():
    user = getenv('USERNAME')
    if not user:
        user = 'default'
    return user
