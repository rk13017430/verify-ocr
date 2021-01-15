import easyocr
import re
import requests
from flask import Flask,request
app = Flask(__name__)
reader = easyocr.Reader(['en'], gpu=True) # need to run only once to load model into memory
def get_data(result):
	try:
		return result
	except:
		return "To be Curated"
def get_dob(result):
	try:
	  dob_regex = "\d{2}/\d{2}/\d{4}"
	  x = re.search(dob_regex, result)
	  return x.group()
	except:
	  dobs_regex = "\d{2}-\d{2}-\d{4}"
	  y = re.search(dobs_regex, result)
	  if y:
		  return y.group()
	  return "To be Curated"
def get_adhar(data):
	edata = data
	try:
		adhar_regex = "\d{4}\s\d{4}\s\d{4}"
		x = re.search(adhar_regex, data)
		return x.group()
	except:
		adhars_regex = "\d{4}\_\d{4}\_\d{4}"
		dob_regrex = "\d{2}/\d{2}/\d{4}"
		z = re.search(dob_regrex, edata)
		y = re.search(adhars_regex, edata)
		if y:
			return y.group()
		if z:
			data = edata.split()
			valueIndex = data.index(z.group())
			#print(valueIndex)
			return ' '.join(data[valueIndex + 3:valueIndex + 6])
		else:
			return "To be Curated"
def get_gender(data):
	data  = data.lower()
	if "female" in data:
		return "female"
	elif "male" in data:
		return "male"
	else:
		return "To be Curated"
def get_adhar_name(data):
	try:
		dob_regex = "\d{2}/\d{2}/\d{4}"
		x = re.search(dob_regex, data)
		data = data.split()
		valueIndex = data.index(x.group())
		return ' '.join(data[valueIndex - 5:valueIndex - 3])
	except:
		return "To be Curated"
def get_pan(data):
	edata = data
	if "card" in edata.lower():
		data = edata.split()
		valueIndex = data.index("Card")
		return ' '.join(data[valueIndex + 1: valueIndex + 2])
	try:
		pan_regex = "[A-Z]{5}[0-9]{4}[A-Z]{1}"
		x = re.search(pan_regex, edata)
		return x.group()
	except:
		dob_regex = "\d{2}/\d{2}/\d{4}"
		x = re.search(dob_regex, edata)
		if x:
			data = edata.split()
			valueIndex = data.index(x.group())
			# print("valueIndex")
			return ' '.join(data[valueIndex + 4:valueIndex + 5])
		else:
			return "To be Curated"
def get_pan_name(data):
	edata = data
	try:
		data = data.split()
		if "name" not in edata.lower():
			valueIndex = data.index("OF")
			if "tax" not in edata.lower():
				return ' '.join(data[valueIndex + 2:valueIndex + 4])
			valueindex = data.index("TAX")
			if valueIndex > valueindex:
				return ' '.join(data[valueIndex + 2:valueIndex + 4])
			else:
				return ' '.join(data[valueindex + 2:valueindex + 4])
		else:
			valueIndex = data.index("Card")
			return ' '.join(data[valueIndex + 4:valueIndex + 6])
	except:
		dob_regex = "\d{2}/\d{2}/\d{4}"
		x = re.search(dob_regex, edata)
		if x:
			data = edata.split()
			valueIndex = data.index(x.group())
			return ' '.join(data[valueIndex - 5:valueIndex - 3])
		else:
			return "To be Curated"
def get_pan_fname(data):
	edata = data.replace("'", " ")
	data = edata.split()
	try:
		if "father" in edata.lower():
			valueIndex = data.index("Father")
			return ' '.join(data[valueIndex + 3:valueIndex + 6])
		else:
			dob_regex = "\d{2}/\d{2}/\d{4}"
			x = re.search(dob_regex, edata)
			valueIndex = data.index(x.group())
			return ' '.join(data[valueIndex - 2:valueIndex])
	except:
		return "To be Curated"
def get_dl(result):
	try:
	  dl_regex = "[0-9]{11}"
	  x = re.search(dl_regex, result)
	  if "Uttarakhand" in result:
		  y= "UK-"+x.group()
		  return y
	  if "Uttar" in result:
		  z= "UP63-"+x.group()
		  return z
	  return x.group()
	except:
	  return "To be Curated"
