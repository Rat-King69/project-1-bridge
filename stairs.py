from PySide6 import QtWidgets, QtCore, QtGui
import MASH.api as mapi
import maya.cmds as cmds



#get window working with connections later
class StairsWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stairs")
        self.setMinimumSize(500, 300)

        layout = QtWidgets.QVBoxLayout(self)

        self.create_button = QtWidgets.QPushButton("Create")
        self.create_button.clicked.connect(self.create_mash_network)
        
        self.line_edit = QtWidgets.QLabel()
        self.line_edit = QtWidgets.QLineEdit("enter a number here number of objects")
        self.update_button = QtWidgets.QPushButton("update")
        self.update_button.clicked.connect(self.update_Number_obj)
        
        layout.addWidget(self.create_button)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.update_button)
        layout.addStretch()

        #creation of mash based on selection 
    def create_mash_network(self, name="Stairs"):
        #Create a MASH network from the currently selected object.
        self.network = mapi.Network()
        self.network.createNetwork(name="Stairs")

            #maybe cange to linear to radial selection must rotate selected object for radial


            #input of number of points
    def update_Number_obj(self):
        #update number of points
        count = int(self.line_edit.text())
        cmds.setAttr(self.network.distribute + ".pointCount", count)






            #distance modifier for x and y

            #scale input

            #rotate input


            #offset of z





win = StairsWindow()
win.show()


