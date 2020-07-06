import cv2 as cv
import numpy as np
import imutils
from model import *
from processing import auto_constrast
from keys import KeyboardManager

class GM:
  STATE = {0:'Menu',\
            1:'Game',\
            2:'Lose',\
            3:'Win'}

  SIZE            = 5          #5 row & col
  UI_CELL_SIZE    = 56 #56*56 px
  UI_ROW_START_X  = 333
  UI_ROW_START_Y  = 12

  UI_COL_START_X  = 12
  UI_COL_START_Y  = 333

  UI_SPACE        = 8

  def __init__(self,model,frame):
    self.model = model

    self.state = GM.STATE[0]

    self.km = KeyboardManager()

    self.frame = frame

    self.board = [[0 for _ in range(GM.SIZE)] for _ in range(GM.SIZE)]

    self.infos = {"rows":{},"cols":{}}
    
    self.km.run_game()

    self.get_game_info()




  def get_digit(self,roi):
    assert len(roi.shape) == 2, "get_digit(): Image must be binary"

    roi_cstr = auto_constrast(roi)
    _,th = cv.threshold(roi_cstr,35,255,cv.THRESH_BINARY_INV)
    # cv.imshow(f"get_digit",np.hstack([roi,roi_cstr,th]))
    th[20:th.shape[1],0:36] = 0 #Remove THIS FUCKING VOLTORB
    th[th.shape[1]-7:th.shape[1]] = 0 #Remove Line that apperas sometimes and breaks the contours pipeline

    cnts = cv.findContours(th.copy(), cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    return cnts,th

  def get_contour_precedence(self,contour, cols):
    tolerance_factor = 10
    origin = cv.boundingRect(contour)
    return ((origin[1] // tolerance_factor) * tolerance_factor) * cols + origin[0]

  def set_info(self,m_id,mode='rows'):
    roi = self.infos[mode][m_id]['roi']
    cnts,th = self.get_digit(roi)
    cnts = sorted(cnts,key=lambda x:self.get_contour_precedence(x,th.shape[1]))
    digits = []
    for cnt in cnts:
      (x, y, w, h) = cv.boundingRect(cnt)
      r = cv.resize(th[y:y+h,x:x+w],(32,32))
      digits.append(r)

    X = np.array(digits).reshape(-1,32,32,1)
    X = tf.keras.utils.normalize(X,axis=1)
    predictions = self.model.model.predict(X)
    assert len(predictions) == 3, f"set_info({m_id}, {mode}): cell must have 3 digits,but only {len(predictions)} found"

    pts = int( str(np.argmax(predictions[0])) + str(np.argmax(predictions[1])) )
    bombs = int( np.argmax(predictions[2]) )
    self.infos[mode][m_id]["pts"] = pts
    self.infos[mode][m_id]["bombs"] = bombs


  def get_game_info(self):
    for i in range(GM.SIZE):
      self.infos["rows"][i] = {"id":i,\
                                "pts":-1,\
                                "bomb":-1,\
                                "loc": {"x":GM.UI_ROW_START_X,\
                                        "y":GM.UI_ROW_START_Y+i*(GM.UI_SPACE+GM.UI_CELL_SIZE),\
                                        "w":GM.UI_CELL_SIZE,\
                                        "h":GM.UI_CELL_SIZE\
                                        }\
                              }
      self.infos["rows"][i]["roi"] = self.frame[self.infos["rows"][i]["loc"]['y']:self.infos["rows"][i]["loc"]['y']+self.infos["rows"][i]["loc"]['h'],\
                                                self.infos["rows"][i]["loc"]['x']:self.infos["rows"][i]["loc"]['x']+self.infos["rows"][i]["loc"]['w']]

      self.infos["cols"][i] = {"id":i,\
                                "pts":-1,\
                                "bomb":-1,\
                                "loc": {"x":GM.UI_COL_START_X+i*(GM.UI_SPACE+GM.UI_CELL_SIZE),\
                                        "y":GM.UI_COL_START_Y,\
                                        "w":GM.UI_CELL_SIZE,\
                                        "h":GM.UI_CELL_SIZE\
                                        }\
                              }

      self.infos["cols"][i]["roi"] = self.frame[self.infos["cols"][i]["loc"]['y']:self.infos["cols"][i]["loc"]['y']+self.infos["cols"][i]["loc"]['h'],\
                                                self.infos["cols"][i]["loc"]['x']:self.infos["cols"][i]["loc"]['x']+self.infos["cols"][i]["loc"]['w']]

      self.set_info(i)
      self.set_info(i,mode='cols')

