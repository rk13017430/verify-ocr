import pika
import base64
import json
import config as cfg



#Create a new instance of the Connection object
credentials = pika.PlainCredentials(cfg.queue['userName'],cfg.queue['password'])

connection = pika.BlockingConnection(pika.ConnectionParameters(host=cfg.queue['queueURL'],credentials=credentials))
#Create a new channel with the next available channel number or pass in a channel number to use
channel = connection.channel()

#Declare queue, create if needed. This method creates or checks a queue. When creating a new queue the client can specify various properties that control the durability of the queue and its contents, and the level of sharing for the queue.
channel.queue_declare(queue=cfg.queue['queueName'],durable=True)

doc_img = "resources/pan.jpg"


channel.basic_publish(exchange='', routing_key=cfg.queue['queueName'], body=json.dumps({"userId": "I0AC5EA155B6C4DC0A214BC514309AADA"}))    

print("[x] Sent Document Image")

connection.close()


# PAN Card
# Voter ID