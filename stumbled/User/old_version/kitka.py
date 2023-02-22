import requests,os,hashlib,json,time as tm
from requests.structures import CaseInsensitiveDict
from time import time 
from random import randint
import datetime,sys

from dotenv import load_dotenv
load_dotenv()

user_login = os.getenv('user_login')
user_edit = os.getenv('user_edit')
#-----------------------#
#links loader
main_new = os.getenv('main_new')
main_old = os.getenv('main_old')
#endpoints loader
user_login = os.getenv('user_login')
user_updat = os.getenv('user_updat')
#keys
login_key = os.getenv('login_key')
head_key = os.getenv('head_key')
#-----------------------#

from colorama import Fore, Back, Style
from colorama import init
init()


defaultheader = headers = {'Content-Type': 'application/json','use_response_compression': 'true'}


class User():
    def __init__(self, DeviceId, FacebookId='',GoogleId='',SteamTicket='',AppleId='',Version='0.37'):

        self.FacebookId = FacebookId
        self.GoogleId = GoogleId
        self.DeviceId = DeviceId
        self.SteamTicket = SteamTicket
        self.AppleId = AppleId
        self.Version = Version
        
    def console_user_logs(self,local,log,Error=None):
        if Error == None:
            print(f"{Fore.GREEN}[{local}]{Fore.MAGENTA}[{datetime.datetime.now()}]: {Fore.WHITE} {log}")
        elif Error =='Log':
            print(f"{Fore.CYAN}[{local}]{Fore.MAGENTA}[{datetime.datetime.now()}]: {Fore.CYAN} {log}")
        else:
            print(f"{Fore.RED}[ERROR]{Fore.GREEN}[{local}]{Fore.MAGENTA}[{datetime.datetime.now()}]: {Fore.WHITE} {log}")

    def Login(self,Proxies=None):
        data = {"Id":993692134,"DeviceId":self.DeviceId,"Version":self.Version,"FacebookId":self.FacebookId,"AppleId":'',"GoogleId":self.GoogleId,"Timestamp":1654374366,"AdvertisingId":"","SteamTicket":self.SteamTicket,"Hash":""}
       
        r = requests.post(main_old+f'/user/login', headers=defaultheader,data=str(data),proxies=Proxies)

        if r.status_code == 403 or r.status_code == 404 or r.status_code == 400 or r.text == "BANNED":
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"{r.text} {r.status_code} {r.reason}",Error='y')
            return f'{r.text} {r.status_code} {r.reason}'

        self.Full = r.json()
        try:
            self.UserId = r.json()['User']['Id']
        except:
            print('Error: ',r.text)

        Levels = [{"RequiredXP":1000},{"RequiredXP":2000},{"RequiredXP":4000},{"RequiredXP":8000},{"RequiredXP":12000},{"RequiredXP":20000},{"RequiredXP":30000},{"RequiredXP":40000},{"RequiredXP":60000},{"RequiredXP":80000},{"RequiredXP":120000},{"RequiredXP":140000},{"RequiredXP":160000},{"RequiredXP":180000},{"RequiredXP":200000},{"RequiredXP":220000},{"RequiredXP":240000},{"RequiredXP":260000},{"RequiredXP":280000},{"RequiredXP":300000}]
        self.Version = r.json()['User']['Version']
        self.Token = r.json()['User']['Token']
        #self.GoogleId = ''
        #self.FacebookId = ''
        self.StumbleId = r.json()['User']['StumbleId']
        self.Username = r.json()['User']['Username']
        self.SkillRating = r.json()['User']['SkillRating']
        self.Exp = r.json()['User']['Experience']
        self.Level =len([True for req in Levels if req['RequiredXP']<self.Exp])
        self.Crowns = r.json()['User']['Crowns']
        self.Skins = r.json()['User']['Skins']
        self.Emotes = r.json()['User']['Emotes']
        self.Animations = r.json()['User']['Animations']
        self.Footsteps = r.json()['User']['Footsteps']
        self.HasBattlePass = ['No' if r.json()['User']['BattlePass']['HasPurchased'] == False else 'Yes']
        self.BattlePassLevel = r.json()['User']['BattlePass']['PassTokens']/100
        self.Animations = r.json()['User']['Animations']
        self.Balances = r.json()['User']['Balances']
        self.BalancesUp = r.json()['User']['Balances']
        self.Gems = [item['Amount'] for item in self.BalancesUp if item['Name'] == 'gems'][0]
        self.Dust = [item['Amount'] for item in self.BalancesUp if item['Name'] == 'dust'][0]
        names = ['video','remove_ads','gems','video_gems','special_video','skin_charge','skin_purchase','gem_charge','dust']
        balances_info = [f"[{item['Name'].upper()} AMOUNT(min/max)]: {item['Amount']}/{item['MaxAmount']}\n[LAST RECHARGE(minutes ago)]: {item['SecondsSince']/60:.2f}\n[DAILY RECHARGE(minutes)]: {item['SecondsPerUnit']/60:.2f}" for item in r.json()['User']['Balances'] if item['Name'] in names]
        self.BalancesInfoTrashed = balances_info
        self.Auth = {'DeviceId': self.DeviceId, 'GoogleId': f'{self.GoogleId}', 'FacebookId': f'{self.FacebookId}', 'AppleId': '', 'Token': self.Token, 'Timestamp': 1657411202,'Hash': '128053146036d1bfcda08eedcc177bb625f90bb1'}
        
        self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"Logged has {Fore.GREEN}{r.json()['User']['Username']} Level:{self.Level}{Fore.WHITE} Skins:{len(self.Skins)} BattlePassLevel:{self.BattlePassLevel}")
        
        self.FreeGemsAmount = 0
        return r
     
    def ChangeUsername(self,username):
        self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"Arg(username): {username}",Error='Log')
        data = str({"Username":f"{username}"})
        auth_hash = hashstumble(self.Auth ,f'/user/update',data)
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth_hash),
        'use_response_compression': 'false',
        }
        
        r = requests.post(main_old+f'/user/update', headers=headers,data=data)

        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "BANNED") or (r.status_code == 400) or (r.status_code == 401):
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"{r.text} {r.status_code}",Error='y')
            print({'new_search': f'❌ - Error em search\n⛔\n[{r.status_code}] Error log: {r.text}\n⛔'})
            return {'new_username': f'❌ - Username não alterado\n⛔\n[{r.status_code}] Error log: {r.text, r.reason}\n⛔'}
        else:
            print({'status':r.status_code, 'new_search':  r.json()['User']['Username']})
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"[STATUS {r.status_code}] New username: {r.json()['User']['Username']}")
            return {'status':r.status_code, 'new_username': r.json()['User']['Username']}
    
    def Search(self,username):

        data = str({"userName":f"{username}"})
        auth_hash = hashstumble(self.Auth ,f'/friends/search',data)
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth_hash),
        'use_response_compression': 'false',
        }
        
        r = requests.post(main_new+f'/friends/search', headers=headers,data=data)

        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "BANNED") or (r.status_code == 400) or (r.status_code == 401):
            print({'new_search': f'❌ - Error em search\n⛔\n[{r.status_code}] Error log: {r.text}\n⛔'})
            return {'new_search': f'❌ - Error em search\n⛔\n[{r.status_code}] Error log: {r.text}\n⛔'}
        else:
            self.console_user_logs(local=sys._getframe().f_code.co_name, log={'status':r.status_code, 'reason':r.reason ,'new_search': r.text})
            return {'status':r.status_code, 'new_search': r.json()['userName']}
    
    def Friends(self):
        auth_hash = hashstumble(self.Auth ,f'/friends','')
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth_hash),
        'use_response_compression': 'false',
        }
        
        r = requests.get(main_new+f'/friends', headers=headers)
        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "BANNED") or (r.status_code == 400):
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"{len(r.json()),r.status_code ,r.reason}", Error='y')
            return {'friends': f'❌ - Error em search\n⛔\n[{r.status_code}] Error log: {r.text}\n⛔'}
        else:
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"{len(r.json()),r.status_code ,r.reason}")
            return r.json()
    
    def Friend_request(self,userid:int):
        data = str({"UserId":userid})
        auth_hash = hashstumble(self.Auth ,f'/friends/request',data)
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth_hash),
        'use_response_compression': 'false',
        }
        
        r = requests.post(main_new+f'/friends/request', headers=headers,data=data)
        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "BANNED") or (r.status_code == 400):
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"{r.text,r.status_code ,r.reason}", Error='y')
            return {'request_to': f'❌ - Error em search\n⛔\n[{r.status_code}] Error log: {r.text}\n⛔'}
        else:
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"{r.text,r.status_code ,r.reason}")
            return {'request_to': f'{r.text,r.status_code,r.reason}'}
    
    def FriendsDelete(self,userid):
        auth_hash = hashstumble(self.Auth ,f'/friends/{userid}','')
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth_hash),
        'use_response_compression': 'false',
        }
        
        r = requests.delete(main_new+f'/friends/{userid}', headers=headers)
        print(r.text)
        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "BANNED") or (r.status_code == 400):
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"{r.text,r.status_code ,r.reason}",Error='y')
            return {'request_to': f'❌ - Error em search\n⛔\n[{r.status_code}] Error log: {r.text}\n⛔'}
        else:
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"{r.text,r.status_code ,r.reason}")
            #print({'request_to': f'{r.text,r.status_code,r.reason}'})
            return {'request_to': f'{r.text,r.status_code,r.reason}'}

    def SetSkin(self,skinid):
        from requests.structures import CaseInsensitiveDict
        data = str({"Category":"Skin","ItemId":f"{skinid}"})
        author = self.Auth
        print(author)
        author_convert = hashstumble(author,'/user/inventory/selection',data)
        headers = CaseInsensitiveDict()
        headers["authorization"] = str(author_convert)
        #5afd46daced9498575cd9ff53d52b5f43811e048
        headers["use_response_compression"] = "true"
        headers["User-Agent"] = "Unity-2020.3.38f1"
        headers["Content-Type"] = "application/json"
        headers["Accept-Encoding"] = "gzip, deflate"
        headers["Content-Length"] = "19"


        resp = requests.post(main_new+f'/user/inventory/selection', headers=headers, data=data,verify=False)
        print(resp.text, resp.reason,resp.status_code)
    
    def FriendAccepted(self,userid:int):
        data = str({"UserId":userid})   
        auth_hash = hashstumble(self.Auth ,f'/friends/request/accept',data)
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth_hash),
        'use_response_compression': 'false',
        }
        
        r = requests.post(main_new+f'/friends/request/accept', headers=headers,data=data)
        print(r.text)
        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "BANNED") or (r.status_code == 400):
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"{r.text,r.status_code ,r.reason}", Error='y')
            return {'request_to': f'❌ - Error em search\n⛔\n[{r.status_code}] Error log: {r.text}\n⛔'}
        else:
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"{r.text,r.status_code ,r.reason}")
            #print({'request_to': f'{r.text,r.status_code,r.reason}'})
            return {'request_to': f'{r.text,r.status_code,r.reason}'}
    

    def Regretfriend_request(self, userid:int):
        data = str({"UserId":userid})
        auth_hash = hashstumble(self.Auth ,f'/friends/request/decline',data)
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth_hash),
        'use_response_compression': 'false',
        }
        
        r = requests.post(main_new+f'/friends/request/decline', headers=headers,data=data)
        print(r.text)
        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "BANNED") or (r.status_code == 400):
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"{r.text,r.status_code ,r.reason}",Error='y')

            return {'request_to': f'❌ - Error em search\n⛔\n[{r.status_code}] Error log: {r.text}\n⛔'}
        else:
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"{r.text,r.status_code ,r.reason}")
            return {'request_to': f'{r.text,r.status_code,r.reason}'}
    
    def WinRound(self):
        self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"started", Error='Log')
        round = randint(2, 3) #win or 2place
        auth = hashstumble(self.Auth,f'/round/finishv2/{round}','')
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth),
        'use_response_compression': 'true',
        }
        r = requests.get(main_old+f'/round/finishv2/{round}', headers=headers)

        try: 
           print(f"Skill: {r.json()['User']['SkillRating']} : XP: {r.json()['User']['Experience']} : Partidas ganhas: {r.json()['User']['Crowns']} : HiddenRating {r.json()['User']['HiddenRating']}")
           print(f"Nivel no passe de batalha: {r.json()['User']['BattlePass']['PassTokens']/100} ({r.json()['User']['BattlePass']['PassTokens']})")
           print("Passe pago?:", r.json()['User']['BattlePass']['HasPurchased'])
           print("Free: ", r.json()['User']['BattlePass']['FreePassRewards'])
           print("Premium: ", r.json()['User']['BattlePass']['PremiumPassRewards'])
        except Exception as e:
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"{r.text, e}", Error='y')

    def WinRoundv1_fixsec(self,round:int,Proxies=None):
        self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"started", Error='Log')
        #round = randint(2, 3) #win or 2place
        auth = hashstumble(self.Auth,f'/round/finish/{round}','')
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth),
        'use_response_compression': 'true',
        }
        r = requests.get(main_old+f'/round/finish/{round}', headers=headers,proxies=Proxies)

        try: 
           print(f"FixSecNormalSkill: {r.json()['User']['SkillRating']} : XP: {r.json()['User']['Experience']} : Partidas ganhas: {r.json()['User']['Crowns']} : HiddenRating {r.json()['User']['HiddenRating']}")
           print(f"Nivel no passe de batalha: {r.json()['User']['BattlePass']['PassTokens']/100} ({r.json()['User']['BattlePass']['PassTokens']})")
           print("Passe pago?:", r.json()['User']['BattlePass']['HasPurchased'])
           print("Free: ", r.json()['User']['BattlePass']['FreePassRewards'])
           print("Premium: ", r.json()['User']['BattlePass']['PremiumPassRewards'])
           return r.json()['User']['Crowns']
        except Exception as e:
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"{r.text, e}", Error='y')

    def WinRoundv2_fixsec(self,round:int,Proxies=None):
        self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"started", Error='Log')
        #round = randint(2, 3) #win or 2place
        auth = hashstumble(self.Auth,f'/round/finishv2/{round}','')
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth),
        'use_response_compression': 'true',
        }
        r = requests.get(main_old+f'/round/finishv2/{round}', headers=headers,proxies=Proxies)

        try: 
           print(f"FixSecv2 Skill: {r.json()['User']['SkillRating']} : XP: {r.json()['User']['Experience']} : Partidas ganhas: {r.json()['User']['Crowns']} : HiddenRating {r.json()['User']['HiddenRating']}")
           print(f"Nivel no passe de batalha: {r.json()['User']['BattlePass']['PassTokens']/100} ({r.json()['User']['BattlePass']['PassTokens']})")
           print("Passe pago?:", r.json()['User']['BattlePass']['HasPurchased'])
           print("Free: ", r.json()['User']['BattlePass']['FreePassRewards'])
           print("Premium: ", r.json()['User']['BattlePass']['PremiumPassRewards'])
           return r.json()['User']['Crowns']
        except Exception as e:
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"{r.text, e}", Error='y')
    
    def SetSkin(self,skinid):
        from requests.structures import CaseInsensitiveDict
        data = str({"Category":"Skin","ItemId":f"{skinid}"})
        author = self.Auth
        print(author)
        author_convert = hashstumble(author,'/user/inventory/selection',data)
        headers = CaseInsensitiveDict()
        headers["authorization"] = str(author_convert)
        #5afd46daced9498575cd9ff53d52b5f43811e048
        headers["use_response_compression"] = "true"
        headers["User-Agent"] = "Unity-2020.3.38f1"
        headers["Content-Type"] = "application/json"
        headers["Accept-Encoding"] = "gzip, deflate"
        headers["Content-Length"] = "19"


        resp = requests.post(main_new+f'/user/inventory/selection', headers=headers, data=data,verify=False)
        print(resp.text, resp.reason,resp.status_code)
    
    def Getfriend_request(self):
        auth_hash = hashstumble(self.Auth ,f'/friends/request','')
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth_hash),
        'use_response_compression': 'false',
        }
        
        r = requests.get(main_new+f'/friends/request', headers=headers)
        print(r.text)
        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "BANNED") or (r.status_code == 400):
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"{r.text,r.status_code ,r.reason}")
            return {'invites': f'❌ - Error em search\n⛔\n[{r.status_code}] Error log: {r.text}\n⛔'}
        else:
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"{r.text,r.status_code ,r.reason}")
            return {'invites': r.json(),'status':r.status_code,'reason':r.reason}
    

    def LinkGoogle(self,GoogleId):
        
        self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"Args: {GoogleId}", Error='Log')
        
        STEAM_AUTH = {"DeviceId":self.DeviceId,"GoogleId":GoogleId,"FacebookId":"","Token":self.Token,"Timestamp":1670722613,"Hash":"cef004de227997bfd9d922389121c077047abf52"}
        #O certo seria o Steam auth ir com GoogleId e FacebookId de acordo com as informaçções da conta, porém o token aprova a request mesmo com a informação incorreta.
        data = str({"UserId":self.UserId,"Token":self.Token,"FacebookId":"",'GoogleId':GoogleId})#Presta atenção em UserId e Token junto com GoogleId ou Facebook, qualquer erro = Error Token
        auth = hashstumble(STEAM_AUTH,f'/user/linkgoogle',data)
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth),
        'use_response_compression': 'true',
        }     
        r = requests.post(main_old+f'/user/linkgoogle', headers=headers,data=data)
        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "BANNED") or (r.status_code == 400):
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f'[STATUS {r.status_code}] Error: {r.text}', Error='y')

        else:
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"[STATUS {r.status_code}] GoogleId {GoogleId} has Linked to {r.json()['Username']} {r.text}")

     
    def LinkFacebook(self,FaceboookId):
        self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"Args: {FaceboookId}", Error='Log')
    
        STEAM_AUTH = {"DeviceId":self.DeviceId,"GoogleId":"","FacebookId":FaceboookId,"Token":self.Token,"Timestamp":1670722613,"Hash":"cef004de227997bfd9d922389121c077047abf52"}
        #O certo seria o Steam auth ir com GoogleId e FacebookId de acordo com as informaçções da conta, porém o token aprova a request mesmo com a informação incorreta.
        data = str({"UserId":self.UserId,"Token":self.Token,"FacebookId":"",'GoogleId':FaceboookId})#Presta atenção em UserId e Token junto com GoogleId ou Facebook, qualquer erro = Error Token
        auth = hashstumble(STEAM_AUTH,f'/user/linkgoogle',data)
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth),
        'use_response_compression': 'true',
        }     
        r = requests.post(main_old+f'/user/linkgoogle', headers=headers,data=data)
        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "BANNED") or (r.status_code == 400):
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f'[STATUS {r.status_code}] Error: {r.text}', Error='y')
        else:
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"[STATUS {r.status_code}] GoogleId {FaceboookId} has Linked to {r.json()['Username']} {r.text}")
     
    def DeleteAccount(self):
        #Function Perigossima, cautela
        account_info = f"Account Information: Username['{self.Username}'] Stats['Crowns: {self.Crowns}', 'Skill: {self.SkillRating}']\n{self.Auth}"
        input('WARNING!! THIS CAN REMOVE YOUR ACCOUNT FROM THE DATABASE')
        print(account_info)
        input('WARNING!! THIS CAN REMOVE YOUR ACCOUNT FROM THE DATABASE')
        print(account_info)
        input('WARNING!! THIS CAN REMOVE YOUR ACCOUNT FROM THE DATABASE')
        print(account_info)

        ab = input('Delete account?\nSend "1" for Yes\n')
        if ab != "1":
            return False  
        
        auther = {'DeviceId': self.DeviceId, 'GoogleId': 'None', 'FacebookId': 'None', 'AppleId': '', 'Token': self.Token, 'Timestamp': 1657411202, 'Hash': '128053146036d1bfcda08eedcc177bb625f90bb1'}
        auth = hashstumble(auther,f'/user/deleteaccount','')
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth),
        'use_response_compression': 'true',
        }
        r = requests.get(main_old+f'/user/deleteaccount', headers=headers)
        
        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "BANNED") or (r.status_code == 400):
            print(f'[STATUS {r.status_code}] Error: {r.text}')
        else:
            print(f"[STATUS {r.status_code}] Account {self.Username} Has Deleted")

     
    def FreeGems(self):
        self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"started", Error='Log')
        """
        prices: [{amount: 1, currency: "video_gems"}, {amount: 1, currency: "video"}]
        rewards: [{max: 8, min: 8, type: "CURRENCY", typeInfo: "gems"}]
        """
        self.FreeGemsAmount = 0
        auth = hashstumble(self.Auth,'/economy/purchase/free_gems','')
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth),
        'use_response_compression': 'true',
        }
        if [item['Amount'] for item in self.BalancesUp if item['Name'] == 'video_gems'][0] == 0:
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f'FreeGems is null', Error='y')
            return 'FreeGems is null'
        try:
            free_gems = requests.post(main_old+f'/economy/purchase/free_gems', headers=headers)
            
            if 'Update currency would give negative balance' in free_gems.text:
                    print('FreeGems negative balance')
                    return 'FreeGems negative balance'
            
            videogems_amount = [item['Amount'] for item in free_gems.json()['User']['Balances'] if item['Name'] == 'video_gems']
            #cada 8 gemas ganhas é gasto 1 video_gems amount em balances com o maximo de 80 gemas ganhas
            self.FreeGemsAmount = 8*videogems_amount[0]

            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f'FreeGemsAmount: {self.FreeGemsAmount}')
        
        except:
            recharg = [item['SecondsPerUnit']/60 for item in free_gems.json()['User']['Balances'] if item['Name'] == 'video_gems']
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"[FreeGems STATUS {free_gems.status_code} LOG] {free_gems.text} Next recharge in {recharg[0]:.2f}", Error='y')
            return f"[FreeGems STATUS {free_gems.status_code} LOG] {free_gems.text} Next recharge in {recharg[0]:.2f} "
        for _ in range(videogems_amount[0]):
            tm.sleep(0.5)
            try:
                go = requests.post(main_old+f'/economy/purchase/free_gems', headers=headers)
            except Exception as Erro:
                return str(Erro, '[FreeGems]', go.text)
            names = ['gems','video_gems']
            #print(go.json()['User']['Rewards'])
            #self.BalancesUp = 'freegems_bug_fix'
        self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"finish", Error='Log')
        return 'Finish'
        
    def FreeGemsVideo(self):
        self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"started", Error='Log')
        """
        prices: [{amount: 1, currency: "special_video"}, {amount: 1, currency: "video"}]
        special video load time 8 hours
        rewards: [{max: 10, min: 10, type: "CURRENCY", typeInfo: "gems"}]
        """
        auth = hashstumble(self.Auth,'/economy/purchase/video_gems','')
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth),
        'use_response_compression': 'true',
        }
        special_video_amount = [item['Amount'] for item in self.Balances if item['Name'] == 'special_video']

        if special_video_amount[0] > 1:
            for _ in range(special_video_amount[0]):

                r = requests.post(main_old+f'/economy/purchase/video_gems', headers=headers)
                if 'Update currency would give negative balance' in r.text:
                    self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"Negative Balance FreeGemsVideo", Error='y')
                    return 0

            self.BalancesUp = r.json()['User']['Balances']
        self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"finish", Error='Log')
        return f"{special_video_amount[0]*10}"
     
    def FreeGemsMenu(self):
        self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"started", Error='Log')
    
        auth = hashstumble(self.Auth,'/economy/purchase/gemvideo_charge','')
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth),
        'use_response_compression': 'true',
        }
        try:
            free_gems_menu = requests.post(main_old+f'/economy/purchase/gemvideo_charge', headers=headers)
            daily_gem_purchase = [item['Amount'] for item in free_gems_menu.json()['User']['Balances'] if item['Name'] == 'gem_purchase']
        except:
            print(f"[STATUS {free_gems_menu.status_code} LOG] {free_gems_menu.text}")
            return f"[STATUS {free_gems_menu.status_code} LOG] {free_gems_menu.text}"

        if daily_gem_purchase[0] > 0:
            for _ in range(4):
                tm.sleep(0.5)
                go = requests.post(main_old+f'/economy/purchase/gemvideo_charge', headers=headers)
                names = ['gem_charge']
                for item in go.json()['User']['Balances']:
                    if item['Name'] in names:
                        print('---------------------')
                        print(f"[{item['Name'].upper()} AMOUNT(min/max)]: {item['Amount']}/{item['MaxAmount']}\n[LAST RECHARGE(minutes ago)]: {item['SecondsSince']/60:.2f}\n[DAILY RECHARGE(minutes)]: {item['SecondsPerUnit']/60:.2f}")
                        print('---------------------')
            auth = hashstumble(self.Auth,'/economy/purchase/menu_free_gems','')
            headers = {
            'Content-Type': 'application/json',
            'authorization': str(auth),
            'use_response_compression': 'true',
            }
            try:
                take_free_gens_menu = requests.post(main_old+f'/economy/purchase/menu_free_gems', headers=headers)
                names = ['gemvideo_charge','gem_purchase']
                for item in go.json()['User']['Balances']:
                    if item['Name'] in names:
                        print('---------------------')
                        print(f"[{item['Name'].upper()} AMOUNT(min/max)]: {item['Amount']}/{item['MaxAmount']}\n[LAST RECHARGE(minutes ago)]: {item['SecondsSince']/60:.2f}\n[DAILY RECHARGE(minutes)]: {item['SecondsPerUnit']/60:.2f}")
                        print('---------------------')   
                self.BalancesUp = take_free_gens_menu.json()['User']['Balances']
                return take_free_gens_menu.json()['User']['Rewards'] 
            except:
                print(f"[FreeGemsMenu(take_free_gens_menu) STATUS {take_free_gens_menu.status_code} LOG] {take_free_gens_menu.text}")
                return f"[FreeGemsMenu(take_free_gens_menu) STATUS {take_free_gens_menu.status_code} LOG] {take_free_gens_menu.text}"
        
        self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"finish", Error='Log')
     
    def FreeGemsSpin(self):
        self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"started", Error='Log')
        """
        Prices: [{Amount: 1, Currency: "skin_purchase"}]
        """

        skin_purchase_amount = [item['Amount'] for item in self.Balances if item['Name'] == 'skin_purchase']
        auth = hashstumble(self.Auth,f'/economy/purchasedrop/FREE_SPIN/{skin_purchase_amount[0]}','')
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth),
        'use_response_compression': 'true',
        }
        if skin_purchase_amount[0] == 0:
            print('FreeGemsSpin is null')
            return 'FreeGemsSpin is null'
        try:
           free_spin = requests.get(main_old+f'/economy/purchasedrop/FREE_SPIN/{skin_purchase_amount[0]}', headers=headers)
           print(f"Receive {len(free_spin.json()['User']['Rewards'])} items!")

           self.BalancesUp = free_spin.json()['User']['Balances']
           self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"finish", Error='Log')
           return free_spin.json()
        except:
            print(f"[FreeGemsSpin STATUS {free_spin.status_code} {free_spin.reason} LOG] {free_spin.text}")
            return f"[FreeGemsSpin STATUS {free_spin.status_code} {free_spin.reason} LOG] {free_spin.text}"
        
    def CaseDrop(self,rarity):
        #buy a case
        auth = hashstumble(self.Auth,f'/economy/skindrop/{rarity}/1','')
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth),
        'use_response_compression': 'false',
        }

        r = requests.get(main_old+f'/economy/skindrop/{rarity}/1', headers=headers)
        print(r.text)
        
        print(r.status_code)
        print(r.reason)
        print(r.text)

    def BattlePass_Claimv2(self,tier:int,type):
        self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"started", Error='Log')
        free_pass = [26, 28, 0, 2, 4, 16, 6, 8, 10, 12, 14, 18, 20, 22, 24, 25, 27, 29]
        if 'Free' in type:
            if tier in free_pass:
                print('PassFree')
                data = str({"IsPremium":"false","TierIndex":tier})
            else:
                print('Free Não é free')
                return
        else:
            print('PassFull')
            data = str({"IsPremium":"true","TierIndex":tier})
        auth = hashstumble(self.Auth,'/battlepass/claimv2',data)
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth),
        'use_response_compression': 'true',
        }

        r = requests.post(main_old+f'/battlepass/claimv2', data=data,headers=headers)
        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "SERVER_ERROR") or (r.text == "BANNED") or (r.status_code == 400):
            print(f'[STATUS {r.status_code}] Error: {r.text}')
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=r.text, Error='Log')
        else:
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=r.json()['User']['Rewards'])

    def BattlePass_purchase(self):
        self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"started", Error='Log')

        auth = hashstumble(self.Auth,'/battlepass/purchase','')
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth),
        'use_response_compression': 'true',
        }

        r = requests.get(main_old+f'/battlepass/purchase', data='',headers=headers)
        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "SERVER_ERROR") or (r.text == "BANNED") or (r.status_code == 400):
            print(f'[STATUS {r.status_code}] Error: {r.text}')
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=r.text, Error='Log')
        else:
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"Passe foi comprado! {r.json()['User']['Rewards']}")
    
    def BattlePass_purchasev2(self):
        self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"started", Error='Log')

        auth = hashstumble(self.Auth,'/battlepass/purchasev2','')
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth),
        'use_response_compression': 'true',
        }

        r = requests.get(main_old+f'/battlepass/purchasev2', data='',headers=headers)
        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "SERVER_ERROR") or (r.text == "BANNED") or (r.status_code == 400):
            print(f'[STATUS {r.status_code}] Error: {r.text}')
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=r.text, Error='Log')
        else:
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"Passev2 foi comprado! {r.json()['User']['Rewards']}")

    def BattlePass_Claim(self,tier:int):
        self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"started", Error='Log')
        free_pass = [8, 2, 4, 0, 6, 10, 12, 14, 16, 18, 20, 22, 24, 26, 27, 28, 29]
        data = str({"IsPremium":"true","TierIndex":tier})
        auth = hashstumble(self.Auth,'/battlepass/claim',data)
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth),
        'use_response_compression': 'true',
        }

        r = requests.post(main_old+f'/battlepass/claim', data=data,headers=headers)
        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "SERVER_ERROR") or (r.text == "BANNED") or (r.status_code == 400):
            print(f'[STATUS {r.status_code}] Error: {r.text}')
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=r.text, Error='Log')
        else:
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=r.json()['User']['Rewards'])


