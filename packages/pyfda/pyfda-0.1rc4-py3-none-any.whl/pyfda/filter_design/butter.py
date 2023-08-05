# -*- coding: utf-8 -*-
"""
Design Butterworth filters (LP, HP, BP, BS) with fixed or minimum order,
return the filter design in zeros, poles, gain (zpk) or second-order sections
(sos) format

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
from scipy.signal import buttord

from pyfda.pyfda_lib import fil_save, SOS_AVAIL, lin2unit

__version__ = "1.4"

filter_classes = {'Butter':'Butterworth'}

class Butter(object):
    
    if SOS_AVAIL:
        FRMT = 'sos' # output format of filter design routines 'zpk' / 'ba' / 'sos'
    else:
        FRMT = 'zpk'

    def __init__(self):

        # common messages for all man. / min. filter order response types:
        msg_man = ("Enter the filter order <b><i>N</i></b> and the -3 dB corner "
            "frequency(ies) <b><i>F<sub>C</sub></i></b> .")
        msg_min = ("Enter maximum pass band ripple <b><i>A<sub>PB</sub></i></b>, "
                    "minimum stop band attenuation <b><i>A<sub>SB</sub> </i></b>"
                    "&nbsp;and the corresponding corner frequencies of pass and "
                    "stop band(s), <b><i>F<sub>PB</sub></i></b>&nbsp; and "
                    "<b><i>F<sub>SB</sub></i></b> .")

        # VISIBLE widgets for all man. / min. filter order response types:
        vis_man = ['fo','fspecs','tspecs'] # manual filter order
        vis_min = ['fo','fspecs','tspecs'] # minimum filter order

        # DISABLED widgets for all man. / min. filter order response types:
        dis_man = ['tspecs'] # manual filter order
        dis_min = ['fspecs'] # minimum filter order

        # common PARAMETERS for all man. / min. filter order response types:
        par_man = ['N', 'f_S', 'F_C', 'A_PB', 'A_SB'] # manual filter order
        par_min = ['f_S', 'A_PB', 'A_SB'] # minimum filter order

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
          "BP": {"man":{"par":['F_C2']},
                 "min":{"par":['F_SB','F_PB','F_PB2','F_SB2']}},
          "BS": {"man":{"par":['F_C2']},
                 "min":{"par":['F_PB','F_SB','F_SB2','F_PB2']}}
                 }

        self.info = """
**Butterworth filters**

have ripple in neither pass- nor stopband(s).

For the filter design, only the order :math:`N` and
the - 3dB corner frequency / frequencies :math:`F_C` can be specified.

The ``buttord()`` helper routine calculates the minimum order :math:`N` and the 
critical frequency from pass and stop band specifications.

**Design routines:**

