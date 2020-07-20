from screen import *
import cv2 as cv
import numpy as np


# setWindow()
screen = grab_screen((L_X,L_Y),(S_X,S_Y))
template = cv.cvtColor(cv.imread('play_button.png'),cv.COLOR_BGR2GRAY)
height,width = template.shape
match = cv.matchTemplate(screen, template, cv.TM_CCOEFF_NORMED)
print(match)
screen = cv.cvtColor(screen,cv.COLOR_GRAY2BGR)
threshold = 0.8
position = np.where(match >= threshold) #get the location of template in the image
for point in zip(*position[::-1]): #draw the rectangle around the matched template
   cv.rectangle(screen, point, (point[0] + width, point[1] + height), (0, 204, 153), 3)


(_, val_max, _, loc_max) = cv.minMaxLoc(match)
print(val_max,loc_max)
cv.imshow('Template Found', screen)
cv.waitKey(0)


# p_s_x = 281
# p_s_y = 137
# p_l_x = 210
# p_l_y = 34
# cv.imshow("C",screen)
# cv.imshow("Play",screen[p_s_y:p_s_y+p_l_y,p_s_x:p_s_x+p_l_x])
# cv.waitKey(0)
cv.destroyAllWindows()