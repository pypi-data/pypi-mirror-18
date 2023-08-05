# -*- coding: utf-8 -*-
"""
Tabbed container with all plot widgets

Author: Christian Münker
"""
from __future__ import print_function, division, unicode_literals, absolute_import

from ..compat import QTabWidget,QVBoxLayout


from pyfda.plot_widgets import (plot_hf, plot_phi, plot_pz, plot_tau_g, plot_impz,
                          plot_3d)

#------------------------------------------------------------------------------
class PlotTabWidgets(QTabWidget):
    def __init__(self, parent):
        super(PlotTabWidgets, self).__init__(parent)

        self.pltHf = plot_hf.PlotHf(self)
        self.pltPhi = plot_phi.PlotPhi(self)
        self.pltPZ = plot_pz.PlotPZ(self)
        self.pltTauG = plot_tau_g.PlotTauG(self)
        self.pltImpz = plot_impz.PlotImpz(self)
        self.plt3D = plot_3d.Plot3D(self)

        self._init_UI()


#------------------------------------------------------------------------------
    def _init_UI(self):
        """ Initialize UI with tabbed subplots """
        tabWidget = QTabWidget()
        tabWidget.setObjectName("plot_tabs")
        tabWidget.addTab(self.pltHf, '|H(f)|')
        tabWidget.addTab(self.pltPhi, 'phi(f)')
        tabWidget.addTab(self.pltPZ, 'P/Z')
        tabWidget.addTab(self.pltTauG, 'tau_g')
        tabWidget.addTab(self.pltImpz, 'h[n]')
        tabWidget.addTab(self.plt3D, '3D')

        layVMain = QVBoxLayout()
        layVMain.addWidget(tabWidget)
        layVMain.setContentsMargins(1,1,1,1)#(left, top, right, bottom)
#
        self.setLayout(layVMain)

#------------------------------------------------------------------------------
    def update_data(self):
        """ Calculate subplots with new filter DATA and redraw them """
        self.pltHf.draw()
        self.pltPhi.draw()
        self.pltPZ.draw()
        self.pltTauG.draw()
        self.pltImpz.draw()
        self.plt3D.draw()

#------------------------------------------------------------------------------
    def update_view(self):
        """ Update plot limits with new filter SPECS and redraw all subplots """
        self.pltHf.update_view()
        self.pltPhi.update_view()
        self.pltTauG.update_view()
        self.pltImpz.update_view()

#        self.pltPZ.draw()
#        self.plt3D.draw()

#------------------------------------------------------------------------

def main():
    import sys
    from pyfda import pyfda_rc as rc
    from ..compat import QApplication
    
    app = QApplication(sys.argv)
    app.setStyleSheet(rc.css_rc)

    mainw = PlotTabWidgets(None)
    app.setActiveWindow(mainw) 
    mainw.show()
    
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()
