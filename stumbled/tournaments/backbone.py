import requests


class Client():
    def __init__(self):
        print('fdfdsfds')
    
    def refreshAccessToken(self):
    
        headers = {
            'Host': 'backbone-client-api.azurewebsites.net',
            'User-Agent': 'UnityPlayer/2020.3.38f1 (UnityWebRequest/1.0, libcurl/7.80.0-DEV)',
            'Accept': '*/*',
            'BACKBONE_APP_ID': 'PUBLIC_GITHUB',
            'ACCESS_TOKEN': '',
            'X-Unity-Version': '2020.3.38f1',
        }

        data = {
            'accessToken': 'PUBLIC_GITHUB',
            'refreshToken': 'a',
            'deviceId': 'PUBLIC_GITHUB',
        }

        response = requests.post('https://backbone-client-api.azurewebsites.net/api/v1/refreshAccessToken', headers=headers, data=data)
        print(response.text)

    def tournamentGetList(self):

        headers = {
        'Host': 'backbone-client-api.azurewebsites.net',
        'User-Agent': 'UnityPlayer/2019.4.15f1 (UnityWebRequest/1.0, libcurl/7.52.0-DEV)',
        'Accept': '*/*',
        'BACKBONE_APP_ID': 'PUBLIC_GITHUB',
        'ACCESS_TOKEN': 'PUBLIC_GITHUB',
        'X-Unity-Version': '2019.4.15f1',
        'Content-Type': 'application/x-www-form-urlencoded',
        }
        
        data = {
            'sinceDate': '2023-01-28T00:52:41',
            'untilDate': '2023-02-14T00:52:41',
            'maxResults': '250',
            'page': '1',
            'accessToken': 'PUBLIC_GITHUB',
        }        
        
        response = requests.post('https://backbone-client-api.azurewebsites.net/api/v2/tournamentGetList', headers=headers, data=data)
       # print(response.json())
        return response.json()
    
    def tournamentGetData(self,jogar:int):    

        headers = {
            'Host': 'backbone-client-api.azurewebsites.net',
            'User-Agent': 'UnityPlayer/2020.3.38f1 (UnityWebRequest/1.0, libcurl/7.80.0-DEV)',
            'Accept': '*/*',
            'BACKBONE_APP_ID': 'PUBLIC_GITHUB',
            'ACCESS_TOKEN': 'PUBLIC_GITHUB',
            'X-Unity-Version': '2020.3.38f1',
        }

        data = {
            'tournamentId': '671191390574616748',
            'getAllData': '1',
            'readyForNextMatch': jogar,#0 para não jogar #1 para jogar
            'accessToken': 'PUBLIC_GITHUB',
        }
        response = requests.post('https://backbone-client-api.azurewebsites.net/api/v2/tournamentGetData', headers=headers, data=data)
        print(response.text)
    
    def tournamentMatchGetGameSessions(self,tournamentId:int):    

        headers = {
            'Host': 'backbone-client-api.azurewebsites.net',
            'User-Agent': 'UnityPlayer/2020.3.38f1 (UnityWebRequest/1.0, libcurl/7.80.0-DEV)',
            'Accept': '*/*',
            'BACKBONE_APP_ID': 'PUBLIC_GITHUB',
            'ACCESS_TOKEN': 'PUBLIC_GITHUB',
            'X-Unity-Version': '2020.3.38f1',
        }

        data = {
            'tournamentMatchId': '672607104170732562',
        }
        response = requests.post('https://backbone-client-api.azurewebsites.net/api/v1/tournamentMatchGetGameSessions', headers=headers, data=data)
        print(response.text)

    def tournamentPartyRemoveUser(self,userid:int):    

        headers = {
            'Host': 'backbone-client-api.azurewebsites.net',
            'User-Agent': 'UnityPlayer/2020.3.38f1 (UnityWebRequest/1.0, libcurl/7.80.0-DEV)',
            'Accept': '*/*',
            'BACKBONE_APP_ID': 'PUBLIC_GITHUB',
            'ACCESS_TOKEN': 'PUBLIC_GITHUB',
            'X-Unity-Version': '2020.3.38f1',
        }

        data = {
            'tournamentId': '671191390574616748',
            'removeUserId': f'{userid}',
        }
        response = requests.post('https://backbone-client-api.azurewebsites.net/api/v1/tournamentPartyRemoveUser', headers=headers, data=data)
        print(response.text)

    def ConnectRoutine(self,userid:int):    

        headers = {
            'Host': 'backbone-client-api.azurewebsites.net',
            'User-Agent': 'UnityPlayer/2020.3.38f1 (UnityWebRequest/1.0, libcurl/7.80.0-DEV)',
            'Accept': '*/*',
            'BACKBONE_APP_ID': 'PUBLIC_GITHUB',
            'ACCESS_TOKEN': 'PUBLIC_GITHUB',
            'X-Unity-Version': '2020.3.38f1',
        }

        data = {
            'tournamentId': '672251554195057987',
            'removeUserId': f'{userid}',
        }
        response = requests.post('https://backbone-client-api.azurewebsites.net/api/v1/userConnect', headers=headers, data=data)
        print(response.text)

    def tournamentGetMatches(self):
        headers = {
            'Host': 'backbone-client-api.azurewebsites.net',
            'User-Agent': 'UnityPlayer/2020.3.38f1 (UnityWebRequest/1.0, libcurl/7.80.0-DEV)',
            'Accept': '*/*',
            'BACKBONE_APP_ID': 'PUBLIC_GITHUB',
            'ACCESS_TOKEN': 'PUBLIC_GITHUB',
            'X-Unity-Version': '2020.3.38f1',
        }

        data = {
            'tournamentId': '672251554195057987',
            'phaseId': '1',
            'groupId': '1',
            'fromRoundId': '1',
            'toRoundId': '1',
            'maxResults': '100',
            'page': '1',
            'onlyInProgress': '0',
            'accessToken': 'PUBLIC_GITHUB',
        }

        response = requests.post('https://backbone-client-api.azurewebsites.net/api/v1/tournamentGetMatches', headers=headers, data=data)
        print(response.json())
        return response.json()

    def userGet(self):

        headers = {
        'Host': 'backbone-client-api.azurewebsites.net',
        'User-Agent': 'UnityPlayer/2020.3.38f1 (UnityWebRequest/1.0, libcurl/7.80.0-DEV)',
        'Accept': '*/*',
        'BACKBONE_APP_ID': 'PUBLIC_GITHUB',
        'ACCESS_TOKEN': 'PUBLIC_GITHUB',
        'X-Unity-Version': '2020.3.38f1',
            }

        data = {
        'lastUpdate': '1900-01-01T00:00:00',
        'lastSync': '1900-01-01T00:00:00',
        'generateQuests': '0',
        'getQuests': '0',
        'getTiles': '0',
        'getLayouts': '0',
        'accessToken': 'PUBLIC_GITHUB',
        }

        response = requests.post('https://backbone-client-api.azurewebsites.net/api/v1/userGet', headers=headers, data=data)
        print(response.text)
    
    def userChangeNick(self):
        headers = {
            'Host': 'backbone-client-api.azurewebsites.net',
            'User-Agent': 'UnityPlayer/2019.4.15f1 (UnityWebRequest/1.0, libcurl/7.52.0-DEV)',
            'Accept': '*/*',
            'BACKBONE_APP_ID': 'PUBLIC_GITHUB',
            'ACCESS_TOKEN': 'PUBLIC_GITHUB',
            'X-Unity-Version': '2019.4.15f1',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = 'nickName=Player By3N8mCwiS&accessToken=PUBLIC_GITHUB'

        response = requests.post('https://backbone-client-api.azurewebsites.net/api/v1/userChangeNick', headers=headers, data=data)
        print(response.text)

    def userLoginExternal(self):
        headers = {
            'Host': 'backbone-client-api.azurewebsites.net',
            'User-Agent': 'UnityPlayer/2020.3.38f1 (UnityWebRequest/1.0, libcurl/7.80.0-DEV)',
            'Accept': '*/*',
            'BACKBONE_APP_ID': 'PUBLIC_GITHUB',
            'X-Unity-Version': '2020.3.38f1',
        }
        data = {
            'createNewUser': '1',
            'deviceId': 'PUBLIC_GITHUB',
            'deviceName': '<unknown>',
            'devicePlatform': '11',# 2 é pc
            'nickName': 'Player R1WOqeOkAs', #tanto faz o nick
            'clientToken': 'PUBLIC_GITHUB',
            'userId': 'PUBLIC_GITHUB',
            'clientParameters': 'nickName,clientToken,userId',
        }
        response = requests.post('https://backbone-client-api.azurewebsites.net/api/v1/userLoginExternal', headers=headers, data=data)
        print(response.text)

#673614709605278945-QBdTkoMOxS9cELOZycCuOujFohQngp1L:9uF50WKVjldr+l93+dxDRD9XkArGCD/IBQEQjrdWXCPuhkK9OHhNXqUdYdqHPKo0PIAJ9HcXIDRyL81suV2GrQ==

def get():
    cl = Client()
    torneios = cl.tournamentGetList()
    try:
        tor1 = torneios['tournaments']
    except:
        print(torneios)
    for torneio in tor1:
        print(torneio['name'], torneio['data']['tournament-data']['invitation-setting'][0]['requirements'][0]['custom-requirement'][0]['@value'])
    print(tor1)
#cl = Client()
#torneios = cl.tournamentMatchGetGameSessions(1)

def UnEscapeURL(data:str):
    replace = data.replace('+',' ')
    print(replace)


