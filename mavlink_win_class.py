import sys, time
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer
#import viewMdi
import mavlink_win_clock_class
from PyQt5.QtWidgets import QMainWindow , QAction, qApp , QMdiArea , QMdiSubWindow, QWidget, QListWidget, QVBoxLayout, QListWidgetItem, QMessageBox, QAbstractItemView, QFormLayout, QLineEdit, QTextEdit, QTableWidget, QTableWidgetItem, QHeaderView, QItemDelegate, QPushButton, QCheckBox, QGridLayout, QLabel, QRadioButton
from PyQt5.QtGui import QDoubleValidator , QTextCursor
from PyQt5.QtGui import QPalette, QColor
#
import MavVars 
import pandas as pd

from datetime import datetime, timedelta
#
# pyqt5 colors names of color https://www.w3.org/TR/SVG11/types.html#ColorKeywords


class FloatDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super().__init__()

    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        editor.setValidator(QDoubleValidator())
        return editor


class TableWidget(QTableWidget):
    def __init__(self, df):
        super().__init__()
        self.df = df
        self.setStyleSheet('font-size: 20px;')

        # set table dimension
        nRows, nColumns = self.df.shape
        self.setColumnCount(nColumns)
        self.setRowCount(nRows)
        #
        #Qt.Vertical?
        #headers = dict_.keys()
        #print( "TableWidget::init df.columns column titles:", df.columns )
        self.setHorizontalHeaderLabels(df.columns) # is dict.keys()
        
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.setItemDelegateForColumn(1, FloatDelegate())

        # data insertion
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                self.setItem(i, j, QTableWidgetItem(str(self.df.iloc[i, j])))
                print( "DF frame rows, cols, colTitle, ColdataFormatted: ", i, j , self.horizontalHeaderItem(j).text(), str(self.df.iloc[i, j]) )  
                # header = self.horizontalHeaderItem(column).text()  # dict_ = {'time_unix_usec' : '1662239279616000', 'time_boot_ms' : '347174300'}
                MavVars.G5simDataDict[ self.horizontalHeaderItem(j).text() ] = str(self.df.iloc[i, j])
        self.cellChanged[int, int].connect(self.updateDF)   

    def updateDF(self, row, column):
        text = self.item(row, column).text()
        self.df.iloc[row, column] = text


    def textchanged(self, text):
        print ("contents of text box: "+text)
    
    def enterPress(self):
        print ("edited")
        
    def onClicked(self):
        # printing button pressed
        print(" onClicked listbox button pressed")

    def onClicked(self, item):
        QMessageBox.information(self, "Info", item.text())

    #def exitApp(self):
        # printing button pressed
        #print(" exitApp button pressed")
        #sys.exit(qApp.quit) 

# Buttons Panel
class ControlPanelWin(QtWidgets.QWidget):              # Add ControlPanelWin -------------------------------------------------------
    def __init__(self, parent ): # parent = None
        QtWidgets.QWidget.__init__(self, parent)
        self.initUI(self)  
 
    def initUI(self, controlPanelWin):
        
        # create Exit action so can quit app from button      
        self.exitAction = QAction('&Exit', self)    #_#_#_#_Created UI->ControlWin->addSubWindow() title:  2 : SYSTEM_TIME  added new subWindow widget inside UI msg window...
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(qApp.quit)
        #
        self.exit_button = QtWidgets.QPushButton(self) #exit_button= Button(mainWindow, text="Exit", bg='#c3d8ec',command=sys.exit).place(x=25, y=25,  height=65, width=200 ) 
        self.exit_button.setGeometry(QtCore.QRect(5, 40, 150, 75)) #A QRect can be constructed with a set of left, top, width and height integers, 
        self.exit_button.move(100,100)
        self.exit_button.setText("Exit")
        self.exit_button.setObjectName("Exit")
        self.exit_button.setStyleSheet("QPushButton{background-color : lightblue;} QPushButton::pressed{background-color : red;}")
        # adding action to a button
        self.exit_button.clicked.connect(self.exitApp) # self.clickme     # adding action to a button  #self.connect_button.clicked.connect(self.connectVeh) # self.clickme  # adding action to a button
        
        # adding action to a button
        #self.comms_button = QtWidgets.QPushButton(self)
        #self.comms_button.setGeometry(QtCore.QRect(5, 40, 150, 50)) #A QRect can be constructed with a set of left, top, width and height integers, 
        #self.comms_button.move(100,150)
        #self.comms_button.setText("Comms")
        #self.comms_button.setObjectName("Comms")

        # adding action to a button
        self.connect_button = QtWidgets.QPushButton(self)
        self.connect_button.setGeometry(QtCore.QRect(5, 40, 150, 50)) #A QRect can be constructed with a set of left, top, width and height integers, 
        self.connect_button.move(100,200)
        self.connect_button.setText("Connect")
        self.connect_button.setObjectName("Connect")
        self.connect_button.clicked.connect(self.clickConnectButton)
        self.connect_button.setStyleSheet("QPushButton{background-color : red;} QPushButton::pressed{background-color : lightgreen;}")

        #self.ARM_button = QtWidgets.QPushButton("PAUSE",self) #QtWidgets.QPushButton(self)
        #self.RecvON_button.setGeometry(QtCore.QRect(5, 40, 150, 25)) #A QRect can be constructed with a set of left, top, width and height integers, 
        #self.RecvON_button.move(100,275)
        #self.RecvON_button.setText("PAUSE")
        #self.RecvON_button.setObjectName("PAUSE")
        #self.RecvON_button.clicked.connect(self.clickbox)  # (lambda: self.clear(self.listWidget))

        self.ARM_button = QtWidgets.QPushButton(self) #QCheckBox("ARM_button",self) 
        self.ARM_button.setGeometry(QtCore.QRect(5, 40, 150, 50)) #A QRect can be constructed with a set of left, top, width and height integers, 
        self.ARM_button.move(100,300)
        self.ARM_button.setText("ARM")
        self.ARM_button.setObjectName("ARM_button")
        self.ARM_button.clicked.connect(self.ARM_clicked)  # (lambda: self.clear(self.listWidget))
        self.ARM_button.setStyleSheet("QPushButton{background-color : lightgreen;} QPushButton::pressed{background-color : orange}")
        
        self.DISARM_button = QtWidgets.QPushButton(self) #QCheckBox("DISARM_button",self) 
        self.DISARM_button.setGeometry(QtCore.QRect(5, 40, 150, 50)) #A QRect can be constructed with a set of left, top, width and height integers, 
        self.DISARM_button.move(300,300)
        self.DISARM_button.setText("DISARM")
        self.DISARM_button.setObjectName("DISARM_button")
        self.DISARM_button.clicked.connect(self.DISARM_clicked)  # (lambda: self.clear(self.listWidget))
        self.DISARM_button.setStyleSheet("QPushButton{background-color : lightgreen;} QPushButton::pressed{background-color : orange}")
        
        #self.MATCH_ON_button = QCheckBox("MATCH SELECTED MSGS",self) # QtWidgets.QPushButton(self)
        #self.MATCH_ON_button.setGeometry(QtCore.QRect(5, 40, 150, 25)) #A QRect can be constructed with a set of left, top, width and height integers, 
        #self.MATCH_ON_button.move(100,325)
        #self.MATCH_ON_button.setText("MATCH SELECTED MSGS FROM LIST BELOW:   \/")
        #self.MATCH_ON_button.setObjectName("MATCH ON")
        #self.MATCH_ON_button.clicked.connect(self.match_clickbox)  # (lambda: self.clear(self.listWidget))

        #self.DispMatch_button = QCheckBox("DISPMATCH ON",self) #QtWidgets.QPushButton(self)
        #self.DispMatch_button.setGeometry(QtCore.QRect(5, 40, 150, 25)) #A QRect can be constructed with a set of left, top, width and height integers, 
        #self.DispMatch_button.move(100,350)
        #self.DispMatch_button.setText("DISPMATCH ON")
        #self.DispMatch_button.setObjectName("DISPMATCH ON")
        #self.DispMatch_button.clicked.connect(self.clickbox)  # (lambda: self.clear(self.listWidget))

        # adding action to a button
        #self.pause_button = QtWidgets.QPushButton(self)
        #self.pause_button.setGeometry(QtCore.QRect(5, 40, 150, 50)) #A QRect can be constructed with a set of left, top, width and height integers, 
        #self.pause_button.move(100,350)
        #self.pause_button.setText("PAUSE")
        #self.pause_button.setObjectName("PAUSE")

        # adding action to a button
        # show all msgs from vehicle
        #self.showall_button = QtWidgets.QPushButton(self)
        #self.showall_button.setGeometry(QtCore.QRect(5, 40, 150, 50)) #A QRect can be constructed with a set of left, top, width and height integers, 
        #self.showall_button.move(100,400)
        #self.showall_button.setText("SHOW-ALL")
        #self.showall_button.setObjectName("SHOW-ALL")

        #
        # adding action to a button
        #self.connect_button.clicked.connect(self.connectVeh) # self.clickme     # adding action to a button
        # show all msgs from vehicle
        #self.show_match_button = QtWidgets.QPushButton(self)
        #self.show_match_button.setGeometry(QtCore.QRect(5, 40, 150, 50)) #A QRect can be constructed with a set of left, top, width and height integers, 
        #self.show_match_button.move(100,250)
        #self.show_match_button.setText("SHOW-MATCH")
        #self.show_match_button.setObjectName("SHOW-MATCH")
        
        self.vbox = QVBoxLayout(self) # self.setLayout(self.vbox)
        # list widget with clear button at bottom of widget
        #self.listWidget = QListWidget()

        # adding action to a button
        # clearlist_button msgs from vehicle
        self.clearlist_button = QtWidgets.QPushButton(self)
        self.clearlist_button.setGeometry(QtCore.QRect(5, 40, 100, 30)) #A QRect can be constructed with a set of left, top, width and height integers, 
        self.clearlist_button.move(100,450)
        self.clearlist_button.setText("CLEAR SELECTION")
        self.clearlist_button.setObjectName("clear-list")
        # set signal to also clear the list elsewhere
        self.clearlist_button.clicked.connect(lambda: self.clear(self.listWidget))
        
        #self.CullEmptyWins_button = QtWidgets.QPushButton(self) #QCheckBox("CULL_EMPTY_WINS",self) #QtWidgets.QPushButton(self)
        #self.CullEmptyWins_button.setGeometry(QtCore.QRect(5, 40, 150, 25)) #A QRect can be constructed with a set of left, top, width and height integers, 
        #self.CullEmptyWins_button.move(100,475)
        #self.CullEmptyWins_button.setText("CULL_EMPTY MAVLINK MSG WINDOWS")
        #self.CullEmptyWins_button.setObjectName("CULL_EMPTY_MSGS")
        #self.CullEmptyWins_button.clicked.connect(self.cull_empy_wins_clickbox)  # (lambda: self.clear(self.listWidget))

        ## multiple selections allowed
        #self.listWidget.setSelectionMode(QAbstractItemView.MultiSelection)
        ## Insert multiple elements into the messages ypr listbox
        ##print(myButton.clicked.connect(lambda: clear(myListWidget))" \n\n ControlWin class , MAVLinkDict ", MavVars.MAVLinkDict)
        #for key in MavVars.MAVLinkDict:
        #    self.listWidget.addItem(MavVars.MAVLinkDict[key])  #self.listWidget.addItem(key + ":" + MavVars.MAVLinkDict[key] )
        #    print(" inserting new msg type into listbox -- key, name", key, MavVars.MAVLinkDict[key])
        #print("\n\n") 
        ##
        #self.listWidget.itemDoubleClicked.connect(self.onClicked)    
        #self.listWidget.itemClicked.connect(self.onClicked)
        ##
        self.vbox.addWidget(self.exit_button)
        self.vbox.addWidget(self.connect_button)
        ##self.vbox.addWidget(self.comms_button)
        #self.vbox.addWidget(self.RecvON_button)
        #self.vbox.addWidget(self.DispALL_button)
        #self.vbox.addWidget(self.MATCH_ON_button)
        #self.vbox.addWidget(self.listWidget)
        #self.vbox.addWidget(self.clearlist_button)
        #self.vbox.addWidget(self.CullEmptyWins_button)
        ##
        self.setLayout(self.vbox)
        self.setGeometry(0, 0, 600, 1200) # x , y , w , h
        #self.mdiChild.setGeometry(0, 0, 600, 600) # x , y , w , h
        self.setWindowTitle('Controls')
        self.show()
        #self.clickConnectButton()

    def clear(self, listwidget):
        print("clear listwidget.item(i).setSelected(False) ")
        for i in range(listwidget.count()):  # unselect / unhighlight listbox items selected
            self.item = listwidget.item(i)
            self.listWidget.item(i).setSelected(False) #listwidget.setSelected(self.item, False)
        MavVars.clearall = True # DELETE unused windows in main
               
    def clickConnectButton(self):
        #self.connect_button.setStyleSheet("QPushButton{background-color : yellow;} QPushButton::pressed{background-color : red;}")
        if MavVars.veh_connected:
            self.connect_button.setStyleSheet(" QPushButton{background-color : lightgreen;} QPushButton::pressed{background-color : red;}")
            self.connect_button.setText("Connected")
        else:
            self.connect_button.setStyleSheet("QPushButton{background-color : red;} QPushButton::pressed{background-color : lightgreen;}")
            self.connect_button.setText("NOT Connected")
        self.show()
        print("Clicked Connect Button")

    # action method clickme
    def connectVeh(self): 
        # printing button pressed
        print(" connectVeh button pressed")
        # run connectVehicle()

    def match_clickbox(self):
        # button pressed
        print(" match_clickbox pressed ")

    def clickbox(self):
        # button pressed
        print(" clickbox pressed ")
    
    def cull_empy_wins_clickbox(self):
        print(" --cull_empy_wins_clickbox start total MAVLinkDict msgs: ", len(MavVars.MAVLinkDict) , MavVars.MAVLinkDict )
        # delete windows if "empty" in timediff field unused msg windows
        print(" --cull_empy_wins_clickbox pressed() end", "\n\n" ,  MavVars.MAVmsgsToWatchDict)

    def ARM_clicked(self):
        print(" --ARM_button pressed()... ")
        
    def DISARM_clicked(self):
        print(" --DISARM_button pressed()... ")

    # action method clickme
    def clickme(self):
        # printing button pressed
        print(" clickme action method button pressed")

    def onClicked(self): # when listbox item or button pressed
        MavVars.clearall = False
        print ("--onClicked listbox item clicked")  
        for i in range(self.listWidget.count()):
            #print ("--onClicked self.listWidget.item(index).Selected(): ",self.listWidget.item(i).isSelected() , "  self.item ", self.item )
            if self.listWidget.item(i).isSelected() == True:
                tmp = self.listWidget.currentItem().text()  # selected listbox item text
                msg = tmp.split(" ") # splits the id and the name of recvd msg
                MavVars.MAVmsgsToWatchDict[msg[0]] = msg[1]
                print("--onClicked listbox button pressed,  self.listWidget.currentItem() ", self.listWidget.currentItem() , "  self.listWidget.currentItem().text() ", self.listWidget.currentItem().text()," msg0 ", msg[0]," msg1 ", msg[1], " MavVars.MAVmsgsToWatchDict ", MavVars.MAVmsgsToWatchDict ) 
                
    # action method
    def exitApp(self):
        # printing button pressed
        print(" exit button pressed")
        sys.exit(qApp.quit) 



