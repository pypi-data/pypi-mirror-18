# -*- coding: utf-8 -*-
"""
Design equiripple-Filters (LP, HP, BP, BS) with fixed or minimum order, return
the filter design in coefficients format ('ba')

Attention: 
This class is re-instantiated dynamically everytime the filter design method
is selected, calling the __init__ method.

Version info:   
    1.0: initial working release
    1.1: mark private methods as private
    1.2: - new API using fil_save & fil_convert (allow multiple formats, 
                save 'ba' _and_ 'zpk' precisely)
         - include method _store_entries in _update_UI
    1.3: new public methods destruct_UI + construct_UI (no longer called by __init__)         
    1.4: module attribute `filter_classes` contains class name and combo box name
         instead of class attribute `name`
        `FRMT` is now a class attribute
    
Author: Christian Muenker 2014 - 2016
"""
from __future__ import print_function, division, unicode_literals, absolute_import

from ..compat import (QWidget, QLabel, QLineEdit, pyqtSignal, QFrame, QCheckBox,
                      QVBoxLayout, QHBoxLayout)


import numpy as np

import pyfda.filterbroker as fb
from pyfda.pyfda_lib import fil_save, fil_convert #, round_odd, ceil_even, remezord, 

__version__ = "1.4"

filter_classes = {'MA':'Moving Average'}   
         
class MA(QWidget):
        
    FRMT = {'zpk', 'ba'} # output format(s) of filter design routines 'zpk' / 'ba' / 'sos'


    info ="""
**Moving average filters**

can only be specified via their length and the number of cascaded sections. 

The minimum order to fulfill the target specifications (minimum attenuation at
a given frequency can be calculated via the si function (not implemented yet).

**Design routines:**

``ma.calc()``\n
    """

    sigFiltChanged = pyqtSignal()

    def __init__(self):
        QWidget.__init__(self)       

        # common messages for all man. / min. filter order response types:
        msg_man = ("Enter desired order (= delays) <b><i>N</i></b> per stage and "
                    " and the number of stages. Target frequencies and amplitudes"
                    " are only used for comparison, not for the design.")
                    
        msg_min = ""

        # VISIBLE widgets for all man. / min. filter order response types:
        vis_man = ['fo', 'tspecs'] # manual filter order
        vis_min = [] # minimum filter order

        # INFORMATIONAL widgets for all response types, these widgets are coloured,
        # signalling that they can be edited but only for informational purposes:
        info_man = ['tspecs']

        # DISABLED widgets for all man. / min. filter order response types:
        dis_man = [] # manual filter order
        dis_min = [] # manual filter order

        # common PARAMETERS for all man. / min. filter order response types:
        par_man = ['N', 'f_S'] # manual filter order
        par_min = []
        
        # Common data for all man. / min. filter order response types:
        # This data is merged with the entries for individual response types
        # (common data comes first):
        self.com = {"man":{"vis":vis_man, "dis":dis_man, "msg":msg_man, "par": par_man},
                    "min":{"vis":vis_min, "dis":dis_min, "msg":msg_min, "par": par_min}}
        self.ft = 'FIR'
        self.rt = {
            "LP": {"man":{"par":['F_PB', 'A_PB', 'F_SB', 'A_SB']},
                   #"targ":{"par":['F_PB', 'F_SB', 'A_PB', 'A_SB']}
                   },
            "HP": {"man":{"par":['F_SB', 'A_SB', 'F_PB', 'A_PB']},
                   #"targ":{"par":['F_SB', 'F_PB', 'A_SB', 'A_PB']}
                   }} 

        self.info_doc = []
