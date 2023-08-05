# -*- coding: utf-8 -*-
"""
Widget collecting subwidgets for the target filter specifications (currently
only amplitude and frequency specs.)

Author: Christian Muenker
"""
from __future__ import print_function, division, unicode_literals, absolute_import
import sys
import logging
logger = logging.getLogger(__name__)

from ..compat import (QtCore, QtGui,
                      QWidget, QLabel, QLineEdit, QComboBox, QFrame, QFont, QCheckBox,
                      QTableWidget, QTableWidgetItem, QTextBrowser, QTextCursor,
                      QVBoxLayout, QHBoxLayout, QGridLayout, QSizePolicy,
                      pyqtSignal, Qt, QEvent)


import pyfda.filterbroker as fb
from pyfda.input_widgets import amplitude_specs, freq_specs


class TargetSpecs(QWidget):
    """
    Build and update widget for entering the target specifications (frequencies
    and amplitudes) like F_sb, F_pb, A_SB, etc.
    """

    # class variables (shared between instances if more than one exists)
    sigSpecsChanged = pyqtSignal() # emitted when filter has been changed


    def __init__(self, parent, title = "Target Specs"):
        super(TargetSpecs, self).__init__(parent)

        self.title = title
        
        self._construct_UI()

#------------------------------------------------------------------------------
    def _construct_UI(self):
        """
        Construct user interface
        """

        # subwidget for Frequency Specs
        self.f_specs = freq_specs.FreqSpecs(self, title = "Frequency")
        # subwidget for Amplitude Specs
        self.a_specs = amplitude_specs.AmplitudeSpecs(self, title = "Amplitude")

        self.a_specs.setVisible(True)
        """
        LAYOUT
        """
        bfont = QFont()
        bfont.setBold(True)
#            bfont.setWeight(75)
        lblTitle = QLabel(self) # field for widget title
        lblTitle.setText(self.title)
        lblTitle.setFont(bfont)
        
        layVFreq = QVBoxLayout()  # add stretch at bottom of ampSpecs
        layVFreq.addWidget(self.f_specs) # to compensate for different number of 
        layVFreq.addStretch()           # arguments
        
        layVAmp = QVBoxLayout()  # add stretch at bottom of freqSpecs
        layVAmp.addWidget(self.a_specs) # to compensate for different number of 
        layVAmp.addStretch()           # arguments
        
        layGMain = QGridLayout()
        layGMain.addWidget(lblTitle,0,0,1,2)# title
        layGMain.addLayout(layVFreq,1,0)  # frequency specifications
        layGMain.addLayout(layVAmp,1,1)  # amplitude specifications

        layGMain.setContentsMargins(1,1,1,1)

        self.setLayout(layGMain)

        #----------------------------------------------------------------------
        #  SIGNALS & SLOTS
        self.a_specs.sigSpecsChanged.connect(self.sigSpecsChanged.emit)
        self.f_specs.sigSpecsChanged.connect(self.sigSpecsChanged.emit)
        
        self.update_UI() # first time initialization
        

#------------------------------------------------------------------------------
    def update_UI(self, freq_params = [], amp_params = []):
        """
        Called when a new filter design algorithm has been selected
        Pass frequency and amplitude labels to the amplitude and frequency
        spec widgets
        The sigSpecsChanged signal is emitted already by select_filter.py
        """

        # pass new labels to widgets
        # set widgets invisible if param list is empty
        self.f_specs.update_UI(new_labels = freq_params) # update frequency spec labels
        self.a_specs.setVisible(amp_params != [])
        self.a_specs.update_UI(new_labels = amp_params)

#        self.sigSpecsChanged.emit() # ->pyFDA -> pltWidgets.updateAll()

#------------------------------------------------------------------------------
    def load_entries(self):
        """
        Update entries from global dict fb.fil[0]
        parameters, using the "load_entries" methods of the classes
        """
        self.a_specs.load_entries() # magnitude specs with unit
        self.f_specs.load_entries() # weight specification

#------------------------------------------------------------------------------

if __name__ == '__main__':

    from ..compat import QApplication
    app = QApplication(sys.argv)

    # Read freq / amp / weight labels for current filter design
    rt = fb.fil[0]['rt']
    ft = fb.fil[0]['ft']
    fc = fb.fil[0]['fc']

    if 'min' in fb.fil_tree[rt][ft][fc]:
        my_params = fb.fil_tree[rt][ft][fc]['min']['par']
    else:
        my_params = {}

    # build separate parameter lists according to the first letter
    freq_params = [l for l in my_params if l[0] == 'F']
    amp_params = [l for l in my_params if l[0] == 'A']

    mainw = TargetSpecs(None, title = "Test Specs")
    mainw.update_UI(freq_params, amp_params)
    
    app.setActiveWindow(mainw) 
    mainw.show()
    sys.exit(app.exec_())