``scipy.signal.butter()``
``scipy.signal.buttord()``

        """

        self.info_doc = []
        self.info_doc.append('butter()\n========')
        self.info_doc.append(sig.butter.__doc__)
        self.info_doc.append('buttord()\n==========')
        self.info_doc.append(buttord.__doc__)

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
    

    def _get_params(self,fil_dict):
        """
        Translate parameters from the passed dictionary to instance
        parameters, scaling / transforming them if needed.
        """
        self.analog = False # set to True for analog filters
        self.N     = fil_dict['N']
        # Frequencies are normalized to f_Nyq = f_S/2, ripple specs are in dB
        self.F_PB  = fil_dict['F_PB'] * 2
        self.F_SB  = fil_dict['F_SB'] * 2
        self.F_C   = fil_dict['F_C'] * 2 
        self.F_PB2 = fil_dict['F_PB2'] * 2
        self.F_SB2 = fil_dict['F_SB2'] * 2
        self.F_C2   = fil_dict['F_C2'] * 2 
        self.F_PBC = None

        self.A_PB = lin2unit(fil_dict['A_PB'], 'IIR', 'A_PB', unit='dB')
        self.A_SB = lin2unit(fil_dict['A_SB'], 'IIR', 'A_SB', unit='dB')
        
        # butter filter routines support only one amplitude spec for
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
        
        fil_save(fil_dict, arg, self.FRMT, __name__) # save & convert

        
        # For min. filter order algorithms, update filter dictionary with calculated
        # new values for filter order N and corner frequency(s) F_PBC
        if str(fil_dict['fo']) == 'min': 
            fil_dict['N'] = self.N

            if str(fil_dict['rt']) == 'LP' or str(fil_dict['rt']) == 'HP':
                fil_dict['F_C'] = self.F_PBC / 2. # HP or LP - single  corner frequency
            else: # BP or BS - two corner frequencies
                fil_dict['F_C'] = self.F_PBC[0] / 2.
                fil_dict['F_C2'] = self.F_PBC[1] / 2.

#------------------------------------------------------------------------------
#
#         DESIGN ROUTINES
#
#------------------------------------------------------------------------------


    # LP: F_PB < F_SB  -------------------------------------------------------- 
    def LPmin(self, fil_dict):
        self._get_params(fil_dict)
        self.N, self.F_PBC = buttord(self.F_PB,self.F_SB, self.A_PB,self.A_SB,
                                                     analog = self.analog)
        self._save(fil_dict, sig.butter(self.N, self.F_PBC, btype='low',
                                       analog=self.analog, output=self.FRMT))

    def LPman(self, fil_dict):
        self._get_params(fil_dict)
        self._save(fil_dict, sig.butter(self.N, self.F_C,
                            btype='low', analog=self.analog, output=self.FRMT))

    # HP: F_SB < F_PB -------------------------------------------------------
    def HPmin(self, fil_dict):
        self._get_params(fil_dict)
        self.N, self.F_PBC = buttord(self.F_PB,self.F_SB, self.A_PB,self.A_SB,
                                                         analog = self.analog)
        self._save(fil_dict, sig.butter(self.N, self.F_PBC, btype='highpass',
                                      analog=self.analog, output=self.FRMT))

    def HPman(self, fil_dict):
        self._get_params(fil_dict)
        self._save(fil_dict, sig.butter(self.N, self.F_PB, btype='highpass',
                                      analog=self.analog, output=self.FRMT))


    # For BP and BS, F_xx have two elements each,  A_xx only have one element

    # BP: F_SB[0] < F_PB[0], F_SB[1] > F_PB[1] --------------------------------
    def BPmin(self, fil_dict):
        self._get_params(fil_dict)
        self.N, self.F_PBC = buttord([self.F_PB, self.F_PB2],
            [self.F_SB, self.F_SB2], self.A_PB, self.A_SB, analog = self.analog)
        self._save(fil_dict, sig.butter(self.N, self.F_PBC, btype='bandpass',
                                       analog=self.analog, output=self.FRMT))

    def BPman(self, fil_dict):
        self._get_params(fil_dict)
        self._save(fil_dict, sig.butter(self.N, [self.F_C,self.F_C2],
                    btype='bandpass', analog=self.analog, output=self.FRMT))

    # BS: F_SB[0] > F_PB[0], F_SB[1] < F_PB[1] --------------------------------
    def BSmin(self, fil_dict):
        self._get_params(fil_dict)
        self.N, self.F_PBC = buttord([self.F_PB, self.F_PB2],
            [self.F_SB, self.F_SB2], self.A_PB,self.A_SB, analog = self.analog)
        self._save(fil_dict, sig.butter(self.N, self.F_PBC, btype='bandstop',
                                       analog=self.analog, output=self.FRMT))

    def BSman(self, fil_dict):
        self._get_params(fil_dict)
        self._save(fil_dict, sig.butter(self.N, [self.F_C,self.F_C2],
                        btype='bandstop', analog=self.analog, output=self.FRMT))
                           
#------------------------------------------------------------------------------

if __name__ == '__main__':
    import pyfda.filterbroker as fb # importing filterbroker initializes all its globals 
    filt = Butter()        # instantiate filter
    filt.LPman(fb.fil[0])  # design a low-pass with parameters from global dict
    print(fb.fil[0][filt.FRMT]) # return results in default format