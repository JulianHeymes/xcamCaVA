from PyQt4 import QtGui 

# Create window
class Window(QtGui.QWidget):

    #This block adds features into the window init
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setWindowTitle('Monterey Bay Sea Level Rise')
        self.resize(300, 240)
        self.addWidgets1()

    def addWidgets1(self):

        self.layout = QtGui.QFormLayout()
        self.setLayout(self.layout)

        #Add drop-down list for selecting forecast year

        # You don't need to set to parent of the widgets to self anymore, the
        # layout will set the parent automatically when you add the widgets
        self.year_lbl = QtGui.QLabel("1. Select Forecast Year")
        # self.year_lbl.move(5,0) # Can be removed. The layout takes care of it.
        year = QtGui.QComboBox()
        year.addItem('2030')
        year.addItem('2060')
        year.addItem('2100')
        self.layout.addRow(self.year_lbl, year)        

        #Add drop-down list for selecting hazard
        self.hazard_lbl = QtGui.QLabel("2. Select Coastal Hazard")
        self.hazard = QtGui.QComboBox()
        self.hazard.addItem('Rising Tides')
        self.hazard.addItem('Coastal Storm Flooding')
        self.hazard.addItem('Cliff Erosion')
        self.hazard.addItem('Dune Erosion')
        self.hazard.activated[str].connect(self.updateComboboxes) 
        self.layout.addRow(self.hazard_lbl, self.hazard)        

        #Add drop-down list for inputing model intensity (s1,s2,s3)
        self.intensity_lbl = QtGui.QLabel("3. Select Intensity")
        intensity = QtGui.QComboBox()
        intensity.addItem('Low')
        intensity.addItem('Mid')
        intensity.addItem('High') 
        self.layout.addRow(self.intensity_lbl, intensity)        

        self.types_lbl = QtGui.QLabel("3. Select type of changes")
        self.types = QtGui.QComboBox()
        self.types.addItem('Long-term')
        self.types.addItem('Storm induced')
        self.layout.addRow(self.types_lbl, self.types)        

        self.storm_lbl = QtGui.QLabel("4. Select for stormier")
        self.storm = QtGui.QComboBox()
        self.storm.addItem('No Change')
        self.storm.addItem('Stormier')
        self.layout.addRow(self.storm_lbl, self.storm)        

        # show initial state
        self.updateComboboxes() 


    def updateComboboxes(self, text=None):
        #if hazard is cliff erosion or dune erosion we want to update the widget
        #... to include wstorm,long_term AND no_change,stormier

        if text is None:
            text = self.hazard.currentText()

        usable = (text == 'Cliff Erosion' or text == 'Dune Erosion')

        if True: # change to False to use enabling/disabling widgets
            # May cause other widgets to be relocated
            self.types_lbl.setVisible(usable)
            self.types.setVisible(usable)
            self.storm_lbl.setVisible(usable)
            self.storm.setVisible(usable)
        else:
            # This option doesn't relocate widgets
            # Also may give additional clue to the uses that this exsits
            self.types_lbl.setEnabled(usable)
            self.types.setEnabled(usable)
            self.storm_lbl.setEnabled(usable)
            self.storm.setEnabled(usable)

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    #window.resize(100, 60)
    window.show()
    sys.exit(app.exec_())
