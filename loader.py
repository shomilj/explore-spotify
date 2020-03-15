import json

class SpotifyAPI():
    
    def __init__(self, root='data'):
        self.root = root + '/spotify/'
        
    def load_searches(self):
        with open(self.root + 'SearchQueries.json', 'r') as file:
            data = json.load(file)
            return data
    
    def load_streaming(self):
        data0 = json.load(open(self.root + 'StreamingHistory0.json', 'r'))
        data1 = json.load(open(self.root + 'StreamingHistory1.json', 'r'))
        data2 = json.load(open(self.root + 'StreamingHistory2.json', 'r'))
        return data0 + data1 + data2
    
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
        
        
class HealthLoader():
    
    def __init__(self, root='/data'):
        self.root = root + '/apple_health_export/'
    
    