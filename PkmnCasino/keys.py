from keyboard import press, release
from time import sleep




class KeyboardManager:
  def input_key(self,val):
    press(val)
    sleep(.01)
    release(val)
    if val == 'b':sleep(1)
    elif val == 'a':sleep(.75)
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
    self.input_key('a')
    self.input_key('a')
    self.input_key('a')
    self.input_key('a')
