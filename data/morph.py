import numpy as np
import cv2

def hsv2gray2bin(img):
    bgr = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
    return cv2.threshold(cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY), 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    

before = cv2.cvtColor(cv2.imread("harvey-wharton-before.jpg"), cv2.COLOR_BGR2HSV)
after = cv2.cvtColor(cv2.imread("harvey-wharton-after.jpg"), cv2.COLOR_BGR2HSV, -1)
#after = cv2.imread("harvey-wharton-after.jpg")

# diff = cv2.absdiff(before, after)
# hsvDiff = cv2.cvtColor(diff, cv2.COLOR_BGR2HSV)

water_lower = np.array([0,35,90])
water_upper = np.array([10,255,255])

mask = cv2.inRange(after, water_lower, water_upper)

res = hsv2gray2bin(cv2.bitwise_and(after, after, mask=mask))

res = cv2.erode(res, np.ones((3,3), np.uint8))

res = cv2.dilate(res, np.ones((25,25), np.uint8))
for _ in range(25):
    res = cv2.dilate(res, np.ones((3,3), np.uint8))

# for _ in range(50):
#     res = cv2.erode(res, np.ones((3,3), np.uint8))

# res = cv2.erode(res, np.ones((20,20), np.uint8))

cv2.imwrite("result.png", cv2.GaussianBlur(res, (3,3),0))

overlay = np.zeros((after.shape[0], after.shape[1], 4), np.uint8)
for h in range(res.shape[0]):
    for w in range(res.shape[1]):
        if res[h,w] == 0:
            overlay[h,w] = (0,0,0,0)
        else:
            overlay[h,w] = (127,0,0,127)

cv2.imwrite("overlay.png", overlay)