class ControlWin(QtWidgets.QWidget):              # Add ControlWin -------------------------------------------------------
    def __init__(self, parent ): # parent = None
        QtWidgets.QWidget.__init__(self, parent)
        self.initUI(self)  
 
    def initUI(self, controlWin):
        
        # create Exit action so can quit app from button      
        self.exitAction = QAction('&Exit', self)    #_#_#_#_Created UI->ControlWin->addSubWindow() title:  2 : SYSTEM_TIME  added new subWindow widget inside UI msg window...
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(qApp.quit)
        #
        self.exit_button = QtWidgets.QPushButton(self) #exit_button= Button(mainWindow, text="Exit", bg='#c3d8ec',command=sys.exit).place(x=25, y=25,  height=65, width=200 ) 
        self.exit_button.setGeometry(QtCore.QRect(5, 40, 150, 75)) #A QRect can be constructed with a set of left, top, width and height integers, 
        self.exit_button.move(100,100)
        self.exit_button.setText("Exit")
        self.exit_button.setObjectName("Exit")
        self.exit_button.setStyleSheet("QPushButton{background-color : lightblue;} QPushButton::pressed{background-color : red;}")
        # adding action to a button
        self.exit_button.clicked.connect(self.exitApp) # self.clickme     # adding action to a button  #self.connect_button.clicked.connect(self.connectVeh) # self.clickme  # adding action to a button
        
        # adding action to a button
        #self.comms_button = QtWidgets.QPushButton(self)
        #self.comms_button.setGeometry(QtCore.QRect(5, 40, 150, 50)) #A QRect can be constructed with a set of left, top, width and height integers, 
        #self.comms_button.move(100,150)
        #self.comms_button.setText("Comms")
        #self.comms_button.setObjectName("Comms")

        # adding action to a button
        self.connect_button = QtWidgets.QPushButton(self)
        self.connect_button.setGeometry(QtCore.QRect(5, 40, 150, 50)) #A QRect can be constructed with a set of left, top, width and height integers, 
        self.connect_button.move(100,200)
        self.connect_button.setText("Connect")
        self.connect_button.setObjectName("Connect")
        self.connect_button.clicked.connect(self.clickConnectButton)
        self.connect_button.setStyleSheet("QPushButton{background-color : red;} QPushButton::pressed{background-color : lightgreen;}")

        self.RecvON_button = QtWidgets.QPushButton("PAUSE",self) #QtWidgets.QPushButton(self)
        self.RecvON_button.setGeometry(QtCore.QRect(5, 40, 150, 25)) #A QRect can be constructed with a set of left, top, width and height integers, 
        self.RecvON_button.move(100,275)
        self.RecvON_button.setText("PAUSE")
        self.RecvON_button.setObjectName("PAUSE")
        self.RecvON_button.clicked.connect(self.clickbox)  # (lambda: self.clear(self.listWidget))

        self.DispALL_button = QCheckBox("SHOW ALL MAVLINK MSGS",self) #QtWidgets.QPushButton(self)
        self.DispALL_button.setGeometry(QtCore.QRect(5, 40, 150, 25)) #A QRect can be constructed with a set of left, top, width and height integers, 
        self.DispALL_button.move(100,300)
        self.DispALL_button.setText("SHOW ALL MAVLINK MSGS")
        self.DispALL_button.setObjectName("SHOW_ALL MSGS")
        self.DispALL_button.clicked.connect(self.disp_all_clickbox)  # (lambda: self.clear(self.listWidget))
        
        self.MATCH_ON_button = QCheckBox("MATCH SELECTED MSGS",self) # QtWidgets.QPushButton(self)
        self.MATCH_ON_button.setGeometry(QtCore.QRect(5, 40, 150, 25)) #A QRect can be constructed with a set of left, top, width and height integers, 
        self.MATCH_ON_button.move(100,325)
        self.MATCH_ON_button.setText("MATCH SELECTED MSGS FROM LIST BELOW:   \/")
        self.MATCH_ON_button.setObjectName("MATCH ON")
        self.MATCH_ON_button.clicked.connect(self.match_clickbox)  # (lambda: self.clear(self.listWidget))

        #self.DispMatch_button = QCheckBox("DISPMATCH ON",self) #QtWidgets.QPushButton(self)
        #self.DispMatch_button.setGeometry(QtCore.QRect(5, 40, 150, 25)) #A QRect can be constructed with a set of left, top, width and height integers, 
        #self.DispMatch_button.move(100,350)
        #self.DispMatch_button.setText("DISPMATCH ON")
        #self.DispMatch_button.setObjectName("DISPMATCH ON")
        #self.DispMatch_button.clicked.connect(self.clickbox)  # (lambda: self.clear(self.listWidget))

        # adding action to a button
        #self.pause_button = QtWidgets.QPushButton(self)
        #self.pause_button.setGeometry(QtCore.QRect(5, 40, 150, 50)) #A QRect can be constructed with a set of left, top, width and height integers, 
        #self.pause_button.move(100,350)
        #self.pause_button.setText("PAUSE")
        #self.pause_button.setObjectName("PAUSE")

        # adding action to a button
        # show all msgs from vehicle
        #self.showall_button = QtWidgets.QPushButton(self)
        #self.showall_button.setGeometry(QtCore.QRect(5, 40, 150, 50)) #A QRect can be constructed with a set of left, top, width and height integers, 
        #self.showall_button.move(100,400)
        #self.showall_button.setText("SHOW-ALL")
        #self.showall_button.setObjectName("SHOW-ALL")

        #
        # adding action to a button
        #self.connect_button.clicked.connect(self.connectVeh) # self.clickme     # adding action to a button
        # show all msgs from vehicle
        #self.show_match_button = QtWidgets.QPushButton(self)
        #self.show_match_button.setGeometry(QtCore.QRect(5, 40, 150, 50)) #A QRect can be constructed with a set of left, top, width and height integers, 
        #self.show_match_button.move(100,250)
        #self.show_match_button.setText("SHOW-MATCH")
        #self.show_match_button.setObjectName("SHOW-MATCH")
        
        self.vbox = QVBoxLayout(self) # self.setLayout(self.vbox)
        # list widget with clear button at bottom of widget
        self.listWidget = QListWidget()

        # adding action to a button
        # clearlist_button msgs from vehicle
        self.clearlist_button = QtWidgets.QPushButton(self)
        self.clearlist_button.setGeometry(QtCore.QRect(5, 40, 100, 30)) #A QRect can be constructed with a set of left, top, width and height integers, 
        self.clearlist_button.move(100,450)
        self.clearlist_button.setText("CLEAR SELECTION")
        self.clearlist_button.setObjectName("clear-list")
        # set signal to also clear the list elsewhere
        self.clearlist_button.clicked.connect(lambda: self.clear(self.listWidget))
        
        self.CullEmptyWins_button = QtWidgets.QPushButton(self) #QCheckBox("CULL_EMPTY_WINS",self) #QtWidgets.QPushButton(self)
        self.CullEmptyWins_button.setGeometry(QtCore.QRect(5, 40, 150, 25)) #A QRect can be constructed with a set of left, top, width and height integers, 
        self.CullEmptyWins_button.move(100,475)
        self.CullEmptyWins_button.setText("CULL_EMPTY MAVLINK MSG WINDOWS")
        self.CullEmptyWins_button.setObjectName("CULL_EMPTY_MSGS")
        self.CullEmptyWins_button.clicked.connect(self.cull_empy_wins_clickbox)  # (lambda: self.clear(self.listWidget))

        # multiple selections allowed
        self.listWidget.setSelectionMode(QAbstractItemView.MultiSelection)
        # Insert multiple elements into the messages ypr listbox
        #print(myButton.clicked.connect(lambda: clear(myListWidget))" \n\n ControlWin class , MAVLinkDict ", MavVars.MAVLinkDict)
        for key in MavVars.MAVLinkDict:
            self.listWidget.addItem(MavVars.MAVLinkDict[key])  #self.listWidget.addItem(key + ":" + MavVars.MAVLinkDict[key] )
            print(" inserting new msg type into listbox -- key, name", key, MavVars.MAVLinkDict[key])
        print("\n\n") 
        #
        self.listWidget.itemDoubleClicked.connect(self.onClicked)    
        self.listWidget.itemClicked.connect(self.onClicked)
        #
        self.vbox.addWidget(self.exit_button)
        self.vbox.addWidget(self.connect_button)
        #self.vbox.addWidget(self.comms_button)
        self.vbox.addWidget(self.RecvON_button)
        self.vbox.addWidget(self.DispALL_button)
        self.vbox.addWidget(self.MATCH_ON_button)
        self.vbox.addWidget(self.listWidget)
        self.vbox.addWidget(self.clearlist_button)
        self.vbox.addWidget(self.CullEmptyWins_button)
        #
        self.setLayout(self.vbox)
        self.setGeometry(0, 0, 600, 1200) # x , y , w , h
        #self.mdiChild.setGeometry(0, 0, 600, 600) # x , y , w , h
        self.setWindowTitle('Controls')
        self.show()
        self.clickConnectButton()

    def clear(self, listwidget):
        print("clear listwidget.item(i).setSelected(False) ")
        for i in range(listwidget.count()):  # unselect / unhighlight listbox items selected
            self.item = listwidget.item(i)
            self.listWidget.item(i).setSelected(False) #listwidget.setSelected(self.item, False)
        MavVars.clearall = True # DELETE unused windows in main
               
    def clickConnectButton(self):
        #self.connect_button.setStyleSheet("QPushButton{background-color : yellow;} QPushButton::pressed{background-color : red;}")
        if MavVars.veh_connected:
            self.connect_button.setStyleSheet(" QPushButton{background-color : lightgreen;} QPushButton::pressed{background-color : red;}")
            self.connect_button.setText("Connected")
        else:
            self.connect_button.setStyleSheet("QPushButton{background-color : red;} QPushButton::pressed{background-color : lightgreen;}")
            self.connect_button.setText("NOT Connected")
        self.show()
        print("Clicked Connect Button")

    # action method clickme
    def connectVeh(self): 
        # printing button pressed
        print(" connectVeh button pressed")
        # run connectVehicle()

    def match_clickbox(self):
        # button pressed
        print(" match_clickbox pressed ")

    def clickbox(self):
        # button pressed
        print(" clickbox pressed ")
    
    def cull_empy_wins_clickbox(self):
        print(" --cull_empy_wins_clickbox start total MAVLinkDict msgs: ", len(MavVars.MAVLinkDict) , MavVars.MAVLinkDict )
        # delete windows if "empty" in timediff field unused msg windows
        print(" --cull_empy_wins_clickbox pressed() end", "\n\n" ,  MavVars.MAVmsgsToWatchDict)


    def disp_all_clickbox(self):
        # MavVars.MAVmsgsToWatchDict button pressed
        #MavVars.MAVmsgsToWatchDict = MavVars.MAVLinkDict
        #for key in MavVars.MAVmsgsToWatchDict:
        #>>> x = OrderedDict((("a", "1"), ("c", '3'), ("b", "2")))
        #>>> x["d"] = 4
        #>>> x.keys().index("d")
        #3
        #>>> x.keys().index("c")
        #1
        #For those using Python 3
        #>>> list(x.keys()).index("c")
        #1
        print(" --disp_all_clickbox start inserting new msg type into listbox --  total MAVLinkDict msgs: ", len(MavVars.MAVLinkDict) , MavVars.MAVLinkDict )
        for key in MavVars.MAVLinkDict:  # all msgs
                print(" --disp_all_clickbox inserting new msg type into listbox -- key, name", key, len(MavVars.MAVLinkDict[key]))
                tmp = MavVars.MAVLinkDict[key] # each listbox item gets put into msgs to watch list below
                #tmp = self.listWidget.currentItem().text()  # selected listbox item text
                msg = tmp.split(" ") # splits the id and the name of recvd msg
                MavVars.MAVmsgsToWatchDict[msg[0]] = msg[1]
                print("--disp_all_clickbox,  self.listWidget.currentItem() ", self.listWidget.currentItem() , "  self.listWidget.currentItem().text() ", MavVars.MAVLinkDict[key] ," msg0 ", msg[0]," msg1 ", msg[1] ) #   , " MavVars.MAVmsgsToWatchDict ", MavVars.MAVmsgsToWatchDict
        #    self.listWidget.addItem(MavVars.MAVLinkDict[key])  #self.listWidget.addItem(key + ":" + MavVars.MAVLinkDict[key] )
        #    print(" inserting new msg type into listbox -- key, name", key, MavVars.MAVLinkDict[key])
        #print("\n\n") 
        print(" --clickbox_disp_all pressed() end, copied all mav link msgs into to msgs to watch dict .. MavVars.MAVmsgsToWatchDict = MavVars.MAVLinkDict ", "\n\n" ,  MavVars.MAVmsgsToWatchDict)

    # action method clickme
    def clickme(self):
        # printing button pressed
        print(" clickme action method button pressed")

    def onClicked(self): # when listbox item or button pressed
        MavVars.clearall = False
        print ("--onClicked listbox item clicked")  
        for i in range(self.listWidget.count()):
            #print ("--onClicked self.listWidget.item(index).Selected(): ",self.listWidget.item(i).isSelected() , "  self.item ", self.item )
            if self.listWidget.item(i).isSelected() == True:
                tmp = self.listWidget.currentItem().text()  # selected listbox item text
                msg = tmp.split(" ") # splits the id and the name of recvd msg
                MavVars.MAVmsgsToWatchDict[msg[0]] = msg[1]
                print("--onClicked listbox button pressed,  self.listWidget.currentItem() ", self.listWidget.currentItem() , "  self.listWidget.currentItem().text() ", self.listWidget.currentItem().text()," msg0 ", msg[0]," msg1 ", msg[1], " MavVars.MAVmsgsToWatchDict ", MavVars.MAVmsgsToWatchDict ) 
                
    # action method
    def exitApp(self):
        # printing button pressed
        print(" exit button pressed")
        sys.exit(qApp.quit) 


