# -*- coding: utf-8 -*-
"""
Widget stacking all subwidgets for filter specification and design

Author: Christian Muenker
"""
from __future__ import print_function, division, unicode_literals, absolute_import
import sys
from pprint import pformat
import logging
logger = logging.getLogger(__name__)

import numpy as np

from ..compat import (QWidget, QLabel, QFrame, QPushButton,
                      QVBoxLayout, QGridLayout, QSizePolicy,
                      pyqtSignal)
                      
import pyfda.filterbroker as fb
import pyfda.filter_factory as ff
#from pyfda.pyfda_lib import HLine

from pyfda.input_widgets import (select_filter, amplitude_specs,
                                 freq_specs, freq_units,
                                 weight_specs, target_specs)


class FilterSpecs(QWidget):
    """
    Build widget for entering all filter specs
    """
    # class variables (shared between instances if more than one exists)
    sigFilterDesigned = pyqtSignal()  # emitted when filter has been designed
    sigSpecsChanged = pyqtSignal() # emitted when specs have been changed
    sigViewChanged = pyqtSignal() # emitted when view has changed
    sigQuit = pyqtSignal() # emitted when >QUIT< button is clicked

    def __init__(self, parent):
        super(FilterSpecs, self).__init__(parent)

        self._construct_UI()

    def _construct_UI(self):
        """
        Construct User Interface from all input subwidgets
        """
        # Subwidget for selecting filter with response type rt (LP, ...), 
        #    filter type ft (IIR, ...) and filter class fc (cheby1, ...)
        self.sel_fil = select_filter.SelectFilter(self)
        self.sel_fil.setObjectName("select_filter")
        # Subwidget for selecting the frequency unit and range
        self.f_units = freq_units.FreqUnits(self)
        self.f_units.setObjectName("freq_units")
        # Subwidget for Frequency Specs
        self.f_specs = freq_specs.FreqSpecs(self)
        self.f_specs.setObjectName("freq_specs")
        # Subwidget for Amplitude Specs
        self.a_specs = amplitude_specs.AmplitudeSpecs(self)
        self.a_specs.setObjectName("amplitude_specs")
        # Subwidget for Weight Specs
        self.w_specs = weight_specs.WeightSpecs(self)
        self.w_specs.setObjectName("weight_specs")
        # Subwidget for target specs (frequency and amplitude)
        self.t_specs = target_specs.TargetSpecs(self, title="Target Specifications")
        self.t_specs.setObjectName("target_specs")
        # Subwidget for displaying infos on the design method
        self.lblMsg = QLabel(self)
        self.lblMsg.setWordWrap(True)
#        self.lblMsg.setFrameShape(QFrame.StyledPanel|QFrame.Sunken)

        layVMsg = QVBoxLayout()
        layVMsg.addWidget(self.lblMsg)

        frmMsg = QFrame()
        frmMsg.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
        frmMsg.setLayout(layVMsg)
        frmMsg.setSizePolicy(QSizePolicy.Minimum,
                             QSizePolicy.Minimum)

        self.butDesignFilt = QPushButton("DESIGN FILTER", self)
        self.butQuit = QPushButton("Quit", self)

        #----------------------------------------------------------------------
        # LAYOUT for input specifications and buttons
        #----------------------------------------------------------------------
        layGMain = QGridLayout()
        layGMain.addWidget(self.sel_fil, 0, 0, 1, 2)  # Design method (IIR - ellip, ...)
        layGMain.addWidget(self.f_units, 1, 0, 1, 2)  # Frequency units
        layGMain.addWidget(self.f_specs, 2, 0, 1, 2)  # Freq. specifications
        layGMain.addWidget(self.a_specs, 3, 0, 1, 2)  # Amplitude specs
        layGMain.addWidget(self.w_specs, 4, 0, 1, 2)  # Weight specs
        layGMain.addWidget(frmMsg, 5, 0, 1, 2)        # Text message
        layGMain.addWidget(self.t_specs, 6, 0, 1, 2)  # Target specs
        layGMain.setRowStretch(7,1)
#        layGMain.addWidget(HLine(QFrame, self), 7,0,1,2) # create HLine

        layGMain.addWidget(self.butDesignFilt, 8, 0)  # <Design Filter> button
        layGMain.addWidget(self.butQuit, 8, 1)        # <Quit> button
        layGMain.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layGMain) # main layout of widget

        #----------------------------------------------------------------------
        # SIGNALS & SLOTS
        #
        # Changing the filter design requires updating UI because number or 
        # kind of input fields changes -> Call update_all_UIs, emitting 
        # sigFilterChanged when it's finished
        self.sel_fil.sigFiltChanged.connect(self.update_UI)

        # Changing the frequency unit requires re-display of frequency specs
        # but it does not influence the actual specs (no specsChanged )
        self.f_units.sigUnitChanged.connect(self.f_specs.load_entries)
        self.f_units.sigUnitChanged.connect(self.t_specs.load_entries)
        self.f_units.sigUnitChanged.connect(self.sigViewChanged)
        # Activating the "Sort" button triggers sigSpecsChanged, requiring 
        # sorting and storing the frequency entries
        self.f_units.sigSpecsChanged.connect(self.f_specs.sort_dict_freqs)
        self.f_units.sigSpecsChanged.connect(self.t_specs.f_specs.sort_dict_freqs)


        # Changing filter parameters / specs requires reloading of parameters
        # in other hierarchy levels, e.g. in the plot tabs
        # bundle sigSpecsChanged signals and propagate to next hierarchy level
