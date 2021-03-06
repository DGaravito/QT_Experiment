from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QSpinBox, QLineEdit, QVBoxLayout, QDialog, \
    QCheckBox, QFormLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from os import path


class WDErrorBox(QDialog):
    """
    This is a popup window that may come up after the settingsguis window checks to see if the directory that the user
    put in is actually a directory. If not, this popup lets the user know that they goofed.
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Error')

        # Make  layout
        dialayout = QVBoxLayout()

        # Make labels for text
        self.mainerror = QLabel('It looks like you entered an invalid directory!')
        self.mainerror.setStyleSheet('padding :5px')

        text = 'If you\'re on Windows, make sure to include your drive name (i.e., C:).\n' \
               'Mac example: ~/Users/DGaravito/Desktop\n' \
               'Windows example: C:/users/dgara/Desktop'

        self.instruction = QLabel(text)
        self.instruction.setStyleSheet('padding :5px')

        # Add stuff to overarching layout
        dialayout.addWidget(self.mainerror),
        dialayout.addWidget(self.instruction)

        self.setLayout(dialayout)


class FileErrorBox(QDialog):
    """
    This is a popup window that may come up after the settingsguis window checks to see if the file that the user
    will create alreaedy exists. If so, this popup lets the user know that they goofed and tells them to delete the
    old file or change their settings
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Error')

        # Make  layout
        dialayout = QVBoxLayout()

        # Make labels for text
        self.mainerror = QLabel('It looks like your file already exists!')
        self.mainerror.setStyleSheet('padding :5px')

        self.instruction = QLabel('Either delete the old file, pick a new directory, or change your ID, session name' +
                                  ', or task.')
        self.instruction.setStyleSheet('padding :5px')

        # Add stuff to overarching layout
        dialayout.addWidget(self.mainerror),
        dialayout.addWidget(self.instruction)

        self.setLayout(dialayout)


class MathErrorBox(QDialog):
    """
    This is a popup window that may come up after the settingsguis window checks to see if the math works out.
    Condition is determined by the settingsguis GUI that has the error and the settingsguis within that. For example,
    PBT needs to be divisible by 4 because there are four pictures. Framing needs to be divisible by 2 if gains and
    losses are enabled, divisible by 3 if FTT is enabled, and divisible by 6 if both are enabled.
    """

    def __init__(self, state):
        super().__init__()

        self.setWindowTitle('Input Error')

        # Make  layout
        dialayout = QVBoxLayout()

        # Make labels for text

        self.mainerror = QLabel('Your number of trials isn\'t compatible with the settings and/or task you chose!')
        self.mainerror.setStyleSheet('padding :5px')

        match state:

            case 1:

                followupstring = 'There are 4 pictures for stimuli, so the total number of trials must be ' \
                                 'divisible by 4.'

            case 2:

                followupstring = 'You enabled gains and losses, so your number of trials should be divisible by 2.'

            case 3:

                followupstring = 'You enabled FTT, so your number of trials should be divisible by 3.'

            case 4:

                followupstring = 'You enabled FTT and need gains and losses, so your number of trials should' \
                                 ' be divisible by 6 (minimum Gist, Mixed, and Verbatim version of 1 gain and' \
                                 ' 1 loss question.'

            case 5:

                followupstring = 'There are 4 task difficulty levels, so the total number of trials must be ' \
                                 'divisible by 3 (enough for 1 to be compared to 2, 3, and 4) in the original task.'

            case 6:

                followupstring = 'There are 4 task difficulty levels, so the total number of trials must be ' \
                                 'divisible by 6 (enough for each difficulty to be compared) in the alternate task.'

            case 7:

                followupstring = 'It seems that the number of high value and low trials you entered means that ' \
                                 'the participants could end up with less money than the minimum allowed.' \
                                 '\n(# of low value trials X $0.15) + (# of low value trials X $0.03) <= ' \
                                 'starting money - minimum money that a participants can leave with.'

            case 8:

                followupstring = 'To easily balance the number of neutral vs. emotional faces, please make sure your' \
                                 ' number of trials is divisible by 4.'

            case _:

                followupstring = 'I don\'t know what you put, but the math doesn\'t work out'

        self.followup = QLabel(followupstring)
        self.followup.setStyleSheet('padding :5px')

        # Add stuff to overarching layout
        dialayout.addWidget(self.mainerror),
        dialayout.addWidget(self.followup)

        self.setLayout(dialayout)