#        self.info_doc.append('remez()\n=======')
#        self.info_doc.append(sig.remez.__doc__)
#        self.info_doc.append('remezord()\n==========')
#        self.info_doc.append(remezord.__doc__)
        # additional dynamic widgets that need to be set in the main widgets
        self.wdg = True
        
        self.hdl = ['ma', 'cic']
        #----------------------------------------------------------------------

    def construct_UI(self):
        """
        Create additional subwidget(s) needed for filter design with the 
        names given in self.wdg :
        These subwidgets are instantiated dynamically when needed in 
        select_filter.py using the handle to the filter instance, fb.fil_inst.
        """

        self.lbl_ma_1 = QLabel("Stages:")
        self.lbl_ma_1.setObjectName('wdg_lbl_ma_1')
        self.led_ma_1 = QLineEdit()
        self.led_ma_1.setText("1")
        self.led_ma_1.setObjectName('wdg_led_ma_1')
        self.led_ma_1.setToolTip("Set number of stages ")
        
        self.lbl_ma_2 = QLabel("Normalize:")
        self.lbl_ma_2.setObjectName('wdg_lbl_ma_2')
        self.chk_ma_2 = QCheckBox()
        self.chk_ma_2.setChecked(True)
        self.chk_ma_2.setObjectName('wdg_chk_ma_2')
        self.chk_ma_2.setToolTip("Normalize to| H_max = 1|")
        
        self.layHWin = QHBoxLayout()
        self.layHWin.setObjectName('wdg_layGWin')
        self.layHWin.addWidget(self.lbl_ma_1)
        self.layHWin.addWidget(self.led_ma_1)
        self.layHWin.addWidget(self.lbl_ma_2)
        self.layHWin.addWidget(self.chk_ma_2)
        self.layHWin.setContentsMargins(0,0,0,0)
        # Widget containing all subwidgets (cmbBoxes, Labels, lineEdits)
        self.wdg_fil = QWidget()
        self.wdg_fil.setObjectName('wdg_fil')
        self.wdg_fil.setLayout(self.layHWin)

        #----------------------------------------------------------------------
        # SIGNALS & SLOTs
        #----------------------------------------------------------------------
        self.led_ma_1.editingFinished.connect(self._update_UI)
        # fires when edited line looses focus or when RETURN is pressed
        self.chk_ma_2.clicked.connect(self._update_UI)
        #----------------------------------------------------------------------

        self._load_entries() # get initial / last setting from dictionary
        self._update_UI()
        
    def _update_UI(self):
        """
        Update UI when line edit field is changed (here, only the text is read
        and converted to integer.)
        """
        self.ma_stages = int(abs(round(float(self.led_ma_1.text()))))
        self.led_ma_1.setText(str(self.ma_stages))
        """
        Store parameter settings in filter dictionary.
        """
        fb.fil[0].update({'wdg_dyn':{'ma_stages':self.ma_stages,
                                     'ma_normalize':self.chk_ma_2.isChecked()}})
        self.sigFiltChanged.emit() # -> input_filt -> input_specs                                     


    def destruct_UI(self):
        """
        - Disconnect all signal-slot connections to avoid crashes upon exit
        - Delete dynamic widgets
        (empty method, nothing to do in this filter)
        """
        self.led_ma_1.editingFinished.disconnect()
        self.chk_ma_2.clicked.disconnect()

        
    def _load_entries(self):
        """
        Reload parameter(s) from filter dictionary and set UI elements 
        when filter is loaded from disk.
        """
        try:
            dyn_wdg_par = fb.fil[0]['wdg_dyn']
            if 'ma_stages' in dyn_wdg_par:
                self.ma_stages = dyn_wdg_par['ma_stages']
                self.led_ma_1.setText(str(self.ma_stages))
                self.chk_ma_2.setChecked(dyn_wdg_par['ma_normalize'])
        except KeyError as e:
            print("Key Error:",e)


#    def _store_entries(self):
#        """
#        Store parameter settings in filter dictionary.
#        """
#        fb.fil[0].update({'wdg_dyn':{'ma_stages':self.ma_stages,
#                                     'ma_normalize':self.chk_ma_2.isChecked()}})



    def _get_params(self, fil_dict):
        """
        Translate parameters from the passed dictionary to instance
        parameters, scaling / transforming them if needed.
        """
        self.N     = fil_dict['N']
        self.F_SB  = fil_dict['F_SB']
        self.A_SB  = fil_dict['A_SB']
        

    def _save(self, fil_dict):
        """
        Convert between poles / zeros / gain, filter coefficients (polynomes)
        and second-order sections and store all available formats in the passed
        dictionary 'fil_dict'.
        """
        if 'zpk' in self.FRMT:        
            fil_save(fil_dict, self.zpk, 'zpk', __name__, convert = False)
        if 'ba' in self.FRMT:
            fil_save(fil_dict, self.b, 'ba', __name__, convert = False)
        fil_convert(fil_dict, self.FRMT)

        if str(fil_dict['fo']) == 'min': 
            fil_dict['N'] = self.N  # yes, update filterbroker