#        self.f_units.sigSpecsChanged.connect(self.sigSpecsChanged)
        self.f_specs.sigSpecsChanged.connect(self.sigSpecsChanged)
        self.t_specs.sigSpecsChanged.connect(self.sigSpecsChanged)
        self.a_specs.sigSpecsChanged.connect(self.sigSpecsChanged)
        self.a_specs.sigUnitChanged.connect(self.sigViewChanged)
        self.w_specs.sigSpecsChanged.connect(self.sigSpecsChanged)

        # Other signal-slot connections
        self.butDesignFilt.clicked.connect(self.start_design_filt)
        self.butQuit.clicked.connect(self.sigQuit) # pass on to main application
        #----------------------------------------------------------------------

        self.update_UI() # first time initialization
        self.start_design_filt() # design first filter using default values

#------------------------------------------------------------------------------
    def update_UI(self):
        """
        update_all_UIs is called every time the filter design method or order
        (min / man) has been changed. This usually requires a different set of
        frequency and amplitude specs.
        
        At this time, the actual filter object instance has been created from 
        the name of the design method (e.g. 'cheby1') in select_filter.py. 
        Its handle has been stored in fb.fil_inst.

        fb.fil[0] (currently selected filter) is read, then general information
        for the selected filter type and order (min/man) is gathered from
        the filter tree [fb.fil_tree], i.e. which parameters are needed, which
        widgets are visible and which message shall be displayed.

        Then, the UIs of all subwidgets are updated using their "updateUI" method,
        finally the signal 'sigSpecsChanged' is emitted.
        """

        rt = fb.fil[0]['rt'] # e.g. 'LP'
        ft = fb.fil[0]['ft'] # e.g. 'FIR'
        fc = fb.fil[0]['fc'] # e.g. 'equiripple'
        fo = fb.fil[0]['fo'] # e.g. 'man'
        # read all parameters for selected filter type, e.g. 'F_SB':
        all_params = fb.fil_tree[rt][ft][fc][fo]['par']

        vis_wdgs = fb.fil_tree[rt][ft][fc][fo]['vis'] # visible widgets
        dis_wdgs = fb.fil_tree[rt][ft][fc][fo]['dis'] # disabled widgets
        msg      = fb.fil_tree[rt][ft][fc][fo]['msg'] # message

        # Read freq / amp / weight labels for current filter design, building
        # separate parameter lists according to the first letter
        f_params = [l for l in all_params if l[0] == 'F'] # curr. not used
        a_params = [l for l in all_params if l[0] == 'A']
        w_params = [l for l in all_params if l[0] == 'W']
        logger.debug("update_all_UIs\n"
            "all_params = %s\n"
            "a_params = %s\n"
            "f_params = %s\n"
            "w_params = %s\n",
            all_params, a_params, f_params, w_params)

        self.sel_fil.load_filter_order() # update filter order from dict

        # build separate parameter lists for min. and man. filter order 
        # and target specs   
        min_params = man_params = targ_params = []
        
        if "min" in fb.fil_tree[rt][ft][fc]:
            min_params = fb.fil_tree[rt][ft][fc]['min']['par']
            
        if "man" in fb.fil_tree[rt][ft][fc]:
            man_params = fb.fil_tree[rt][ft][fc]['man']['par']

        if "targ" in fb.fil_tree[rt][ft][fc]:
            targ_params = fb.fil_tree[rt][ft][fc]['targ']['par']


        # always use parameters for MANUAL filter order for f_specs widget,
        # frequency specs for minimum order are displayed in target specs
        f_man_params = [l for l in man_params if l[0] == 'F']
        self.f_specs.setVisible("fspecs" in vis_wdgs)
        self.f_specs.setEnabled("fspecs" not in dis_wdgs)
        self.f_specs.update_UI(new_labels=f_man_params)

        # always use parameters for MINIMUM filter order for target frequency
        # spec widget
        f_min_params = [l for l in min_params if l[0] == 'F']
        f_targ_params = [l for l in targ_params if l[0] == 'F']

        self.t_specs.setVisible("tspecs" in vis_wdgs)
        self.t_specs.setEnabled("tspecs" not in dis_wdgs)
        self.t_specs.update_UI(f_min_params, a_params)
        
        # self.a_specs.setVisible(a_params != [])
        self.a_specs.setVisible("aspecs" in vis_wdgs)
        self.a_specs.setEnabled("aspecs" not in dis_wdgs)
        self.a_specs.update_UI(new_labels=a_params)

        self.w_specs.setVisible("wspecs" in vis_wdgs)
        self.w_specs.setEnabled("wspecs" not in dis_wdgs)
        self.w_specs.update_UI(new_labels=w_params)

        self.lblMsg.setText(msg)

        self.sigSpecsChanged.emit()

