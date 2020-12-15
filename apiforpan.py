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
def get_pan(data):
    try:
      edata = data
      pan_regex = "[A-Z]{5}[0-9]{4}[A-Z]{1}"
      x = re.search(pan_regex, data)
      return x.group()
    except Exception as e:
      print(e)
      dob_regex = "\d{2}/\d{2}/\d{4}"
      x = re.search(dob_regex, edata)
      if x:
          data = edata.split()
          valueIndex = data.index(x.group())
          print(valueIndex)
          return ' '.join(data[valueIndex +4:valueIndex+5])
      else:
          return "None"
def get_dob(result):
    try:
      dob_regex = "\d{2}/\d{2}/\d{4}"
      x = re.search(dob_regex, result)
      return x.group()
    except Exception as e:
      print(e)
      return "None"
def get_name(data):
    try:
      edata = data
      data = data.split()
      valueIndex = data.index("INDIA")
      return ' '.join(data[valueIndex+1:valueIndex+3])
    except Exception as e:
      print(e)
      dob_regex = "\d{2}/\d{2}/\d{4}"
      x = re.search(dob_regex, edata)
      if x:
        data = edata.split()
        valueIndex = data.index(x.group())
        print(valueIndex)
        return ' '.join(data[valueIndex-5:valueIndex-3])
      else:
        return "None"
def get_fname(data):
    try:
      dob_regex = "\d{2}/\d{2}/\d{4}"
      x = re.search(dob_regex, data)
      data = data.split()
      valueIndex = data.index(x.group())
      print(valueIndex)
      return ' '.join(data[valueIndex-2:valueIndex])
    except Exception as e:
      print(e)
      return "None"
def check(img):
    data = {
        "NAME": "",
        "FATHER_NAME": "",
        "DOB": "",
        "PAN": "",
        "identifier": ""
    }
    result = reader.readtext(img,detail = 0)
   # print(" ".join(result))
    result = " ".join(result)
    print(result)
    data['PAN'] = get_pan(result)
    data['DOB'] = get_dob(result)
    data['NAME'] = get_name(result)
    data['FATHERNAME'] = get_fname(result)
    data['identifier'] = get_pan(result)
    return data
@app.route('/curation', methods=['POST'])
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

   app.run(host='0.0.0.0', port=5000)


