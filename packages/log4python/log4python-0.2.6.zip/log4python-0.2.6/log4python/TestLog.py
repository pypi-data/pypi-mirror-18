#!/usr/local/python/bin
# coding=utf-8
import time
from Log4python import log

xxlog = log("xxx")
yylog = log("yyy")
count = 0
while True:
    print("Enter")
    try :
        '''增加用例：当主线程异常退出时，日志记录线程主动退出！'''
        count = count + 1
        if count > 150000:
            print(12 / 0)
    except:
        print("Error")
        raise
    xxlog.info("info")
    xxlog.error("yyy")
    xxlog.debug("debug")
    yylog.debug("xxxxxxxxxxxx")
    yylog.error("yylogError")
    time.sleep(2)
    print("END")
