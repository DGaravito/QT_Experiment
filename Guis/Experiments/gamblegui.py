import random
import time

from PyQt6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt, pyqtSignal

from Guis.Experiments import gui


class ARTTExp(gui.Experiment):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__(person)

        # Instructions
        self.instructions.setText('Press ' + self.person.leftkey[0] + ' for the left option and ' +
                                  self.person.rightkey[0] + ' for the right option')

        # Set up Left option
        self.left = QLabel('')
        self.left.setFont(QFont('Helvetica', 40))
        self.left.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Set up right option
        self.righttoptext = QLabel('')
        self.righttoptext.setFont(QFont('Helvetica', 40))
        self.righttoptext.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.rightpic = QLabel()
        self.rightpic.setPixmap(QPixmap())
        self.rightpic.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.rightbottomtext = QLabel('')
        self.rightbottomtext.setFont(QFont('Helvetica', 40))
        self.rightbottomtext.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Put right option stuff in a vertical layout
        rightlayout = QVBoxLayout()

        rightlayout.addWidget(self.righttoptext)
        rightlayout.addWidget(self.rightpic)
        rightlayout.addWidget(self.rightbottomtext)

        # Put Left and Right options in horizontal layout
        explayout = QHBoxLayout()

        explayout.addStretch(1)
        explayout.addWidget(self.left)
        explayout.addStretch(1)
        explayout.addWidget(self.middle)
        explayout.addStretch(1)
        explayout.addLayout(rightlayout)
        explayout.addStretch(1)

        # Put everything in vertical layout
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addLayout(explayout)
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addWidget(self.quitbutton)

    def generatenext(self):
        """
        Generate the info for the next trial and put it on screen. if the final trial was just completed, then the next
        round is started or the completion text is put on screen
        """

        # stop the timer
        self.ititimer.stop()

        # reset the borders in case there was one
        self.righttoptext.setStyleSheet('border: 0px;')
        self.rightbottomtext.setStyleSheet('border: 0px;')
        self.left.setStyleSheet('border: 0px;')

        # if-then statement to determine whether the amount of trials completed is less than the number of trials the
        # user wants
        if self.trialsdone < self.person.get_trials():

            # get trial text
            info = self.person.get_design_text()

            # set the left and right side using the trial text
            self.left.setText(info[0])
            pixmap = 'Assets/' + info[2]
            self.rightpic.setPixmap(QPixmap(pixmap))

            if info[3] == 1:
                self.righttoptext.setText(info[1])
                self.rightbottomtext.setText('0')

            else:
                self.rightbottomtext.setText(info[1])
                self.righttoptext.setText('0')

            # set the middle to or
            self.middle.setText('OR')

            # log the trial onset time
            self.starttime = time.time() - self.overallstart

            # start the trial timer
            self.timer.start(5000)

            # enable participant responses
            self.responseenabled = 1

            # if fmri mode, then set the new trial timer now
            if self.person.fmri == 'Yes':
                self.ititimer.start(5500)

        # if the trials requested have been completed
        else:

            # blank out the sides
            self.left.setText('')
            self.righttoptext.setText('')
            self.righttoptext.setText('')

            # increase the number of rounds done and reset the number of trials done to 0
            self.roundsdone += 1
            self.trialsdone = 0

            # set the middle text to the appropriate text from the participant class
            self.middle.setText(self.person.nextround(self.roundsdone))

            # if all of the requested rounds have been completed
            if self.person.rounds == self.roundsdone:

                # output the trial data and thank the participant
                self.person.output()
                self.instructions.setText('Thank you!')

                # if the user wanted one of the participant's choices to get randomly chosen, then put that on screen
                if self.person.outcomeopt == 'Yes':
                    outcome = random.choice(self.person.outcomelist)
                    self.middle.setText('Your outcome: ' + outcome)

            # if not, indicate that you are now between rounds
            else:

                self.betweenrounds = 1

    def iti(self, state=0):
        """
        this function blanks out the screen and either warns the participant to be faster or has a fixation cross in the
        middle, depending on the value of state. It then sets the next design text
        :param state: default 0; only changes to 1 if it called from the timeout function and the experiment is in fmri
        mode. The value only serves to indicate this state
        """

        # blank out the sides
        self.left.setText('')
        self.rightpic.setPixmap(QPixmap())
        self.righttoptext.setText('')
        self.rightbottomtext.setText('')

        # if state is 1, that means the participant timed out and the experiment is in fmri mode, so change iti to the
        # warning
        if state == 1:

            self.middle.setText('Please try to be quicker')

        # if the experiment is not in fmri mode or the participant did not time out, then leave this as a cross
        else:

            self.middle.setText('+')

        # if you are not in fmri mode and you have at least completed one trial, then start the timer for the next round
        if (self.person.fmri == 'No') & (self.trialsdone > 0):

            self.ititimer.start(1000)

        # if this function is called before the first trial is set up, then set up a timer for the first trial
        if self.trialsdone == 0:

            self.ititimer.start(1000)

    def timeout(self):
        """
        if the timer runs out and the participant doesn't respond, then the timers stop, 9999 gets put in as the
        reaction time, and the trial is "completed" without a response
        """

        # stop the timer
        self.timer.stop()

        # blank out the sides
        self.left.setText('')
        self.rightpic.setPixmap(QPixmap())
        self.righttoptext.setText('')
        self.rightbottomtext.setText('')

        # set the middle to a warning
        self.middle.setText('Please try to be quicker')

        # send the trial data to the participant class
        self.person.updateoutput(self.trialsdone, self.starttime, 9999)

        # if you're not in fmri mode, then warn and start the reset timer
        if self.person.fmri == 'No':

            self.middle.setText('Please try to be quicker')
            self.trialresettimer.start(1000)

        # if you are in fmri mode, then disable participant input, increment the trial counter, and go to the iti screen
        else:

            self.trialsdone += 1
            self.responseenabled = 0
            self.iti(1)

    def responsereset(self):
        """
        if you're not in fmri mode, then this function resets the trial so that the participant can complete it
        """

        # stop the reset timer
        self.trialresettimer.stop()

        # get the trial text
        info = self.person.get_design_text()

        # set the left using the trial text
        self.left.setText(info[0])

        # get the picture for the right
        pixmap = 'Assets/' + info[2]
        self.rightpic.setPixmap(QPixmap(pixmap))

        # set the right text depending on if the trial is a risk or an ambiguous one
        if info[3] == 1:
            self.righttoptext.setText(info[1])
            self.rightbottomtext.setText('0')

        else:
            self.rightbottomtext.setText(info[1])
            self.righttoptext.setText('0')

        # set the middle text to or
        self.middle.setText('OR')

        # start the timer again
        self.timer.start(5000)

    def keyaction(self, key):
        """
        Reads the keys that are pressed and does the corresponding actions
        :param key: the key that was pressed
        """

        # if someone presses the g key and the participant is between rounds...
        if (key in ['g', 'G']) & (self.betweenrounds == 1):

            # indicate that the participant is no longer between rounds so g and i keys won't mess things up
            self.betweenrounds = 0

            # if this is the first trial of the first round, set the global start time to make the onset time make more
            # sense
            if (self.trialsdone == 0) & (self.roundsdone == 0):

                self.overallstart = time.time()

            # set the window to the iti screen
            self.iti()

        # if the participant presses the left or right keys and is allowed to respond
        if ((key in self.person.rightkey) | (key in self.person.leftkey)) & (self.responseenabled == 1):

            # stop the timer and prevent users from sending more inputs
            self.timer.stop()
            self.responseenabled = 0

            # increment the trial counter
            self.trialsdone += 1

            # use time.time and the start time variable to compute rt
            endtime = time.time() - self.overallstart
            rt = endtime - self.starttime

            # if the key was the right key...
            if key in self.person.rightkey:

                # put a border around the middle to indicate a user input was received
                self.righttoptext.setStyleSheet('border: 3px solid blue;')
                self.rightbottomtext.setStyleSheet('border: 3px solid blue;')

                # set response to 1
                response = 1

            # if the key was the left key...
            else:

                # put a border around the middle to indicate a user input was received
                self.left.setStyleSheet('border: 3px solid blue;')

                # set response to 0
                response = 0

            # send the trial data to the participant class
            self.person.updateoutput(self.trialsdone, self.starttime, rt, response)

            self.iti()

        # if someone presses the i key and the participant is between rounds...
        if (key in ['i', 'I']) & (self.betweenrounds == 1):

            # increase the index for the instructions
            self.inst += 1

            # if the instruction index is five, then load the relevant picture
            if self.inst == 5:

                pixmap = QPixmap('Assets/ARTT_risk_25.png')
                self.middle.setPixmap(pixmap.scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio))

            # if the instruction index is eleven, then load the relevant picture
            elif self.inst == 11:

                pixmap = QPixmap('Assets/ARTT_ambig_50.png')
                self.middle.setPixmap(pixmap.scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio))

            else:
                # get the associated text
                self.middle.setText(self.person.get_instructions(self.inst))

            # if the index reaches fifteen...
            if self.inst == 15:

                # reset to zero so the instructions can be viewed again
                self.inst = 0


