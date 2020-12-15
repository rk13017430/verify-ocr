
import pymongo
from PIL import Image
import requests
from io import BytesIO
userId = "I0AC5EA155B6C4DC0A214BC514309AADA"

# def create_payload(userId):
myclient = pymongo.MongoClient("mongodb://penny:boostersA123@34.236.58.116:27017/verifyer?authSource=admin")
mydb = myclient["verifyer"]
mycol = mydb["document"]
myquery = { "userId": userId }


mydoc = mycol.find(myquery)

for x in mydoc:   
    print(x) 
#         docName = x['docName']
#         url = x['doc'][0]['path']

#     response = requests.get(url)
#     img = Image.open(BytesIO(response.content))
#     img.save("images/"+userId+".png")
#     # print(img.filename)

#     image = "images/"+userId+".png"
#     return image,userId,docName

# print(create_payload("I0AC5EA155B6C4DC0A214BC514309AADA"))

# newvalues = { "$set": { "accuracy": accuracy ,"facePath":filePath,"curatedData":data} }
# mycol.update_one(myquery, newvalues)






# mongodb://penny:boostersA123@34.236.58.116:27017/verifyer?authSource=admin

