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
        
        self.obj_edit = QtWidgets.QLabel()
        self.obj_edit = QtWidgets.QLineEdit("enter a number here of objects")
        self.update_obj = QtWidgets.QPushButton("update")
        self.update_obj.clicked.connect(self.update_Number_obj)

        self.dis_edit_x = QtWidgets.QLabel()
        self.dis_edit_x = QtWidgets.QLineEdit("enter a number here for x offset")
        self.dis_edit_y = QtWidgets.QLabel()
        self.dis_edit_y = QtWidgets.QLineEdit("enter a number here for y offset")
        self.update_dis_x = QtWidgets.QPushButton("update_x")
        self.update_dis_x.clicked.connect(self.update_distance_x)

        self.update_dis_y = QtWidgets.QPushButton("update_y")
        self.update_dis_y.clicked.connect(self.update_distance_y)

        self.dis_edit_z = QtWidgets.QLabel()
        self.dis_edit_z = QtWidgets.QLineEdit("enter a number here for z offset")

        self.update_dis_z = QtWidgets.QPushButton("update_z")
        self.update_dis_z.clicked.connect(self.update_offset_z)

        self.rot_edit_y = QtWidgets.QLabel()
        self.rot_edit_y = QtWidgets.QLineEdit("enter a number here for y rotate")

        self.update_rot_y = QtWidgets.QPushButton("update_y")
        self.update_rot_y.clicked.connect(self.update_rotate_y)

        
        layout.addWidget(self.create_button)
        layout.addWidget(self.obj_edit)
        layout.addWidget(self.update_obj)
        layout.addWidget(self.dis_edit_x)
        layout.addWidget(self.dis_edit_y)
        layout.addWidget(self.update_dis_x)
        layout.addWidget(self.update_dis_y)
        layout.addWidget(self.dis_edit_z)
        layout.addWidget(self.update_dis_z)
        layout.addWidget(self.rot_edit_y)
        layout.addWidget(self.update_rot_y)
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
        pnt_count = int(self.obj_edit.text())
        cmds.setAttr(self.network.distribute + ".pointCount", pnt_count)


            #distance modifier for x and y
    def update_distance_x(self):
        dis_count_x = int(self.dis_edit_x.text())
        cmds.setAttr(self.network.distribute + ".amplitudeX", dis_count_x)


    def update_distance_y(self):
        dis_count_y = int(self.dis_edit_y.text())
        cmds.setAttr(self.network.distribute + ".amplitudeY", dis_count_y)


            #scale input

            #offset of z
    def update_offset_z(self):
        dis_count_z = int(self.dis_edit_z.text())
        cmds.setAttr(self.network.distribute + ".amplitudeZ", dis_count_z)


            #rotate input
    def update_rotate_y(self):
        rot_rotate_y = int(self.rot_edit_y.text())
        cmds.setAttr(self.network.distribute + ".rotateY", rot_rotate_y)


        




win = StairsWindow()
win.show()


