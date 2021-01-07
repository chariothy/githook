from chariothy_common import AppTool
import os, sys, shutil, time


APP = AppTool('githook', os.getcwd())

def now():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

