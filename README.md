# Image to text converter(Adhar,Pan,dl,voter,passport,gst,cin and many documents)
image to text converter and output in Structured data Json format.
->clone this git .
->creat a new project by creating virtual environment.
Installtion.
pip3 install easyocr
pip3 install scikit-build
pip3 install cmake
pip3 install flask



now run  file for easy ocr of data,
I have created api also so using these you can check it on local host or server.
Default port is 5000.
url->localhost:5000/....



# for unstrutred data make a test file and run test.py in python shell (insert below code in test.py)


import easyocr
reader = easyocr.Reader(['en','hi'])
img = "Resume.pdf"
result = reader.readtext(img,detail = 0)
res =  " ".join(result)
print(res)

############################Rakesh##################Kumar###############################################################################################################################################################################################################################################################################
 
