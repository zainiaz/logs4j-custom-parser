import logging
from datetime import datetime

class Logger: 
    levels = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }
    def __init__(self, level, path):
        logging.basicConfig(filename=path+'//logs_analyzer.log', level=self.levels[level])
        
        self.add('debug', ":::::::::: New script execution ::::::::::")

    def add(self, level, message):
        log_message = f"[{self.get_datetime_string()}] " + message
        getattr(logging, level)(log_message)

    def get_datetime_string(self):
        current_date = datetime.now()
        
        return current_date.strftime("%Y-%m-%d %H:%M:%S")
    
# logging.basicConfig(filename='example.log', level=logging.DEBUG)

# logging.debug('This message should go to the log file')
# logging.info('So should this')
# logging.warning('And this, too')