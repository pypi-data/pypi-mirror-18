# -*- coding: utf-8 -*-
"""
Design ellip-Filters (LP, HP, BP, BS) with fixed or minimum order, return
the filter design in zeros, poles, gain (zpk) format

Attention:
This class is re-instantiated dynamically everytime the filter design method
is selected, calling the __init__ method.

Version info:   
    1.0: initial working release
    1.1: - copy A_PB -> A_PB2 and A_SB -> A_SB2 for BS / BP designs
         - mark private methods as private
    1.2: new API using fil_save (enable SOS features when available)
    1.3: new public methods destruct_UI + construct_UI (no longer called by __init__)    
    1.4: module attribute `filter_classes` contains class name and combo box name
         instead of class attribute `name`
         `FRMT` is now a class attribute

Author: Christian Muenker
"""
from __future__ import print_function, division, unicode_literals
import scipy.signal as sig
from scipy.signal import ellipord

from pyfda.pyfda_lib import fil_save, SOS_AVAIL, lin2unit

__version__ = "1.4"

filter_classes = {'Ellip':'Elliptic'}
    
class Ellip(object):

    if SOS_AVAIL:
        FRMT = 'sos' # output format of filter design routines 'zpk' / 'ba' / 'sos'
    else:
        FRMT = 'zpk'
        
    info = """
**Elliptic filters**

(also known as Cauer filters) have a constant ripple :math:`A_PB` resp.
:math:`A_SB` in both pass- and stopband(s).

For the filter design, the order :math:`N`, minimum stopband attenuation
:math:`A_SB` and
the critical frequency / frequencies :math:`F_PB` where the gain first drops below
the maximum passband ripple :math:`-A_PB` have to be specified.

The ``ellipord()`` helper routine calculates the minimum order :math:`N` and the 
critical passband frequency :math:`F_C` from pass and stop band specifications.

**Design routines:**

``scipy.signal.ellip()``
``scipy.signal.ellipord()``

        """

    def __init__(self):

        # common messages for all man. / min. filter order response types:
        msg_man = ("Enter the filter order <b><i>N</i></b>, the minimum stop "
            "band attenuation <b><i>A<sub>SB</sub></i></b> and the frequency or "
            "frequencies <b><i>F<sub>PB</sub></i></b>  where the gain first "
            "drops below the maximum passband ripple <b><i>-A<sub>PB</sub></i></b> ."
            "Stop band corner frequency(ies) <b><i>F<sub>SB</sub></i></b>&nbsp;"
            "are not regarded.")
        msg_min = ("Enter maximum pass band ripple <b><i>A<sub>PB</sub></i></b>, "
                    "minimum stop band attenuation <b><i>A<sub>SB</sub> </i></b>"
                    "&nbsp;and the corresponding corner frequencies of pass and "
                    "stop band(s), <b><i>F<sub>PB</sub></i></b>&nbsp; and "
                    "<b><i>F<sub>SB</sub></i></b> .")
        # VISIBLE widgets for all man. / min. filter order response types:
        vis_man = ['fo','tspecs'] # manual filter order
        vis_min = ['fo','tspecs'] # minimum filter order

        # DISABLED widgets for all man. / min. filter order response types:
        dis_man = [] # manual filter order
        dis_min = [] # minimum filter order

        # parameters for all man. / min. filter order response types:
        par_man = ['N', 'f_S', 'A_PB', 'A_SB']
        par_min = ['f_S', 'A_PB', 'A_SB']

        # Common data for all man. / min. filter order response types:
        # This data is merged with the entries for individual response types
        # (common data comes first):
        self.com = {"man":{"vis":vis_man, "dis":dis_man, "msg":msg_man, "par":par_man},
                    "min":{"vis":vis_min, "dis":dis_min, "msg":msg_min, "par":par_min}}

        self.ft = 'IIR'
        self.rt = {
          "LP": {"man":{"par":[]},
                 "min":{"par":['F_PB','F_SB']}},
          "HP": {"man":{"par":[]},
                 "min":{"par":['F_SB','F_PB']}},
          "BP": {"man":{"par":[]},
                 "min":{"par":['F_SB','F_PB','F_PB2','F_SB2']}},
          "BS": {"man":{"par":[]},
                 "min":{"par":['F_PB','F_SB','F_SB2','F_PB2']}}
                 }


        self.info_doc = []
        self.info_doc.append('ellip()\n========')
        self.info_doc.append(sig.ellip.__doc__)
        self.info_doc.append('ellipord()\n==========')
        self.info_doc.append(ellipord.__doc__)

    def construct_UI(self):
        """
        Create additional subwidget(s) needed for filter design with the 
        names given in self.wdg :
        These subwidgets are instantiated dynamically when needed in 
        select_filter.py using the handle to the filter instance, fb.fil_inst.
        (empty method, nothing to do in this filter)
        """
        pass
        

    def destruct_UI(self):
        """
        - Disconnect all signal-slot connections to avoid crashes upon exit
        - Delete dynamic widgets
        (empty method, nothing to do in this filter)
        """
        pass


    def _get_params(self, fil_dict):
        """
        Translate parameters from the passed dictionary to instance
        parameters, scaling / transforming them if needed.
        """
        # Frequencies are normalized to f_Nyq = f_S/2, ripple specs are in dB
        self.analog = False # set to True for analog filters
        self.N     = fil_dict['N']
        self.F_PB  = fil_dict['F_PB'] * 2
        self.F_SB  = fil_dict['F_SB'] * 2
        self.F_PB2 = fil_dict['F_PB2'] * 2
        self.F_SB2 = fil_dict['F_SB2'] * 2
        self.F_PBC = None

        self.A_PB = lin2unit(fil_dict['A_PB'], 'IIR', 'A_PB', unit='dB')
        self.A_SB = lin2unit(fil_dict['A_SB'], 'IIR', 'A_SB', unit='dB')
        
        # ellip filter routines support only one amplitude spec for
        # pass- and stop band each
        if str(fil_dict['rt']) == 'BS':
            fil_dict['A_PB2'] = fil_dict['A_PB']
        elif str(fil_dict['rt']) == 'BP':
            fil_dict['A_SB2'] = fil_dict['A_SB']


    def _save(self, fil_dict, arg):
        """
        Convert results of filter design to all available formats (pz, ba, sos)
        and store them in the global filter dictionary. 
        
        Corner frequencies and order calculated for minimum filter order are 
        also stored to allow for an easy subsequent manual filter optimization.
        """
        fil_save(fil_dict, arg, self.FRMT, __name__)

        # For min. filter order algorithms, update filter dictionary with calculated
        # new values for filter order N and corner frequency(s) F_PBC
        if str(fil_dict['fo']) == 'min': 
            fil_dict['N'] = self.N 

            if str(fil_dict['rt']) == 'LP' or str(fil_dict['rt']) == 'HP':
                fil_dict['F_PB'] = self.F_PBC / 2. # HP or LP - single  corner frequency
            else: # BP or BS - two corner frequencies
                fil_dict['F_PB'] = self.F_PBC[0] / 2.
                fil_dict['F_PB2'] = self.F_PBC[1] / 2.
                
