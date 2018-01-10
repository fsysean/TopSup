# -*- coding: utf-8 -*-

# @Author  : Skye
# @Time    : 2018/1/9 19:34
# @desc    :

from PIL import Image
import pytesseract

# 二值化算法
def binarizing(img,threshold):
    pixdata = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255
    return img


# 去除干扰线算法
def depoint(img):   #input: gray image
    pixdata = img.load()
    w,h = img.size
    for y in range(1,h-1):
        for x in range(1,w-1):
            count = 0
            if pixdata[x,y-1] > 245:
                count = count + 1
            if pixdata[x,y+1] > 245:
                count = count + 1
            if pixdata[x-1,y] > 245:
                count = count + 1
            if pixdata[x+1,y] > 245:
                count = count + 1
            if count > 2:
                pixdata[x,y] = 255
    return img

def ocr_img(image):

    # 切割题目和选项位置，左上角坐标和右下角坐标,自行测试分辨率
    
    choices_im = image.crop((75, 800, 1167, 1450))
    question_im = image.crop((75, 315, 1167, 900)) # iPhone 7P

    # 转化为灰度图
    question_im = question_im.convert('L')
    choices_im = choices_im.convert('L')
    # 把图片变成二值图像。
    question_im=binarizing(question_im,190)
    choices_im = binarizing(choices_im, 190)
    

    # tesseract 路径
    #pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'
    pytesseract.pytesseract.tesseract_cmd = '/usr/local/Cellar/tesseract/3.05.01/bin/tesseract'
# Include the above line, if you don't have tesseract executable in your PATH

    # 语言包目录和参数
    tessdata_dir_config = '--tessdata-dir "/opt/local/share/tessdata/"'
    #tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata" --psm 6'

    # lang 指定中文简体
    question = pytesseract.image_to_string(question_im, lang='chi_sim', config=tessdata_dir_config)
    question = question.replace("\n", "")[2:]

    choice = pytesseract.image_to_string(choices_im, lang='chi_sim', config=tessdata_dir_config)
    choices = choice.strip().split("\n")
    choices = [ x.replace(' ','') for x in choices if x != '' and x!=' ' ]

    return question, choices


if __name__ == '__main__':
    image = Image.open("./screenshot.png")
    question,choices = ocr_img(image)

    print("识别结果:")
    print(question)
    print(choices)
