import pickle
import os

formatType = "format=json"

FILENAME = 'C:\\ProgramData\\SteamAchHunt\\User_ID.pk'

def getUser_ID():
    with open(FILENAME, 'r') as file:
        contents = file.read()
        if contents:
            with open(FILENAME,'rb') as fi:
                userID = pickle.load(fi)
            return (userID)
    return ""

def setUser_ID(userID: str):
    with open(FILENAME,'wb') as fi:
        pickle.dump(userID, fi)