class RecvdCommsWin(QtWidgets.QWidget):
    def __init__(self, parent ): # parent = None
        QtWidgets.QWidget.__init__(self, parent)
        self.initUI(self)  

    def on_clickConnect1Button(self):
        MavVars.ConnectTo = 1
        print("RecvdCommsWin::on_clickConnect1Button\n")

    def on_clickConnect2Button(self):
        MavVars.ConnectTo = 2
        MavVars.vehIPAddr = self.vehIPAddr.toPlainText()
        MavVars.vehIPport = self.vehIPport.toPlainText()
        print("RecvdCommsWin::on_clickConnect2Button\n")

    def on_clickConnect3Button(self):
        MavVars.ConnectTo = 3
        MavVars.vehSERPort = self.vehSERPort.toPlainText()
        MavVars.vehSERBaud = self.vehSERBaud.toPlainText()
        print("RecvdCommsWin::on_clickConnect3Button\n")

    def initUI(self, RecvdMsgsWin):
        #self.setGeometry(0,0,300,300)
        #self.layout = QFormLayout()
        self.layout = QGridLayout()  # grid.addWidget(widget,col,row)
        #self.setLayout(grid)
        #self.vbox = QVBoxLayout()  # Add box layout, add table to box layout and add box layout to widget
        # widgets in layout

        #self.textEdit = QTextEdit("empty")  #self.textEdit.setReadOnly(True)
        #self.textEditLabel = QLabel("empty")
        #self.textLastMsg = QTextEdit("empty")
        #self.textLastMsg.setMaximumHeight(30)
        #self.mainLayout.addWidget(self.textLastMsg)
        #self.textLastMsg.setText("empty") # since text object already exists from init = QTextEdit("TEST") #msg)

        #self.textLastMsg = QTextEdit("empty")
        #self.textLastMsg.setMaximumHeight(30)
        #self.mainLayout.addWidget(self.textLastMsg)
        #self.textLastMsg.setText("empty") # since text object already exists from init = QTextEdit("TEST") #msg)
        # radiobuttons
        #self.ConnectToLabel = QLabel('Label')
        self.ConnectTo1 = QRadioButton('Internal SITL')
        self.ConnectTo2 = QRadioButton('TCP SITL/Autopilot')
        self.ConnectTo3 = QRadioButton('USB or Serial Port ')
        #
        self.layout.addWidget(self.ConnectTo1,1,1)
        self.layout.addWidget(self.ConnectTo2,2,1) 
        self.layout.addWidget(self.ConnectTo3,3,1) 

        self.ConnectTo1.clicked.connect(self.on_clickConnect1Button)
        self.ConnectTo2.clicked.connect(self.on_clickConnect2Button)
        self.ConnectTo3.clicked.connect(self.on_clickConnect3Button)

        
        if   MavVars.ConnectTo == 1: 
            self.ConnectTo1.setChecked(True)
        elif MavVars.ConnectTo == 2: 
            self.ConnectTo2.setChecked(True)
        elif MavVars.ConnectTo == 3: 
            self.ConnectTo3.setChecked(True)

        # Label MavVars.vehIPAddr = "192.168.1.4"
        self.vehIPAddrLabel = QLabel("          vehIPAddr:")
        self.vehIPAddrLabel.setMaximumHeight(30)
        self.vehIPAddrLabel.setMaximumWidth(250)
        self.layout.addWidget(self.vehIPAddrLabel,3,1)  
        # TextEdit
        self.vehIPAddr = QTextEdit(MavVars.vehIPAddr)
        self.vehIPAddr.setMaximumHeight(30)
        self.vehIPAddr.setMaximumWidth(200)
        self.layout.addWidget(self.vehIPAddr,3,2) 
        self.ConnectTo3.clicked.connect(self.on_clickConnect3Button) # get vars

        # Label MavVars.vehIPport = "5760"
        self.vehIPportLabel = QLabel("          vehIPport:")
        self.vehIPportLabel.setMaximumHeight(30)
        self.vehIPAddrLabel.setMaximumWidth(250)
        self.layout.addWidget(self.vehIPportLabel,4,1)  
        # TextEdit
        self.vehIPport = QTextEdit(MavVars.vehIPport)
        self.vehIPport.setMaximumHeight(30)
        self.vehIPport.setMaximumWidth(250)
        self.layout.addWidget(self.vehIPport,4,2) #grid.addWidget(widget,col,row)
        self.ConnectTo2.clicked.connect(self.on_clickConnect2Button) # get vars
        #
        self.ConnectTo3 = QRadioButton('SerialPort Autopilot')
        self.layout.addWidget(self.ConnectTo3,5,1) 
        self.ConnectTo3.clicked.connect(self.on_clickConnect3Button)
        # Label MavVars.vehSERPort = "/dev/ttyACM0"
        self.vehSERPortLabel = QLabel("          vehSERPort:")
        self.vehSERPortLabel.setMaximumHeight(30)
        self.vehSERPortLabel.setMaximumWidth(250)
        self.layout.addWidget(self.vehSERPortLabel,6,1)  
        # TextEdit
        self.vehSERPort = QTextEdit(MavVars.vehSERPort)
        self.vehSERPort.setMaximumHeight(30)
        self.vehSERPort.setMaximumWidth(250)
        self.layout.addWidget(self.vehSERPort,6,2) 
        self.ConnectTo3.clicked.connect(self.on_clickConnect3Button) # get vars

        #Label MavVars.vehSERBaud = "115200"
        self.vehSERBaudLabel = QLabel("          vehSERBaud:")
        self.vehSERBaudLabel.setMaximumHeight(30)
        self.vehSERBaudLabel.setMaximumWidth(250)
        self.layout.addWidget(self.vehSERBaudLabel,7,1)  
        # TextEdit
        self.vehSERBaud = QTextEdit(MavVars.vehSERBaud)
        self.vehSERBaud.setMaximumHeight(30)
        self.vehSERBaud.setMaximumWidth(250)
        self.layout.addWidget(self.vehSERBaud,7,2)
        self.ConnectTo3.clicked.connect(self.on_clickConnect3Button) # get vars

        # add row to textEdit
        #self.flo.addRow(self.textEdit)  # msg is raw
        #self.textEdit.setText("empty") # since text object already exists from init = QTextEdit("TEST") #msg
   
        #self.layout.addWidget(self.textEdit)
        self.setLayout(self.layout)

        self.setGeometry(0, 0, 250, 250) # x , y , w , h
        self.setWindowTitle("RecvdCommsWin...")
        self.show() # show widgets just added

        #QMessageBox.information(self, "RecvdMsgsWin "+msgid+" -- "+MavVars.MAVmsgsToWatchDict[msgid] , " field enums "+MavVars.MAVLinkMsgFieldEnums[msgid]+"     str(MavVars.MAVLinkMsgFieldEnums[key].count('type') "+str(MavVars.MAVLinkMsgFieldEnums[msgid].count("type")) )

    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

    def displayMAVmsg(self, msg, msgid):  # msg is raw
        self.textEdit.setText(msg) # since text object already exists from init = QTextEdit("TEST") #msg)
        
        self.show()
        #print("RecvdMsgsWin:displayMAVmsg(msg) msg", msg, "\n") # mainWin.RecvdMsgsWin.displayMAVmsg(msg)

    def textchanged(self, text):
        print ("contents of text box: "+text)
    
    def enterPress(self):
        print ("edited")
        
    def onClicked(self):
        # printing button pressed
        print(" onClicked listbox button pressed")

    def onClicked(self, item):
        QMessageBox.information(self, "Info", item.text())

    def exitApp(self):
        # printing button pressed
        print(" exit button pressed")
        sys.exit(qApp.quit) 




