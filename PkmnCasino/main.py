import screen
from model import *
import cv2 as cv
from game_manager import *
import keyboard

import time
S_X = 14
S_Y = 469
L_X = 500
L_Y = 378

def run(gm):
  screen.setWindow()
  # gm.start_game()
  gm.update(screen.grab_screen((L_X,L_Y),(S_X,S_Y)),cells=False)
  gm.get_game_info()
  

  
  # while gm.gameState == 1:
  probaList = gm.calc_proba()
  best = sorted(probaList,key=lambda x: x[1],reverse=True)[0]
  target_cell = best[0]

  c_r,c_c = gm.current_cell//GM.SIZE,gm.current_cell%GM.SIZE
  t_r,t_c = target_cell//GM.SIZE,target_cell%GM.SIZE
  move_dir_list = gm.get_move_dir((c_r,c_c),(t_r,t_c))

  print(move_dir_list)

  for move in move_dir_list:
    gm.move(move)
  gm.action()





  gm.update(screen.grab_screen((L_X,L_Y),(S_X,S_Y)))
  cv.imshow('??',screen.grab_screen((L_X,L_Y),(S_X,S_Y)))
  cv.imshow('ui',gm.ui_board())


  cv.waitKey(0)


if __name__ == "__main__":


  model_name = "pkmn_casino_digit_reader.h5"
  model = Model(32,32,model_name)

  gm = GM(model)

  # run(gm)
  screen.setWindow()
  # gm.start_game()
  gm.update(screen.grab_screen((L_X,L_Y),(S_X,S_Y)),cells=False)
  gm.get_game_info()
  
  cv.imshow("f",gm.ui_board())
  cv.waitKey(0)



  cv.destroyAllWindows()