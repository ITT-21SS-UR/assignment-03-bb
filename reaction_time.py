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
        self.ui = uic.loadUi("experiment.ui", self)
        self.timesDict = {'ID':[], 'condition':[], 'shown stimulus':[], 'pressed key':[], 'correct key':[],
              'reaction time':[], 'timestamp':[]}


    def keyPressEvent(self, ev):
        if ev.key() == QtCore.Qt.Key_Space:
            self.counter += 1
            self.update()

    def start_test(self,testtype):
        #set explanation text
        print(testtype)

    def start_reaction(self, waittime):

    def save_results(self,dict):
        resultsdf = pd.read_csv("results.csv")





def main():
    app = QtWidgets.QApplication(sys.argv)
    experiment = Experiment()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()