class RAExp(gui.Experiment):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__(person)

        # Instructions
        self.instructions.setText('Press ' + self.person.leftkey[0] + ' for the left option and ' +
                                  self.person.rightkey[0] + ' for the right option')

        # Left and right options (and middle stuff) with font settingsguis
        self.left = QLabel('')
        self.left.setFont(QFont('Helvetica', 40))
        self.left.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.rightgain = QLabel('')
        self.rightgain.setFont(QFont('Helvetica', 40))
        self.rightgain.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.rightloss = QLabel('')
        self.rightloss.setFont(QFont('Helvetica', 40))
        self.rightloss.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Put Left and Right visual options in horizontal layout
        gamblelayout = QVBoxLayout()

        gamblelayout.addWidget(self.rightgain)
        gamblelayout.addWidget(self.rightloss)

        # Put Left and Right words for options in horizontal layout
        mainhlayout = QHBoxLayout()

        mainhlayout.addStretch(1)
        mainhlayout.addWidget(self.left)
        mainhlayout.addStretch(1)
        mainhlayout.addWidget(self.middle)
        mainhlayout.addStretch(1)
        mainhlayout.addLayout(gamblelayout)
        mainhlayout.addStretch(1)

        # Put everything in vertical layout
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addLayout(mainhlayout)
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addWidget(self.quitbutton)

    def generatenext(self):
        """
        Generate the info for the next trial and put it on screen. if the final trial was just completed, then the next
        round is started or the completion text is put on screen
        """

        # stop the timer
        self.ititimer.stop()

        # reset the borders in case there was one
        self.rightgain.setStyleSheet('border: 0px;')
        self.rightloss.setStyleSheet('border: 0px;')
        self.left.setStyleSheet('border: 0px;')

        # if-then statement to determine whether the amount of trials completed is less than the number of trials the
        # user wants
        if self.trialsdone < self.person.get_trials():

            # get trial text
            info = self.person.get_design_text()

            # set the left and right side using the trial text
            self.left.setText('Getting $0')
            self.rightgain.setText(info[0])
            self.rightloss.setText(info[1])

            # set the middle to or
            self.middle.setText('OR')

            # log the trial onset time
            self.starttime = time.time() - self.overallstart

            # start the trial timer
            self.timer.start(5000)

            # enable participant responses
            self.responseenabled = 1

            # if fmri mode, then set the new trial timer now
            if self.person.fmri == 'Yes':
                self.ititimer.start(5500)

        # if the trials requested have been completed
        else:

            # blank out the sides
            self.left.setText('')
            self.rightgain.setText('')
            self.rightloss.setText('')

            # increase the number of rounds done and reset the number of trials done to 0
            self.roundsdone += 1
            self.trialsdone = 0

            # set the middle text to the appropriate text from the participant class
            self.middle.setText(self.person.nextround(self.roundsdone))

            # if all of the requested rounds have been completed
            if self.person.rounds == self.roundsdone:

                # output the trial data and thank the participant
                self.person.output()
                self.instructions.setText('Thank you!')

                # if the user wanted one of the participant's choices to get randomly chosen, then put that on screen
                if self.person.outcomeopt == 'Yes':
                    outcome = random.choice(self.person.outcomelist)
                    self.middle.setText('Your outcome: ' + outcome)

            # if not, indicate that you are now between rounds
            else:

                self.betweenrounds = 1

    def iti(self, state=0):
        """
        this function blanks out the screen and either warns the participant to be faster or has a fixation cross in the
        middle, depending on the value of state. It then sets the next design text
        :param state: default 0; only changes to 1 if it called from the timeout function and the experiment is in fmri
        mode. The value only serves to indicate this state
        """

        # blank out the sides
        self.left.setText('')
        self.rightgain.setText('')
        self.rightloss.setText('')

        # if state is 1, that means the participant timed out and the experiment is in fmri mode, so change iti to the
        # warning
        if state == 1:

            self.middle.setText('Please try to be quicker')

        # if the experiment is not in fmri mode or the participant did not time out, then leave this as a cross
        else:

            self.middle.setText('+')

        # update the design text
        self.person.set_design_text()

        # if you are not in fmri mode and you have at least completed one trial, then start the timer for the next round
        if (self.person.fmri == 'No') & (self.trialsdone > 0):

            self.ititimer.start(1000)

        # if this function is called before the first trial is set up, then set up a timer for the first trial
        if self.trialsdone == 0:

            self.ititimer.start(1000)

    def timeout(self):
        """
        if the timer runs out and the participant doesn't respond, then the timers stop, 9999 gets put in as the
        reaction time, and the trial is "completed" without a response
        """

        # stop the timer
        self.timer.stop()

        # blank out the sides
        self.left.setText('')
        self.rightgain.setText('')
        self.rightloss.setText('')

        # set the middle to a warning
        self.middle.setText('Please try to be quicker')

        # send the trial data to the participant class
        self.person.updateoutput(self.trialsdone, self.starttime, 9999)

        # if you're not in fmri mode, then warn and start the reset timer
        if self.person.fmri == 'No':

            self.middle.setText('Please try to be quicker')
            self.trialresettimer.start(1000)

        # if you are in fmri mode, then disable participant input, increment the trial counter, and go to the iti screen
        else:

            self.trialsdone += 1
            self.responseenabled = 0
            self.iti(1)

    def responsereset(self):
        """
        if you're not in fmri mode, then this function resets the trial so that the participant can complete it
        """

        # stop the reset timer
        self.trialresettimer.stop()

        # get the trial text
        info = self.person.get_design_text()

        # set the left and right using the trial text
        self.left.setText('0')
        self.rightgain.setText(info[0])
        self.rightloss.setText(info[1])

        # set the middle text to or
        self.middle.setText('OR')

        # start the timer again
        self.timer.start(5000)

    def keyaction(self, key):
        """
        Reads the keys that are pressed and does the corresponding actions
        :param key: the key that was pressed
        """

        # if someone presses the g key and the participant is between rounds...
        if (key in ['g', 'G']) & (self.betweenrounds == 1):

            # indicate that the participant is no longer between rounds so g and i keys won't mess things up
            self.betweenrounds = 0

            # if this is the first trial of the first round, set the global start time to make the onset time make more
            # sense
            if (self.trialsdone == 0) & (self.roundsdone == 0):

                self.overallstart = time.time()

            # set the window to the iti screen
            self.iti()

        # if the participant presses the left or right keys and is allowed to respond
        if ((key in self.person.rightkey) | (key in self.person.leftkey)) & (self.responseenabled == 1):

            # stop the timer and prevent users from sending more inputs
            self.timer.stop()
            self.responseenabled = 0

            # increment the trial counter
            self.trialsdone += 1

            # use time.time and the start time variable to compute rt
            endtime = time.time() - self.overallstart
            rt = endtime - self.starttime

            # if the key was the right key...
            if key in self.person.rightkey:

                # put a border around the middle to indicate a user input was received
                self.rightgain.setStyleSheet('border: 3px solid blue;')
                self.rightloss.setStyleSheet('border: 3px solid blue;')

                # set response to 1
                response = 1

            # if the key was the left key...
            else:

                # put a border around the middle to indicate a user input was received
                self.left.setStyleSheet('border: 3px solid blue;')

                # set response to 0
                response = 0

            # send the trial data to the participant class
            self.person.updateoutput(self.trialsdone, self.starttime, rt, response)

            self.iti()

        # if someone presses the i key and the participant is between rounds...
        if (key in ['i', 'I']) & (self.betweenrounds == 1):

            # increase the index for the instructions
            self.inst += 1

            # get the associated text
            self.middle.setText(self.person.get_instructions(self.inst))

            # if the index reaches five...
            if self.inst == 5:

                # reset to zero so the instructions can be viewed again
                self.inst = 0


