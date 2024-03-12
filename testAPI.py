import requests
import controlsAPI 
import os

def testAPI(apiKey: str):
    steamPath = "ISteamWebAPIUtil/GetSupportedAPIList/v0001/"
    url = f"{controlsAPI.steamAPIURL}{steamPath}"
    extraFields = {"key":apiKey}
    response = requests.get(url,params=extraFields)
    if(response.status_code == 200):
        return True
    else:
        print(f"Returned HTTP response for API validation: {response.status_code}")
        return False