import easyocr

reader = easyocr.Reader(['en','hi'])
img = "Resume.pdf"
result = reader.readtext(img,detail = 0)
res =  " ".join(result)
print(res)