class Settings(QWidget):
    """
    Main class for the settingsguis window. This guy has all of the characteristics and things that every settingsguis
    window should have: A quit button, a submit settingsguis button, a minimum window size, a function for checking
    that the user inputted a valid directory, etc.
    """

    def __init__(self, task):
        super().__init__()

        # Window title
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # setting the geometry of window
        self.setGeometry(0, 0, 700, 400)

        # center window
        self.centerscreen()

        # Defaults for various tasks and options
        self.task = task
        self.buttonboxstate = 'No'
        self.outcome = 'No'
        self.eyetracking = 'No'
        self.fmri = 'No'
        self.ftt = 'No'
        self.stt = 'No'
        self.happy = 'No'
        self.fear = 'No'
        self.angry = 'No'
        self.sad = 'No'

        # Default directory
        self.wd = QLineEdit('C:/users/dgara/Desktop')

        # Make overarching layout
        self.over_layout = QVBoxLayout()

        # Make a label with instructions
        self.header = QLabel('Enter the appropriate values:', self)
        self.header.setFont(QFont('Helvetica', 30))
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add header to overarching layout
        self.over_layout.addWidget(self.header)

        # Make form layout for all the settingsguis
        self.layout = QFormLayout()

        # ID
        self.idform = QLineEdit()
        self.idform.setText('9999')
        self.layout.addRow(QLabel('Subject ID:'), self.idform)

        # Session form
        self.sessionin = QLineEdit()
        self.sessionin.setText('Pretest')
        self.layout.addRow(QLabel('Session name/number (enter \"Practice\" to not have output):'), self.sessionin)

        # Trials input
        self.trialsin = QSpinBox()
        self.trialsin.setValue(5)
        self.trialsin.setRange(1, 1000)

        # Blocks input
        self.blocksin = QSpinBox()
        self.blocksin.setValue(1)
        self.blocksin.setMinimum(1)

        # Starting money input
        self.smoneyin = QSpinBox()
        self.smoneyin.setValue(25)
        self.smoneyin.setRange(0, 10000)

        # Button checkbox
        self.buttontoggle = QCheckBox()
        self.buttontoggle.stateChanged.connect(self.clickbox)

        # Eyetracking checkbox
        self.eyetrackingtoggle = QCheckBox()
        self.eyetrackingtoggle.stateChanged.connect(self.clickbox)

        # fMRI checkbox
        self.fmritoggle = QCheckBox()
        self.fmritoggle.stateChanged.connect(self.clickbox)

        # FTT checkbox for framing task
        self.ftttoggle = QCheckBox()
        self.ftttoggle.stateChanged.connect(self.clickbox)

        # ST Trials checkbox for paired recall task
        self.stttoggle = QCheckBox()
        self.stttoggle.stateChanged.connect(self.clickbox)

        # checkbox for getting a random outcome
        self.outcometoggle = QCheckBox()
        self.outcometoggle.stateChanged.connect(self.clickbox)

        # Submit button
        self.submit = QPushButton('Submit')
        self.submit.clicked.connect(self.checksettings)

        # Quit button
        self.quitbutton = QPushButton('Quit')
        self.quitbutton.clicked.connect(QApplication.instance().quit)
        self.quitbutton.resize(self.quitbutton.sizeHint())

        # Checkboxes for Emo Go/No-Go TODO Figure out a way to put these just in the task
        # Happy checkbox
        self.happytoggle = QCheckBox('Happy?')
        self.happytoggle.stateChanged.connect(self.clickbox)

        # Sad checkbox
        self.sadtoggle = QCheckBox('Sad?')
        self.sadtoggle.stateChanged.connect(self.clickbox)

        # Anger checkbox
        self.angertoggle = QCheckBox('Angry?')
        self.angertoggle.stateChanged.connect(self.clickbox)

        # Fear checkbox
        self.feartoggle = QCheckBox('Fearful?')
        self.feartoggle.stateChanged.connect(self.clickbox)

        # Show all elements
        self.show()

    def centerscreen(self):
        """
        Finds the geometry of the computer's screen and moves the window to the center of it
        """

        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def clickbox(self):
        """
        This is a function that will activate whenever you click on one of the checkboxes. When one box is clicked, the
        function will check the status of every box and edit the respective class variable based on the state of the
        box.
        """

        if self.buttontoggle.isChecked():
            self.buttonboxstate = 'Yes'
        else:
            self.buttonboxstate = 'No'

        if self.outcometoggle.isChecked():
            self.outcome = 'Yes'
        else:
            self.outcome = 'No'

        if self.eyetrackingtoggle.isChecked():
            self.eyetracking = 'Yes'
        else:
            self.eyetracking = 'No'

        if self.fmritoggle.isChecked():
            self.fmri = 'Yes'
        else:
            self.fmri = 'No'

        if self.ftttoggle.isChecked():
            self.ftt = 'Yes'
        else:
            self.ftt = 'No'

        if self.happytoggle.isChecked():
            self.happy = 'Yes'
        else:
            self.happy = 'No'

        if self.sadtoggle.isChecked():
            self.sad = 'Yes'
        else:
            self.sad = 'No'

        if self.angertoggle.isChecked():
            self.angry = 'Yes'
        else:
            self.angry = 'No'

        if self.feartoggle.isChecked():
            self.fear = 'Yes'
        else:
            self.fear = 'No'

    def checksettings(self):
        """
        Once you hit submit, the following function is called, which figures out if the selected directory is valid. If
        not, it calls the directory error function. If the directory is valid, it then checks if a file exists in that
        location that would be overwritten. If there is, it calls the file error function. If there is not pre-existing
        file, then it calls the function that submits the settings.
        """

        if path.isdir(self.wd.text()):

            if path.isfile(self.wd.text() + '/' + self.idform.text() + '_' + self.task + '_' + self.sessionin.text() +
                           '.xlsx'):
                self.fileerrordialog()

            else:
                self.submitsettings()

        else:
            self.wderrordialog()

    def wderrordialog(self):
        """
        This function activates if there is the output directory submitted is not valid
        """

        error = WDErrorBox()

        error.exec()

    def fileerrordialog(self):
        """
        This function activates if the output directory is valid but a file exists there that would be overwritten if
        the program were to run with the selected task.
        """

        error = FileErrorBox()

        error.exec()

    def matherrordialog(self, state):
        """
        This function activates if there is a problem with the settings such that the math doesn't work out. It takes
        one argument which determines the text of the resulting error dialog window.
        :param state: an integer that indicates what type of math error happened and what the resulting text in the
        error should be.
        """

        error = MathErrorBox(state)

        error.exec()

    def submitsettings(self):
        """
        This function activates if you hit submit on a settings window and both the directory is valid and a file
        doesn't already exist. Since the resulting actions will depend on the selected task, this is left blank here.
        """

        print('If you see this, panic')
