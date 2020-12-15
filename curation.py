import easyocr
import re
import requests
from flask import Flask,request
app = Flask(__name__)
def get_dob(result):
	try:
	  dob_regex = "\d{2}/\d{2}/\d{4}"
	  x = re.search(dob_regex, result)
	  return x.group()
	except Exception as e:
	  print(e)
	  return "none"
def get_adhar(data):
	try:
	  edata = data
	  data = data.split()
	  adhar_regex = "\d{4}\s\d{4}\s\d{4}"
	  x = re.search(adhar_regex, data)
	  return x.group()
	except Exception as e:
	  print(e)
	  adhars_regex = "\d{4}\_\d{4}\_\d{4}"
	  y = re.search(adhars_regex, edata)
	  if y:
		  return  y.group()
	  else:
		  return "None"
def get_gender(data):
	data  = data.lower()
	if "female" in data:
		return "female"
	elif "male" in data:
		return "male"
	else:
		return "None"
def get_adhar_name(data):
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
def get_pan_name(data):
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
def get_pan_fname(data):
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
def get_dl(result):
	try:
	  dl_regex = "[0-9]{11}"
	  x = re.search(dl_regex, result)
	  return x.group()
	except Exception as e:
	  print(e)
	  return "None"
def get__licence_name(data):
  try:
	  edata = data
	  data = data.split()
	  valueIndex = data.index("Name")
	  return ' '.join(data[valueIndex+1:valueIndex+3])
  except Exception as e:
	  print(e)
	  dob_regex = "\d{2}/\d{2}/\d{4}"
	  x = re.search(dob_regex, edata)
	  if x:
		  data = edata.split()
		  valueIndex = data.index(x.group())
		  return ' '.join(data[valueIndex-8:valueIndex-5])
	  else:
		  return "None"
def get_licence_fname(data):
	try:
	  edata = data
	  data = data.split()
	  valueIndex = data.index("Name")
	  return ' '.join(data[valueIndex+4:valueIndex+8])
	except Exception as e:
	  print(e)
	  dob_regex = "\d{2}/\d{2}/\d{4}"
	  x = re.search(dob_regex, data)
	  if x:
		  data = data.split()
		  valueIndex = data.index(x.group())
		  return ' '.join(data[valueIndex-3:valueIndex-1])
	  else:
		  return "None"
def get_address(data):
  try:
	  data = data.split()
	  valueIndex = data.index("Address")
	  return ' '.join(data[valueIndex+1:valueIndex+8])
  except Exception as e:
	  print(e)
	  valueIndex = data.index("Name")
	  return ' '.join(data[valueIndex+12:valueIndex+20])
def get_expiry(data):
  try:
	  data = data.split()
	  valueIndex = data.index("Validity(NT)")
	  return ' '.join(data[valueIndex+1:valueIndex+2])
  except Exception as e:
	  print(e)
	  return "None"
def get_lmv(data):
  try:
	  data = data.split()
	  valueIndex = data.index("LMV")
	  return ' '.join(data[valueIndex+1:valueIndex+2])
  except Exception as e:
	  print(e)
	  return "None"
def get_mcwg(data):
  try:
	  data = data.split()
	  valueIndex = data.index("MCWG")
	  return ' '.join(data[valueIndex+1:valueIndex+2])
  except Exception as e:
	  print(e)
	  return "None"
def get_issue(data):
  try:
	  data = data.split()
	  valueIndex = data.index("Validity(NT)")
	  return ' '.join(data[valueIndex-1:valueIndex])
  except Exception as e:
	  print(e)
	  return "None"
def ocr(img):
	reader = easyocr.Reader(['en']) # need to run only once to load model into memory
	result = reader.readtext(img,detail = 0)
	return " ".join(result)
def adhar_ocr(img):
	result = ocr(img)
	print(result)
	data = {
		"NAME": "",
		"DOB": "",
		"ADHARNUMBER": "",
		"GENDER":"",
		"identifier": ""
	}
	data['Adhar_NUMBER'] = get_adhar(result)
	data['DOB'] = get_dob(result)
	data['NAME'] = get_adhar_name(result)
	data["GENDER"] = get_gender(result)
	data['identifier'] = get_adhar(result)
	return data
def pan_ocr(img):
	result = ocr(img)
	data = {
		"NAME": "",
		"FATHERNAME": "",
		"DOB": "",
		"PAN": "",
		"identifier": ""
	}
	data['PAN'] = get_pan(result)
	data['DOB'] = get_dob(result)
	data['NAME'] = get_pan_name(result)
	data['FATHERNAME'] = get_pan_fname(result)
	data['identifier'] = get_pan(result)
	return data
def licence_ocr(img):
	result = ocr(img)
	data = {
		"NAME": "",
		"FATHER_NAME": "",
		"DOB": "",
		"Dl_NO": "",
		"Address": "",
		"Expiry": "",
		"LMV": "",
		"MCWG": "",
		"issue_date": "",
		"identifier": ""
	}
	data['Dl_NO'] = get_dl(result)
	data['DOB'] = get_dob(result)
	data['NAME'] = get__licence_name(result)
	data['FATHER_NAME'] = get_licence_fname(result)
	data['Address'] = get_address(result)
	data['issue_date'] =get_issue(result)
	data['Expiry'] = get_expiry(result)
	data['LMV'] = get_lmv(result)
	data['MCWG'] = get_mcwg(result)
	data['identifier'] = get_dl(result)
	return data
@app.route('/')
def hello_world():
	return 'Hello, World!'
@app.route('/curation', methods=['POST'])
def detect_f():
	data ={}
	if request.json['type'] == "adhar":
		adhar = requests.get(request.json['url']).content
		data['adhar_data' ]= adhar_ocr(adhar)
	if request.json['type'] == "pan":
		pan = requests.get(request.json['url']).content
		data['pan_data'] = pan_ocr(pan)
	if request.json['type'] == "licence":
		licence = requests.get(request.json['url']).content
		data['licence_data'] = licence_ocr(licence)
	return data
app.run(host='0.0.0.0',port=5004)