def get_dlname(data):
	edata = data
	try:
		data = data.split()
		valueIndex = data.index("Name")
		if "Uttarakhand" in edata:
			return ' '.join(data[valueIndex+1 :valueIndex+4])
		return ' '.join(data[valueIndex + 1:valueIndex + 3])
	except:
		dob_regex = "\d{2}/\d{2}/\d{4}"
		x = re.search(dob_regex, edata)
		if "Name:" in edata.split():
			data = edata.split()
			valueIndex = data.index("Name:")
			return ' '.join(data[valueIndex+1:valueIndex+4])
		if x:
			data = edata.split()
			valueIndex = data.index(x.group())
			return ' '.join(data[valueIndex - 8:valueIndex - 5])
		else:
			return "To be Curated"
def get_dlfname(data):
	edata = data
	try:
		data = data.split()
		valueIndex = data.index("Name")
		return ' '.join(data[valueIndex + 4:valueIndex + 8])
	except:
		data= edata.split()
		dob_regex = "\d{2}/\d{2}/\d{4}"
		x = re.search(dob_regex, edata)
		if "of:" in data:
			valueIndex = data.index("of:")
			return ' '.join(data[valueIndex+1:valueIndex+3])
		if x:
			valueIndex = data.index(x.group())
			# print(valueIndex)
			return ' '.join(data[valueIndex - 3:valueIndex - 1])
		else:
			return "To be Curated"
def get_dladdress(data):
	edata = data
	try:
		data = data.split()
		valueIndex = data.index("Address")
		return ' '.join(data[valueIndex + 1:valueIndex + 8])
	except:
		data = edata.split()
		if "Address:" in data:
			valueIndex = data.index("Address:")
			return ' '.join(data[valueIndex+1:valueIndex +8])
		if "Name" in data:
			valueIndex = data.index("Name")
			return ' '.join(data[valueIndex + 12:valueIndex + 20])
		else:
			return "To be Curated"
def get_expiry(data):
	try:
		data = data.split()
		valueIndex = data.index("Validity(NT)")
		return ' '.join(data[valueIndex + 1:valueIndex + 2])
	except:
		return "To be Curated"
def get_gstn(result):
	try:
		gst_regex = "\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}"
		x = re.search(gst_regex, result)
		if x:
			return x.group()
		else:
			gst_regex = "\d{2}[A-Z]{5}\d{3}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}"
			x = re.search(gst_regex, result)
			return x.group()
	except:
		return "To be Curated"
def get_voterid(data):
	try:
		id_regex = "([a-zA-Z]){3}([0-9]){7}"
		x = re.search(id_regex, data)
		return x.group()
	except:
		if "CARD" in data:
			data=data.split()
			valueIndex=data.index("CARD")
			return ' '.join(data[valueIndex+1:valueIndex+2])
		return "To be Curated"
def get_cin(result):
	try:
		cin_regex = "([L|U]{1})([0-9]{5})([A-Za-z]{2})([0-9]{4})([A-Za-z]{3})([0-9]{6})"
		x = re.search(cin_regex, result)
		return x.group()
	except:
		return "to be Curated"
def get_tan(result):
	try:
		tan_regex = "[A-Z]{4}[0-9]{5}[A-Z]{1}"
		x = re.search(tan_regex, result)
		return x.group()
	except:
		return "To be Curated"
def get_passport(data):
	edata = data
	try:
		passport_regrex = "[A-Z]{1}[0-9]{7}"
		x = re.search(passport_regrex, edata)
		return x.group()
	except:
		if 'INVD' in edata.split():
			data = edata.split()
			valueIndex = data.index("INVD")
			return ' '.join(data[valueIndex + 1:valueIndex + 2])
		return "To be Curated"
def get_legal(data):
    try:
        data = data.split()
        valueIndex = data.index("Legal")
        return ' '.join(data[valueIndex -3:valueIndex])
    except:
        return "To be Curated"
def get_trade(data):
    try:
        data = data.split()
        valueIndex = data.index("Trade")
        return ' '.join(data[valueIndex+3:valueIndex+5])
    except:
        return "To be Curated"
