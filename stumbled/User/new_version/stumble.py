import requests,os,hashlib,json,time as tm
from requests.structures import CaseInsensitiveDict

from time import time 
from random import randint
import datetime,sys

from dotenv import load_dotenv
load_dotenv()

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


class User_debug():
    """
    For testing new apis with new security
    """
    def __init__(self,Version,DeviceId,StumbleId_login='',FacebookId='',GoogleId='',SteamTicket=''):
        self.FacebookId = FacebookId
        self.GoogleId = GoogleId
        self.DeviceId = DeviceId
        self.Ticket = SteamTicket
        self.Version = Version
        self.StumbleId_login = StumbleId_login
        

    def console_user_logs(self,local,log,Error=None):
        if Error == None:
            print(f"{Fore.GREEN}DEBUG [{local}]{Fore.MAGENTA}[{datetime.datetime.now()}]: {Fore.WHITE} {log}")
        elif Error =='Log':
            print(f"{Fore.CYAN}LOG [{local}]{Fore.MAGENTA}[{datetime.datetime.now()}]: {Fore.CYAN} {log}")
        else:
            print(f"{Fore.RED}DEBUG [ERROR]{Fore.GREEN}[{local}]{Fore.MAGENTA}[{datetime.datetime.now()}]: {Fore.WHITE} {log}")

    def Login(self,Proxies=''):
        self.Proxies = Proxies

        print('Login with:', self.Proxies)

        auth = {"Id":193589870,"DeviceId":self.DeviceId,"Version":self.Version,"FacebookId":self.FacebookId,"AppleId":"","GoogleId":self.GoogleId,"Timestamp":1654374366,"AdvertisingId":"","StumbleId":self.StumbleId_login,"SteamTicket":self.Ticket,"Hash":""}

        key = login_key
        deviceid = auth['DeviceId']
        facebook = auth['FacebookId']
        GoogleId = auth['GoogleId']
        device_user_id = ''
        version = auth['Version']
        id_2 = '' 
        stumbleid = auth['StumbleId']
        if len(auth['SteamTicket']) > 2:
            print('Conta steam ticket detectada')
            id_2 = auth['SteamTicket']
        ts = int(time())
        merge_items = f"{key}{deviceid}{facebook}{GoogleId}{device_user_id}{version}{id_2}{ts}{stumbleid}"        
        hashe = hashlib.sha1(bytes(''.join(merge_items), 'utf-8')).hexdigest()           
        jsonA  = {"Id": 193589871,"DeviceId":auth['DeviceId'],'Version': version,"FacebookId":f'{self.FacebookId}',"AppleId":"","GoogleId":f'{self.GoogleId}',"Timestamp":ts, "AdvertisingId": None,"StumbleId":self.StumbleId_login,"SteamTicket":id_2,"Hash":hashe} 
        #print(jsonA)        
        r = requests.post(main_new+user_login, headers={'Content-Type': 'application/json','User-Agent': 'Unity-2020.3.38f1'}, data=json.dumps(jsonA))
        print(r.text)
        if "LOGIN_ERROR" in r:
            tm.sleep(2)
            r = requests.post(main_new+user_login, headers={'Content-Type': 'application/json','User-Agent': 'Unity-2020.3.38f1'}, data=json.dumps(jsonA))
        try:
            self.UserId = r.json()['User']['Id']
        except:
            print('Error: ',r.text)

        Levels = [{"RequiredXP":1000},{"RequiredXP":2000},{"RequiredXP":4000},{"RequiredXP":8000},{"RequiredXP":12000},{"RequiredXP":20000},{"RequiredXP":30000},{"RequiredXP":40000},{"RequiredXP":60000},{"RequiredXP":80000},{"RequiredXP":120000},{"RequiredXP":140000},{"RequiredXP":160000},{"RequiredXP":180000},{"RequiredXP":200000},{"RequiredXP":220000},{"RequiredXP":240000},{"RequiredXP":260000},{"RequiredXP":280000},{"RequiredXP":300000}]
        self.Version = r.json()['User']['Version']
        self.Token = r.json()['User']['Token']
        #self.GoogleId = r.json()['User']['GoogleId']
        #self.FacebookId = r.json()['User']['FacebookId']
        self.StumbleId = r.json()['User']['StumbleId']
        self.Username = r.json()['User']['Username']
        self.SkillRating = r.json()['User']['SkillRating']
        self.Exp = r.json()['User']['Experience']
        self.Level = len([True for req in Levels if req['RequiredXP']<self.Exp])
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
        self.Auth = {'DeviceId': self.DeviceId, 'GoogleId': f'{self.GoogleId}', 'FacebookId': f'{self.FacebookId}', 'AppleId': '', 'Token': self.Token, 'Timestamp': 1657411202,"StumbleId":self.StumbleId,'Hash': 'a'}
        self.videogems_amount = [item['Amount'] for item in r.json()['User']['Balances'] if item['Name'] == 'video_gems'][0]
        self.special_video_amount = [item['Amount'] for item in r.json()['User']['Balances'] if item['Name'] == 'special_video']
           
        self.FreeGemsAmount_get = 8 * self.videogems_amount

        self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"Logged has {Fore.GREEN}{r.json()['User']['Username']} Level: {self.Level}{Fore.WHITE}")
        
        self.FreeGemsAmount = 0
        return r
    
    def ChangeUsername(self,username):
        self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"Arg(username): {username}",Error='Log')
        data = str({"Username":f"{username}"})
        print(data)
        print(self.Auth)
        auth_hash = special_hash_request(self.Auth ,f'/user/update',data)
        print(auth_hash)
        headers = {
        "Content-Type": "application/json;charset=utf-8",
        'authorization': str(auth_hash),
        'use_response_compression': 'false',
        }
        
        r = requests.post(main_old+user_updat, headers=headers,data=data)
        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "BANNED") or (r.text == "SERVER_ERROR") or (r.status_code == 400):
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"{r.text} {r.status_code} {r.reason}",Error='y')
            return {'new_username': f'❌ - Username não alterado\n⛔\n[{r.status_code}] Error log: {r.text}\n⛔'}
        else:
            try:
                self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"[STATUS {r.status_code}] New username: {r.json()['User']['Username']}")
                return {'status':r.status_code, 'new_username': r.json()['User']['Username']}
            except Exception as e:
                print('Error estranho: ', e, r.text,r.reason)
    
    def change_name_v2():
        data = '{"Username":"K031cで"}'
        headers = CaseInsensitiveDict()
        headers["authorization"] = '{"DeviceId":"","GoogleId":"","FacebookId":"","AppleId":"","Token":"","Timestamp":"","StumbleId":"","Hash":""}'
        headers["use_response_compression"] = "true"
        headers["User-Agent"] = "Unity-2020.3.38f1"
        headers["Content-Type"] = "application/json"
        headers["Accept-Encoding"] = "gzip, deflate"
        headers["Content-Length"] = "23"

        resp = requests.post(main_new+'/user/update', headers=headers, data=data)

        print(resp.status_code)

    
    def WinRound(self):
        self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"started", Error='Log')
        round = randint(2, 3) #win or 2place
        #dasow is here ;)
        auth = special_hash_request(self.Auth,f'/round/finishv2/{round}','')
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth),
        'use_response_compression': 'true'}
        r = requests.get(main_old+f'/round/finishv2/{round}', headers=headers)

        try: 
           print(f"Skill: {r.json()['User']['SkillRating']} : XP: {r.json()['User']['Experience']} : Partidas ganhas: {r.json()['User']['Crowns']} : HiddenRating {r.json()['User']['HiddenRating']}")
           print(f"Nivel no passe de batalha: {r.json()['User']['BattlePass']['PassTokens']/100} ({r.json()['User']['BattlePass']['PassTokens']})")
           print("Passe pago?:", r.json()['User']['BattlePass']['HasPurchased'])
           print("Free: ", r.json()['User']['BattlePass']['FreePassRewards'])
           print("Premium: ", r.json()['User']['BattlePass']['PremiumPassRewards'])
        except Exception as e:
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"{r.text, e}", Error='y')

     
    def LinkGoogle(self,GoogleId):
        
        self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"Args: {GoogleId}", Error='Log')
        
        STEAM_AUTH = {"DeviceId":self.DeviceId,"GoogleId":GoogleId,"FacebookId":"","AppleId": '', "Token": self.Token, 'Timestamp': 1657411202,"StumbleId":self.StumbleId,'Hash': 'a'}
        #O certo seria o Steam auth ir com GoogleId e FacebookId de acordo com as informaçções da conta, porém o token aprova a request mesmo com a informação incorreta.
        data = str({"UserId":self.UserId,"Token":self.Token,"FacebookId":"",'GoogleId':GoogleId})#Presta atenção em UserId e Token junto com GoogleId ou Facebook, qualquer erro = Error Token
        auth = special_hash_request(STEAM_AUTH,f'/user/linkgoogle',data)
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
    
        STEAM_AUTH = {"DeviceId":self.DeviceId,"GoogleId":"","FacebookId":FaceboookId,"AppleId": '', "Token": self.Token, 'Timestamp': 1657411202,"StumbleId":self.StumbleId,'Hash': 'a'}
        #O certo seria o Steam auth ir com GoogleId e FacebookId de acordo com as informaçções da conta, porém o token aprova a request mesmo com a informação incorreta.
        data = str({"UserId":self.UserId,"Token":self.Token,"FacebookId":FaceboookId,'GoogleId':""})#Presta atenção em UserId e Token junto com GoogleId ou Facebook, qualquer erro = Error Token
        auth = special_hash_request(STEAM_AUTH,f'/user/linkgoogle',data)
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth),
        'use_response_compression': 'true',
        }     
        r = requests.post(main_old+f'/user/linkfacebook', headers=headers,data=data)
        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "BANNED") or (r.status_code == 400):
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f'[STATUS {r.status_code}] Error: {r.text}', Error='y')
        else:
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"[STATUS {r.status_code}] Faceebok {FaceboookId} has Linked to {r.json()['Username']} {r.text}")
     
    def LinkFacebook_getlinked(self,FaceboookId):
        self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"Args: {FaceboookId}", Error='Log')
    
        STEAM_AUTH = {"DeviceId":self.DeviceId,"GoogleId":"","FacebookId":FaceboookId,"AppleId": '', "Token": self.Token, 'Timestamp': 1657411202,"StumbleId":self.StumbleId,'Hash': 'a'}
        #O certo seria o Steam auth ir com GoogleId e FacebookId de acordo com as informaçções da conta, porém o token aprova a request mesmo com a informação incorreta.
        data = str({"UserId":433576617,"Token":self.Token,"FacebookId":FaceboookId,'GoogleId':FaceboookId})#Presta atenção em UserId e Token junto com GoogleId ou Facebook, qualquer erro = Error Token
        auth = special_hash_request(STEAM_AUTH,f'/user/linkfacebook',data)
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth),
        'use_response_compression': 'true',
        }     
        r = requests.post(main_old+f'/user/linkfacebook?_method=PUT', headers=headers,data=data)
        print(r.text)
        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "BANNED") or (r.status_code == 400):
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f'[STATUS {r.status_code}] Error: {r.text}', Error='y')
        else:
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"[STATUS {r.status_code}] Faceebok {FaceboookId} has Linked to {r.json()['Username']} {r.text}")
     


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
        
        auther = {'DeviceId': self.DeviceId, 'GoogleId': '', 'FacebookId': '', 'AppleId': '', 'Token': self.Token, 'Timestamp': 1657411202, 'StumbleId': self.StumbleId_login,'Hash': '128053146036d1bfcda08eedcc177bb625f90bb1'}

        auth = special_hash_request(auther,f'/user/deleteaccount','')
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth),
        'use_response_compression': 'true',
        }
        r = requests.get(main_old+f'/user/deleteaccount', headers=headers)
        
        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "BANNED") or (r.status_code == 400):
            print(f'[STATUS {r.status_code}] Error: {r.text}')
        else:
            print(f"[STATUS {r.status_code}] Account {self.Username} Has Deleted", r.reason, r.status_code)

     
    def FreeGems(self):
        self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"started", Error='Log')
        """
        prices: [{amount: 1, currency: "video_gems"}, {amount: 1, currency: "video"}]
        rewards: [{max: 8, min: 8, type: "CURRENCY", typeInfo: "gems"}]
        """
        self.FreeGemsAmount = 0
        auth = special_hash_request(self.Auth,'/economy/purchase/free_gems','')
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
            print(free_gems.text)
            
            if 'Update currency would give negative balance' in free_gems.text:
                    print('FreeGems negative balance')
                    return 'FreeGems negative balance'
            
           
            #cada 8 gemas ganhas é gasto 1 video_gems amount em balances com o maximo de 80 gemas ganhas
            self.FreeGemsAmount = 8 * self.videogems_amount

            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f'FreeGemsAmount: {self.FreeGemsAmount}')
        
        except:
            recharg = [item['SecondsPerUnit']/60 for item in free_gems.json()['User']['Balances'] if item['Name'] == 'video_gems']
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"[FreeGems STATUS {free_gems.status_code} LOG] {free_gems.text} Next recharge in {recharg[0]:.2f}", Error='y')
            return f"[FreeGems STATUS {free_gems.status_code} LOG] {free_gems.text} Next recharge in {recharg[0]:.2f} "
        for _ in range(self.videogems_amount):
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
        auth = special_hash_request(self.Auth,'/economy/purchase/video_gems','')
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
    
        auth = special_hash_request(self.Auth,'/economy/purchase/gemvideo_charge','')
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
            auth = special_hash_request(self.Auth,'/economy/purchase/menu_free_gems','')
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
                compa = take_free_gens_menu.json()['User']['Rewards'][0] 
                return f'{compa["Amount"]} {compa["TypeInfo"]}'
            except:
                print(f"[FreeGemsMenu(take_free_gens_menu) STATUS {take_free_gens_menu.status_code} LOG] {take_free_gens_menu.text}")
                return f"[FreeGemsMenu(take_free_gens_menu) STATUS {take_free_gens_menu.status_code} LOG]"
        else:
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"finish", Error='Log')
            return 'Nothing'

    
    def FreeGemsSpin(self):
        self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"started", Error='Log')
        """
        Prices: [{Amount: 1, Currency: "skin_purchase"}]
        """

        skin_purchase_amount = [item['Amount'] for item in self.Balances if item['Name'] == 'skin_purchase']
        auth = special_hash_request(self.Auth,f'/economy/purchasedrop/FREE_SPIN/{skin_purchase_amount[0]}','')
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
           return free_spin.json()['User']['Rewards']
        except:
            print(f"[FreeGemsSpin STATUS {free_spin.status_code} {free_spin.reason} LOG] {free_spin.text}")
            return f"[FreeGemsSpin STATUS {free_spin.status_code} {free_spin.reason} LOG] {free_spin.text}"    
    
    def WinRoundv1_fixsec(self,round:int,Proxies=None):
        #self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"started", Error='Log')
        #round = randint(2, 3) #win or 2place
        auth = special_hash_request(self.Auth,f'/round/finish/{round}','')
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth),
        'use_response_compression': 'true',
        }
        r = requests.get(main_old+f'/round/finish/{round}', headers=headers,proxies=Proxies)

        try:
           information = f"{Fore.LIGHTYELLOW_EX}[FixSecv2.1] {Fore.BLUE}Name:{Fore.WHITE}{r.json()['User']['Username']} {Fore.BLUE}SkillRating:{Fore.GREEN}{r.json()['User']['SkillRating']} {Fore.BLUE}Wins:{Fore.GREEN}{r.json()['User']['Crowns']}{Fore.WHITE}{Fore.RED} HiddenRating:{r.json()['User']['HiddenRating']}"
           print(information)
           #print(f"[{r.json()['User']['Username']}] FixSecv2.1 Skill:{r.json()['User']['SkillRating']} XP:{r.json()['User']['Experience']} Partidas ganhas:{r.json()['User']['Crowns']} HiddenRating: {r.json()['User']['HiddenRating']}")
           #print(f"Nivel no passe de batalha: {r.json()['User']['BattlePass']['PassTokens']/100} ({r.json()['User']['BattlePass']['PassTokens']})")
           #print("Passe pago?:", r.json()['User']['BattlePass']['HasPurchased'])
           #print("Free: ", r.json()['User']['BattlePass']['FreePassRewards'])
           #print("Premium: ", r.json()['User']['BattlePass']['PremiumPassRewards'])
           return r.json()['User']['Crowns']
        except Exception as e:
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"{r.text, e}", Error='y')

    def WinRoundv2_fixsec(self,round:int,Proxies=None):
        #self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"started", Error='Log')
        #round = randint(2, 3) #win or 2place
        auth = special_hash_request(self.Auth,f'/round/finishv2/{round}','')
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth),
        'use_response_compression': 'true',
        }
        r = requests.get(main_old+f'/round/finishv2/{round}', headers=headers,proxies=Proxies)

        try:
           information = f"{Fore.LIGHTYELLOW_EX}[FixSecv2.2] {Fore.BLUE}Name:{Fore.WHITE}{r.json()['User']['Username']} {Fore.BLUE}SkillRating:{Fore.GREEN}{r.json()['User']['SkillRating']} {Fore.BLUE}Wins:{Fore.GREEN}{r.json()['User']['Crowns']}{Fore.RED} HiddenRating:{r.json()['User']['HiddenRating']}"
           print(information)
           #print(f"[{r.json()['User']['Username']}] FixSecv2 Skill:{r.json()['User']['SkillRating']} XP:{r.json()['User']['Experience']} Partidas ganhas:{r.json()['User']['Crowns']} HiddenRating: {r.json()['User']['HiddenRating']}")
           #print(f"Nivel no passe de batalha: {r.json()['User']['BattlePass']['PassTokens']/100} ({r.json()['User']['BattlePass']['PassTokens']})")
           #print("Passe pago?:", r.json()['User']['BattlePass']['HasPurchased'])
           #print("Free: ", r.json()['User']['BattlePass']['FreePassRewards'])
           #print("Premium: ", r.json()['User']['BattlePass']['PremiumPassRewards'])
           return r.json()['User']['Crowns']
        except Exception as e:
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"{r.text, e}", Error='y')

    def WinRound_api(self,round:int,Proxies=None):
        #self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"started", Error='Log')
        #round = randint(2, 3) #win or 2place
        auth = special_hash_request(self.Auth,f'/round/finish/{round}','')
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth),
        'use_response_compression': 'true',
        }
        r = requests.get(main_new+'/round/finish/{round}', headers=headers,proxies=Proxies)

        try:
           information = f"{Fore.LIGHTYELLOW_EX}[FixSecv2] {Fore.BLUE}Name:{Fore.WHITE}{r.json()['User']['Username']} {Fore.BLUE}SkillRating:{Fore.GREEN}{r.json()['User']['SkillRating']} {Fore.BLUE}Wins:{Fore.GREEN}{r.json()['User']['Crowns']}{Fore.RED}HiddenRating: {r.json()['User']['HiddenRating']}"
           print(information)
           #print(f"[{r.json()['User']['Username']}] FixSecv2 Skill:{r.json()['User']['SkillRating']} XP:{r.json()['User']['Experience']} Partidas ganhas:{r.json()['User']['Crowns']} HiddenRating: {r.json()['User']['HiddenRating']}")
           #print(f"Nivel no passe de batalha: {r.json()['User']['BattlePass']['PassTokens']/100} ({r.json()['User']['BattlePass']['PassTokens']})")
           #print("Passe pago?:", r.json()['User']['BattlePass']['HasPurchased'])
           #print("Free: ", r.json()['User']['BattlePass']['FreePassRewards'])
           #print("Premium: ", r.json()['User']['BattlePass']['PremiumPassRewards'])
           return r.json()['User']['Crowns']
        except Exception as e:
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"{r.text, e}", Error='y')
    

        
    def CaseDrop(self,rarity):
        #buy a case
        auth = special_hash_request(self.Auth,f'/economy/skindrop/{rarity}/1','')
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth),
        'use_response_compression': 'false',
        }

        r = requests.get(main_old+f'/economy/skindrop/{rarity}/1', headers=headers)

        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "BANNED") or (r.status_code == 400):
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f'[STATUS {r.status_code}] Error: {r.text}', Error='y')
            return {'CaseDrop': f'❌ - Error em search\n⛔\n[{r.status_code}] Error log: {r.text}\n⛔'}
        else:
            try:
                self.console_user_logs(local=sys._getframe().f_code.co_name, log={'CaseDrop': r.json()['User']['Rewards']})
            except requests.exceptions.JSONDecodeError:
                self.console_user_logs(local=sys._getframe().f_code.co_name, log={'CaseDrop': r.text,'JsonDecodeError':'yes'})

            return {'CaseDrop': r.text}
    
    def PurshaseDrop(self,name):
        #buy a drop
        auth = special_hash_request(self.Auth,f'/economy/purchasedrop/{name}/1','')
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth),
        'use_response_compression': 'false',
        }

        r = requests.get(main_old+f'/economy/purchasedrop/{name}/1', headers=headers)

        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "BANNED") or (r.status_code == 400):
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f'[STATUS {r.status_code}] Error: {r.text}', Error='y')
            return {'PurshaseDrop': f'❌ - Error em search\n⛔\n[{r.status_code}] Error log: {r.text}\n⛔'}
        else:
            try:
                self.console_user_logs(local=sys._getframe().f_code.co_name, log={'PurshaseDrop': r.json()['User']['Rewards']})
            except requests.exceptions.JSONDecodeError:
                self.console_user_logs(local=sys._getframe().f_code.co_name, log={'PurshaseDrop': r.text,'JsonDecodeError':'yes'})

            return {'PurshaseDrop': r.text}
    
    def Purchase(self,name):
        #buy a gacha or somt in PurchasableItems
        auth = special_hash_request(self.Auth,f'/economy/purchase/{name}','')
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth),
        'use_response_compression': 'false',
        }

        r = requests.get(main_new+f'/economy/purchase/{name}', headers=headers)

        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "BANNED") or (r.status_code == 400):
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f'[STATUS {r.status_code}] Error: {r.text}', Error='y')
            return {'Purchase': f'❌ - Error em search\n⛔\n[{r.status_code}] Error log: {r.text}\n⛔'}
        else:
            try:
                self.console_user_logs(local=sys._getframe().f_code.co_name, log={'Purchase': r.json()['User']['Rewards']})
            except requests.exceptions.JSONDecodeError:
                self.console_user_logs(local=sys._getframe().f_code.co_name, log={'Purchase': r.text,'JsonDecodeError':'yes','Reason':r.reason})

            return {'Purchase': r.text}

    def Purchase_gacha(self,name,quantidade:int):
        #buy a gacha or somt in PurchasableItems
        auth = special_hash_request(self.Auth,f'/economy/purchasegacha/{name}/{quantidade}','')
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth),
        'use_response_compression': 'false',
        }

        r = requests.get(main_new+f'/economy/purchasegacha/{name}/{quantidade}', headers=headers)

        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "BANNED") or (r.status_code == 400):
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f'[STATUS {r.status_code}] Error: {r.text}', Error='y')
            return {'Purchase': f'❌ - Error em search\n⛔\n[{r.status_code}] Error log: {r.text}\n⛔'}
        else:
            try:
                self.console_user_logs(local=sys._getframe().f_code.co_name, log={'Purchase_gacha': r.json()['User']['Rewards']})
            except requests.exceptions.JSONDecodeError:
                self.console_user_logs(local=sys._getframe().f_code.co_name, log={'Purchase_gacha': r.text,'JsonDecodeError':'yes','Reason':r.reason})

            return {'Purchase': r.text}


    #/economy/purchase/Bunny_Knight_Bundle
    def Search(self,username):

        data = str({"UserName":f"{username}"})
        author = self.Auth
        print(author)
        author_convert = special_hash_request(author,'/friends/search',data)
        headers = CaseInsensitiveDict()
        headers["authorization"] = str(author_convert)
        headers["use_response_compression"] = "true"
        headers["User-Agent"] = "Unity-2020.3.38f1"
        headers["Content-Type"] = "application/json"

        headers["Accept-Encoding"] = "gzip, deflate"
        headers["Content-Length"] = "19"


        resp = requests.post(main_new+'/friends/search', headers=headers, data=data,verify=False)

        print(resp.text)
    
    def SetSkin(self,skinid):
        
        data = str({"Category":"Skin","ItemId":f"{skinid}"})
        author = self.Auth
        print(author)
        author_convert = special_hash_request(author,'/user/inventory/selection',data)
        headers = CaseInsensitiveDict()
        headers["authorization"] = str(author_convert)
        headers["use_response_compression"] = "true"
        headers["User-Agent"] = "Unity-2020.3.38f1"
        headers["Content-Type"] = "application/json"
        headers["Accept-Encoding"] = "gzip, deflate"
        headers["Content-Length"] = "19"


        resp = requests.post(main_new+'/user/inventory/selection', headers=headers, data=data,verify=False)
        print(resp.text, resp.reason,resp.status_code)


    def Friends(self):
        auth_hash = special_hash_request(self.Auth ,f'/friends','')
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth_hash),
        'use_response_compression': 'false',
        }
        
        r = requests.get(main_new+'/friends', headers=headers,verify=False)
        print(r.text)
        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "BANNED") or (r.status_code == 400):
            return {'friends': f'❌ - Error em search\n⛔\n[{r.status_code}] Error log: {r.text}\n⛔'}
        else:
            return {'friends': r.json()}
    
    def FriendsDelete(self,userid):
        auth_hash = special_hash_request(self.Auth ,f'/friends/{userid}','')
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth_hash),
        'use_response_compression': 'false',
        }
        
        r = requests.delete(main_new+f'/friends/{userid}', headers=headers,verify=False)
        print(r.text)
        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "BANNED") or (r.status_code == 400):
            print({'request_to': f'❌ - Error em search\n⛔\n[{r.status_code}] Error log: {r.text}\n⛔'})
            return {'request_to': f'❌ - Error em search\n⛔\n[{r.status_code}] Error log: {r.text}\n⛔'}
        else:
            print({'request_to': f'{r.text,r.status_code,r.reason}'})
            return {'request_to': f'{r.text,r.status_code,r.reason}'}

    def Friend_sendrequest(self,userid):
        data = str({"UserId":userid})
        auth_hash = special_hash_request(self.Auth ,f'/friends/request',data)
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth_hash),
        'use_response_compression': 'false',
        }
        
        r = requests.post(main_new+f'/friends/request', headers=headers,data=data,verify=False)
        print(r.text)
        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "BANNED") or (r.status_code == 400):
            print({'request_to': f'❌ - Error em search\n⛔\n[{r.status_code}] Error log: {r.text}\n⛔'})
            return {'request_to': f'❌ - Error em search\n⛔\n[{r.status_code}] Error log: {r.text}\n⛔'}
        else:
            print({'request_to': f'{r.text,r.status_code,r.reason}'})
            return {'request_to': f'{r.text,r.status_code,r.reason}'}
   
    def friend_getrequests(self):
        auth_hash = special_hash_request(self.Auth ,f'/friends/request','')
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth_hash),
        'use_response_compression': 'false',
        }
        
        r = requests.get(main_new+f'/friends/request', headers=headers,verify=False)
        print(r.text)
        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "BANNED") or (r.status_code == 400):
            print({'requests': f'❌ - Error em search\n⛔\n[{r.status_code}] Error log: {r.text}\n⛔'})
            return {'requests': f'❌ - Error em search\n⛔\n[{r.status_code}] Error log: {r.text}\n⛔'}
        else:
            print({'requests': r.json(),'status':r.status_code,'reason':r.reason})
            return {'requests': r.json(),'status':r.status_code,'reason':r.reason}
    def Regretfriend_request(self, userid:int):
        data = str({"UserId":userid})
        auth_hash = special_hash_request(self.Auth ,f'/friends/request/decline',data)
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth_hash),
        'use_response_compression': 'false',
        }
        
        r = requests.delete(main_new+f'/friends/request/decline', headers=headers,data=data)
        print(r.text)
        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "BANNED") or (r.status_code == 400):
            print({'request_to': f'❌ - Error em search\n⛔\n[{r.status_code}] Error log: {r.text}\n⛔'})
            return {'request_to': f'❌ - Error em search\n⛔\n[{r.status_code}] Error log: {r.text}\n⛔'}
        else:
            print({'request_to': f'{r.text,r.status_code,r.reason}'})
            return {'request_to': f'{r.text,r.status_code,r.reason}'}
    
    def FriendAccepted(self,userid):
        data = str({"UserId":userid})   
        auth_hash = special_hash_request(self.Auth ,f'/friends/request/accept',data)
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth_hash),
        'use_response_compression': 'false',
        }
        
        r = requests.post(main_new+f'/friends/request/accept', headers=headers,data=data,verify=False)
        print(r.text)
        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "BANNED") or (r.status_code == 400):
            print({'request_to': f'❌ - Error em search\n⛔\n[{r.status_code}] Error log: {r.text}\n⛔'})
            return {'request_to': f'❌ - Error em search\n⛔\n[{r.status_code}] Error log: {r.text}\n⛔'}
        else:
            print({'request_to': f'{r.text,r.status_code,r.reason}'})
            return {'request_to': f'{r.text,r.status_code,r.reason}'}
    
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
        auth = special_hash_request(self.Auth,'/battlepass/claimv2',data)
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

        auth = special_hash_request(self.Auth,'/battlepass/purchase','')
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

        auth = special_hash_request(self.Auth,'/battlepass/purchasev2','')
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

    def BattlePass_Claim(self,tier:int,type):
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
        auth = special_hash_request(self.Auth,'/battlepass/claim',data)
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

    def buyGemsSteam(self,iapid):
        self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"started", )
        data = str({"IapName":f"{iapid}","LanguageCode":"portuguese"})
        auth = special_hash_request(self.Auth,'/economy/steam/inittxnv3/',data)
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth),
        'use_response_compression': 'true',
        }

        r = requests.post(main_new+f'/economy/steam/inittxnv3/',data=data,headers=headers)
        #print(r.text,r.reason)
        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "SERVER_ERROR") or (r.text == "BANNED") or (r.status_code == 400):
            print(f'[STATUS {r.status_code}] Error: {r.text}')
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=r.text, Error='Log')
        else:
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"Steam buy ticket: {r.text}")
            return r.text
    
    def buyGemsSteamOrder_v1(self,orderid:int):
        self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"started", )

        auth = special_hash_request(self.Auth,f'/economy/steam/finalizetxn/{orderid}')
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth),
        'use_response_compression': 'true',
        }

        r = requests.get(main_new+'/economy/steam/finalizetxn/{orderid}', headers=headers)
        #print(r.text)
        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "SERVER_ERROR") or ('SteamException' in r.text)or (r.text == "BANNED") or (r.status_code == 400):
            print(f'[STATUS {r.status_code}] Error: {r.text}')
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=r.text, Error='Log')
        else:
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"Steam ticket rewards log! {r.json()['User']['Rewards']}")


    def buyGemsSteamOrder(self,orderid:int):
        self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"started", )

        auth = special_hash_request(self.Auth,f'/economy/steam/finalizetxnv2/{orderid}')
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth),
        'use_response_compression': 'true',
        }

        r = requests.get(main_new+'/economy/steam/finalizetxnv2/{orderid}', headers=headers)
        #print(r.text)
        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "SERVER_ERROR") or ('SteamException' in r.text)or (r.text == "BANNED") or (r.status_code == 400):
            print(f'[STATUS {r.status_code}] Error: {r.text}')
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=r.text, Error='Log')
        else:
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"Steam ticket rewards log! {r.json()['User']['Rewards']}")

    def purchaserandom(self,tier:int):
        self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"started", Error='Log')
        print('compra skins random custa 240 gemaw tier 5')
        auth = special_hash_request(self.Auth,f'/economy/purchaserandomskinv4/{tier}')
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth),
        'use_response_compression': 'true',
        }
        r = requests.get(main_old+f'/economy/purchaserandomskinv4/{tier}',headers=headers)
        print(r.text,r.reason)
        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "SERVER_ERROR") or (r.text == "BANNED") or (r.status_code == 400):
            print(f'[STATUS {r.status_code}] Error: {r.text}')
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=r.text, Error='Log')
        else:
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=r.json()['User']['Rewards'])

    def buyGemsMobile(self):
        self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"started", Error='Log')
        print('compra skins random custa 240 gemaw tier 5')
        auth = special_hash_request(self.Auth,f'/economy/purchase/gem_pack2')
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth),
        'use_response_compression': 'true',
        }
        r = requests.get(main_old+f'/economy/purchase/gem_pack2',headers=headers)
        print(r.text,r.reason)
        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "SERVER_ERROR") or (r.text == "BANNED") or (r.status_code == 400):
            print(f'[STATUS {r.status_code}] Error: {r.text}')
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=r.text, Error='Log')
        else:
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=r.json()['User']['Rewards'])

    def partyinvite(self,partyid,userids:list):
        #user ids = whatid do pusher
        data = str({"UserIds":userids,"PhotonAppId":"795799b9-486c-4ef9-b5a9-7b80278e58af","PhotonRoomCode":partyid,"PhotonRegion":"SA"})
        auth_hash = special_hash_request(self.Auth ,f'/party/invite',data)
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth_hash),
        'use_response_compression': 'false',
        }
        r = requests.post(main_new+f'/party/invite', headers=headers,data=data,verify=False)
        print(r.text)
        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "BANNED") or (r.status_code == 400):
            print({'request_to': f'❌ - Error em search\n⛔\n[{r.status_code}] Error log: {r.text}\n⛔'})
            return {'request_to': f'❌ - Error em search\n⛔\n[{r.status_code}] Error log: {r.text}\n⛔'}
        else:
            print({'request_to': f'{r.text,r.status_code,r.reason}'})
            return {'request_to': f'{r.text,r.status_code,r.reason}'}

    def partycancel(self,partyid,userids:list):
        #user ids = whatid do pusher
        data = str({"UserIds":userids,"PhotonAppId":"795799b9-486c-4ef9-b5a9-7b80278e58af","PhotonRoomCode":partyid,"PhotonRegion":"SA"})
        auth_hash = special_hash_request(self.Auth ,f'/party/cancel',data)
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth_hash),
        'use_response_compression': 'false',
        }
        r = requests.post(main_new+f'/party/cancel', headers=headers,data=data,verify=False)
        print(r.text)
        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "BANNED") or (r.status_code == 400):
            print({'request_to': f'❌ - Error em search\n⛔\n[{r.status_code}] Error log: {r.text}\n⛔'})
            return {'request_to': f'❌ - Error em search\n⛔\n[{r.status_code}] Error log: {r.text}\n⛔'}
        else:
            print({'request_to': f'{r.text,r.status_code,r.reason}'})
            return {'request_to': f'{r.text,r.status_code,r.reason}'}
    
    def authorize(self):
        data = str({"channel_name":"private-user-56765573","socket_id":"7150.1616399"})
        auth_hash = special_hash_request(self.Auth ,f'/pusher/authorize',data)
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth_hash),
        'use_response_compression': 'false',
        }
        r = requests.post(main_new+f'/pusher/authorize', headers=headers,data=data,verify=False)
        print(r.text)
        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "BANNED") or (r.status_code == 400):
            print({'request_to': f'❌ - Error em search\n⛔\n[{r.status_code}] Error log: {r.text}\n⛔'})
            return {'request_to': f'❌ - Error em search\n⛔\n[{r.status_code}] Error log: {r.text}\n⛔'}
        else:
            print({'request_to': f'{r.text,r.status_code,r.reason}'})
            return {'request_to': f'{r.text,r.status_code,r.reason}'}
    
    def autheticate(self,socket='7308.574987'):
        data = str({"channel_name":"private-user-56765573","socket_id":socket})#7150.1616354
        auth_hash = special_hash_request(self.Auth ,f'/pusher/authenticate',data)
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth_hash),
        'use_response_compression': 'false',
        }
        r = requests.post(main_new+f'/pusher/authenticate', headers=headers,data=data,verify=False)
        print(r.text)
        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "BANNED") or (r.status_code == 400):
            print({'request_to': f'❌ - Error em search\n⛔\n[{r.status_code}] Error log: {r.text}\n⛔'})
            return {'request_to': f'❌ - Error em search\n⛔\n[{r.status_code}] Error log: {r.text}\n⛔'}
        else:
            print({'request_to': f'{r.text,r.status_code,r.reason}'})
            return {'request_to': f'{r.text,r.status_code,r.reason}'}

    def sendAge(self,age:int):
        #user ids = whatid do pusher
        data = str({"age":age})
        auth_hash = special_hash_request(self.Auth ,f'/user/age',data)
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth_hash),
        'use_response_compression': 'false',
        }
        r = requests.post(main_new+f'/user/age', headers=headers,data=data,verify=False)
        print(r.text)
        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "BANNED") or (r.status_code == 400):
            print({'request_to': f'❌ - Error em search\n⛔\n[{r.status_code}] Error log: {r.text}\n⛔'})
            return {'request_to': f'❌ - Error em search\n⛔\n[{r.status_code}] Error log: {r.text}\n⛔'}
        else:
            print({'request_to': f'{r.text,r.status_code,r.reason}'})
            return {'request_to': f'{r.text,r.status_code,r.reason}'}
    
    def Userinfo(self):
        #user ids = whatid do pusher
        
        auth_hash = special_hash_request(self.Auth ,f'/user/')
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth_hash),
        'use_response_compression': 'false',
        }
        r = requests.post(main_new+f'/user/', headers=headers)
        print(r.text)
        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "BANNED") or (r.status_code == 400):
            print({'request_to': f'❌ - Error em search\n⛔\n[{r.status_code}] Error log: {r.text}\n⛔'})
            return {'request_to': f'❌ - Error em search\n⛔\n[{r.status_code}] Error log: {r.text}\n⛔'}
        else:
            print({'request_to': f'{r.text,r.status_code,r.reason}'})
            return {'request_to': f'{r.text,r.status_code,r.reason}'}

    def Userrefresh(self):
        #user ids = whatid do pusher
        
        auth_hash = special_hash_request(self.Auth ,f'/user/refresheconomy')
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth_hash),
        'use_response_compression': 'false',
        }
        r = requests.get(main_new+f'/user/refresheconomy', headers=headers)
        print(r.text)
        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "BANNED") or (r.status_code == 400):
            print({'request_to': f'❌ - Error em search\n⛔\n[{r.status_code}] Error log: {r.text}\n⛔'})
            return {'request_to': f'❌ - Error em search\n⛔\n[{r.status_code}] Error log: {r.text}\n⛔'}
        else:
            print({'request_to': f'{r.text,r.status_code,r.reason}'})
            return {'request_to': f'{r.text,r.status_code,r.reason}'}


    def purchaseskinv2(self,skinid):
        #user ids = whatid do pusher

        auth_hash = special_hash_request(self.Auth ,f'/economy/purchaseskinv2/{skinid}')
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth_hash),
        'use_response_compression': 'false',
        }
        r = requests.get(main_old+f'/economy/purchaseskinv2/{skinid}', headers=headers)
        
        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "SERVER_ERROR") or (r.text == "BANNED") or (r.status_code == 400):
            print(f'[STATUS {r.status_code}] Error: {r.text}')
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=r.text, Error='Log')
        else:
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=r.json()['User']['Rewards'])

    def purchaseofferskin(self,skinid):
        #user ids = whatid do pusher
        print('Only works in kitkabackend in skins range SKIN1-SKIN76')
        auth_hash = special_hash_request(self.Auth ,f'/economy/purchaseofferskin/{skinid}')
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth_hash),
        'use_response_compression': 'false',
        }
        r = requests.get(main_old+f'/economy/purchaseofferskin/{skinid}', headers=headers)
       
        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "SERVER_ERROR") or (r.text == "BANNED") or (r.status_code == 400):
            print(f'[STATUS {r.status_code}] Error: {r.text}')
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=r.text, Error='Log')
        else:
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=r.json()['User']['Rewards'])

