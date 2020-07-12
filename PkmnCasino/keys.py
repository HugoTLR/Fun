from keyboard import press, release
from mouse import click
from time import sleep
import cv2 as cv
class KeyboardManager:
  play_button = cv.cvtColor(cv.imread("play_button.png"),cv.COLOR_BGR2GRAY)

  def input_key(self,val):
    press(val)
    sleep(.01)
    release(val)
    sleep(.3)


  def move(self,val):
    self.input_key(val)

  def activate(self):
    self.input_key('a')
    self.input_key('a') #Avoid game dialog box

  def run_game(self):
    self.input_key('a')


