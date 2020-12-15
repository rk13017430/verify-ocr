!pip install easyocr
import easyocr
import re
reader = easyocr.Reader(['en']) # need to run only once to load model into memory
result = reader.readtext('pan5.jpg',detail = 0)
# print(" ".join(result))
result = " ".join(result)
print(result)
def get_pan(result):
    try:  
      pan_regex = "[A-Z]{5}[0-9]{4}[A-Z]{1}"
      x = re.search(pan_regex, result)
      return x.group()
    except Exception as e:
      print(e)
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
        return ' '.join(data[valueIndex-3:valueIndex])
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
data = {
        "NAME": "",
        "FATHERNAME": "",
        "DOB": "",
        "PAN": ""
    }
data['PAN'] = get_pan(result)
data['DOB'] = get_dob(result)
data['NAME'] = get_name(result)
data['FATHERNAME'] = get_fname(result)
print(data)
