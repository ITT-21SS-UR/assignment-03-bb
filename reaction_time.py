import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import random
import time
import pandas as pd

#csv rows
FIELDNAMES = ['ID', 'condition', 'shown stimulus', 'pressed key', 'correct key', 
              'reaction time', 'timestamp']


class Experiment():

    def __init__(self):
        
        


def main():
    app = QtWidgets.QApplication(sys.argv)
    experiment = Experiment()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()