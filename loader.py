import json
from xml.etree.ElementTree import iterparse
import pandas as pd
from tqdm import tqdm_notebook as tqdm
from dateutil.parser import parse
import pytz
from pytz import timezone

class SpotifyAPI():
    
    def __init__(self, root='data'):
        self.root = root + '/spotify/'
        
    def load_searches(self):
        with open(self.root + 'SearchQueries1.json', 'r') as file:
            data = json.load(file)
            return data
    
    def load_streaming(self):
        data = []
        included = set()
        for i in range(0, 15):
            for row in json.load(open(self.root + f'StreamingHistory{i}.json', 'r')):
                if row.get('endTime') not in included:
                    included.add(row.get('endTime'))
                    data.append(row)
                
        data = list(sorted(data, key=lambda row : row.get('endTime')))
        return data
    
    def load_tracks(self):
        with open(self.root + 'YourLibrary.json', 'r') as file:
            return json.load(file).get('tracks')
       
    def help(self):
        print(f"""
        Available Features:
        • load_searches ({len(self.load_searches())} records)
        • load_streaming ({len(self.load_streaming())} records)
        • load_tracks ({len(self.load_tracks())} records)
        """)
        
        
class HealthAPI():
    
    def __init__(self, root='data'):
        self.root = root + '/apple_health_export/'

    def help(self):
        print(f"""
Available Features:
• load_heartbeats()
        """)

    def load_heartbeats(self):
        dataset = []
        for _ , elem in tqdm(iterparse(self.root + 'export.xml')):
            if elem.tag == "Record":
                record = elem.attrib
                if record.get('type') == 'HKQuantityTypeIdentifierHeartRate':
                    c = parse(record.get('creationDate')).astimezone(pytz.utc)
                    s = parse(record.get('startDate')).astimezone(pytz.utc)
                    e = parse(record.get('endDate')).astimezone(pytz.utc)
                    v = record.get('value')
                    dataset.append([c, s, e, v])
                    
        dataset = pd.DataFrame(dataset, columns=['creationDate', 'startDate', 'endDate', 'value'])
        return dataset
    