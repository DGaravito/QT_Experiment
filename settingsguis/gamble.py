from PyQt6.QtWidgets import QLabel, QSpinBox, QFormLayout, QVBoxLayout, QCheckBox, QComboBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from adopy.tasks.cra import TaskCRA

from settingsguis import settings
from participants import gamblep
from expguis import gamblegui


class ARTTSettings(settings.Settings):

    def __init__(self):
        super().__init__()

        # setting  the geometry of window
        self.setGeometry(0, 0, 650, 350)

        # center window
        self.centerscreen()

        # Add in elements
        self.elements()

        # Show all elements
        self.show()

    def elements(self):
        # Make overarching layout
        over_layout = QVBoxLayout()

        # Make a label with instructions
        self.header = QLabel('Enter the appropriate values:', self)

        # setting font style and size
        self.header.setFont(QFont('Helvetica', 30))

        # center header
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add header to overarching layout

        over_layout.addWidget(self.header)

        # Trials input
        self.trialsin = QSpinBox()
        self.trialsin.setSpecialValueText('10')

        # probability input
        # self.probriskin = QLineEdit()
        # self.probriskin.setText('.13, .25, .38, .5, .75')
        self.probabilities = [.13, .25, .38, .5, .62, .75, .87]

        # proportion input
        # self.probambin = QLineEdit()
        # self.probambin.setText('.25, .5, .75')
        self.proportions = [.25, .5, .75]

        # Smallest reward input
        self.srewin = QSpinBox()
        self.srewin.setSpecialValueText('5')

        # Largest reward input
        self.lrewin = QSpinBox()
        self.lrewin.setSpecialValueText('50')

        # Dropdown box for gains, losses, or both
        self.design = QComboBox()
        self.design.addItems(['Gains only', 'Losses only', 'Gains and Losses'])

        # Make form layout for all the settingsguis
        layout = QFormLayout()

        layout.addRow(QLabel('Subject ID:'), self.idform)
        layout.addRow(QLabel('Number of trials:'), self.trialsin)
        # layout.addRow(QLabel('Enter the probablities for risky trials:'), self.probriskin)
        # layout.addRow(QLabel('Enter the proportions covered for ambiguous trials:'), self.probambin)
        layout.addRow(QLabel('Fixed reward/loss magnitude:'), self.srewin)
        layout.addRow(QLabel('Largest reward/loss possible:'), self.lrewin)
        layout.addRow(QLabel('What type of questions do you want?:'), self.design)
        layout.addRow(QLabel('Where do you want to save the output?'), self.wdset)
        layout.addRow(self.submit, self.quitbutton)

        # Add form layout to overarching layout
        over_layout.addLayout(layout)

        self.setLayout(over_layout)

    def submitsettings(self):

        # riskstring = self.probriskin.text()
        # risklist = list(riskstring.split(", "))

        # ambstring = self.probambin.text()
        # amblist = list(ambstring.split(", "))


        person = gamblep.ARTTParticipant(self.idform.text(),
                                         self.trialsin.text(),
                                         self.wdset.text(),
                                         TaskCRA(),
                                         self.probabilities,
                                         self.proportions,
                                         self.srewin.text(),
                                         self.lrewin.text(),
                                         self.design.currentText())

        self.exp = gamblegui.ARTTExp(person)
        self.exp.show()
        self.hide()


