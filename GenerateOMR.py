import cv2
import numpy as np
import barcode
from barcode.writer import ImageWriter


from PIL import Image, ImageDraw
questions = 10
height = (questions * 100) + 260
width = 450
img = np.zeros((height,width,3), np.uint8)
img[:,:] = (255,255,255)
img = cv2.rectangle(img, (width - 300, 40), (width -30, 120), (0, 0, 0), 2)

CODE = "12,4,001";
barcode_format = barcode.get_barcode_class('code128')
barcode_img = barcode_format(CODE , writer=ImageWriter())
writer=ImageWriter()
# b = barcode_format.save('b.png')
img2 = barcode.get ('code128', CODE, writer = ImageWriter ())
img2.save('ar')
img = cv2.rectangle(img, (20, 200), (width -30, height - 60), (0, 0, 0), 5)
choicePosition = [65, 165, 265, 365]
questionPosition = 250
for x in range(questions) :
    image = cv2.circle(img, (choicePosition[0], questionPosition), 30, (0, 0, 0), 5)
    image = cv2.circle(img, (choicePosition[1], questionPosition), 30, (0, 0, 0), 5)
    image = cv2.circle(img, (choicePosition[2], questionPosition), 30, (0, 0, 0), 5)
    image = cv2.circle(img, (choicePosition[3], questionPosition), 30, (0, 0, 0), 5)
    questionPosition += 100

cv2.imwrite("T1.jpg", img)

s_img = cv2.imread("ar.png")
l_img = cv2.imread("T1.jpg")
x_offset=y_offset=50
l_img[y_offset:y_offset+s_img.shape[0], x_offset:x_offset+s_img.shape[1]] = s_img
s_img = np.array(s_img)
s_img = s_img[:, :, ::-1].copy()
img[y_offset:y_offset+s_img, x_offset:x_offset+s_img] = s_img
cv2.imwrite("T1.jpg", img)