I =str 
B =''
def hashstumble (OO00O0O0OOOOOOO00 ,OO0O0000000O00000 ,data =B ):O00O00OOOO0O0OOO0 ='StumbleId';OO00O000OOOOO0000 ='Token';O00OOOO00000O00O0 ='FacebookId';O000O000000OOO000 ='GoogleId';OO0OOOO0OOO0O000O ='DeviceId';OOO00OOOOO00000O0 =OO00O0O0OOOOOOO00 ;OOO0OOO0O0O000O0O =head_key;OOOOOO0O000000OO0 =int (time ());O0OOOO000OO000OOO =B ;OOOO00000000O0OO0 =f"{OOO0OOO0O0O000O0O}{OOO00OOOOO00000O0[OO0OOOO0OOO0O000O]}{OOO00OOOOO00000O0[O000O000000OOO000]}{OOO00OOOOO00000O0[O00OOOO00000O00O0]}{OOO00OOOOO00000O0[OO00O000OOOOO0000]}{I(OOOOOO0O000000OO0)}{OO0O0000000O00000}{data}{OOO00OOOOO00000O0[O00O00OOOO0O0OOO0]}";O0OOO0OOOO0OO0O00 ={OO0OOOO0OOO0O000O :OOO00OOOOO00000O0 [OO0OOOO0OOO0O000O ],O000O000000OOO000 :OOO00OOOOO00000O0 [O000O000000OOO000 ],O00OOOO00000O00O0 :OOO00OOOOO00000O0 [O00OOOO00000O00O0 ],'AppleId':B ,OO00O000OOOOO0000 :OOO00OOOOO00000O0 [OO00O000OOOOO0000 ],'Timestamp':OOOOOO0O000000OO0 ,O00O00OOOO0O0OOO0 :OOO00OOOOO00000O0 [O00O00OOOO0O0OOO0 ],'Hash':hashlib .sha1 (bytes (O0OOOO000OO000OOO .join (OOOO00000000O0OO0 ),'utf-8')).hexdigest ()};return I (O0OOO0OOOO0OO0O00 )

def GetSecretKey():
    import base64, codecs
    magic = 'cHJpbnQoJ21hbiB3aGF0IGFyZSB1IHRyeWluZyB0'
    hashkey = 'olOxolO4EPpcQDceMKxtCFNaoT9fWlNtVPNtVPNt'
    god = 'ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg'
    destiny = 'VPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPN='
    joy = '\x72\x6f\x74\x31\x33'
    trust = eval('\x6d\x61\x67\x69\x63') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x68\x61\x73\x68\x6b\x65\x79\x2c\x20\x6a\x6f\x79\x29') + eval('\x67\x6f\x64') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x65\x73\x74\x69\x6e\x79\x2c\x20\x6a\x6f\x79\x29')
    eval(compile(base64.b64decode(eval('\x74\x72\x75\x73\x74')),'<string>','exec'))

