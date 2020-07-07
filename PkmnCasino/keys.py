from keyboard import press, release
from time import sleep




class KeyboardManager:
  def input_key(self,val):
    press(val)
    sleep(.01)
    release(val)
    if val == 'b':sleep(1)
    elif val == 'a':sleep(1)
    else:sleep(.1)

  def move(self,val):
    self.input_key(val)

  def activate(self):
    self.input_key('a')
    self.input_key('a') #Avoid game dialog box

  def run_game(self):
    self.input_key('a')

  def game_over(self):
    self.input_key('a')

  def quit(self):
    self.input_key('b')
    for _ in range(4):
      self.input_key('a')

  def game_win(self):
    for _ in range(6):
      self.input_key('a')
    self.input_key('right') #In case we trigger lvl up ?