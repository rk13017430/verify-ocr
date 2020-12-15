mysql = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "",
    "database": "verifyer-me",
    "storagPath": "verifyer/",
    "CTPN_config": "CTPN_AI/ctpn/text.yml"
}

queue = {
    "queueURL": "34.236.58.116",
    "queueName": "document_Queue",
    "queueRoute": "OCRQueue",
    "userName":"admin",
    "password":"boostersA123"
}


mongo = {
    "con_string":"mongodb://penny:boostersA123@34.236.58.116:27017/verifyer?authSource=admin",
    "db":"verifyer",
    "collection":"document"
}

other ={
    "processedDocPath":"/var/www/html/processedDoc/",
    "processedDocHost":"localhost/processedDoc/",
    "watermark":"false"

}