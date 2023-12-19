import os
import csv
import sys
import time
import pygame as pg
from dataclasses import dataclass

WIDTH = 1600
HEIGHT = 1000
MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]

def main():
    titlefont = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 100)
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0
            
    