def ocr(img):
	#reader = easyocr.Reader(['en']) # need to run only once to load model into memory
	import cv2
	import numpy as np
	img = np.asarray(bytearray(img), dtype="uint8")
	img = cv2.imdecode(img, cv2.IMREAD_COLOR)
	#print(type(img))

	img = cv2.resize(img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	result = reader.readtext(img,detail = 0)
	return " ".join(result)
def adhar_ocr(img):
	result = ocr(img)
	#print(result)
	data = {
		"data":{
		"NAME": get_adhar_name(result),
		"DOB": get_dob(result),
		"ADHARNUMBER": get_adhar(result),
		"GENDER": get_gender(result)},
		"IDENTIFIER": get_adhar(result),
		"UNSTRUCTRED": get_data(result)
	}
	return data
def pan_ocr(img):
	result = ocr(img)
	data = {
		"data":{
		"NAME": get_pan_name(result),
		"FATHERNAME": get_pan_fname(result),
		"DOB": get_dob(result),
		"PAN": get_pan(result)},
		"IDENTIFIER": get_pan(result),
		"UNSTRUCTRED": get_data(result)
	}
	return data
def dl_ocr(img):
	result = ocr(img)
	data = {
		"data":{
		"NAME": get_dlname(result),
		"FATHER_NAME": get_dlfname(result),
		"DOB": get_dob(result),
		"DL_NO": get_dl(result),
		"ADDRESS": get_dladdress(result),
		"EXPIRY": get_expiry(result) },
		"IDENTIFIER": get_dl(result),
		"UNSTRUCTRED":get_data(result)
	}
	return data
def gst_ocr(img):
	result = ocr(img)
	data = {
		"data":{
		"GST_NO": get_gstn(result),
        "LEGAL_NAME": get_legal(result),
        "TRADE_NAME": get_trade(result)},
		"IDENTIFIER": get_gstn(result),
		"UNSTRUCTRED": get_data(result)
	}
	return data
def voter_ocr(img):
	result = ocr(img)
	data = {
		"data":{
		"VOTER_NO": get_voterid(result),
		"GENDER": get_gender(result),
		"NAME": get_dlname(result)},
		"IDENTIFIER": get_voterid(result),
		"UNSTRUCTRED": get_data(result)
	}
	return data
def cin_ocr(img):
	result = ocr(img)
	data = {
		"data":{
		"CIN": get_cin(result),
		"TAN": get_tan(result),
		"PAN": get_pan(result)},
		"IDENTIFIER": get_cin(result),
		"UNSTRUCTRED": get_data(result)
	}
	return data
def passport_ocr(img):
	result = ocr(img)
	data = {
		"data":{
		"DOB": get_dob(result),
		"PASSPORT_NO":get_passport(result),
		"GENDER": "M",
		"NAME": "To be Curated"},
		"UNSTRUCTRED": get_data(result),
		"IDENTIFIER": get_passport(result)
	}
	return data
def unstruct_ocr(img):
	result = ocr(img)
	data = {
		"data":{
		"IDENTITY": "To be Curated"
		},
		"UNSTRUCTRED": get_data(result)
	}
	return data
@app.route('/')
def hello_world():
	return 'GET Curated Data!'
@app.route('/curation', methods=['POST'])
def detect_f():
	data ={}
	if request.json['type'] == "10000006":
		adhar = requests.get(request.json['url']).content
		data = adhar_ocr(adhar)
		return data
	elif request.json['type'] == "10000003" or request.json['type'] == "10000041":
		pan = requests.get(request.json['url']).content
		data  = pan_ocr(pan)
		return data
	elif request.json['type'] == "10000002":
		licence = requests.get(request.json['url']).content
		data  = dl_ocr(licence)
		return data
	elif request.json['type'] == "10000038":
		gst = requests.get(request.json['url']).content
		data = gst_ocr(gst)
		return data
	elif request.json['type'] == "10000004":
		voter = requests.get(request.json['url']).content
		data = voter_ocr(voter)
		return data
	elif request.json['type'] == "10000035":
		cin = requests.get(request.json['url']).content
		data = cin_ocr(cin)
		return data
	elif request.json['type'] == "10000001":
		passport = requests.get(request.json['url']).content
		data = passport_ocr(passport)
		return data
	else:
		#request.json['type'] != "Rakesh":
		unstruct = requests.get(request.json['url']).content
		data = unstruct_ocr(unstruct)
	return data
app.run(host='0.0.0.0',port=5004)
