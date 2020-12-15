#!pip install flask-ngrok

#!pip install easyocr
from flask import Flask,request, render_template,send_file
#from flask_ngrok import run_with_ngrok

import os
import easyocr
import numpy as np
import cv2
import re
import urllib

reader = easyocr.Reader(['en']) # need to run only once to load model into memory
app = Flask(__name__)
#run_with_ngrok(app)   #starts ngrok when the app is run
PEOPLE_FOLDER = os.path.join('static', 'pics')
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER


def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = urllib.request.urlopen(url).read()
    image = np.asarray(bytearray(resp), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    # return the image
    return image

def get_dob(result):
    try:
       dob_regex = "\d{2}/\d{2}/\d{4}"
       x = re.search(dob_regex, result)
       #y = re.search(dob1_regex, result)
       return x.group()
    except Exception as e:
       print(e)
       return "None"
def get_adhar(data):
    try:
      edata = data
      data = data.split()
      adhar_regex = "\d{4}\s\d{4}\s\d{4}"
      x = re.search(adhar_regex, data)
     # y = re.search(adhars_regex, data)
      return x.group()
    except Exception as e:
      print(e)
      adhars_regex = "\d{4}\_\d{4}\_\d{4}"
      dob_regrex = "\d{2}/\d{2}/\d{4}"
      z = re.search(dob_regrex, edata)
      y = re.search(adhars_regex, edata)
      if y:
          return  y.group()
      if z:
          data = edata.split()
          valueIndex = data.index(z.group())
          print(valueIndex)
          return ' '.join(data[valueIndex + 3:valueIndex + 6])
      else:
          return "none"
def get_gender(data):
    data  = data.lower()

    if "female" in data:
        return "female"
    elif "male" in data:
        return "male"
    else:
        return "None"

def get_name(data):
    try:
       dob_regex = "\d{2}/\d{2}/\d{4}"
       x = re.search(dob_regex, data)
       data = data.split()
       valueIndex = data.index(x.group())
       print(valueIndex)
       return ' '.join(data[valueIndex-5:valueIndex-3])
    except Exception as e:
       print(e)
       return "None"



def check(img):
    data = {
        "NAME": "",
        "Adhar_Number": "",
        "DOB": "",
        "gender": "",
        "identifier": ""
    }

    result = reader.readtext(img,detail = 0)
   # print(" ".join(result))
    result = " ".join(result)
    print(result)
    data['gender'] = get_gender(result)
    data['DOB'] = get_dob(result)
    data['NAME'] = get_name(result)
    data['Adhar_Number'] = get_adhar(result)
    data['identifier'] = get_adhar(result)
    return data
@app.route('/adharocr', methods=['POST'])
def ocr():
   #filestr = requests.get('url')
   req = request.get_json()
   url = req['url']
   img = url_to_image(url)
   res = check(img)
   return res
   # filestr = request.files['img'].read()
   # npimg = numpy.fromstring(filestr, numpy.uint8)
   # img = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)
   # res = check(img)
   # return res
if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5001)