class FrameExp(gui.Experiment):
    keyPressed = pyqtSignal(str)

    def __init__(self, person):
        super().__init__(person)

        # Instructions
        self.instructions.setText('Press ' + self.person.leftkey[0] + ' for the left option and ' +
                                  self.person.rightkey[0] + ' for the right option')

        # Left and right options (and middle stuff) with font settingsguis
        self.left = QLabel('')
        self.left.setFont(QFont('Helvetica', 40))
        self.left.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.righttop = QLabel('')
        self.righttop.setFont(QFont('Helvetica', 40))
        self.righttop.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.rightbottom = QLabel('')
        self.rightbottom.setFont(QFont('Helvetica', 40))
        self.rightbottom.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Put gamble parts in vertical layout
        gamblelayout = QVBoxLayout()

        gamblelayout.addWidget(self.righttop)
        gamblelayout.addWidget(self.rightbottom)

        # Put Left and Right words for options in horizontal layout
        mainhlayout = QHBoxLayout()

        mainhlayout.addStretch(1)
        mainhlayout.addWidget(self.left)
        mainhlayout.addStretch(1)
        mainhlayout.addWidget(self.middle)
        mainhlayout.addStretch(1)
        mainhlayout.addLayout(gamblelayout)
        mainhlayout.addStretch(1)

        # Put everything in vertical layout
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addLayout(mainhlayout)
        self.instquitlayout.addStretch(1)
        self.instquitlayout.addWidget(self.quitbutton)

    def generatenext(self):
        """
        Generate the info for the next trial and put it on screen. if the final trial was just completed, then the next
        round is started or the completion text is put on screen
        """

        # stop the timer
        self.ititimer.stop()

        # reset the borders in case there was one
        self.righttop.setStyleSheet('border: 0px;')
        self.rightbottom.setStyleSheet('border: 0px;')
        self.left.setStyleSheet('border: 0px;')

        # if-then statement to determine whether the amount of trials completed is less than the number of trials the
        # user wants
        if self.trialsdone < self.person.get_trials():

            # get the trial text
            info = self.person.get_design_text()

            # set the sides to the trial text
            self.left.setText(info[0])
            self.righttop.setText(info[1])
            self.rightbottom.setText(info[2])

            # set middle to or
            self.middle.setText('OR')

            # get the time that the trial starts
            self.starttime = time.time() - self.overallstart

            # start the response timer
            self.timer.start(5000)

            # allow participant input
            self.responseenabled = 1

            # if fmri mode, then set the new trial timer now
            if self.person.fmri == 'Yes':
                self.ititimer.start(5500)

        # if the trials requested have been completed
        else:

            # blank out the sides
            self.left.setText('')
            self.righttop.setText('')
            self.rightbottom.setText('')

            # increase the number of rounds done and reset the number of trials done to 0
            self.roundsdone += 1
            self.trialsdone = 0

            # set the middle text to the appropriate text from the participant class
            self.middle.setText(self.person.nextround(self.roundsdone))

            # if all of the requested rounds have been completed
            if self.person.rounds == self.roundsdone:

                # output the trial data and thank the participant
                self.person.output()
                self.instructions.setText('Thank you!')

                # if the user wanted one of the participant's choices to get randomly chosen, then put that on screen
                if self.person.outcomeopt == 'Yes':
                    outcome = random.choice(self.person.outcomelist)
                    self.middle.setText('Your outcome: ' + outcome)

            # if not, indicate that you are now between rounds
            else:

                self.betweenrounds = 1

    def iti(self, state=0):
        """
        this function blanks out the screen and either warns the participant to be faster or has a fixation cross in the
        middle, depending on the value of state. It then sets the next design text
        :param state: default 0; only changes to 1 if it called from the timeout function and the experiment is in fmri
        mode. The value only serves to indicate this state
        """

        # blank out the sides
        self.left.setText('')
        self.righttop.setText('')
        self.rightbottom.setText('')

        # if state is 1, that means the participant timed out and the experiment is in fmri mode, so change iti to the
        # warning
        if state == 1:
            self.middle.setText('Please try to be quicker')

        # if the experiment is not in fmri mode or the participant did not time out, then leave this as a cross
        else:
            self.middle.setText('+')

        # if this function is called before the first trial is set up, then set up a timer for the first trial
        if self.trialsdone == 0:

            self.ititimer.start(1000)

        # update the design text
        self.person.set_design_text()

        # if you are not in fmri mode and you have at least completed one trial, then start the timer for the next round
        if (self.person.fmri == 'No') & (self.trialsdone > 0):
            self.ititimer.start(1000)

    def timeout(self):
        """
        if the timer runs out and the participant doesn't respond, then the timers stop, 9999 gets put in as the
        reaction time, and the trial is "completed" without a response
        """

        # stop the timer
        self.timer.stop()

        # set text
        self.left.setText('')
        self.righttop.setText('')
        self.rightbottom.setText('')

        # send the trial data to the participant class
        self.person.updateoutput(self.trialsdone, self.starttime, 9999)

        # if you're not in fmri mode, then start the reset timer
        if self.person.fmri == 'No':
            self.middle.setText('Please try to be quicker')
            self.trialresettimer.start(1000)

        # if you are in fmri mode, then disable participant input, increment the trial counter, and go to the iti screen
        else:

            self.trialsdone += 1
            self.responseenabled = 0
            self.iti(1)

    def responsereset(self):
        """
        if you're not in fmri mode, then this function resets the trial so that the participant can complete it
        """

        # stop the timer
        self.trialresettimer.stop()

        # set the trial text
        info = self.person.get_design_text()

        # set the text to the sides
        self.left.setText(info[0])
        self.righttop.setText(info[1])
        self.rightbottom.setText(info[2])

        # set the middle text
        self.middle.setText('OR')

        # start the response timer
        self.timer.start(5000)

    def keyaction(self, key):
        """
        Reads the keys that are pressed and does the corresponding actions
        :param key: the key that was pressed
        """

        # if someone presses the g key and the participant is between rounds...
        if (key in ['g', 'G']) & (self.betweenrounds == 1):

            # indicate that the participant is no longer between rounds so g and i keys won't mess things up
            self.betweenrounds = 0

            # if this is the first trial of the first round, set the global start time to make the onset time make more
            # sense
            if (self.trialsdone == 0) & (self.roundsdone == 0):
                self.overallstart = time.time()

            # set the window to the iti screen
            self.iti()

        # if the participant presses the left or right keys and is allowed to respond
        if ((key in self.person.rightkey) | (key in self.person.leftkey)) & (self.responseenabled == 1):

            # stop the timer and prevent users from sending more inputs
            self.timer.stop()
            self.responseenabled = 0

            # increment the trial counter
            self.trialsdone += 1

            # use time.time and the start time variable to compute rt
            endtime = time.time() - self.overallstart
            rt = endtime - self.starttime

            # if the key was the right key...
            if key in self.person.rightkey:

                # put a border around the middle to indicate a user input was received
                self.righttop.setStyleSheet('border: 3px solid blue;')
                self.rightbottom.setStyleSheet('border: 3px solid blue;')

                # set response to 1
                response = 1

            # if the key was the left key...
            else:

                # put a border around the middle to indicate a user input was received
                self.left.setStyleSheet('border: 3px solid blue;')

                # set response to 0
                response = 0

            # send the trial data to the participant class
            self.person.updateoutput(self.trialsdone, self.starttime, rt, response)

            self.iti()

        # if someone presses the i key and the participant is between rounds...
        if (key in ['i', 'I']) & (self.betweenrounds == 1):

            # increase the index for the instructions
            self.inst += 1

            # get the associated text
            self.middle.setText(self.person.get_instructions(self.inst))

            # if the index reaches five...
            if self.inst == 5:

                # reset to zero so the instructions can be viewed again
                self.inst = 0