class RASettings(settings.Settings):

    def __init__(self):
        super().__init__()

        # setting  the geometry of window
        self.setGeometry(0, 0, 650, 350)

        # center window
        self.centerscreen()

        # STT default
        self.stt = 0

        # Add in elements
        self.elements()

        # Show all elements
        self.show()

    def elements(self):
        # Make overarching layout
        over_layout = QVBoxLayout()

        # Make a label with instructions
        self.header = QLabel('Enter the appropriate values:', self)

        # setting font style and size
        self.header.setFont(QFont('Helvetica', 30))

        # center header
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add header to overarching layout

        over_layout.addWidget(self.header)

        # Trials input
        self.trialsin = QSpinBox()
        self.trialsin.setSpecialValueText('30')

        # Minimum input
        self.minin = QSpinBox()
        self.minin.setSpecialValueText('1')

        # Maximum input
        self.maxin = QSpinBox()
        self.maxin.setSpecialValueText('30')

        # Make form layout for all the settingsguis
        layout = QFormLayout()

        layout.addRow(QLabel('Subject ID:'), self.idform)
        layout.addRow(QLabel('Number of trials:'), self.trialsin)
        layout.addRow(QLabel('Smallest possible gain:'), self.minin)
        layout.addRow(QLabel('Largest possible gain:'), self.maxin)
        layout.addRow(QLabel('Where do you want to save the output?'), self.wdset)
        layout.addRow(self.submit, self.quitbutton)

        # Add form layout to overarching layout
        over_layout.addLayout(layout)

        self.setLayout(over_layout)

    def submitsettings(self):

        person = gamblep.RAParticipant(self.idform.text(),
                                       self.trialsin.text(),
                                       self.wdset.text(),
                                       'Risk Aversion',
                                       self.minin.text(),
                                       self.maxin.text())

        self.exp = gamblegui.RAExp(person)
        self.exp.show()
        self.hide()


class FrameSettings(settings.Settings):

    def __init__(self):
        super().__init__()

        # setting  the geometry of window
        self.setGeometry(0, 0, 650, 350)

        # center window
        self.centerscreen()

        # STT default
        self.ftt = 0

        # Add in elements
        self.elements()

        # Show all elements
        self.show()

    def elements(self):
        # Make overarching layout
        over_layout = QVBoxLayout()

        # Make a label with instructions
        self.header = QLabel('Enter the appropriate values:', self)

        # setting font style and size
        self.header.setFont(QFont('Helvetica', 30))

        # center header
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add header to overarching layout

        over_layout.addWidget(self.header)

        # Trials input
        self.trialsin = QSpinBox()
        self.trialsin.setSpecialValueText('30')

        # min EV input
        self.minin = QSpinBox()
        self.minin.setSpecialValueText('1')

        # max EV input
        self.maxin = QSpinBox()
        self.maxin.setSpecialValueText('50')

        # Dropdown box for gains, losses, or both
        self.design = QComboBox()
        self.design.addItems(['Gains only', 'Losses only', 'Gains and Losses'])

        # FTT  input
        self.ftttoggle = QCheckBox('', self)
        self.ftttoggle.stateChanged.connect(self.clickBox)

        # Make form layout for all the settingsguis
        layout = QFormLayout()

        layout.addRow(QLabel('Subject ID:'), self.idform)
        layout.addRow(QLabel('Number of trials:'), self.trialsin)
        layout.addRow(QLabel('Minimum expected value:'), self.minin)
        layout.addRow(QLabel('Maximum expected value:'), self.maxin)
        layout.addRow(QLabel('What type of questions do you want?:'), self.design)
        layout.addRow(QLabel('Do you want FTT truncations (i.e., Gist, Mixed, Verbatim)?:'), self.ftttoggle)
        layout.addRow(QLabel('Where do you want to save the output?'), self.wdset)
        layout.addRow(self.submit, self.quitbutton)

        # Add form layout to overarching layout
        over_layout.addLayout(layout)

        self.setLayout(over_layout)

    def clickBox(self):

        if self.ftttoggle.isChecked():
            self.ftt = 'Yes'
        else:
            self.ftt = 'No'

    def submitsettings(self):

        if (
                (self.design.currentText() == 'Gains and Losses') &
                (self.ftt == 'Yes') &
                int(self.trialsin.text()) % 6 != 0
        ):

            self.matherrordialog(4)

        elif (self.ftt == 'Yes') & (int(self.trialsin.text()) % 3 != 0):

            self.matherrordialog(3)

        elif (self.design.currentText() == 'Gains and Losses') & (int(self.trialsin.text()) % 2 != 0):

            self.matherrordialog(2)

        else:

            person = gamblep.FrameParticipant(self.idform.text(),
                                              self.trialsin.text(),
                                              self.wdset.text(),
                                              'Framing',
                                              self.minin.text(),
                                              self.maxin.text(),
                                              self.design.currentText(),
                                              self.ftt)

            self.exp = gamblegui.FrameExp(person)
            self.exp.show()
            self.hide()

    def matherrordialog(self, state):

        error = settings.MathErrorBox(state)

        error.exec()