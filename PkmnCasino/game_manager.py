import cv2 as cv
import numpy as np
import imutils
from model import *
from processing import auto_constrast
from keys import KeyboardManager
from screen import grab_screen
from screen import L_X, L_Y, S_X, S_Y

class GM:
  STATE = {0:'Menu',\
            1:'Game',\
            2:'Lose',\
            3:'Win'}

  SIZE            = 5          #5 row & col
  UI_CELL_SIZE    = 56 #56*56 px

  UI_ROW_START_X  = 326
  UI_ROW_START_Y  = 6

  UI_COL_START_X  = 6
  UI_COL_START_Y  = 326

  UI_SPACE        = 8
  UI_OFFSET       = 6


  def __init__(self,model):
    self.model = model
    self.km = KeyboardManager()



    # self.get_game_info()


  def start_game(self):

    self.board = [[0 for _ in range(GM.SIZE)] for _ in range(GM.SIZE)]
    self.infos = {"rows":{},"cols":{},"cells":{}}

    self.state = GM.STATE[0]
    self.current_cell = 0
    
    self.km.run_game()
    self.state = GM.STATE[1]

    self.update(grab_screen((L_X,L_Y),(S_X,S_Y)))
    self.get_game_info()


  def quit_game(self):
    self.km.quit()
    self.state = GM.STATE[0]

  def get_move_dir(self,p1,p2):
    y_diff = p2[0]-p1[0]
    x_diff = p2[1]-p1[1]
    moves = []
    if y_diff < 0:
      for _ in range(abs(y_diff)):
        moves.append('up')
    elif y_diff > 0:
      for _ in range(y_diff):
        moves.append('down')
    if x_diff < 0:
      for _ in range(abs(x_diff)):
        moves.append('left')
    elif x_diff > 0:
      for _ in range(x_diff):
        moves.append('right')
    return moves
  def update(self,frame,cell=None):
    self.frame = frame
    if cell != None:
      self.update_cell(cell)

  def game_over(self):
    self.km.game_over()


  def move(self,move):
    self.km.move(move)
    if move == 'up':
      self.current_cell -= GM.SIZE
    elif move == 'down':
      self.current_cell += GM.SIZE
    elif move == "right":
      self.current_cell += 1
    elif move == "left":
      self.current_cell -= 1

  def action(self):
    self.km.activate()

  def get_digit(self,roi,cell=False):
    assert len(roi.shape) == 2, "get_digit(): Image must be binary"

    if roi.shape[0] != GM.UI_CELL_SIZE or roi.shape[1] != GM.UI_CELL_SIZE:
      roi = cv.resize(roi,(GM.UI_CELL_SIZE,GM.UI_CELL_SIZE)) 

    roi_cstr = auto_constrast(roi)

    _,th = cv.threshold(roi_cstr,45,255,cv.THRESH_BINARY_INV)
    if not cell:
      th[20:th.shape[1],0:36] = 0 #Remove THIS FUCKING VOLTORB
    else:
       th = self.clear_th(th)
    th[th.shape[1]-7:th.shape[1]] = 0 #Remove Line that apperas sometimes and breaks the contours pipeline

    cnts = cv.findContours(th.copy(), cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    return cnts,th,roi_cstr

  def get_contour_precedence(self,contour, cols):
    tolerance_factor = 10
    origin = cv.boundingRect(contour)
    return ((origin[1] // tolerance_factor) * tolerance_factor) * cols + origin[0]

  def set_info(self,m_id,mode='rows'):
    roi = self.infos[mode][m_id]['roi']
    if roi.shape[0] != GM.UI_CELL_SIZE or roi.shape[1] != GM.UI_CELL_SIZE:
      roi = cv.resize(roi,(GM.UI_CELL_SIZE,GM.UI_CELL_SIZE))
    cnts,th,processed = self.get_digit(roi)
    cnts = sorted(cnts,key=lambda x:self.get_contour_precedence(x,th.shape[1]))
    digits = []
    for cnt in cnts:
      (x, y, w, h) = cv.boundingRect(cnt)
      r = cv.resize(th[y:y+h,x:x+w],(32,32))
      digits.append(r)
    assert len(digits) == 3, f"set_info({m_id}, {mode}): cell must have 3 digits,but only {len(digits)} found"

    X = np.array(digits).reshape(-1,32,32,1)
    X = tf.keras.utils.normalize(X,axis=1)
    predictions = self.model.model.predict(X)

    pts = int( str(np.argmax(predictions[0])) + str(np.argmax(predictions[1])) )
    bombs = int( np.argmax(predictions[2]) )
    self.infos[mode][m_id]["pts"] = pts
    self.infos[mode][m_id]["bombs"] = bombs

    self.infos[mode][m_id]["processed"] = processed
    self.infos[mode][m_id]["th"] = th
    self.infos[mode][m_id]["roi"] = roi

  def calc_proba(self):
    probList = []
    for r in range(GM.SIZE):
      for c in range(GM.SIZE):
        if self.infos['cells'][r*GM.SIZE+c]['val'] == -1:
          if self.infos['rows'][r]["bombs"] == 0 or self.infos['cols'][c]["bombs"] == 0:
            probList.append((r*GM.SIZE + c,0.0))
          elif self.infos['rows'][r]["bombs"] == self.infos['rows'][r]["hidden"] or self.infos['cols'][c]["bombs"] == self.infos['cols'][c]["hidden"]:
            probList.append((r*GM.SIZE + c,1.0))
          else:
            probList.append( ( r*GM.SIZE + c , (self.infos['rows'][r]["bombs"] / self.infos['rows'][r]["hidden"])* (self.infos['cols'][c]["bombs"] / self.infos['cols'][c]["hidden"]) ))
    return probList

  def update_cell(self,cell):
    i,j = cell
    cell = self.infos['cells'][i*GM.SIZE+j]
    roi = self.frame[cell['loc']['y']:cell['loc']['y']+cell['loc']['h'], cell['loc']['x']:cell['loc']['x']+cell['loc']['w']]
    # assert roi.shape != (GM.UI_CELL_SIZE,GM.UI_CELL_SIZE), f"UpdateCell Invalid SHAPE {roi.shape}"
    cnts,th,processed = self.get_digit(roi,cell=True)
    if cnts:
      digits = []
      for cnt in cnts:
        (x, y, w, h) = cv.boundingRect(cnt)
        r = cv.resize(th[y:y+h,x:x+w],(32,32))
        digits.append(r)
      assert len(digits) == 1, f"update_cell({cell}): cell must have 1 digits,but {len(digits)} found"

      X = np.array(digits).reshape(-1,32,32,1)
      X = tf.keras.utils.normalize(X,axis=1)
      predictions = self.model.model.predict(X)

      val = int( np.argmax(predictions[0]) )
      # print(f"Cell[{i*GM.SIZE+j}] = {val}")

      if val == 8:#We discovered voltorb (retrain model by adding voltorb icon in trainable class)
        self.state = GM.STATE[2]
        return

      self.infos["cells"][i*GM.SIZE+j]['val'] = val

      self.infos["cells"][i*GM.SIZE+j]['roi'] = roi
      self.infos["cells"][i*GM.SIZE+j]['processed'] = processed
      self.infos["cells"][i*GM.SIZE+j]['th'] = th

      self.infos['rows'][i]['hidden'] -= 1
      self.infos['cols'][j]['hidden'] -= 1

      self.infos['rows'][i]['pts'] -= val
      self.infos['cols'][j]['pts'] -= val

  
  def get_game_info(self):
    for i in range(GM.SIZE):
      self.infos["rows"][i] = {"id":i,
                                "pts":-1,
                                "hidden":GM.SIZE,
                                "bombs":-1,
                                "loc": {"x":GM.UI_ROW_START_X,
                                        "y":GM.UI_ROW_START_Y+i*(GM.UI_SPACE+GM.UI_CELL_SIZE),
                                        "w":GM.UI_CELL_SIZE,
                                        "h":GM.UI_CELL_SIZE} }
      self.infos["rows"][i]["roi"] = self.frame[self.infos["rows"][i]["loc"]['y']:self.infos["rows"][i]["loc"]['y']+self.infos["rows"][i]["loc"]['h'],\
                                                self.infos["rows"][i]["loc"]['x']:self.infos["rows"][i]["loc"]['x']+self.infos["rows"][i]["loc"]['w']]

      self.infos["cols"][i] = {"id":i,
                                "pts":-1,
                                "hidden":GM.SIZE,
                                "bombs":-1,
                                "loc": {"x":GM.UI_COL_START_X+i*(GM.UI_SPACE+GM.UI_CELL_SIZE),
                                        "y":GM.UI_COL_START_Y,
                                        "w":GM.UI_CELL_SIZE,
                                        "h":GM.UI_CELL_SIZE} }

      self.infos["cols"][i]["roi"] = self.frame[self.infos["cols"][i]["loc"]['y']:self.infos["cols"][i]["loc"]['y']+self.infos["cols"][i]["loc"]['h'],\
                                                self.infos["cols"][i]["loc"]['x']:self.infos["cols"][i]["loc"]['x']+self.infos["cols"][i]["loc"]['w']]

      self.set_info(i)
      self.set_info(i,mode='cols')


      for j in range(GM.SIZE):
        self.infos["cells"][i*GM.SIZE+j] = {"id":i*GM.SIZE+j,
                                            "val":-1,
                                            "row":i,
                                            "col":j,
                                            "loc":{"x":(GM.UI_OFFSET)+j*(GM.UI_CELL_SIZE+GM.UI_SPACE),
                                                    "y":(GM.UI_OFFSET)+i*(GM.UI_CELL_SIZE+GM.UI_SPACE),
                                                    "w":GM.UI_CELL_SIZE,
                                                    "h":GM.UI_CELL_SIZE},
                                            "roi":None,
                                            "processed": None,
                                            "th":None}

  def clear_th(self,th):
    th[:6,:] =0
    th[-6:,:] =0
    th[:,:6] =0
    th[:,-6:] =0
    return th

  def build_image(self,mode='roi'):
    im = np.zeros(((GM.SIZE+1)*GM.UI_CELL_SIZE,(GM.SIZE+1)*GM.UI_CELL_SIZE),dtype=np.uint8)
    for i in range(GM.SIZE+1):

      for j in range(GM.SIZE+1):
        tl,br = (i*GM.UI_CELL_SIZE,j*GM.UI_CELL_SIZE), (i*GM.UI_CELL_SIZE+GM.UI_CELL_SIZE,j*GM.UI_CELL_SIZE+GM.UI_CELL_SIZE)

        roi = None
        if i < GM.SIZE and j < GM.SIZE:
          roi = self.infos["cells"][i*GM.SIZE+j][mode]
        elif i < GM.SIZE and j == GM.SIZE:
          roi = self.infos["rows"][i][mode]
        elif  j < GM.SIZE and i == GM.SIZE:
          roi = self.infos["cols"][j][mode]
        if roi is not None:
          im[tl[0]:br[0],tl[1]:br[1]] = roi
    return im                                                          
  
  def ui_board(self):
    im = self.build_image()
    processed = self.build_image('processed')
    th = self.build_image('th')  
    return np.hstack([im,processed,th])