#        self._store_entries()
        
        
    def _create_ma(self, fil_dict, rt='LP'):
        """
        Calculate coefficients and P/Z for moving average filter based on
        filter length L = N + 1 and number of cascaded stages and save the 
        result in the filter dictionary.
        """
        b = 1.
        k = 1.
        L = self.N + 1
        if rt == 'LP':
            b0 = np.ones(L)
            z0 = np.exp(-2j*np.pi*np.arange(1,L)/L)
        elif rt == 'HP':
            b0 = np.ones(L)
            b0[::2] = -1.
            i = np.arange(L)
            if (L % 2 == 0): # even order, remove middle element
                i = np.delete(i ,round(L/2.))
            else: # odd order, shift by 0.5 and remove middle element
                i = np.delete(i, int(L/2.)) + 0.5
            z0 = np.exp(-2j*np.pi*i/L)
            
        # calculate filter for multiple cascaded stages    
        for i in range(self.ma_stages):
            b = np.convolve(b0, b)
        z = np.repeat(z0, self.ma_stages)
#       print("z0", z0, '\nz',  z)
        
        # normalize filter to |H_max| = 1 is checked:
        if self.chk_ma_2.isChecked():
            b = b / (L ** self.ma_stages)
            k = 1./L ** self.ma_stages
        p = np.zeros(len(z))
        
        # store in class attributes for the _save method
        self.zpk = [z,p,k]
        self.b = b
        self._save(fil_dict)
            

    def LPman(self, fil_dict):
        self._get_params(fil_dict)
        self._create_ma(fil_dict)
                   
#    def LPmin(self, fil_dict):
#        self._get_params(fil_dict)
#        (self.N, F, A, W) = remezord([self.F_PB, self.F_SB], [1, 0],
#            [self.A_PB, self.A_SB], Hz = 1, alg = self.alg)
#
#        self._save(fil_dict, sig.remez(self.N, F, [1, 0], weight = W, Hz = 1,
#                        grid_density = self.grid_density))

    def HPman(self, fil_dict):
        self._get_params(fil_dict)
        self._create_ma(fil_dict, rt = 'HP')

#    def HPmin(self, fil_dict):
#        self._get_params(fil_dict)
#        (self.N, F, A, W) = remezord([self.F_SB, self.F_PB], [0, 1],
#            [self.A_SB, self.A_PB], Hz = 1, alg = self.alg)
##        
#
#        if (self.N % 2 == 0): # even order
#            self._save(fil_dict, sig.remez(self.N, F,[0, 1], weight = W, Hz = 1, 
#                        type = 'hilbert', grid_density = self.grid_density))
#        else:
#            self._save(fil_dict, sig.remez(self.N, F,[0, 1], weight = W, Hz = 1, 
#                        type = 'bandpass', grid_density = self.grid_density))


#------------------------------------------------------------------------------

if __name__ == '__main__':
    import sys
    from ..compat import QApplication
   
    app = QApplication(sys.argv)
    
    # instantiate filter widget
    filt = MA()
    filt.construct_UI()
    wdg_ma = getattr(filt, 'wdg_fil')

    layVDynWdg = QVBoxLayout()
    layVDynWdg.addWidget(wdg_ma, stretch = 1)

    filt.LPman(fb.fil[0])  # design a low-pass with parameters from global dict
    print(fb.fil[0]['zpk']) # return results in default format

    form = QFrame()
    form.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
    form.setLayout(layVDynWdg)    

    form.show()
    

    app.exec_()
    #------------------------------------------------------------------------------

