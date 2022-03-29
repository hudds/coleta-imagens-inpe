import cv2
import numpy as np
import requests



begin_y = 850
begin_x = 1370
image_goes16 = cv2.imread("S11232958_201801081200.jpg", cv2.IMREAD_COLOR)
cropped_image_16 = image_goes16[begin_y:begin_y+115, begin_x:begin_x+117]
cv2.imshow('image',cropped_image_16)
cv2.waitKey(0)

white_lo=np.array([220,220,220])
white_hi=np.array([256,256,256])

mask=cv2.inRange(cropped_image_16,white_lo,white_hi)

cropped_image_16[mask>0]=(0,0,0)

cv2.imshow('image',cropped_image_16)
cv2.waitKey(0)

blu_trasition = (255,255,255)
light_blu_trasition = (254,254,254)
pink_trasition = (253,253,253)
yellow_trasition = (252,252,252)
orange_trasition = (251,251,251)

blu_lo=np.array([140, 0, 0])
blu_hi=np.array([255, 164, 68])
mask=cv2.inRange(cropped_image_16,blu_lo,blu_hi)
cropped_image_16[mask>0]=blu_trasition
# for testing
cv2.imshow('image',cropped_image_16)
cv2.waitKey(0)

light_blu_lo=np.array([100, 180, 0])
light_blu_hi=np.array([255, 240, 240])
mask=cv2.inRange(cropped_image_16,light_blu_lo,light_blu_hi)
cropped_image_16[mask>0]=light_blu_trasition
# for testing
cv2.imshow('image',cropped_image_16)
cv2.waitKey(0)

yellow_lo=np.array([70,190, 190])
yellow_hi=np.array([130, 255, 255])
mask=cv2.inRange(cropped_image_16,yellow_lo,yellow_hi)
cropped_image_16[mask>0]=yellow_trasition
# for testing
cv2.imshow('image',cropped_image_16)
cv2.waitKey(0)

orange_lo=np.array([0,90, 180])
orange_hi=np.array([200, 255, 255])
mask=cv2.inRange(cropped_image_16,orange_lo,orange_hi)
cropped_image_16[mask>0]=orange_trasition
# for testing
cv2.imshow('image',cropped_image_16)
cv2.waitKey(0)

pink_lo=np.array([180,100, 180])
pink_hi=np.array([255, 180, 255])
mask=cv2.inRange(cropped_image_16,pink_lo,pink_hi)
cropped_image_16[mask>0]=pink_trasition
# for testing
cv2.imshow('image',cropped_image_16)
cv2.waitKey(0)

mask=cv2.inRange(cropped_image_16,orange_trasition,orange_trasition)
cropped_image_16[mask>0]=(125,12,2)
# for testing
cv2.imshow('image',cropped_image_16)
cv2.waitKey(0)

mask=cv2.inRange(cropped_image_16,yellow_trasition,yellow_trasition)
cropped_image_16[mask>0]=(16,232,1)
# for testing
cv2.imshow('image',cropped_image_16)
cv2.waitKey(0)

mask=cv2.inRange(cropped_image_16,light_blu_trasition,light_blu_trasition)
cropped_image_16[mask>0]=(7,251,255)
# for testing
cv2.imshow('image',cropped_image_16)
cv2.waitKey(0)


mask=cv2.inRange(cropped_image_16,blu_trasition,blu_trasition)
cropped_image_16[mask>0]=(0,1,156)
# for testing
cv2.imshow('image',cropped_image_16)
cv2.waitKey(0)

mask=cv2.inRange(cropped_image_16,pink_trasition,pink_trasition)
cropped_image_16[mask>0]=(104,104,104)
# for testing
cv2.imshow('image',cropped_image_16)
cv2.waitKey(0)


def is_edge_for_colors(colors, pixel, next_pixel, last_pixel):
    for color in colors:
        if not np.array_equal(pixel, color) and (np.array_equal(next_pixel, color) or np.array_equal(last_pixel, color)):
            return True
    return False

edge_colors = [ np.array([104,104,104]), np.array([0,1,156]), np.array([7,251,255]), np.array([16,232,1]), np.array([125,12,2])]
for y in range(len(cropped_image_16)):
    
    for x in range(len(cropped_image_16[y])):
        if x+1 >= len(cropped_image_16[y]) or y+1 >= len(cropped_image_16):
            continue
        if x == 0 or y == 0:
            continue
        pixel = cropped_image_16[y][x]
        next_pixel_x = cropped_image_16[y][x+1]
        last_pixel_x = cropped_image_16[y][x-1]
        if is_edge_for_colors(edge_colors, pixel, next_pixel_x, last_pixel_x):
            next_pixel_x = next_pixel_x.astype(np.uint16)
            last_pixel_x = last_pixel_x.astype(np.uint16)
            top_pixel = cropped_image_16[y-1][x].astype(np.uint16)
            top_left_pixel = cropped_image_16[y-1][x-1].astype(np.uint16)
            top_right_pixel = cropped_image_16[y-1][x+1].astype(np.uint16)
            bottom_pixel = cropped_image_16[y+1][x].astype(np.uint16)
            bottom_right_pixel = cropped_image_16[y+1][x+1].astype(np.uint16)
            bottom_left_pixel = cropped_image_16[y+1][x-1].astype(np.uint16)
            avg = (next_pixel_x+last_pixel_x+top_pixel+top_left_pixel+top_right_pixel+bottom_pixel+bottom_right_pixel+bottom_left_pixel) / [8,8,8]
            avg = avg.astype(np.uint8)
            cropped_image_16[y][x] = avg.astype(np.uint8)


cv2.imshow('image',cropped_image_16)
cv2.waitKey(0)

cropped_image_16 = cv2.cvtColor(cropped_image_16,cv2.COLOR_BGR2GRAY)
cv2.imshow('image',cropped_image_16)
cv2.waitKey(0)

print([15,15,15] == np.array([15,15,15]))
cv2.imwrite(filename='masked.jpg',img=cropped_image_16)
cv2.destroyAllWindows()
