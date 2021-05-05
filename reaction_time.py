import sys
from PyQt5 import QtWidgets, QtGui, QtCore, uic
import random
import datetime as dt
import pandas as pd
import time
import os.path as path


class Experiment(QtWidgets.QMainWindow):

    def __init__(self):
        super(Experiment, self).__init__()
        self.ui = uic.loadUi("experiment.ui", self)
        self.reactiondict = {'ID': [], 'condition': [], 'shown_stimulus': [], 'pressed_key': [], 'correct_key': [],
                             'reaction_time_s': [], 'timestamp': []}
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

    # checks the state of the experiment and calls the next steps
    def testhandler(self):
        self.ui.startButton.show()
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

    # starts the experiment when the button is clicked
    def start_test(self):
        self.ui.startButton.hide()
        self.counter = 0
        self.start_reaction()

    # sets the id of the participant from the console input
    def set_participantId(self):
        try:
            self.participant_id = int(sys.argv[1])
        except (ValueError, IndexError):
            print("Please insert a number as an argument")
            self.participant_id = 1

    # initalise the "start"-button
    def init_button(self):
        self.ui.startButton.clicked.connect(self.start_test)

    # if key is pressed while the programm is waiting for a reaction, the reactiontime is saved
    def keyPressEvent(self, ev):
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

    # explanaiton for the first condition
    def explanation_one(self):
        self.ui.explainText.setText("A left arrow will be shown on the screen. "
                                    "When it appears,\npress the 'a'-key "
                                    "on your keyboard as fast as possible.")

    # explanaiton for the second condition
    def explanation_two(self):
        self.ui.explainText.setText("Either a left or right arrow will be shown "
                                    "on the screen. \nPress the 'a'-key "
                                    "on your keyboard when the left arrow appears \n"
                                    "and the 'd'-key when the right one appears "
                                    "-as fast as possible. \n"
                                    "Press the Button below to start")

    # text when experiment is finished
    def show_text_end(self):
        self.ui.explainText.setText("You are done. Thank you for participating in the "
                                    "experiment.")

    # starts the experiment
    def start_reaction(self):
        if self.counter < 10:
            print("setup wait")
            QtCore.QTimer.singleShot(random.randint(2, 6)*1000, lambda: self.show_stimulus())
        else:
            self.testhandler()

    # shows the stimulus on the screen depending on the condition
    def show_stimulus(self):
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
        self.waitforreaction = True

    # returns the reaction time
    def get_reactiontime(self):
        return dt.datetime.now().timestamp() - self.stimulustarttime

    # saves the reaction from the participant to the dictonary
    def save_reaction(self, reactiontime=0.0, pressedkey="left"):
        self.reactiondict["ID"].append(self.participant_id)
        self.reactiondict["condition"].append(self.testtype)
        self.reactiondict["shown_stimulus"].append(self.shownkey)
        self.reactiondict["pressed_key"].append(pressedkey)
        self.reactiondict["reaction_time_s"].append(reactiontime)
        if self.shownkey == pressedkey:
            self.reactiondict["correct_key"].append(True)
        else:
            self.reactiondict["correct_key"].append(False)
        self.reactiondict["timestamp"].append(dt.datetime.now())

    # saves the results to an .csv file
    def save_results(self, dict):
        if path.exists("reaction_time_results.csv"):
            resultsdfold = pd.read_csv("reaction_time_results.csv")
            resultsdfnew = pd.DataFrame.from_dict(dict)
            resultsdf = resultsdfold.append(resultsdfnew)
        else:
            resultsdf = pd.DataFrame.from_dict(dict)
        resultsdf.to_csv("reaction_time_results.csv", index=False)


def main():
    app = QtWidgets.QApplication(sys.argv)
    experiment = Experiment()
    experiment.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
