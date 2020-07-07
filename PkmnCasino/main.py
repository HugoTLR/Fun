import screen
from model import *
import cv2 as cv
from game_manager import *
import keyboard

import time


def run(gm):
  screen.setWindow()

  while True:
    print("NEW GAME")
    gm.start_game()
    while gm.state == 'Game':
      probaList = sorted(gm.calc_proba(),key=lambda x: x[1])
      print(probaList)
      best = probaList[0]
      if best[1] < .15: #.25 means a cell with 50% chance of bomb, if we get there just quit and rerun instead of losing points
        target_cell = best[0]
        c_r,c_c = gm.current_cell//GM.SIZE,gm.current_cell%GM.SIZE
        t_r,t_c = target_cell//GM.SIZE,target_cell%GM.SIZE
        move_dir_list = gm.get_move_dir((c_r,c_c),(t_r,t_c))
        print(f"Best:{target_cell} Moves:{move_dir_list}")

        for move in move_dir_list:
          gm.move(move)
        gm.action()
      else:
        gm.quit_game()
        break
   
      gm.update(screen.grab_screen((L_X,L_Y),(S_X,S_Y)),cell=(t_r,t_c))
      # cv.imshow('ui',gm.ui_board())
      # cv.waitKey(1)

    if gm.state == GM.STATE[0]:
      print(f"We leaved before loosing points")
    else:
      print(f"We exploded on a voltorb")
      gm.game_over()

  # cv.destroyAllWindows()

if __name__ == "__main__":


  model_name = "pkmn_casino_digit_reader.h5"
  model = Model(32,32,model_name)

  gm = GM(model)
  run(gm)




  # cv.destroyAllWindows()