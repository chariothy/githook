from pybeans import AppTool
import os, sys, shutil, time


APP = AppTool('githook')

def now():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())