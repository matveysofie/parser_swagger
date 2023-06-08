import os
import sys
import time


if "win" in sys.platform:
    BASEDIR = os.path.dirname(os.path.dirname(__file__))
elif "linux" in sys.platform:
    BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
SWAGGERDIR = os.path.join(BASEDIR, "swagger")
TESTSUITEDIR = os.path.join(SWAGGERDIR, "test_suites")
TESTCASEDIR = os.path.join(SWAGGERDIR, "test_cases")
APIDIR = os.path.join(SWAGGERDIR, "api")


PROFILEDIR = os.path.join(BASEDIR, "properties")
PROFILEPATH = os.path.join(PROFILEDIR, "config.ini")
  
LOGDIR = os.path.join(BASEDIR, "logs")
LOGFILEPATH = os.path.join(LOGDIR, "AllServer.log")
  
BACKUPDIR = os.path.join(BASEDIR, "swaggerBackUp")

CSVFILEPATH = os.path.join(SWAGGERDIR, "Result.csv")
EXCELFILEPATH = os.path.join(SWAGGERDIR, "Result.xlsx")
BACKTESTCASEPATH = os.path.join(SWAGGERDIR, "Result_back_up{}.xlsx".format(time.strftime('%Y-%m-%d_%H-%m')))


if __name__ == '__main__':
    print(SWAGGERDIR)
