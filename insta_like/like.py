#!/usr/bin/env python

from ppadb.client import Client
import cv2, numpy
from time import sleep

adb = Client(host='127.0.0.1', port=5037)
devices =adb.devices()

if(len(devices) == 0):
	print('No connected devices')
	quit()

device =devices[0]

template = cv2.imread('heart.png', 0)
w,h = template.shape[::-1]

while True:
	device.shell('input touchscreen swipe 500 1000 500 300')
	sleep(0.5)
	image=device.screencap()
	with open('screen.png', 'wb') as f:
		f.write(image)

	img_rgb= cv2.imread('screen.png')
	img_gray =cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

	res =cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
	threshold =0.9
	loc = numpy.where (res>=threshold)

	prev_x=0
	prev_y=0
	diff=50
	for pt in zip(*loc[::-1]):
		if(abs(pt[0]-prev_x)<50 and abs(pt[1]-prev_y)<50):
			continue
		prev_x=pt[0]
		prev_y=pt[1]
		#cv2.rectangle(img_rgb, pt, (pt[0]+w, pt[1]+h), (0,0,255), 2)
		device.shell(f'input tap {int(pt[0]+w/2)} {int(pt[1]+h/2)}')
#cv2.imwrite('res.png', img_rgb)