class DisplayMsgMAVGenericEditor(QtWidgets.QWidget):
    dict_ = {'time_unix_usec' : '1662239279616000', 'time_boot_ms' : '347174300'}
    #print("#-#-#-#--class DisplayMsgMAVGenericEditor init dict_ ",dict_)    
    df = pd.DataFrame([dict_])
    #print(df)
    #
    def __init__(self, parent ): # parent = None
        QtWidgets.QWidget.__init__(self, parent) 
        self.setGeometry(0,0,600,600) 
        #self.resize(300, 300)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.mainLayout = QVBoxLayout()
        # added
        self.dict_ = {} # {'time_unix_usec' : '166223927961666666', 'time_boot_ms' : '3471743333'}
        print("#-#-#-#--class DisplayMsgMAVGenericEditor INIT self.dict_ ",self.dict_)    
        self.df = pd.DataFrame([self.dict_])
        print(" self.df ",self.df)
        #
        self.msg =""
        self.msgid =""
        self.button_print = QPushButton('Display DF')
        self.button_print.setStyleSheet('font-size: 20px')
        self.button_print.clicked.connect(self.print_DF_Values)
        self.mainLayout.addWidget(self.button_print)

        self.button_export = QPushButton('Export to CSV file')
        self.button_export.setStyleSheet('font-size: 20px')
        self.button_export.clicked.connect(self.export_to_csv)
        self.mainLayout.addWidget(self.button_export)    

        self.button_fields = QPushButton('Fields,vals-desc')
        self.button_fields.setStyleSheet('font-size: 20px')
        self.button_fields.clicked.connect(self.fieldsnames)
        self.mainLayout.addWidget(self.button_fields) 

        self.table = TableWidget(self.df) #TableWidget(DisplayMsgMAVGenericEditor.df)
        self.mainLayout.addWidget(self.table) 

        #self.flo = QFormLayout()
        #self.textLastMsg = QTextEdit("empty")  #self.textEdit.setReadOnly(True)
        #self.createTable()
        # Add box layout, add table to box layout and add box layout to widget
        #self.vbox = QVBoxLayout() #  #win = QWidget()
        #self.tableWidget = QTableWidget()
        #self.vbox.addWidget(self.tableWidget) 
        # add row to textEdit
        #self.flo.addRow(self.textEdit)  # msg is raw


        self.textLastMsg = QTextEdit("empty")
        #self.textLastMsgEmpty = True
        self.textLastMsg.setMaximumHeight(30)
        self.mainLayout.addWidget(self.textLastMsg)
        self.textLastMsg.setText("empty") # since text object already exists from init = QTextEdit("TEST") #msg)

        # orig
        #dict_ = {'time_unix_usec' : '1662239279616000', 'time_boot_ms' : '347174300'}
        #print("#-#-#-#--class DisplayMsgMAVGenericEditor INIT dict_ , df ",dict_, DisplayMsgMAVGenericEditor.df)    
        #df = pd.DataFrame([dict_])
        #print(" df ",df)
        #self.setWindowTitle("DisplayMsgMAVGenericEditor-Init") # works here
        #
        self.show()
        self.setLayout(self.mainLayout)
        #
        #print("#-#-#-#-INIT-END-DisplayMsgMAVGenericEditor: end init dict_, df , self.df", DisplayMsgMAVGenericEditor.dict_, DisplayMsgMAVGenericEditor.df, self.df) #, msg, "  ", msgid, "\n") 
        
    def print_DF_Values(self):
        print(self.table.df)
 


    def fieldsnames(self ):
        tmp = MavVars.MAVLinkMsgFieldEnums[self.msgid] #MavVars.MAVLinkMsgFieldEnums[msg[0]] #.replace(',','\n')
        txt = tmp.replace('},{','}\n{') #split(" ")
        flds= txt.split("}\n{")
        print("****DisplayMsgMAVGenericEditor().fieldsnames() self.df.columns:", self.df.columns)
        for field in flds:
           print("*****DisplayMsgMAVGenericEditor().fieldsnames() field:",field," in flds:",flds,"  self.dict_:",self.dict_,"  self.msg:",self.msg, " self.msgid:", self.msgid)
           if "enum" in field: 
               print("enum:",field)
               self.dict2_ = eval("{"+field+"}")
               print("dict2_[enum]=", self.dict2_['enum'] ) #, "  MavVars.MAVLinkEnumsDict=", MavVars.MAVLinkEnumsDict )
               print("dict2_[name]=", self.dict2_['name'] ) 
               fld =   " '" +  self.dict2_['enum']+"'" # has a space ate beginning, err in parsing but works= fld =   " '" +  self.dict_['enum']+"'"
               #
               tmp = MavVars.MAVLinkEnumsDict[fld] #MavVars.MAVLinkMsgFieldEnums[self.msgid] #MavVars.MAVLinkMsgFieldEnums[msg[0]] #.replace(',','\n')
               txt = tmp.replace(":'}", '}') 
               txta = txt.replace("{'{", '{{') 
               txtb = txta.replace("}:{", '},{') 
               txtc = txtb.replace("{{", '{') 
               txtd = txtc.replace("}}", '}')
               print(" txtd=", txtd)
               self.dict3_ = eval(txtd)  # dict3_ contains enums
               print(" enums dict from xml string self.dict3_:",self.dict3_)
               txt2 = self.msg.split(" ")
               print(" self.msg txt2[1:]=", self.msg,"   txt2[1:]=", txt2[1:],"   str(txt2[1:])=", str(txt2[1:]))
               txt3 = str(txt2[1:]).replace('[','')
               print(" self.msg txt3=", txt3)
               txt4 = txt3.replace(", ':',",':')
               txt5 = txt4.replace(']','')
               print(" self.msg txt5=", txt5)
               txt6 = txt5.replace(",'","'")
               print(" self.msg txt6=", txt6)
               self.dict4_ = eval("{"+txt6+"}") # "{"+self.msg+"}" )
               print(" msg dict4_ self.dict4_:",self.dict4_) 
               key   = self.dict2_['name']
               value = self.dict4_[self.dict2_['name']]
               print ( " field enum  key=",key,"  value=", value)
               print ( "   self.dict3_ ", self.dict3_ )
               print ( " self.dict3_[int(value)]=", self.dict3_[ int(value) ])
               #
               try:
                   MavVars.MAVLinkEnumsDict[fld]
                   #self.dict3_=eval(MavVars.MAVLinkEnumsDict[fld])  # create dictionary of enums
                   print(" Try: fld, MavVars.MAVLinkEnumsDict[ self.dict_['enum'] ] = ", fld," ", MavVars.MAVLinkEnumsDict[fld] , "  self.dict2_['name'] ]=", self.dict2_['name'] )
                   QMessageBox.information(self, "enum=self.dict3_[int(value)]="+ self.dict3_[ int(value) ])
                   QMessageBox.information(self, " DisplayMsgMAVGenericEditor().fieldnames() "+self.msgid+" -- "+MavVars.MAVmsgsToWatchDict[self.msgid] , " field enums: \n "+txt+"     str(MavVars.MAVLinkMsgFieldEnums[self.msgid].count('type') "+str(MavVars.MAVLinkMsgFieldEnums[self.msgid].count("type")) + " flds=" + str(flds) + " enums=" + MavVars.MAVLinkEnumsDict[fld] )
               except Exception:
                   fld =   " '" +  self.dict2_['enum']+"'" + ", 'bitmask': 'true'"
                   MavVars.MAVLinkEnumsDict[fld]
                   #self.dict3_=eval(MavVars.MAVLinkEnumsDict[fld]) # create dictionary of enums
                   print("enum=self.dict3_[int(value)]=", self.dict3_[ int(value) ],  " Exception fld, MavVars.MAVLinkEnumsDict[ fld ] = ", fld, MavVars.MAVLinkEnumsDict[fld] , "  self.dict2_['name'] ]=", self.dict2_['name'] )
                   QMessageBox.information(self, "enum=self.dict3_[int(value)]="+ self.dict3_[ int(value) ])
                   QMessageBox.information(self, "enum=self.dict3_[int(value)]="+ self.dict3_[ int(value) ]+" DisplayMsgMAVGenericEditor().fieldnames() "+self.msgid+" -- "+MavVars.MAVmsgsToWatchDict[self.msgid] , " field enums: \n "+txt+"     str(MavVars.MAVLinkMsgFieldEnums[self.msgid].count('type') "+str(MavVars.MAVLinkMsgFieldEnums[self.msgid].count("type")) + " flds=" + str(flds) + " enums=" + MavVars.MAVLinkEnumsDict[fld] )
        #MavVars.MAVLinkEnumsDict[fld]
        #"'"+self.dict_['enum']+"'" ] )  # self.dict_['enum'] 
        #self.enums_ = eval()
        #self.msg = str(msg)
        #self.msg = str(msg)
        #tmp = msgid #MavVars.MAVLinkMsgFieldEnums[msg[0]] #.replace(',','\n')
        #tmp2 = tmp.split(" ") # splits the id and the name of recvd msg msg[0] is first comma delimited value
        #self.msgid = tmp2[0]
        #tmp = msg #MavVars.MAVLinkMsgFieldEnums[msg[0]] #.replace(',','\n')
        #msg = tmp.split(" ") # splits the id and the name of recvd msg msg[0] is first comma delimited value
        ####key = msgid #msg[0] # type id number 0-253-99999
        #msg = msg[1:]
        #tmp = str(msg) #print("Before slice ",tmp," after ",msg," tmp ",tmp)
        #tmp3 = str(tmp).replace(", ':', ",":")
        #tmp4 = str(tmp3).replace("\n",'')
        #####print("DisplayMsgMAVGenericEditor.displayMAVmsg() str(MavVars.MAVLinkMsgFieldEnums[key].count('type') "+str(MavVars.MAVLinkMsgFieldEnums[msgid].count('type'))  )
        #tmp1 = tmp4.replace('[','')
        #tmp5 = "{"+tmp1.replace(']','')+"}"  # mav msg cleaned up
        #rint("tmp4=",tmp4)
        #tmp4 = tmp5.replace(",'","'")
        #self.dict_ = eval(tmp4) #tmp4 eval("{"+tmp4+"}")  mav msg converted to dict

    def export_to_csv(self):
        self.mainLayout = QVBoxLayout()
        self.table = TableWidget(DisplayMsgMAVGenericEditor.df)
        self.mainLayout.addWidget(self.table)

        self.button_print = QPushButton('Display DF')
        self.buttoFn_print.setStyleSheet('font-size: 30px')
        self.button_print.clicked.connect(self.print_DF_Values)
        self.mainLayout.addWidget(self.button_print)

        self.button_export = QPushButton('Export to CSV file')
        self.button_export.setStyleSheet('font-size: 30px')
        self.button_export.clicked.connect(self.export_to_csv)
        self.mainLayout.addWidget(self.button_export)     

        # MavVars.MavMsgsLastMsgRecvd[key] = date_time +"|"+str(MsgFieldsVals)

        #self.setWindowTitle("DisplayMsgMAVGenericEditor-Init")
        self.show()
        self.setLayout(self.mainLayout)
        self.table.df.to_csv('Data export.csv', index=False)
        print('CSV file exported.')

    def displayMAVmsg(self, msg, msgid):  # msg is raw
        #print("#####0 DisplayMsgMAVGenericEditor.msg.displayMAVmsg() start \n", msg, msgid) 
        self.msg = str(msg)
        tmp = msgid #MavVars.MAVLinkMsgFieldEnums[msg[0]] #.replace(',','\n')
        tmp2 = tmp.split(" ") # splits the id and the name of recvd msg msg[0] is first comma delimited value
        self.msgid = tmp2[0]
        tmp = msg #MavVars.MAVLinkMsgFieldEnums[msg[0]] #.replace(',','\n')
        msg = tmp.split(" ") # splits the id and the name of recvd msg msg[0] is first comma delimited value
        #key = msgid #msg[0] # type id number 0-253-99999
        msg = msg[1:]
        tmp = str(msg) #print("Before slice ",tmp," after ",msg," tmp ",tmp)
        tmp3 = str(tmp).replace(", ':', ",":")
        tmp4 = str(tmp3).replace("\n",'')
        #print("DisplayMsgMAVGenericEditor.displayMAVmsg() str(MavVars.MAVLinkMsgFieldEnums[key].count('type') "+str(MavVars.MAVLinkMsgFieldEnums[msgid].count('type'))  )
        tmp1 = tmp4.replace('[','')
        tmp5 = "{"+tmp1.replace(']','')+"}"  # mav msg cleaned up
        #rint("tmp4=",tmp4)
        tmp4 = tmp5.replace(",'","'")
        #print("tmp4=",tmp4)
        title = self.windowTitle()
        #print("#####1 DisplayMsgMAVGenericEditor.msg.displayMAVmsg()  msgid, title, tmp4", msgid , title, tmp4)
        if msgid == title:
            # delete table object and redraw
            self.table.deleteLater() #self.table.setParent(None)
            self.textLastMsg.deleteLater() #self.textLastMsg.setParent(None)
            #for i in reversed(range(layout.count())): 
            #    layout.itemAt(i).widget().setParent(None)
            # check if fileds can make a dict
            lst = tmp4.split(", ") #print(" lst=",lst)
            self.dict_ = {} # fill with only valid keys no malformed ones
            for field in lst:
                tmp = field.split(", ")
                #print ("tmp:",tmp)
                tmp2 = field.split(":") #print(" field, tmp, tmp2, tmp2[0], tmp2[1] =" ,field, " , ",tmp, " , ", tmp2, " , ", tmp2[0], " , ", tmp2[1], " |" )
                #print ("tmp2:",tmp2)
                if len(tmp2) > 1:
                    key =   tmp2[0]
                    if tmp2 : 
                        val =   tmp2[1].replace("{'","'") # remove {} 
                        value = val.replace("'}","'")
                        self.dict_[key]= value
                    else:
                        value=""
                    #print("trying to insert len(MAVmsgFieldsEntriesDict{} =",  str(len(MAVmsgFieldsEntriesDict) ), key, value )
                    #MAVmsgFieldsEntriesDict[key] = value
                else:
                    print("ERROR: line 676 tmp2 has no colon seperator malformed message")
                    break
            # create new df dataframe from dict_
            #self.dict_ = eval(tmp4) #tmp4 eval("{"+tmp4+"}")  mav msg converted to dict
            self.df = pd.DataFrame([self.dict_]) # class variable not instance var  convert dict to dataframe
            #print("#####2 DisplayMsgMAVGenericEditor.msg.displayMAVmsg() in if msgid == tmp[0]:  msgid, tmp[0] self.dict_ self.df ", msgid, tmp[0], self.dict_ , self.df)
            # create  a new tablet widget
            self.table = TableWidget(self.df)  # (DisplayMsgMAVGenericEditor.df)
            self.mainLayout.addWidget(self.table)
            #
            self.textLastMsg = QTextEdit("empty")
            self.textLastMsg.setMaximumHeight(30)
            self.mainLayout.addWidget(self.textLastMsg)
            self.textLastMsg.setText("empty") # since text object already exists from init = QTextEdit("TEST") #msg)
            #self.setWindowTitle("DisplayMsgMAVGenericEditor-Init")
        tmp = str(msgid) #MavVars.MAVLinkMsgFieldEnums[msg[0]] #.replace(',','\n')       
        msgID = tmp.split(" : ") # splits the id and the name of recvd msg msg[0] is first comma delimited value
        #print("++++++2 Msg DisplayMsgMAVGenericEditor.displayMAVmsg() ,msgid, msg , msgID[0], msgID[1] ", msgid, msg , msgID[0], msgID[1], MavVars.MavMsgsLastMsgRecvd)  
        if  (len(MavVars.MavMsgsLastMsgRecvd) != 0): 
            try:
                self.textLastMsg.setText( MavVars.MavMsgsLastMsgRecvd[msgID[0]]  ) # buffer dict oflast msg for each record type
            except Exception:
                pass
                print("++++++3 ignoring DisplayMsgMAVGenericEditor.displayMAVmsg() ERROR, exception override")
        
        if  (len(MavVars.MavMsgsLastMsgRecvd) != 0): 
            try:
                MavVars.MavMsgsLastMsgRecvd[msgID[0]]  
                tmp = str(msgid) #MavVars.MAVLinkMsgFieldEnums[msg[0]] #.replace(',','\n')       
                msgID = tmp.split(" : ")
                tmp = str(MavVars.MavMsgsLastMsgRecvd[msgID[0]]  )
                #
                timeOld = tmp.split("|") # splits the id and the name of recvd msg
                #print("@@@@ RecvdMsgsWin.displayMAVmsg() msgid ", msgid,"  ", "  msg ", msg," timeOld[0]  ", timeOld[0] ) 
                now = datetime.now() 
                date_time = now.strftime("%m/%d/%Y, %H:%M:%S.%f")[:-3] # str(now)
                #print("++++++4 RecvdMsgsWin.displayMAVmsg() msgid=", msgid,"  ", "  msgID[0]=", msgID[0] ,"  msg=", msg, "  timeOld[0]=", timeOld[0] , "  date_time=", date_time ) 
                #'Sun Sep 16 16:05:15 +0000 2012'
                diff = datetime.strptime(date_time,'%m/%d/%Y, %H:%M:%S.%f')  - datetime.strptime(timeOld[0], '%m/%d/%Y, %H:%M:%S.%f')      
                self.textLastMsg.setText("Prev Msg: "+str(diff)+" secs") #self.textEdit.setText( diff )
            except Exception:
                pass
                print("++++++4 ignoring DisplayMsgMAVGenericEditor.displayMAVmsg() ERROR, exception ignored  msgID[0]=", msgID[0], "  MavVars.MavMsgsLastMsgRecvd dict=", MavVars.MavMsgsLastMsgRecvd  )
            
            #'%a %b %d %H:%M:%S +0000 %Y'
            #
            #'09/16/2022, 15:55:15.445'
            #'%b %d %Y, %H:%M:%S +0000 %Y'
            
        #
        self.show()
        #print("#####3 END-DisplayMsgMAVGenericEditor.displayMAVmsg(msg, msgid) tmp4  msgid self.df ", tmp4, "  ", msgid, self.df, self.dict_, "\n") # mainWin.RecvdMsgsWin.displayMAVmsg(msg)



