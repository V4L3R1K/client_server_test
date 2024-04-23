import time
import os

f_name = "./log.log"  # log file


def log(str):
    global f_name
    if not os.path.exists(f_name):
        f_name = time.strftime("log_%Y_%m_%d_%H_%M_%S",
                               time.localtime(time.time()))+".log"
    with open(f_name, "a") as f:
        t = time.strftime("%Y.%m.%d %H:%M:%S", time.localtime(time.time()))
        f.write("["+t+"] "+str+"\n")
