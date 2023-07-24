#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
import PyPDF2
import magic
import mimetypes
import os, sys
import io
import progressbar
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def is_pdf(path, check):
    if check == 'lazy':
        return is_pdf_lazy(path)
    else:
        return is_pdf_trustworthy(path)

def is_pdf_lazy(path):
    mime_type = mimetypes.guess_type(path)
    if mime_type[0] and mime_type[0] == "application/pdf":
        return True
    return False

def is_pdf_trustworthy(path):
    if is_pdf_lazy(path):
        if 'PDF' in magic.from_file(path):
            return True
    return False

def make_overlay_pdf(watermark, position, font, fontsize, color, mediabox, link):
    lowerLeft = (mediabox.lower_left[0].as_numeric(), mediabox.lower_left[1].as_numeric())
    lowerRight = (mediabox.lower_right[0].as_numeric(), mediabox.lower_right[1].as_numeric())
    upperLeft = (mediabox.upper_left[0].as_numeric(), mediabox.upper_left[1].as_numeric())
    upperRight = (mediabox.upper_right[0].as_numeric(), mediabox.upper_right[1].as_numeric())
    width_page = lowerRight[0] - lowerLeft[0]
    height_page = upperLeft[1] - lowerLeft[1]
    margin = {'top': 0.5*cm, 'right': 1*cm, 'bottom': 1*cm, 'left': 1*cm} # margin for top right bottom left in cm
    packet = io.BytesIO()
    pdfmetrics.registerFont(TTFont(font, font+'.ttf','UTF-8'))
    canva = canvas.Canvas(packet, pagesize=(width_page, height_page))
    if fontsize == 0:
        fontsize = int(width_page * 0.0168) # fontsize 9 for A4
    canva.setFont(font, fontsize)
    watermark_width = canva.stringWidth(watermark, font, fontsize)
    hexColor = '0x'+color
    canva.setFillColor(HexColor(hexColor))

    if position == 'top-left':
        x = upperLeft[0] + margin['left']
        y = upperLeft[1] - margin['top'] - fontsize
    elif position == 'top-right':
        x = upperRight[0] - (margin['right'] + watermark_width)
        y = upperRight[1] - margin['top'] - fontsize
    elif position == 'bottom-left':
        x = lowerLeft[0] + margin['left']
        y = lowerLeft[1] + margin['bottom']
    elif position == 'bottom-right':
        x = lowerRight[0] - (margin['right'] + watermark_width)
        y = lowerRight[1] + margin['bottom']
    elif position == 'top-middle':
        x = upperLeft[0] + (upperRight[0]-upperLeft[0])/2.0 - watermark_width/2.0
        y = upperRight[1] - margin['top'] - fontsize
    elif position == 'bottom-middle':
        x = lowerLeft[0] + (lowerRight[0] - lowerLeft[0])/2.0 - watermark_width/2.0
        y = lowerLeft[1] + margin['bottom']

    canva.drawString(x, y, watermark)
    canva.linkURL(link, (x, y, x+watermark_width, y+fontsize))
    canva.save()
    packet.seek(0)
    return PyPDF2.PdfReader(packet, strict=False)

def make_watermark(args):
    watermark = args.watermark
    link = args.link
    position = args.pos_watermark
    font = args.font
    fontsize = int(args.fontsize)
    color = args.color
    filename = args.PDF
    validate = args.validate

    if is_pdf(filename, validate):
        try:
            existing_pdf = PyPDF2.PdfReader(open(filename, "rb"), strict=False)
            output_pdf = PyPDF2.PdfWriter()
            numPages = len(existing_pdf.pages)
            widgets = [os.path.basename(filename), ': ', progressbar.SimpleProgress()]
            pbar = progressbar.ProgressBar(widgets=widgets, maxval=numPages).start()
            for current_page in range(0, numPages):
                pbar.update(current_page)
                page = existing_pdf.pages[current_page]
                overlay_pdf = make_overlay_pdf(watermark, position, font, fontsize, color, page.mediabox, link)
                page.merge_page(overlay_pdf.pages[0])
                output_pdf.add_page(page)
            pbar.finish()
            directory = args.OutPDF
            if not os.path.exists(directory):
                os.makedirs(directory)  
            outputStream = open(os.path.join(directory, args.prefix+os.path.basename(filename)), "wb")
            output_pdf.write(outputStream)
            outputStream.close()
        except Exception as error:
            print("An exception occurred:", error, 'File:',os.path.basename(filename)) 

def parse_args():
    parser = argparse.ArgumentParser(usage="%s -w 'My watermark' -l http://my.domain.local [-i ~/docs] [-f DejaVuSans] "
        "[-s 24] [-c 0645AD] [-p (top-left|top-middle|top-right|bottom-left|bottom-middle|bottom-right)] "
        "[--prefix your_prefix] [--validate trustworthy]" % (os.path.basename(sys.argv[0])))
    parser.add_argument("-i", "--input", action="store", dest="PDF", required=True)
    parser.add_argument("-o", "--output", action="store", dest="OutPDF")
    parser.add_argument("-w", "--watermark", action="store", dest="watermark", required=True)
    parser.add_argument("-l", "--link", action="store", dest="link", required=True)
    parser.add_argument("-s", "--font-size", action="store", dest="fontsize", default="0")
    parser.add_argument("-f", "--font", action="store", dest="font", default="DejaVuSans")
    parser.add_argument("-c", "--color", action="store", dest="color", default="0645AD")
    parser.add_argument("-p", "--position", action="store", dest="pos_watermark",
        metavar="position watermark", choices=["top-left", "top-middle", "top-right", "bottom-left", "bottom-middle", "bottom-right"], default='top-left')
    parser.add_argument("--prefix", action="store", dest="prefix", default="")
    parser.add_argument("--validate", action="store", dest="validate", choices=['lazy', 'trustworthy'], default='lazy')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    make_watermark(args)
