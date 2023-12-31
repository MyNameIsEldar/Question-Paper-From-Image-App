import pytesseract
import cv2 as cv
import numpy as np
import os
import qp_generator.page_dewrap as page_dewrap
import streamlit as st

text = ''

def image_preprocessing(image):

    image = cv.imdecode(np.frombuffer(image, dtype=np.uint8), cv.IMREAD_COLOR)

    dewraped_image = page_dewrap.main([image])
    if len(dewraped_image) != 0:
        result_image = np.array(dewraped_image[0])
    else:
        result_image = image

    return result_image

@st.cache_data
def text_rec(image):

    text = pytesseract.image_to_string(image, lang='rus')

    return text

@st.cache_data
def main(image):
    global text

    pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract" 
    
    # for windows usage

    # tesseract_path = r'C:\Program Files\Tesseract-OCR'
    # os.environ['PATH'] += os.pathsep + tesseract_path
    # pytesseract.pytesseract.tesseract_cmd = tesseract_path + r'\tesseract.exe'

    preproc_img = image_preprocessing(image)
    img_text = text_rec(preproc_img)

    text = img_text

    return img_text