class UI(QMainWindow):  # mainWin
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  
        self.initUI()   

    def displayMAVmsg(self, msg, msgid):  # msg is raw
        print("#-#-#-# UI.displayMAVmsg start  msg  msgid\n", msg, msgid) 
        tmp = msg #MavVars.MAVLinkMsgFieldEnums[msg[0]] #.replace(',','\n')
        msg = tmp.split(" ") # splits the id and the name of recvd msg msg[0] is first comma delimited value
        msg = msg[1:]
        tmp = str(msg)
        print("Before slice ",tmp," after ",msg," tmp ",tmp)
        tmp3 = str(tmp).replace(", ':', ",":")
        tmp4 = str(tmp3).replace("\n",'')
        #print("DisplayMsgMAVGenericEditor.displayMAVmsg() str(MavVars.MAVLinkMsgFieldEnums[key].count('type') "+str(MavVars.MAVLinkMsgFieldEnums[msgid].count('type'))  )
        tmp1 = tmp4.replace('[','')
        tmp4 = "{"+tmp1.replace(']','')+"}"
        dict_ = eval("{"+tmp1.replace(']','')+"}") # dict_ needs eval
        print( "#-#-#-# main.UI.displayMAVmsg--- MATCH ID MAVMsgFieldsVals " , msg )  # matchpacket " , matchpacket,  
        for key in MavVars.MAVmsgsToWatchDict:    
            title = key+" : "+MavVars.MAVmsgsToWatchDict[key]
            print("=====2 main.UI.displayMAVmsg-RefreshToplevelMsgWin()... key  title " , key,"  ",title)
            print("=====3 main.UI.displayMAVmsg-RefreshToplevelMsgWin() send msg to title if match == MatchSelectedMsgs():self.mdiArea.subWindowList()= ", self.mdiArea.subWindowList() )  
            windows = self.mdiArea.subWindowList() ## list all windows in mdiArea
            for i, window  in enumerate(windows):
                 title = window.windowTitle()
                 tmp = title.split(" : ")  # tmp is now a list
                 #print(" tmp ", tmp, "  len(tmp)", len(tmp))
                 # key (tmp[0])   # key 
                 # msg name tmp[1]  # value
                 print("=====4 main.UI.displayMAVmsg-RefreshToplevelMsgWin(): windows-- i addr key name windowAddr", i,  title, window )
                 if (len(tmp) >= 2) and (tmp[1] == MavVars.MAVmsgsToWatchDict[key]): 
                     print("=+=+=+=5 main.UI.displayMAVmsg-REFRESH window title MavVars.MAVmsgsToWatchDict[key]   ", tmp[0], tmp[1], "==", MavVars.MAVmsgsToWatchDict[key]," window= ", window, " title= ", window.windowTitle())
                     # send message to this wondow # mainWin.RecvdMsgsWin.displayMAVmsg(msg)
                     # window.displayMAVmsg(MsgFieldsVals, key)
        print("#-#-#-#=7 END-main.UI:displayMAVmsg(msg, msgid) tmp4  msgid ", tmp4, "  ", msgid, " dict_ ", dict_ , "\n") # mainWin.RecvdMsgsWin.displayMAVmsg(msg)

       
    def updateActiveChild(self, subWindow):  # when you click on window
        print("* window activated UI::updateActiveChild() ") #, self.subWindow.windowTitle()) # subWindow.windowTitle() ", self.subWindow.windowTitle())
        #self.setWindowTitle("MDI Test: ")        
        #print("@@@@@@@ root::updateActiveChild()" subWindow.windowTitle() ) #, self.subWindow.windowTitle())
        #self.setWindowTitle("MDI Test: '%s'" % subWindow.windowTitle())
        #winSuper.setWindowTitle("MDI Test: ") # '%s'" % str(subWindow.windowTitle())) 
        #
        #def updateActiveChild(subWindow):
        #    win.setWindowTitle("MDI Test: '%s'" % subWindow.windowTitle())
        #updateActiveChild(mdiArea.activeSubWindow()) 
        # make active selected window mdiArea.subWindowActivated.connect(updateActiveChild)

    def windowaction(self, q):
        print ("menu action triggered")

    def addMAVmsgGenericSubWindow(self, title):  # mav message window for each id self.title is class instance
        # Add Messages window--- mainWin.RecvdMsgsWin.displayMAVmsg(msg) send mav msg to display
        #
        self.mdiChild = DisplayMsgMAVGenericEditor(self) # create class instance
        MavVars.MavMsgsRcvingClasses[title] = self.mdiChild # dict #MavVars.MavMsgsRcvingClasses.append(self.title) i flist
        print("#-#-#-# UI.addMAVmsgGenericSubWindow MavVars.MavMsgsRcvingClasses=", MavVars.MavMsgsRcvingClasses)
        #self.DisplayMsgMAVGenericEditor = DisplayMsgMAVGenericEditor(self) # create class instance
        # add subwindow
        self.mdiArea.addSubWindow(self.mdiChild)
        self.mdiChild.setGeometry(0,0,300,300)
        self.mdiChild.setWindowTitle(title) # 
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.mdiChild.setStyleSheet("background-color: linen")  # https://www.w3.org/TR/SVG11/types.html#ColorKeywords
        self.mdiChild.show()
        #MavVars.MavMsgsRcvingClasses[title]
        print("#_#_#_#_Created UI->addMAVmsgGenericSubWindow() title self.title=", title, self.mdiChild, MavVars.MavMsgsRcvingClasses[title], MavVars.MavMsgsRcvingClasses )
        self.show()
        #self.mdiArea.tileSubWindows() # force layout to tiled windows
 
        #windows = self.mdiArea.subWindowList() ## list all windows in mdiArea
        #for i, window  in enumerate(windows):
        #    print(" UI class addMAVmsgGenericSubWindow mdiArea window i addr ", i,  window, window.windowTitle()) #window.activateWindow() #time.sleep(1000)

    def addSubWindow(self, title):  # (self, QMdiArea, title):
        self.mdiChild = QMdiSubWindow()
        self.mdiChild.setWindowTitle(title)
        self.mdiArea.addSubWindow(self.mdiChild)
        #self.setFixedSize(self.mdiArea.sizeHint())
        self.mdiChild.setGeometry(0, 0, 600, 600) # x , y , w , h
        self.mdiChild.show()
        self.show()
        #self.mdiArea.tileSubWindows() # tiled windows
        print("UI->addSubWindow() Created ",title," new subWindow widget inside UI msg window...")

    def initUI(self):    
        self.setGeometry(300,300,1900,1200)  # main parent window 
        #  actions for File Menu Arrange windows or quit    
        self.exitAction = QAction('&Exit', self)        
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(qApp.quit)

        self.cascadeAction = QAction('&Cascade', self)        
        self.cascadeAction.setShortcut('Ctrl+S')
        self.cascadeAction.setStatusTip('Arrange CascadeWindows')
        self.cascadeAction.triggered.connect(self.cascade) 

        self.tiledAction = QAction('&Tiled', self)        
        self.tiledAction.setShortcut('Ctrl+T')
        self.tiledAction.setStatusTip('Arrange TiledWindows')
        self.tiledAction.triggered.connect(self.tiled) 

        self.tabbedAction = QAction('&Tabbed', self)        
        self.tabbedAction.setShortcut('Ctrl+T')
        self.tabbedAction.setStatusTip('Arrange TabbedWindows')
        self.tabbedAction.triggered.connect(self.tabbed) 

        # # File menu
        menubar = self.menuBar()
        self.fileMenu = menubar.addMenu('&File')
        self.fileMenu.addAction(self.cascadeAction)
        self.fileMenu.addAction(self.tiledAction)
        self.fileMenu.addAction(self.tabbedAction)
        self.fileMenu.addAction(self.exitAction)   

        # main window title
        print("MavVars.title ", MavVars.title)
        self.setWindowTitle(str(MavVars.title))  # .title = .version + .verdate  #self.setWindowTitle('PyQt5 Basic Menubar Inited')   
 
        self.mdiArea = QMdiArea() # create win to make multiple windows
        self.mdiArea.WindowOrder(QMdiArea.CreationOrder) #QMdiArea.StackingOrder  #setViewMode()
        #self.mdiArea.tileSubWindows() # tiled windows
        print(" self.mdiArea.subWindowList() start_init", self.mdiArea.subWindowList() )   

        # create windows using titles  #    mainWin.addSubWindow(title) # create subwindow
        #for title in ["Info Test"]:  #, "Data:2", "Data:3", "Data:4"]:
            #self.addSubWindow(title) #self.mdiChild = QMdiSubWindow() #self.mdiChild.setWindowTitle(title) #self.mdiArea.addSubWindow(self.mdiChild)
        #for title in ["Comms-SITL", "Params", "MissionWP" ]:  #, "Data:7", "Data:8", "Data:9", "Data:10", "Data:11"]:  

        #
        # Add ClockWindow -------------------------------------------------------
        self.ClockWin = mavlink_win_clock_class.MavLinkWinClock(self)
        mavlink_win_clock_class.viewLCDClock.Ui_Form()
        self.mdiArea.addSubWindow(self.ClockWin)     
        
        # Add RecvdCommsWin window ------------------------------------------------------- mainWin.RecvdMsgsWin.displayMAVmsg(msg) send mav msg to display
        self.RecvdCommsWin = RecvdCommsWin(self)
        self.mdiArea.addSubWindow(self.RecvdCommsWin)
        self.RecvdCommsWin.setGeometry(300,300,250,250)
        self.RecvdCommsWin.setWindowTitle("Comms Settings Window")
        #self.RecvdCommsWin.setStyleSheet("background-color: azure")  # https://www.w3.org/TR/SVG11/types.html#ColorKeywords
        self.RecvdCommsWin.setAutoFillBackground(True)
        #self.RecvdCommsWin.setStyleSheet("background-color: azure")  # https://www.w3.org/TR/SVG11/types.html#ColorKeywords
        self.RecvdCommsWin.setStyleSheet("background-color: lightgreen")
        # main widget self.setStyleSheet("background-color: azure")  # https://www.w3.org/TR/SVG11/types.html#ColorKeywords


        # Add ControlWin -------------------------------------------------------
        self.ControlWin = ControlWin(self)
        self.mdiArea.addSubWindow(self.ControlWin)
        #self.ControlWin.setGeometry(0,0,1250,1250)
        self.ControlWin.setWindowTitle("ControlWin UI.InitUI()")
        self.ControlWin.setAutoFillBackground(True)
        self.ControlWin.setStyleSheet("background-color: wheat")  # https://www.w3.org/TR/SVG11/types.html#ColorKeywords
        
        # Add ControlPanelWin -------------------------------------------------------
        self.ControlPanelWin = ControlPanelWin(self)
        self.mdiArea.addSubWindow(self.ControlPanelWin)
        #self.ControlPanelWin.setGeometry(0,0,1250,1250)
        self.ControlPanelWin.setWindowTitle("ControlPanelWin UI.InitUI()")
        self.ControlPanelWin.setAutoFillBackground(True)
        self.ControlPanelWin.setStyleSheet("background-color: wheat")  # https://www.w3.org/TR/SVG11/types.html#ColorKeywords
        
        
        #
        '''# Add ReceivedMesages win ------------------------------------------------------- mainWin.RecvdMsgsWin.displayMAVmsg(msg) send mav msg to display
               self.RecvdMsgsWin = RecvdMsgsWin(self)
               self.mdiArea.addSubWindow(self.RecvdMsgsWin)
               #self.RecvdMsgsWin.setGeometry(300,300,250,250)
               self.RecvdMsgsWin.setWindowTitle("RecvdMsgsWin Dispatcher UI.InitUI()")'''
        #     gedit



        '''# Add ReceivedMesages win ------------------------------------------------------- mainWin.RecvdMsgsWin.displayMAVmsg(msg) send mav msg to display
        self.RecvdMsgsWin = RecvdMsgsWin(self)
        self.mdiArea.addSubWindow(self.RecvdMsgsWin)
        #self.RecvdMsgsWin.setGeometry(300,300,250,250)
        self.RecvdMsgsWin.setWindowTitle("RecvdMsgsWin Dispatcher UI.InitUI()")'''
        #      

        #
        #### arrange subwindows in Mdi Area #### default is tiled for now 
        print("UI**begin init MavVars.DefaultWinLayout=",MavVars.DefaultWinLayout)
        if   MavVars.DefaultWinLayout == "Tiled":
            self.tiled()
            print("UI init MavVars.DefaultWinLayout=",MavVars.DefaultWinLayout)
        elif MavVars.DefaultWinLayout == "Cascade":
            self.cascade()
            print("UI init MavVars.DefaultWinLayout=",MavVars.DefaultWinLayout)
        elif MavVars.DefaultWinLayout == "Tabbed":
            self.tabbed()
            print("UI init MavVars.DefaultWinLayout=",MavVars.DefaultWinLayout)
        #self.mdiArea.setViewMode(1)       # only for tabbed windows (0) for tiled and cascade
        #self.mdiArea.tileSubWindows() # tiled windows
        #
        # use local func # install local signal handlers
        self.mdiArea.subWindowActivated.connect(self.updateActiveChild) 
        self.updateActiveChild(self.mdiArea.activeSubWindow())
        #
        # use glob func # install local signal handlers
        #self.mdiArea.subWindowActivated.connect(self.parent.updateActiveChild)
        #updateActiveChild(self.mdiArea.activeSubWindow())
        
        print(" self.mdiArea.subWindowList() end_init", self.mdiArea.subWindowList() )  
        windows = self.mdiArea.subWindowList() ## list all windows in mdiArea
        for i, window  in enumerate(windows):
            print("  window i addr ", i,  window)
            #window.activateWindow()
            #time.sleep(1000)
        #    
        #
        self.setCentralWidget(self.mdiArea) # must be set or no mdi area
        self.mdiArea.setActivationOrder(QMdiArea.StackingOrder) #CreationOrder) #ActivationHistoryOrder) #StackingOrder) #  StackingOrder keeps control win in center #   self.mdiArea.setActivationOrder(QMdiArea.CreationOrder)
        self.show()

    def cascade(self):
        self.mdiArea.setViewMode(0)       # tabbed windows
        self.mdiArea.cascadeSubWindows()
        self.setCentralWidget(self.mdiArea)
        self.show()
        MavVars.DefaultWinLayout = "Cascade"
        print("Arrange Cascade windows from File menu ", MavVars.DefaultWinLayout)
      
    def tiled(self):
        self.mdiArea.setViewMode(0)       # tabbed windows
        self.mdiArea.tileSubWindows()
        self.setCentralWidget(self.mdiArea)
        self.show()
        MavVars.DefaultWinLayout = "Tiled"
        print("Arrange Tiled windows from File menu ",MavVars.DefaultWinLayout)

    def tabbed(self):
        self.mdiArea.setViewMode(1)       # tabbed windows
        self.setCentralWidget(self.mdiArea)
        self.show()
        MavVars.DefaultWinLayout = "Tabbed"
        print("Arrange Tabbed from File menu ",MavVars.DefaultWinLayout)

    # action method clickme
    def clickme(self):
        # printing button pressed
        print("button pressed")

    # action method clickme
    def exit(self):
        # printing button pressed
        print("exit button pressed")


