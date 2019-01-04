import pymongo

class Database:

    cursor = ""
    def __init__(self,db_server):
        self.cursor = pymongo.MongoClient(db_server, 27017).net_ease
       
    def insert_song(self, id):
        lst = list(self.cursor.song.find({'id':id}))
        if len(lst) > 0:
            print('repeat')
            return
        self.cursor.song.insert_one({'id':id})
    
    def get_one_song_id(self):
        return list(self.cursor.song.aggregate([{ '$sample': { 'size': 1 } }]))[0]['id']
    
    def insert_one_user(self, uid):
        lst = list(self.cursor.song.find({'uid':uid}))
        if len(lst) > 0:
            print('repeat')
            return
        self.cursor.user.insert_one({'uid':uid})
    
    def get_one_user(self):
        self.cursor.song.find_one()

        