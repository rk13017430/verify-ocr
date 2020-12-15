import easyocr
import re
reader = easyocr.Reader(['en']) # need to run only once to load model into memory
result = reader.readtext('DL1.jpeg',detail = 0)
result = " ".join(result)
print(result)
def get_dl(result):
    try:
      dl_regex = "[0-9]{11}"
      x = re.search(dl_regex, result)
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
      valueIndex = data.index("Name")
      return ' '.join(data[valueIndex+1:valueIndex+3])
  except Exception as e:
      print(e)
      dob_regex = "\d{2}/\d{2}/\d{4}"
      x = re.search(dob_regex, edata)
      if x:
        data = edata.split()
        valueIndex = data.index(x.group())
       # print(valueIndex)
        return ' '.join(data[valueIndex-8:valueIndex-5])
      else:
        return "None"
def get_fname(data):
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
       # print(valueIndex)
        return ' '.join(data[valueIndex-3:valueIndex-1])
      else:
        return "None"
def get_address(data):
  try:
    #edata = data
    data = data.split()
    valueIndex = data.index("Address")
    return ' '.join(data[valueIndex+1:valueIndex+8])
  except Exception as e:
     print(e)
     #edata = data
     #data = data.split()
     valueIndex = data.index("Name")
     return ' '.join(data[valueIndex+12:valueIndex+20])
def get_expiry(data):
  try:
    #edata = data
    data = data.split()
    valueIndex = data.index("Validity(NT)")
    return ' '.join(data[valueIndex+1:valueIndex+2])
  except Exception as e:
    print(e)
    return "Not in data"
def get_lmv(data):
  try:
    #edata = data
    data = data.split()
    valueIndex = data.index("LMV")
    return ' '.join(data[valueIndex+1:valueIndex+2])
  except Exception as e:
    print(e)
    return "Not given in data"
def get_mcwg(data):
  try:
    #edata = data
    data = data.split()
    valueIndex = data.index("MCWG")
    return ' '.join(data[valueIndex+1:valueIndex+2])
  except Exception as e:
    print(e)
    return "not identified"
def get_issue(data):
  try:
    #edata = data
    data = data.split()
    valueIndex = data.index("Validity(NT)")
    return ' '.join(data[valueIndex-1:valueIndex])
  except Exception as e:
    print(e)
    return "not identified"
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
        "unique": ""
    }
data['Dl_NO'] = get_dl(result)
data['DOB'] = get_dob(result)
data['NAME'] = get_name(result)
data['FATHER_NAME'] = get_fname(result)
data['Address'] = get_address(result)
data['issue_date'] = get_issue(result)
data['Expiry'] = get_expiry(result)
data['LMV'] = get_lmv(result)
data['MCWG'] = get_mcwg(result)
data['unique'] = get_dl(result)
print(data)