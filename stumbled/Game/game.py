import requests,os,hashlib,json,time as tm
from requests.structures import CaseInsensitiveDict
from time import time 
from random import randint
import datetime,sys

from dotenv import load_dotenv
load_dotenv()

user_login = os.getenv('user_login')
user_edit = os.getenv('user_edit')
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


defaultheader = {'Content-Type': 'application/json','use_response_compression': 'true'}
class Game():
    def __init__(self):
        self.Version = '0.44'
    
    
    def console_user_logs(self,local,log,Error=None):
        if Error == None:
            print(f"{Fore.GREEN}[{local}]{Fore.MAGENTA}[{datetime.datetime.now()}]: {Fore.WHITE} {log}")
        elif Error =='Log':
            print(f"{Fore.CYAN}[{local}]{Fore.MAGENTA}[{datetime.datetime.now()}]: {Fore.CYAN} {log}")
        else:
            print(f"{Fore.RED}[ERROR]{Fore.GREEN}[{local}]{Fore.MAGENTA}[{datetime.datetime.now()}]: {Fore.WHITE} {log}")
      
    def shared(self):
        r = requests.get(main_old+f'/shared/0/LIVE')
        self.DisableForDevices = r.json()['AdSettings']['DisableForDevices']
        self.Animations = r.json()['Animations_v2']
        self.BackendUrl = r.json()['BackendUrl']
        self.BattlePass = r.json()['BattlePass']
        self.BattlePassRotation = r.json()['BattlePassRotation']
        self.Currencies = r.json()['Currencies']['General']
        self.CustomPartySettings = r.json()['CustomPartySettings']
        self.Emotes = r.json()['Emotes_v2']
        self.Footsteps = r.json()['Footsteps_v2']
        self.BattlePasses = r.json()['BattlePasses']
        self.RoundLevels_v2 = r.json()['RoundLevels_v2']
        self.Skins_v4 = r.json()['Skins_v4']
        self.RoundRewards = r.json()['RoundRewards']
        self.PurchasableItems = r.json()['PurchasableItems']
        self.ShopDef = r.json()['ShopDef']
        self.SharedVersion = r.json()['_SharedVersion']
        self.Offers_v2 = r.json()['ShopDef']['Offers_v2']
        self.Gachas = r.json()['ShopDef']['Gachas']
        
        names = ['video','remove_ads','gems','video_gems','special_video','skin_charge','skin_purchase','gem_charge','dust']
        balances_info = [f"{item['Name'].upper()} ({item['DefaultAmount']}/{item['MaxAmount']}|{item['SecondsPerUnit']/60:.2f}(value / 60)" for item in self.Currencies if item['Name'] in names]

        ##{'DefaultAmount': 101, 'MaxAmount': 0, 'Name': 'coins', 'SecondsPerUnit': 0, 'UnitCost': 0.1}

        infos = (f'Backend_url: {self.BackendUrl}\n'
        f'Animations: {len(self.Animations)} (Last animation: {self.Animations[-1]["ID"]}[Hidden: {self.Animations[-1]["Hidden"]}|Name: {self.Animations[-1]["FriendlyName"]}])\n'
        f'BattlePass Updated: {self.BattlePassRotation[-1]} (Can be bugged)\n'
        f'Currencies: [Name(DefaultAmount/Max|SecondsPerUnit)] {balances_info}\n'
        f'CustomPartySettings: Nada\n'
        f'Emotes: {len(self.Emotes)} (Last emote: {self.Emotes[-1]["ID"]}[Hidden: {self.Emotes[-1]["Hidden"]}|Name: {self.Emotes[-1]["FriendlyName"]}]|InternalID: {self.Emotes[-1]["InternalID"]}])\n'
        f'Footsteps: {len(self.Footsteps)} (Last footstep: {self.Footsteps[-1]["ID"]}[Hidden: {self.Footsteps[-1]["Hidden"]}|Name: {self.Footsteps[-1]["FriendlyName"]}])\n'
        f'_SharedVersion: {self.SharedVersion}')
        self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"{infos} {r.status_code} {r.reason}")
        return infos
      
    def rank(self,min=0,max=100,country='',type=''):
        #/highscore/rank/list? - skillrating rank
        #/highscore/crowns/list - crowns/wins rank
        r = requests.get(main_old+f'/highscore/{type}/list?start={min}&count={max}&country={country}')
        self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"{r.text.encode('utf-8')[0:10]} {r.status_code} {r.reason}")
        return r.json()
        
    def Search(self,username):
        device_ids = ['11b0926e8ffc2c959bdb7553b49740a6']
        login_data = {"Id":994949995,"DeviceId":device_ids[randint(0,3)],"Version":'0.37',"FacebookId":'',"AppleId":"","GoogleId":'',"Timestamp":1654374364,"AdvertisingId":"","SteamTicket":"","Hash":""}

        r = requests.post(main_old+f'/user/login', headers=defaultheader,data=str(login_data))
        Levels = [{"RequiredXP":1000},{"RequiredXP":2000},{"RequiredXP":4000},{"RequiredXP":8000},{"RequiredXP":12000},{"RequiredXP":20000},{"RequiredXP":30000},{"RequiredXP":40000},{"RequiredXP":60000},{"RequiredXP":80000},{"RequiredXP":120000},{"RequiredXP":140000},{"RequiredXP":160000},{"RequiredXP":180000},{"RequiredXP":200000},{"RequiredXP":220000},{"RequiredXP":240000},{"RequiredXP":260000},{"RequiredXP":280000},{"RequiredXP":300000}]
        self.Exp = r.json()['User']['Experience']
        self.Level =len([True for req in Levels if req['RequiredXP']<self.Exp])

        self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"Logged has {Fore.GREEN}{r.json()['User']['Username']} Country:{r.json()['User']['Country']}Level:{self.Level}{Fore.WHITE} Crowns:{r.json()['User']['Crowns']}")
        self.Auth = {'DeviceId': r.json()['User']['DeviceId'], 'GoogleId': f"{r.json()['User']['GoogleId']}", 'FacebookId': f"{r.json()['User']['FacebookId']}", 'AppleId': '', 'Token': r.json()['User']['Token'], 'Timestamp': 1657411202,'Hash': '128053146036d1bfcda08eedcc177bb625f90bb1'}

        data = str({"userName":f"{username}"})
        auth_hash = hashstumble(self.Auth ,f'/friends/search',data)
        headers = {
        'Content-Type': 'application/json',
        'authorization': str(auth_hash),
        'use_response_compression': 'false',
        }
        
        r = requests.post(main_new+f'/friends/search', headers=headers,data=data,verify=False)
        if (r.status_code == 403) or (r.status_code == 404) or (r.text == "BANNED") or (r.status_code == 400) or (r.status_code == 401):
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"{r.text.encode('utf-8')} {r.status_code} {r.reason}", Error='y')
            return {'status':r.status_code, 'new_search': f'Um erro aconteceu, {r.reason}'}
        else:
            self.console_user_logs(local=sys._getframe().f_code.co_name, log=f"{r.text.encode('utf-8')} {r.status_code} {r.reason}")
            return {'status':r.status_code, 'new_search': r.json()}


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

