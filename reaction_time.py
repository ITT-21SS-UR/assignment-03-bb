import sys
from PyQt5 import QtWidgets, QtGui, QtCore, uic
import random
import datetime as dt
import pandas as pd
import time
import os.path as path

#csv rows
FIELDNAMES = ['ID', 'condition', 'shown stimulus', 'pressed key', 'correct key', 
              'reaction time', 'timestamp']


class Experiment(QtWidgets.QMainWindow):

    def __init__(self):
        super(Experiment, self).__init__()
        self.ui = uic.loadUi("experiment.ui", self)
        self.reactiondict = {'ID': [], 'condition': [], 'shown stimulus': [], 'pressed key': [], 'correct key': [],
                             'reaction time (s)': [], 'timestamp': []}
        self.waitforreaction = False
        self.stimulustarttime = dt.datetime.now().timestamp()
        print(type(self.stimulustarttime))
        print(self.stimulustarttime)
        self.shownkey = ""
        self.ui.rightArrowText.hide()
        self.ui.leftArrowText.hide()
        self.set_participantId()
        self.init_button()
        self.counter = 0
        self.testtype = ""
        self.experiment_one_done = False
        self.experiment_two_done = False
        self.testhandler()

    def testhandler(self):
        self.ui.startButton.show()
        print(self.testtype, self.experiment_one_done, self.experiment_two_done)
        if self.testtype == "":
            if self.participant_id % 2:
                self.explanation_one()
                self.testtype = "A"
                self.experiment_one_done = True
            else:
                self.explanation_two()
                self.testtype = "B"
                self.experiment_two_done = True
        elif self.testtype == "A":
            if self.experiment_two_done:
                self.show_text_end()
                self.save_results(self.reactiondict)
                self.ui.startButton.hide()

            else:
                self.explanation_two()
                self.testtype = "B"
                self.experiment_two_done = True

        elif self.testtype == "B":
            if self.experiment_one_done:
                self.show_text_end()
                self.save_results(self.reactiondict)
                self.ui.startButton.hide()

            else:
                self.explanation_one()
                self.testtype = "A"
                self.experiment_one_done = True


    def start_test(self):
        self.ui.startButton.hide()
        self.counter = 0
        self.start_reaction()

    def set_participantId(self):
        try:
            self.participant_id = int(sys.argv[1])
        except (ValueError, IndexError):
            print("Please insert a number as an argument")
            self.participant_id = 1
            #sys.exit(3)


    def init_button(self):
        self.ui.startButton.clicked.connect(self.start_test)


    #if key is pressed while the programm is waiting for a reaction, the reactiontime is saved
    def keyPressEvent(self, ev):
        print(ev.text())
        print(self.waitforreaction)
        if self.waitforreaction:
            if ev.text() == "a":
                self.ui.rightArrowText.hide()
                self.ui.leftArrowText.hide()
                self.waitforreaction = False
                self.save_reaction(reactiontime=self.get_reactiontime(), pressedkey="left")
                self.counter = self.counter + 1
                self.start_reaction()

            if ev.text() == "d":
                self.ui.rightArrowText.hide()
                self.ui.leftArrowText.hide()
                self.waitforreaction = False
                self.save_reaction(reactiontime=self.get_reactiontime(), pressedkey="right")
                self.counter = self.counter + 1
                self.start_reaction()







    def explanation_one(self):
        self.ui.explainText.setText("A left arrow will be shown on the screen. "
                                    "When it appears,\npress the left arrow key "
                                    "on your keyboard as fast as possible. \n"
                                    "Press the Button below to start")

    def explanation_two(self):
        self.ui.explainText.setText("Either a left or right arrow will be shown "
                                    "on the screen. \nPress the suitable arrow key "
                                    "on your keyboard as fast as possible. \n"
                                    "Press the Button below to start")

    def show_text_end(self):
        self.ui.explainText.setText("You are done. Thank you for participating in the "
                                    "experiment.")


    def start_reaction(self):
        if self.counter < 2:
            print("setup wait")
            self.waitforreaction = True
            QtCore.QTimer.singleShot(random.randint(2, 6)*1000, lambda: self.show_stimulus())
        else:
            self.testhandler()




    def show_stimulus (self):
        self.stimulustarttime = dt.datetime.now().timestamp()
        if self.testtype == "A":
            self.ui.leftArrowText.show()
            self.shownkey = "left"
        else:
            if int(dt.datetime.now().timestamp()) % 2 == 0:
                self.ui.rightArrowText.show()
                self.shownkey = "right"
            else:
                self.ui.leftArrowText.show()
                self.shownkey = "left"

    def get_reactiontime(self):
        return dt.datetime.now().timestamp() - self.stimulustarttime

    def save_reaction(self, reactiontime = 0.0, pressedkey = "left"):
        self.reactiondict["ID"].append(self.participant_id)
        self.reactiondict["condition"].append(self.testtype)
        self.reactiondict["shown stimulus"].append(self.shownkey)
        self.reactiondict["pressed key"].append(pressedkey)
        self.reactiondict["reaction time (s)"].append(reactiontime)
        if self.shownkey == pressedkey:
            self.reactiondict["correct key"].append(True)
        else:
            self.reactiondict["correct key"].append(False)
        self.reactiondict["timestamp"].append(dt.datetime.now().timestamp())



    def save_results(self,dict):
        if path.exists("results.csv"):
            resultsdfold = pd.read_csv("results.csv")
            resultsdfnew = pd.DataFrame.from_dict(dict)
            resultsdf = resultsdfold.append(resultsdfnew)
        else:
            print(dict)
            resultsdf = pd.DataFrame.from_dict(dict)
        resultsdf.to_csv("results.csv", index=False)





def main():
    app = QtWidgets.QApplication(sys.argv)
    experiment = Experiment()
    experiment.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()