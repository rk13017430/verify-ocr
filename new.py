def cleanup_text(text):
	# strip out non-ASCII text so we can draw the text on the image
	# using OpenCV
	return "".join([c if ord(c) < 128 else "" for c in text]).strip()


txt = "Address } NO 493/10 GALI PIPAL WAL) MAHAN SINGH GATE AMRITSAR 143001 Issued ON (96-01-2016"
res = cleanup_text(txt)
print(res)