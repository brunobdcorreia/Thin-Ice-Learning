import sys

class Logger(object):
    _instance = None
    def __init__(self,alert_level,file=sys.stderr):
        self.alert_level = alert_level
        self.file_output = file
    
    def log(self, string, *, level=1):
        if level <= self.alert_level:
            print(f"[Alert level {self.alert_level}] ", end="", file=self.file_output)
            print(string,end="\n", file=self.file_output)

    def log_csv(self, *params, level=1):
        if level <= self.alert_level:
            for item in params:
                print(f"{item}", end=",", file=self.file_output)
            print("\n", end="", file=self.file_output)

