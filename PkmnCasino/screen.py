import cv2
import numpy as np
import win32gui, win32ui, win32con, win32api
import pygetwindow as gw

CAP_W = 800
CAP_H = 450
CONV_W = 160
CONV_H = 90
NB_FEATURES = CONV_W * CONV_H

def grab_screen(shape=(800,450),offset=(0,0)):

    hwin = win32gui.GetDesktopWindow()


    width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)+offset[0]
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)++offset[1]
    if shape:
        width = shape[0]
        height = shape[1]

        


    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)
    
    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (height,width,4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())

    return cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)

def setWindow(name="DeSmuME 0.9.11 x64"):
    win = gw.getWindowsWithTitle(name)
    if len(win) == 0:
        print("NO WINDOW ! EXITING")
        return
    tm = win[0]
    tm.activate()
    tm.moveTo(-1920,0)