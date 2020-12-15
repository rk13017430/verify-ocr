from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import PyPDF2

def watermark_apply(input_image_path,
                   output_image_path,
                   text):
    photo = Image.open(input_image_path)
    
    w, h = photo.size
    

    drawing = ImageDraw.Draw(photo)
    font = ImageFont.truetype("Roboto-Black.ttf", 68)
    
    text = "© " + text + "   "
    text_w, text_h = drawing.textsize(text, font)
    
    pos = w - text_w, (h - text_h) - 50
    
    c_text = Image.new('RGB', (text_w, (text_h)), color = '#000000')
    drawing = ImageDraw.Draw(c_text)
    
    drawing.text((0,0), text, fill="#ffffff", font=font)
    c_text.putalpha(100)
   
    photo.paste(c_text, pos, c_text)
    photo.save(output_image_path)

# watermark_apply("new.png","wm.png","TESTED")
# from io import BytesIO

# tmp = BytesIO()
# def compress_pdf(pdfPath,outPath):
#     merger = PyPDF2.PdfFileMerger()
#     merger.append(fileobj=pdfPath)
#     merger.write(tmp)
#     PyPDF2.filters.compress(tmp.getvalue())
#     merger.write(open(outPath, 'wb'))


# compress_pdf("pan.pdf","com.pdf")

import subprocess

def compress_pdf(input_file_path,output_file_path,power):
    quality = {
        0: '/default',
        1: '/prepress',
        2: '/printer',
        3: '/ebook',
        4: '/screen'
    }
    subprocess.call(['gs', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
                    '-dPDFSETTINGS={}'.format(quality[power]),
                    '-dNOPAUSE', '-dQUIET', '-dBATCH',
                    '-sOutputFile={}'.format(output_file_path),
                    '-r100',
                     input_file_path]
    )
# compress_pdf("2312100175895003000.pdf","com.pdf",4)