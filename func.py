from settings import database
import pymongo


async def get(statement: str, **kwargs):
    conn = pymongo.MongoClient("mongodb://{}:{}/".format(database.get('host'), database.get('port')))
    mydb = conn["test"]
    filter = {'store': '', 'stock': {'branch': kwargs.get('branch')}}
    feild = {'_id': 0}
    find = mydb[statement].find(filter.get(statement), feild)
    result = []
    for x in find:
        data = x
        result.append(data)
    return result