I =str 
B =''
def special_hash_request (OO00O0O0OOOOOOO00 ,OO0O0000000O00000 ,data =B ):O00O00OOOO0O0OOO0 ='StumbleId';OO00O000OOOOO0000 ='Token';O00OOOO00000O00O0 ='FacebookId';O000O000000OOO000 ='GoogleId';OO0OOOO0OOO0O000O ='DeviceId';OOO00OOOOO00000O0 =OO00O0O0OOOOOOO00 ;OOO0OOO0O0O000O0O =head_key;OOOOOO0O000000OO0 =int (time ());O0OOOO000OO000OOO =B ;OOOO00000000O0OO0 =f"{OOO0OOO0O0O000O0O}{OOO00OOOOO00000O0[OO0OOOO0OOO0O000O]}{OOO00OOOOO00000O0[O000O000000OOO000]}{OOO00OOOOO00000O0[O00OOOO00000O00O0]}{OOO00OOOOO00000O0[OO00O000OOOOO0000]}{I(OOOOOO0O000000OO0)}{OO0O0000000O00000}{data}{OOO00OOOOO00000O0[O00O00OOOO0O0OOO0]}";O0OOO0OOOO0OO0O00 ={OO0OOOO0OOO0O000O :OOO00OOOOO00000O0 [OO0OOOO0OOO0O000O ],O000O000000OOO000 :OOO00OOOOO00000O0 [O000O000000OOO000 ],O00OOOO00000O00O0 :OOO00OOOOO00000O0 [O00OOOO00000O00O0 ],'AppleId':B ,OO00O000OOOOO0000 :OOO00OOOOO00000O0 [OO00O000OOOOO0000 ],'Timestamp':OOOOOO0O000000OO0 ,O00O00OOOO0O0OOO0 :OOO00OOOOO00000O0 [O00O00OOOO0O0OOO0 ],'Hash':hashlib .sha1 (bytes (O0OOOO000OO000OOO .join (OOOO00000000O0OO0 ),'utf-8')).hexdigest ()};return I (O0OOO0OOOO0OO0O00 )

def GetSecretKey():
    import base64, codecs
    magic = 'cHJpbnQoJ21hbiB3aGF0IGFyZSB1IHRyeWluZyB0'
    hashkey = 'olOxolO4EPpcQDceMKxtCFNaoT9fWlNtVPNtVPNt'
    god = 'ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg'
    destiny = 'VPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPN='
    joy = '\x72\x6f\x74\x31\x33'
    trust = eval('\x6d\x61\x67\x69\x63') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x68\x61\x73\x68\x6b\x65\x79\x2c\x20\x6a\x6f\x79\x29') + eval('\x67\x6f\x64') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x65\x73\x74\x69\x6e\x79\x2c\x20\x6a\x6f\x79\x29')
    eval(compile(base64.b64decode(eval('\x74\x72\x75\x73\x74')),'<string>','exec'))