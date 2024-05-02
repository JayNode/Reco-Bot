from steam import Steam
from decouple import config

KEY = config("STEAM_API_KEY")
steam = Steam(KEY)

def get_user_games(userId):
    # get list of user games from steam
    userGames = steam.users.get_owned_games(userId)['games']
    gameList = []
    gameNames = ""
    #put user games into list
    for i in userGames:
        gameList.append(i['name'])
        
    #seperate list into string
    gameNames = ", ".join(map(str, gameList))

    return gameNames

def get_username(steam_username):
    # get user id from steam username
    userId = steam.users.get_steamid(steam_username)['steamid']
    print("Steam username: " + steam_username)
    print("Steam user Id: " + userId)
    # return user id
    return userId

def main(user):
    #get username of user
    userId = get_username(user)
    
    # uses steam id to access steam library, return user games
    userGames = get_user_games(userId)
    
    return userGames

if __name__ == "__main__":
    main()