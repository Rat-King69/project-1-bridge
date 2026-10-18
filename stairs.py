import MASH.api as mapi
import maya.cmds as cmds

#creation of mash based on selection 

sel = cmds.ls(selection=True)
mapi.Network().createNetwork(name="Stairs")
#scale varitation 





#legnth varitation