class MavLinkClock(QtWidgets.QWidget):
    #def __init__(self):
    #    pass
    def setupUi(self):
        #self.ClockWin = mavlink_win_clock_class.viewLCDClock.Ui_Form()
        pass

class OutMsgsWin(QtWidgets.QWidget):
    def __init__(self, parent ): # parent = None
        QtWidgets.QWidget.__init__(self, parent)
        self.initUI(self)  
    def initUI(self, OutMsgsWin):
        self.setGeometry(300,300,250,250)
        self.setWindowTitle("OutMsgs")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    c = UI() #MavLinkWin()
    c.show()
    sys.exit(app.exec_())

'''
class RecvdMsgsWin(QtWidgets.QWidget):
    msg_txt = ""
    cursor = None
    def __init__(self, parent ): # parent = None
        QtWidgets.QWidget.__init__(self, parent)
        self.initUI(self)  

    def initUI(self, RecvdMsgsWin):
        self.setGeometry(0,0,300,300)
        self.flo = QFormLayout()
        self.vbox = QVBoxLayout() #  #win = QWidget()
        #   
        self.textEdit = QTextEdit("empty")  #self.textEdit.setReadOnly(True)
        self.textEdit.setText("empty") # since text object already exists from init = QTextEdit("TEST") #msg)
        #
        self.process = QTextEdit(self, readOnly=True)
        self.process.setText("process-empty") # since text object already exists from init = QTextEdit("TEST") #msg)
        self.process.ensureCursorVisible()
        self.process.setLineWrapColumnOrWidth(300)
        self.process.setLineWrapMode(QTextEdit.FixedPixelWidth)
        #self.process = QTextEdit(self, readOnly=True)
        #self.process.ensureCursorVisible()
        #
        #self.cursor = self.textCursor()
        #self.createTable()
        # Add box layout, add table to box layout and add box layout to widget
        
        #self.tableWidget = QTableWidget()
        #self.vbox.addWidget(self.tableWidget) 
        # add row to textEdit
        
        self.vbox.addWidget(self.textEdit)
        self.vbox.addWidget(self.process)
        #
        self.flo.addRow(self.textEdit)  # layout add row
        self.flo.addRow(self.process)  # layout add row
        #
        self.cursor = self.process.textCursor()
        #.moveCursor(QTextCursor.End)
        #
        self.setWindowTitle("mav msgs...")
        ##cursor = self.process.textCursor()
        #
        
        #
        self.show()
        #QMessageBox.information(self, "RecvdMsgsWin "+msgid+" -- "+MavVars.MAVmsgsToWatchDict[msgid] , " field enums "+MavVars.MAVLinkMsgFieldEnums[msgid]+"     str(MavVars.MAVLinkMsgFieldEnums[key].count('type') "+str(MavVars.MAVLinkMsgFieldEnums[msgid].count("type")) )
        self.vbox.addWidget(self.textEdit)
        self.setLayout(self.vbox)
        self.setGeometry(0, 0, 600, 600) # x , y , w , h
        self.show() # show widget

    #@pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

    def displayMAVmsg(self, msg, msgid):  # msg is raw
        #

        RecvdMsgsWin.msg_txt = RecvdMsgsWin.msg_txt + "\n" + msg
        # timestamp value in dict MavVars.MavMsgsLastMsgRecvd[msgid]
        self.process.setText(RecvdMsgsWin.msg_txt) # since text object already exists from init = QTextEdit("TEST") #msg)
        tmp = msg 
        msgID = tmp.split(" ") # splits the id and the name of recvd msg
        #print("@@@@ RecvdMsgsWin.displayMAVmsg() msgid,"  ", msg, "  ",msgID[0],"  ", msgID[1],"  ", RecvdMsgsWin.msg_txt ", msgid, msg, msgID[0], msgID[1]) 
        try:
            self.textEdit.setText( MavVars.MavMsgsLastMsgRecvd[ msgid] )
        except Exception:
            pass
            print("ignoring RecvdMsgsWin.displayMAVmsg() exception msgID[0]=", msgID[0])
        #self.process.setText(MavVars.MavMsgsLastMsgRecvd[msgid]) 
        #self.process.movePosition(QTextCursor.End)
        if isinstance(RecvdMsgsWin.msg_txt, bytes):
            RecvdMsgsWin.msg_txt = text.decode()
        self.process.setText(RecvdMsgsWin.msg_txt)   #self.process.insertText(RecvdMsgsWin.msg_txt)
        #self.process.setTextCursor(self.cursor.End)
        self.process.moveCursor(QTextCursor.End)
        #self.process.movePosition(QTextCursor.End)
        #self.textEdit.setTextCursor(QTextCursor.End)
        #self.process.ensureCursorVisible() 
        #self.process.moveCursor(QTextCursor.End)
        #
        #print("RecvdMsgsWin:: self.textEdit.setText(msg) ", msg)
        tmp = msg 
        msg = tmp.split(" ") # splits the id and the name of recvd msg
        tmp1 = tmp.replace('{','')
        tmp2 = tmp1.replace('}','')
        tmp3 = str(tmp2).replace(',','\n')
        txt = tmp + " MavVars.MAVLinkMsgFieldEnums " + tmp3
        #print("RecvdMsgsWin():: "+"  str(MavVars.MAVLinkMsgFieldEnums[key].count('type') "+str(MavVars.MAVLinkMsgFieldEnums[msgid].count('type'))  )
        cols = MavVars.MAVLinkMsgFieldEnums[msgid].count('type')
        #
        #
        #self.table = QtWidgets.QTableWidget(0, cols) # rows, cols
        #self.table.clear()
        # insert row to read data
        #self.table.insertRow( self.table.rowCount() );
        #QMessageBox.information(self, "RecvdMsgsWin"+key+" -- "+MavVars.MAVmsgsToWatchDict[key] ,txt)  # title=key+" -- "+MavVars.MAVmsgsToWatchDict[key]
        #QMessageBox.information(self, "RecvdMsgsWin "+msgid+" -- "+MavVars.MAVmsgsToWatchDict[msgid] , " field enums "+MavVars.MAVLinkMsgFieldEnums[msgid]+"     str(MavVars.MAVLinkMsgFieldEnums[key].count('type') "+str(MavVars.MAVLinkMsgFieldEnumself.table.deleteLater()s[msgid].count("type")) )
        #QMessageBox.information(self,"RecvdMsgsWin "+"  str(MavVars.MAVLinkMsgFieldEnums[key].count('type') ", str(MavVars.MAVLinkMsgFieldEnums[key].count("type")) )
        #self.setWindowTitle(msg[0])
        self.show()
        #print("RecvdMsgsWin:displayMAVmsg(msg) msg", msg, "\n") # mainWin.RecvdMsgsWin.displayMAVmsg(msg)

'''



