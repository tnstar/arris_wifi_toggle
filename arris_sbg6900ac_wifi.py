import requests
import json
from bs4 import BeautifulSoup
import time
wifi_settings = {
    'GetNonce': None,
    'WirelessEnable': 1,
    'OutputPower': 50,
    'Band': 0,
    'NMode': 3,
    'NBandwidth': 20,
    'NSideband': 0,
    'ChannelNumber': 0,
    'restoreWirelessDefaults': 0,
    'commitwlanRadio': 1,
    'scanActions': 0,
    'SelectedRadio': 0
}

user_name = 'username'
user_passwd = 'passwd'
host = 'arris_ip_address'
s = requests.Session()
result = s.get('http://{0}/login.asp'.format(host))
soup = BeautifulSoup(result.content)
chan = soup.findAll('input', id='id_challenge')[0].get('value')
cred = {
    'loginChallenge':chan,
    'loginUsername':user_name,
    'loginPassword':user_passwd
}
s.headers.update(
    {
        'Content-Type':'application/x-www-form-urlencoded',
    }
)
result = s.post('http://{0}/goform/login'.format(host),data=cred)
result = s.get('http://{0}/wlanRadio.asp'.format(host))
soup = BeautifulSoup(result.content)
get_nouce = soup.findAll('input', attrs={'name':'GetNonce','type':'hidden'})[0].get('value')
wifi_settings['GetNonce']=get_nouce
wifi_settings['WirelessEnable']=0
result = s.post('http://192.168.0.1/goform/wlanRadio.pl',data=wifi_settings)
# wait 5 seconds and enable it
time.sleep(5)
wifi_settings['WirelessEnable']=1
result = s.post('http://192.168.0.1/goform/wlanRadio.pl',data=wifi_settings)
