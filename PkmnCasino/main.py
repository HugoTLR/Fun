import screen
from model import *
import cv2 as cv
from game_manager import *
import keyboard

import time
S_X = 7
S_Y = 464
L_X = 514
L_Y = 386



if __name__ == "__main__":
  screen.setWindow()
  frame = screen.grab_screen((L_X,L_Y),(S_X,S_Y))


  print(frame.shape)
  model_name = "pkmn_casino_digit_reader.h5"
  model = Model(32,32,model_name)

  gm = GM(model,frame)




  cv.waitKey()
  cv.destroyAllWindows()