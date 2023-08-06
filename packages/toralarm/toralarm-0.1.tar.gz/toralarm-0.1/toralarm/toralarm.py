'''
Created on 07.12.2016

@author: LukeSkywalker92
'''

import requests
import json

class Toralarm(object):
    '''
    classdocs
    '''

    def __init__(self):
        self.url_main = 'https://ta4-data.de/ta/data/competitions/'
        self.url_table = '/table'
        self.url_standings = '/matches/round/'
        
        self.headers = {
            'Host': 'ta4-data.de',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'User-Agent': 'TorAlarm/20161201 CFNetwork/808.1.4 Darwin/16.1.0',
            'Accept-Language': 'de-de',
            'Accept-Encoding': 'gzip',
            'Content-Length': '49',
        }
        
        self.data = '''{"lng":"de-DE","device_type":0,"decode":"decode"}'''
        
        
    def get_table(self, league):
        
        response = requests.request(
            method='POST',
            url=self.url_main+str(league)+self.url_table,
            headers= self.headers,
            data=self.data,
        )
        
        return json.loads(response.text)["data"][0]["table"]
    
    def get_standings(self, league, round_number=0):
        
        response = requests.request(
            method='POST',
            url=self.url_main+str(league)+self.url_standings+str(round_number),
            headers= self.headers,
            data=self.data,
        )
        
        return json.loads(response.text)
    
if __name__ == "__main__":
    ta = Toralarm()
    print json.dumps(ta.get_standings(35), indent=4, sort_keys=True)