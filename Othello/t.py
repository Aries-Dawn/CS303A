import ctypes
import sys
import time
import random

import pyautogui as pp


def click_tiao_zhan():
    x = 403
    y = 126

    pp.moveTo(x, y, duration=0.2)
    pp.click(x=x, y=y, button='left')
    return


if __name__ == '__main__':
    while True:
        click_tiao_zhan()
        time.sleep(240)
