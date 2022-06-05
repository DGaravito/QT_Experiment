from PyQt6.QtWidgets import QLabel, QSpinBox, QFormLayout, QVBoxLayout, QCheckBox, QComboBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from settingsguis import settings

from participants import memoryp
from expguis import memorygui


class PrSettings(settings.Settings):

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

        # Pairs input
        self.pairsin = QSpinBox()
        self.pairsin.setSpecialValueText('30')

        # ST Trials input
        self.trialsin = QSpinBox()
        self.trialsin.setSpecialValueText('3')

        # ST Trials input
        self.stttoggle = QCheckBox('STT?', self)
        self.stttoggle.stateChanged.connect(self.clickBox)

        # Make form layout for all the settingsguis
        layout = QFormLayout()

        layout.addRow(QLabel('Subject ID:'), self.idform)
        layout.addRow(QLabel('Number of word pairs (Max: 30):'), self.pairsin)
        layout.addRow(QLabel('Number of study-test trials:'), self.trialsin)
        layout.addRow(QLabel('Do you want an STT trial?:'), self.stttoggle)
        layout.addRow(QLabel('Where do you want to save the output?'), self.wdset)
        layout.addRow(self.submit, self.quitbutton)

        # Add form layout to overarching layout
        over_layout.addLayout(layout)

        self.setLayout(over_layout)

    def clickBox(self):

        if self.stttoggle.isChecked():
            self.stt = 1
        else:
            self.stt = 0

    def submitsettings(self):

        person = memoryp.PrParticipant(self.idform.text(),
                                       self.pairsin.text(),
                                       self.wdset.text(),
                                       'Pair Recall Memory',
                                       self.trialsin.text(),
                                       self.stt)

        self.exp = memorygui.PrExp(person)
        self.exp.show()
        self.hide()


class NBackSettings(settings.Settings):

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

        # Rounds input
        self.roundsin = QSpinBox()
        self.roundsin.setSpecialValueText('1')

        # Dropdown box for gains, losses, or both
        self.design = QComboBox()
        self.design.addItems(['1-back', '2-back', '3-back', '4-back'])

        # Make form layout for all the settingsguis
        layout = QFormLayout()

        layout.addRow(QLabel('Subject ID:'), self.idform)
        layout.addRow(QLabel('Number of trials:'), self.trialsin)
        layout.addRow(QLabel('Number of rounds (do you want more than 1 round of X number of trials?):'), self.roundsin)
        layout.addRow(QLabel('What type of n-Back?:'), self.design)
        layout.addRow(QLabel('Where do you want to save the output?'), self.wdset)
        layout.addRow(self.submit, self.quitbutton)

        # Add form layout to overarching layout
        over_layout.addLayout(layout)

        self.setLayout(over_layout)

    def submitsettings(self):

        person = memoryp.NbParticipant(self.idform.text(),
                                       self.trialsin.text(),
                                       self.wdset.text(),
                                       self.design.currentText(),
                                       self.roundsin.text())

        self.exp = memorygui.NbExp(person)
        self.exp.show()
        self.hide()