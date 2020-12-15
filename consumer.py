import pika

import sys
import base64
import json
from digilib import OCR
import config as cfg
import pymongo
from PIL import Image
import requests
from io import BytesIO
from test.ela import ela
from test.watermark import watermark_apply
import shutil

credentials = pika.PlainCredentials(cfg.queue['userName'],cfg.queue['password'])

connection = pika.BlockingConnection(pika.ConnectionParameters(host=cfg.queue['queueURL'],credentials=credentials))

channel = connection.channel()

channel.queue_declare(queue=cfg.queue['queueName'],durable=True)

def create_payload(userId):
    myclient = pymongo.MongoClient(cfg.mongo['con_string'])
    mydb = myclient[cfg.mongo["db"]]
    mycol = mydb[cfg.mongo["collection"]]
    myquery = { "userId": userId }

    mydoc = mycol.find(myquery)
    
    for x in mydoc:    
        docName = x['docName']
        url = x['doc'][0]['path']
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img.save("docs/"+userId+".png")

    image = "docs/"+userId+".png"
    return image,userId,docName

def callback(ch, method, properties, body):
    body = json.loads(body)
    image,userId,docName = create_payload(body['userId'])
    if cfg.other["watermark"] == "true":
        ela_value = ela(image)
        if ela_value >24:
            watermark_apply(image,"watermark/"+userId+".png","MORPHED")
        else:
            watermark_apply(image,"watermark/"+userId+".png","TESTED")

        shutil.copy("watermark/"+userId+".png", cfg.other["processedDocPath"])

        watermark_path = cfg.other["processedDocHost"]+userId+".png"
    else:
        watermark_path = "None"

    
    OCR.performOCR(image,userId,docName,watermark_path)
    
    print(" [x] Received") 

channel.basic_consume(queue=cfg.queue['queueName'], on_message_callback=callback, auto_ack=True)

print(' [*] Consumer is waiting for messages. To exit press CTRL+C')

channel.start_consuming()
