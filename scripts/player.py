def getPlayerId():
    return getPlayer().getId()

def getPlayerName():
    return getPlayer().getName()

def getPlayer():
    from player_global_data import PlayerGlobalData 
    player = PlayerGlobalData()
    if not player.getId():    
        user = getUser()
        profile = getProfile(user)
        player.setName(profile.name)
        player.setId(profile.id)
    return player

def getProfile(user):
    from pcache import Profile
    profile = Profile()
    profile.name = user
    if not profile.fetch():
        profile.add()
    return profile

def getUser():
    from os import getenv
    user = getenv('USERNAME')
    if not user:
        user = 'default'
    return user
