import pickle
import os

steamAPIURL =  "http://api.steampowered.com/"
formatType = "format=json"

FILENAME = 'C:\\ProgramData\\SteamAchHunt\\API_Key.pk'

def getAPI_Key():
    with open(FILENAME, 'r') as file:
        contents = file.read()
        if contents:
            with open(FILENAME,'rb') as fi:
                apiKey = pickle.load(fi)
            return (apiKey)
    return ""

def setAPI_Key(apiKey: str):
    with open(FILENAME,'wb') as fi:
        pickle.dump(apiKey, fi)