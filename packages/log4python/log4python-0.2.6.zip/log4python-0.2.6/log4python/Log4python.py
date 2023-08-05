#coding:utf-8
__author__ = 'root'
from ObserverModel import Subject, Observer
from LogSubject import LogSubject
from pyetc import load, reload, unload
import time
from datetime import datetime

import os
import sys
import logging
import logging.handlers

CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0

if hasattr(sys, 'frozen'): #support for py2exe
    _srcfile = "logging%s__init__%s" % (os.sep, __file__[-4:])
elif __file__[-4:].lower() in ['.pyc', '.pyo']:
    _srcfile = __file__[:-4] + '.py'
else:
    _srcfile = __file__
_srcfile = os.path.normcase(_srcfile)

# Global logger
logSubject = LogSubject()
#logSubject
__all__ = ['set_logger', 'debug', 'info', 'warning', 'error',
           'critical', 'exception']

class ColoredFormatter(logging.Formatter):
    '''A colorful formatter.'''

    def __init__(self, fmt = None, datefmt = None):
        logging.Formatter.__init__(self, fmt, datefmt)

g_logger = None
class log():
    debugFile = "log4py.debug"
    module_name = None
    basePath = ""
    globalsLogSubject = None
    logger = None
    config_all = None
    config_logger = None
    config_appender_list = []
    config_logger_default = {
        'level': 'ERROR',
        'additivity' : True,
    }
    config_appender_default = {
        'console' :{
            'type' :"Console",
            'target' :"console",
            'PatternLayout' :"[%(levelname)s] %(asctime)s %(message)s"
        }
    }
    level_type = {
        'INFO' : logging.INFO,
        'DEBUG' : logging.DEBUG,
        'WARN' : logging.WARN,
        'ERROR' : logging.ERROR,
        'CRITICAL' : logging.CRITICAL,
        }

    def __init__(self, module_name="", filename = None, mode = 'a', level='ERROR:DEBUG',
        fmt = '[%(levelname)s] %(asctime)s %(message)s',
        backup_count = 5, limit = 1024 * 1024 * 20, when = None):
        '''Configure the global logger.'''
        global logSubject, g_logger
        log.globalsLogSubject = logSubject
        self.debugLog("Module[%s]: init logger" %(module_name))
        #if log.globalsLogSubject == None:
        #    log.globalsLogSubject = LogSubject()
        self.basePath = log.globalsLogSubject.basePath
        self.debugLog("LogBasePath:"+self.basePath)
        LogObserver = Observer(log.globalsLogSubject)
        LogObserver.update = self.update
        level = level.split(':')

        if len(level) == 1: # Both set to the same level
            s_level = f_level = level[0]
        else:
            s_level = level[0]  # StreamHandler log level
            f_level = level[1]  # FileHandler log level

        self.config_logger = self.config_logger_default

        self.module_name = module_name
        self.logger = self.init_logger(module_name)
        self.import_log_funcs()
        if module_name != "":
            fmt = ("[module_name:%s], " %(module_name)) + fmt
        self.update(log.globalsLogSubject.data)
        self.debugLog("Module[%s]: finish init log file" %(self.module_name))

    def debugLog(self, msg):
        if self.globalsLogSubject.data['debug'] == False:
            return

        f = open(self.basePath +"/"+self.debugFile, "a+")
        f.write("module:%s; time:%s; Msg:%s" %(__name__, datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S"), msg+"\r\n"))
        f.close()

    def check_exists(self):
        try:
            if (not log.globalsLogSubject.reloadConfig.isAlive()):
                log.globalsLogSubject.restart()
        except:
            error_info = traceback.format_exc()
            self.debugLog(error_info)

    # update logger's configuration
    def update(self, data):
        self.debugLog("Module[%s]: begin update config" %(self.module_name))
        level = logging.CRITICAL
        self.config_all = data
        self.update_logger(self.logger.name)
        self.debugLog("Module[%s]: after update config" %(self.module_name))

    def update_logger(self, logger_name):
        # get logger
        if self.config_all.has_key("loggers") and self.config_all['loggers'].has_key(logger_name):
            self.config_logger = dict(self.config_logger_default, **self.config_all['loggers'][logger_name])
        else:
            if self.config_all.has_key("loggers") and self.config_all['loggers'].has_key("root"):
                self.debugLog("Module[%s]: In the new Configuration No Current Module's logger; then use ROOT's Config" %(self.module_name))
                self.config_logger = dict(self.config_logger_default, **self.config_all['loggers']["root"])
            else:
                self.debugLog("Module[%s]: In the new Configuration No Current Module's logger; No ROOT's logger; use the Deault Configuration" %(self.module_name))
                self.config_logger = self.config_logger_default

        # get appender
        self.config_appender_list = []
        if self.config_logger.has_key("AppenderRef"):
            appenders = self.config_logger['AppenderRef']
            for appender_name in appenders:
                if self.config_all.has_key("appenders") and self.config_all['appenders'].has_key(appender_name):
                    self.config_appender_list.append(dict(self.config_appender_default, **self.config_all['appenders'][appender_name]))
        else:
            self.config_appender_list.append(self.config_appender_default)

        # update logger's parameters
        self.update_logger_config()

    def update_logger_config(self):
        newLogger = self.init_logger(self.module_name)
        # set log's Level
        s_level = self.level_type[self.config_logger['level']]
        # set log's Pattern
        fmt = '[%(levelname)s] %(asctime)s %(message)s'

        # clear old handlers
        self.logger.handlers = []
        for config_appender in self.config_appender_list:
            if config_appender.has_key("PatternLayout"):
                fmt = config_appender['PatternLayout']

            if str(config_appender['type']).upper() == "FILE":
                filename = config_appender['FileName']
                if filename.find("/") < 0:
                    filename = self.basePath +"/"+ filename
                if filename[0] == "/":
                    logDir = os.path.dirname(filename)
                    if not os.path.exists(logDir):
                        os.makedirs(logDir)
                self.debugLog("Module[%s]: init log file[%s]" %(self.module_name, filename))
                mode = 'a'
                backup_count = 5
                limit = 1024 * 1024 * 20
                when = None
                # set log's appender
                self.add_filehandler(newLogger, s_level, fmt, filename, mode, backup_count, limit, when)

            if str(config_appender['type']).upper() == "CONSOLE":
                self.add_streamhandler(newLogger, s_level, fmt)

        # set the New Logger
        self.logger = newLogger

    def add_handler(self, logger, cls, level, fmt, colorful, **kwargs):
        '''Add a configured handler to the global logger.'''

        if isinstance(level, str):
            level = getattr(logging, level.upper(), logging.DEBUG)

        handler = cls(**kwargs)
        handler.setLevel(level)

        if colorful:
            formatter = ColoredFormatter(fmt)
        else:
            formatter = logging.Formatter(fmt)

        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return handler

    def add_streamhandler(self, logger, level, fmt):
        '''Add a stream handler to the global logger.'''
        return self.add_handler(logger,logging.StreamHandler, level, fmt, True)

    def add_filehandler(self, logger, level, fmt, filename , mode, backup_count, limit, when):
        '''Add a file handler to the global logger.'''
        kwargs = {}

        # If the filename is not set, use the default filename
        if filename is None:
            filename = getattr(sys.modules['__main__'], '__file__', 'log.py')
            filename = os.path.basename(filename.replace('.py', '.log'))
            #filename = os.path.join('/tmp', filename)

        kwargs['filename'] = filename

        # Choose the filehandler based on the passed arguments
        if backup_count == 0: # Use FileHandler
            cls = logging.FileHandler
            kwargs['mode' ] = mode
        elif when is None:  # Use RotatingFileHandler
            cls = logging.handlers.RotatingFileHandler
            kwargs['maxBytes'] = limit
            kwargs['backupCount'] = backup_count
            kwargs['mode' ] = mode
        else: # Use TimedRotatingFileHandler
            cls = logging.handlers.TimedRotatingFileHandler
            kwargs['when'] = when
            kwargs['interval'] = limit
            kwargs['backupCount'] = backup_count

        return self.add_handler(logger, cls, level, fmt, False, **kwargs)

    def init_logger(self, module):
        '''Reload the global logger.'''
        logger = None
        if module == "":
            logger = logging.getLogger()
        else:
            logger = logging.getLogger(module)

        logger.setLevel(logging.DEBUG)
        return logger

    def init_logger_bak(self, module):
        '''Reload the global logger.'''
        if self.logger is None:
            if module == "":
                self.logger = logging.getLogger()
            else:
                self.logger = logging.getLogger(module)
        #else:
        #    logging.shutdown()
        #    self.g_logger.handlers = []

        self.logger.setLevel(logging.DEBUG)

    def set_logger(self, module_name="", filename = None, mode = 'a', level='ERROR:DEBUG',
        fmt = '[%(levelname)s] %(asctime)s %(message)s',
        backup_count = 5, limit = 20480, when = None):
        '''Configure the global logger.'''
        level = level.split(':')

        if len(level) == 1: # Both set to the same level
            s_level = f_level = level[0]
        else:
            s_level = level[0]  # StreamHandler log level
            f_level = level[1]  # FileHandler log level

        self.logger = self.init_logger(module_name)
        if module_name != "":
            fmt = ("[module_name:%s], " %(module_name)) + fmt
        self.add_streamhandler(self.logger, s_level, fmt)
        self.add_filehandler(self.logger, f_level, fmt, filename, mode, backup_count, limit, when)

    def import_log_funcs(self):
        '''Import the common log functions from the self.logger to the module.'''
        #curr_mod = sys.modules[__name__]
        log_funcs = ['isEnabledFor', '_log', 'findCaller', 'makeRecord', 'handle']

        for func_name in log_funcs:
            func = getattr(self.logger, func_name)
            setattr(self, func_name, func)

    def critical(self, msg, *args, **kwargs):
        self.check_exists()
        if self.isEnabledFor(CRITICAL):
            self._log(CRITICAL, msg, args, **kwargs)
        if self.config_logger['additivity'] and self.logger.name != 'root' :
            record = self.getRecord(CRITICAL, msg, args, **kwargs)
            g_logger.handleRecord(CRITICAL, record)

    def error(self, msg, *args, **kwargs):
        self.check_exists()
        if self.isEnabledFor(ERROR):
            self._log(ERROR, msg, args, **kwargs)
        if self.config_logger['additivity'] and self.logger.name != 'root' :
            record = self.getRecord(ERROR, msg, args, **kwargs)
            g_logger.handleRecord(CRITICAL, record)

    def warning(self, msg, *args, **kwargs):
        self.check_exists()
        if self.isEnabledFor(WARNING):
            self._log(WARNING, msg, args, **kwargs)
        if self.config_logger['additivity'] and self.logger.name != 'root' :
            record = self.getRecord(WARNING, msg, args, **kwargs)
            g_logger.handleRecord(CRITICAL, record)

    def info(self, msg, *args, **kwargs):
        self.check_exists()
        if self.isEnabledFor(INFO):
            self._log(INFO, msg, args, **kwargs)
        if self.config_logger['additivity'] and self.logger.name != 'root' :
            record = self.getRecord(INFO, msg, args, **kwargs)
            g_logger.handleRecord(CRITICAL, record)

    def debug(self, msg, *args, **kwargs):
        self.check_exists()
        if self.isEnabledFor(DEBUG):
            self._log(DEBUG, msg, args, **kwargs)
        if self.config_logger['additivity'] and self.logger.name != 'root' :
            record = self.getRecord(DEBUG, msg, args, **kwargs)
            g_logger.handleRecord(CRITICAL, record)

    def getRecord(self,level, msg, args, exc_info=None, extra=None):
        if _srcfile:
            #IronPython doesn't track Python frames, so findCaller raises an
            #exception on some versions of IronPython. We trap it here so that
            #IronPython can use logging.
            try:
                fn, lno, func = self.findCaller()
            except ValueError:
                fn, lno, func = "(unknown file)", 0, "(unknown function)"
        else:
            fn, lno, func = "(unknown file)", 0, "(unknown function)"
        if exc_info:
            if not isinstance(exc_info, tuple):
                exc_info = sys.exc_info()
        record = self.makeRecord(self.logger.name, level, fn, lno, msg, args, exc_info, func, extra)

        return record

    def handleRecord(self, level, record):
        if self.isEnabledFor(level):
            self.handle(record)

if g_logger == None:
    g_logger = log("root")
