import sys

class Logger(object):
    _instance = None
    def __init__(self,alert_level,output_type='log',file=sys.stderr):
        self.alert_level = alert_level
        self.output_type = output_type
        self.file_output = file
    
    def log(self, string, *, level=1):
        if level <= self.alert_level:
            if self.output_type == 'log':
                print(f"[Alert level {self.alert_level}] ", end="", file=self.file_output)
                print(string,end="\n", file=self.file_output)
            else:
                pass
    def log_cvs(self, *params, level=1):
        if level <= self.alert_level:
            if self.output_type == 'cvs':
                for item in params:
                    print(f"{item}", end=",", file=self.file_output)
                print("\n", end="", file=self.file_output)
            else:
                pass

