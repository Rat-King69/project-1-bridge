from PySide6 import QtWidgets, QtCore, QtGui
from shiboken6 import wrapInstance
import maya.OpenMayaUI as omui
import MASH.api as mapi
import maya.cmds as cmds


#get window working with connections later
class StairsWindow(QtWidgets.QWidget):
    def __init__(self):

        main_window = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
        super().__init__(main_window)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle("Stairs")
        self.setMinimumSize(500, 300)

        # all networks made in this window, by name
        self.networks = {}

        layout = QtWidgets.QVBoxLayout(self)

        self.create_button = QtWidgets.QPushButton("Create Linear")
        self.create_button.clicked.connect(self.create_mash_network)

        self.create_spiral_button = QtWidgets.QPushButton("Create Spiral")
        self.create_spiral_button.clicked.connect(self.create_spiral_network)

        # choose which network(s) the update buttons affect
        self.network_box = QtWidgets.QComboBox()
        self.network_box.addItem("All")

        # regular buttons that flip the visibility of the left and right banisters
        self.toggle_l = QtWidgets.QPushButton("L")
        self.toggle_l.clicked.connect(lambda checked=False: self.toggle_banister("L"))

        self.toggle_r = QtWidgets.QPushButton("R")
        self.toggle_r.clicked.connect(lambda checked=False: self.toggle_banister("R"))
        
        self.obj_edit = QtWidgets.QLabel()
        self.obj_edit = QtWidgets.QLineEdit("enter a number here of objects")
        self.update_obj = QtWidgets.QPushButton("update")
        self.update_obj.clicked.connect(self.update_Number_obj)

        self.dis_edit_x = QtWidgets.QLabel()
        self.dis_edit_x = QtWidgets.QLineEdit("enter a number here for x offset")
        self.dis_edit_y = QtWidgets.QLabel()
        self.dis_edit_y = QtWidgets.QLineEdit("enter a number here for y offset")
        self.update_dis = QtWidgets.QPushButton("update_offset")
        self.update_dis.clicked.connect(self.update_distance)

        self.dis_edit_z = QtWidgets.QLabel()
        self.dis_edit_z = QtWidgets.QLineEdit("enter a number here for z offset")

        self.update_dis_z = QtWidgets.QPushButton("update_z")
        self.update_dis_z.clicked.connect(self.update_offset_z)

        self.rot_edit_y = QtWidgets.QLabel()
        self.rot_edit_y = QtWidgets.QLineEdit("enter a number here for y rotate")

        self.update_rot_y = QtWidgets.QPushButton("update_rot_y")
        self.update_rot_y.clicked.connect(self.update_rotate_y)

        # create buttons share one row
        create_row = QtWidgets.QHBoxLayout()
        create_row.addWidget(self.create_button)
        create_row.addWidget(self.create_spiral_button)

        # x and y offset fields share one row
        dis_row = QtWidgets.QHBoxLayout()
        dis_row.addWidget(self.dis_edit_x)
        dis_row.addWidget(self.dis_edit_y)

        # L and R buttons share one row
        toggle_row = QtWidgets.QHBoxLayout()
        toggle_row.addWidget(self.toggle_l)
        toggle_row.addWidget(self.toggle_r)

        layout.addLayout(create_row)
        layout.addWidget(self.network_box)
        layout.addLayout(toggle_row)
        layout.addWidget(self.obj_edit)
        layout.addWidget(self.update_obj)
        layout.addLayout(dis_row)
        layout.addWidget(self.update_dis)
        layout.addWidget(self.dis_edit_z)
        layout.addWidget(self.update_dis_z)
        layout.addWidget(self.rot_edit_y)
        layout.addWidget(self.update_rot_y)
        layout.addStretch()

        #creation of a linear mash network, one per selected object
    def create_mash_network(self):
        selection = cmds.ls(selection=True)
        if not selection:
            cmds.warning("Select an object first.")
            return

        for obj in selection:
            # skip MASH networks that are already selected
            if cmds.nodeType(obj) == "MASH_Waiter":
                continue

            # short name of the object (drops any |group|path)
            name = obj.split("|")[-1]

            # createNetwork uses the current selection, so select just this object
            cmds.select(obj, replace=True)

            network = mapi.Network()
            network.createNetwork(name=name)

            self.networks[name] = network
            self.network_box.addItem(name)

        # put the selection back how it was
        cmds.select(selection, replace=True)

        #creation of a mash network set to radial with the radial axis on zx
    def create_spiral_network(self):
        selection = cmds.ls(selection=True)
        if not selection:
            cmds.warning("Select an object first.")
            return

        for obj in selection:
            # skip MASH networks that are already selected
            if cmds.nodeType(obj) == "MASH_Waiter":
                continue

            name = obj.split("|")[-1]

            # rotate the object 90 in x before it goes into the radial network
            cmds.rotate(90, 0, 0, obj, relative=True)

            cmds.select(obj, replace=True)

            network = mapi.Network()
            network.createNetwork(name=name)

            self.networks[name] = network
            self.network_box.addItem(name)

            # distribution type: 1 = linear, 2 = radial
            cmds.setAttr(network.distribute + ".arrangement", 2)

            # radial axis: 3 = zx
            cmds.setAttr(network.distribute + ".modelAxis", 3)

        cmds.select(selection, replace=True)

    def toggle_banister(self, side):
        # flip the visibility of the banister_L / banister_R ReproMesh objects
        for mesh in cmds.ls("banister_" + side + "*_ReproMesh", type="transform"):
            is_visible = cmds.getAttr(mesh + ".visibility")
            cmds.setAttr(mesh + ".visibility", not is_visible)

    def get_targets(self):
        # every network if "All" is picked, otherwise just the chosen one
        choice = self.network_box.currentText()
        if choice == "All":
            return list(self.networks.values())
        return [self.networks[choice]]



            #input of number of points
    def update_Number_obj(self):
        #update number of points
        pnt_count = int(self.obj_edit.text())
        for network in self.get_targets():
            cmds.setAttr(network.distribute + ".pointCount", pnt_count)


            #distance modifier for x and y
    def update_distance(self):
        dis_count_x = int(self.dis_edit_x.text())
        dis_count_y = int(self.dis_edit_y.text())
        for network in self.get_targets():
            cmds.setAttr(network.distribute + ".amplitudeX", dis_count_x)
            cmds.setAttr(network.distribute + ".amplitudeY", dis_count_y)


            #scale input

            #offset of z
    def update_offset_z(self):
        dis_count_z = int(self.dis_edit_z.text())
        for network in self.get_targets():
            cmds.setAttr(network.distribute + ".amplitudeZ", dis_count_z)


            #rotate input
    def update_rotate_y(self):
        rot_rotate_y = int(self.rot_edit_y.text())
        for network in self.get_targets():
            cmds.setAttr(network.distribute + ".rotateY", rot_rotate_y)


win = StairsWindow()
win.show()