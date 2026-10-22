from PySide2 import QtWidgets, QtCore
import MASH.api as mapi
import maya.cmds as cmds



#get window working with connections later
class StairsWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stairs")
        self.setMinimumSize(500, 300)

        layout = contorl_widget.layout()

        self.button = QtWidgets.QPushButton('create', self)
        self.button.clicked.connect(self.create_mash_network)

        #creation of mash based on selection 
    def create_mash_network(self, name="Stairs"):
        #Create a MASH network from the currently selected object.
        sel = cmds.ls(selection=True)

        network = mapi.Network()
        network.createNetwork(name=name)
        return network

#maybe cange to linear to radial selection must rotate selected object for radial


#input of number of points
    def update_Number_obj

#distance modifier for x and y

#scale input

#rotate input


#offset of z





win = StairsWindow()
win.show()