#------------------------------------------------------------------------------
#
#         DESIGN ROUTINES
#
#------------------------------------------------------------------------------

    # LP: F_PB < F_stop -------------------------------------------------------
    def LPmin(self, fil_dict):
        """Elliptic LP filter, minimum order"""
        self._get_params(fil_dict)
        self.N, self.F_PBC = ellipord(self.F_PB,self.F_SB, self.A_PB,self.A_SB,
                                                          analog=self.analog)
        self._save(fil_dict, sig.ellip(self.N, self.A_PB, self.A_SB, self.F_PBC,
                            btype='low', analog=self.analog, output=self.FRMT))
                            
    def LPman(self, fil_dict):
        """Elliptic LP filter, manual order"""
        self._get_params(fil_dict)
        self._save(fil_dict, sig.ellip(self.N, self.A_PB, self.A_SB, self.F_PB,
                            btype='low', analog=self.analog, output=self.FRMT))

    # HP: F_stop < F_PB -------------------------------------------------------
    def HPmin(self, fil_dict):
        """Elliptic HP filter, minimum order"""
        self._get_params(fil_dict)
        self.N, self.F_PBC = ellipord(self.F_PB,self.F_SB, self.A_PB,self.A_SB,
                                                          analog=self.analog)
        self._save(fil_dict, sig.ellip(self.N, self.A_PB, self.A_SB, self.F_PBC,
                        btype='highpass', analog=self.analog, output=self.FRMT))

    def HPman(self, fil_dict):
        """Elliptic HP filter, manual order"""
        self._get_params(fil_dict)
        self._save(fil_dict, sig.ellip(self.N, self.A_PB, self.A_SB, self.F_PB,
                        btype='highpass', analog=self.analog, output=self.FRMT))

    # For BP and BS, F_XX have two elements each, A_XX has only one

    # BP: F_SB[0] < F_PB[0], F_SB[1] > F_PB[1] --------------------------------
    def BPmin(self, fil_dict):
        """Elliptic BP filter, minimum order"""
        self._get_params(fil_dict)
        self.N, self.F_PBC = ellipord([self.F_PB, self.F_PB2],
            [self.F_SB, self.F_SB2], self.A_PB, self.A_SB, analog=self.analog)
        self._save(fil_dict, sig.ellip(self.N, self.A_PB, self.A_SB, self.F_PBC,
                        btype='bandpass', analog=self.analog, output=self.FRMT))
                            
    def BPman(self, fil_dict):
        """Elliptic BP filter, manual order"""
        self._get_params(fil_dict)
        self._save(fil_dict, sig.ellip(self.N, self.A_PB, self.A_SB, 
            [self.F_PB,self.F_PB2], btype='bandpass', analog=self.analog, 
                                                                output=self.FRMT))

    # BS: F_SB[0] > F_PB[0], F_SB[1] < F_PB[1] --------------------------------
    def BSmin(self, fil_dict):
        """Elliptic BP filter, minimum order"""
        self._get_params(fil_dict)
        self.N, self.F_PBC = ellipord([self.F_PB, self.F_PB2],
                                [self.F_SB, self.F_SB2], self.A_PB,self.A_SB,
                                                        analog=self.analog)
        self._save(fil_dict, sig.ellip(self.N, self.A_PB, self.A_SB, self.F_PBC,
                        btype='bandstop', analog=self.analog, output=self.FRMT))

    def BSman(self, fil_dict):
        """Elliptic BS filter, manual order"""
        self._get_params(fil_dict)
        self._save(fil_dict, sig.ellip(self.N, self.A_PB, self.A_SB, 
            [self.F_PB,self.F_PB2], btype='bandstop', analog=self.analog, 
                                                                output=self.FRMT))
                            
#------------------------------------------------------------------------------

if __name__ == '__main__':
    import pyfda.filterbroker as fb # importing filterbroker initializes all its globals 
    filt = Ellip()        # instantiate filter
    filt.LPman(fb.fil[0])  # design a low-pass with parameters from global dict
    print(fb.fil[0][filt.FRMT]) # return results in default format