#------------------------------------------------------------------------------
    def load_entries(self):
        """
        Reload all specs/parameters entries from global dict fb.fil[0],
        using the "load_entries" methods of the individual classes
        """
        self.sel_fil.load_entries() # select filter widget
        self.f_units.load_entries() # frequency units widget
        self.f_specs.load_entries() # frequency specification widget
        self.a_specs.load_entries() # magnitude specs with unit
        self.w_specs.load_entries() # weight specification
        self.t_specs.load_entries() # target specs

#------------------------------------------------------------------------------
    def start_design_filt(self):
        """
        Start the actual filter design process:
        - store the entries of all input widgets in the global filter dict.
        - call the design method, passing the whole dictionary as the
          argument: let the design method pick the needed specs
        - update the input widgets in case weights, corner frequencies etc.
          have been changed by the filter design method
        - the plots are updated via signal-slot connection
        """
        logger.debug("start_design_filt - Specs:\n"
            "fb.fil[0]: %s\n"
            "fb.fil[0]['fc'] %s.%s%s", 
            pformat(fb.fil[0]), str(fb.fil[0]['fc']), str(fb.fil[0]['rt']), 
                         str(fb.fil[0]['fo']))

        logger.info("startDesignFilt using: %s\nmethod: %s\n",
            str(type(ff.fil_inst)), str(fb.fil[0]['fc']))

        try:
            #----------------------------------------------------------------------
            # A globally accessible instance fb.fil_inst of selected filter class fc 
            # has been instantiated in InputFilter.set_design_method, now
            # call the method specified in the filter dict fil[0].
    
            # The name of the instance method is constructed from the response 
            # type (e.g. 'LP') and the filter order (e.g. 'man'), giving e.g. 'LPman'.
            # The filter is designed by passing the specs in fil[0] to the method, 
            # resulting in e.g. cheby1.LPman(fb.fil[0]) and writing back coefficients,
            # P/Z etc. back to fil[0].

            err = ff.fil_factory.call_fil_method(fb.fil[0]['rt'] + fb.fil[0]['fo'], fb.fil[0])
            # this is the same as e.g.
            # from pyfda.filter_design import ellip
            # inst = ellip.ellip()
            # inst.LPmin(fb.fil[0])
            #-----------------------------------------------------------------------
            
            if err > 0:
                raise AttributeError("Unknown design method.")
                self.color_design_button("error")
    
            # Update filter order. weights and freq display in case they
            # have been changed by the design algorithm
            self.sel_fil.load_filter_order()
            self.w_specs.load_entries()
            self.f_specs.load_entries()
            self.color_design_button("ok")
    
            self.sigFilterDesigned.emit() # emit signal -> InputTabWidgets.update_all

        except Exception as e:
            logger.warning("start_design_filt:\n%s\n%s\n", e.__doc__, e)
            self.color_design_button("error")

        logger.debug("start_design_filt - Results:\n"
            "F_PB = %s, F_SB = %s\n" 
            "Filter order N = %s\n"
            "NDim fil[0]['ba'] = %s\n\n"
            "b,a = %s\n\n"
            "zpk = %s\n",
            str(fb.fil[0]['F_PB']), str(fb.fil[0]['F_SB']), str(fb.fil[0]['N']),
            str(np.ndim(fb.fil[0]['ba'])), pformat(fb.fil[0]['ba']),
                pformat(fb.fil[0]['zpk'])
              )


#------------------------------------------------------------------------------
    def color_design_button(self, state):
        """
        Color the >> DESIGN FILTER << button according to the filter design state:
        "ok":  green, filter has been designed, everything ok
        "changed": yellow, filter specs have been changed
        "error" : red, an error has occurred during filter design
        "failed" : orange, filter fails to meet target specs

        The actual colors are defined in pyfda_rc.py
        """
        self.butDesignFilt.setProperty("state", str(state))
        fb.design_filt_state = state
        self.butDesignFilt.style().unpolish(self.butDesignFilt)
        self.butDesignFilt.style().polish(self.butDesignFilt)
        self.butDesignFilt.update()

#------------------------------------------------------------------------------

if __name__ == '__main__':
    from ..compat import QApplication
    app = QApplication(sys.argv)
    mainw = FilterSpecs(None)
    app.setActiveWindow(mainw) 
    mainw.show()

    sys.exit(app.exec_())
