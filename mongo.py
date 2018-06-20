import pymongo
import re


class MongoDB:
    connection = pymongo.MongoClient()
    db = connection['crawler']  # database
    ecommerce = ['amazon','paytm','flipkart']

    def __init__(self, coll_name):
        self.collection = coll_name

    @staticmethod
    def format_query(query):
        l = []
        q = query.lower()
        query = re.sub('[-,/@()]', ' ', q)
        query = query.split()
        for i in query:
            l.append(i.strip())
        l.sort()
        return l

    # data is passed , self will contain the collection
    # data is a list of dictionary
    def insert(self, data):
        c = MongoDB.db[self.collection]
        for i in data:
            dic = c.find_one({'name': i['name']})
            if str(dic) == 'None':  # if name not found,insert it
                c.insert_one(i)

            elif i['url'] != dic['url']:  # if name has diff URL, Update it
                c.update_one({'_id': dic['_id']}, {'$set': {'url': i['url']}})
        MongoDB.connection.close()





    @staticmethod
    def getData(query):
        search_set = []
        for i in MongoDB.ecommerce:  # for each collection
            collection = MongoDB.db[i]  # get collection
            data = collection.find({'name.0':query[0]})  # get Data
            if str(data) == 'None':
                continue
                # crawl the links for this e-commerce

            else:
                for j in data:  # get each result from data(dictionary)
                    name=j['name']  #list
                    c=0
                    for k in range(len(query)):
                        if query[k] not in name:
                            c=1
                            break
                    if c==0:
                        search_set.append(j)
                        break


        return search_set
