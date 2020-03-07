from maya import cmds
import maya.api.OpenMaya as om

class FootRoll(object):
    SIDE = "l"
    NAME_OVERRIDE = None
    FOOT_WIDTH = 5
    ANKLE_OFFSET = 3
    GRND_HGT_OFFSET = 0
    
    controller = None
    ik_handle = None
    ankle_bone = None
    foot_ball_bone = None
    foot_toe_bone = None
    
    def __init__(self, side="l", foot_width=5, ankle_offset=3, grnd_hgt_offset=0, name_override=None):
        self.SIDE = side
        self.NAME_OVERRIDE = name_override
        self.FOOT_WIDTH = foot_width
        self.ANKLE_OFFSET = ankle_offset
        self.GRND_HGT_OFFSET = grnd_hgt_offset
    
    def assign_ik(self):
        sel = cmds.ls(type="ikHandle", selection=True) or []
        if not sel:
            om.MGlobal.displayError("You must select one ikHandle.")
        elif len(sel) > 1:
            om.MGlobal.displayError("Too many selections. Select only one ikHandle.")
        else:
            self.ik_handle = sel[0]
    
    def assign_joints(self):
        sel = cmds.ls(type="joint", selection=True) or []
        if not len(sel) == 3:
            om.MGlobal.displayError("You must select THREE joints in this order (ankle, ball, toe).")
        else:
            self.ankle_bone = sel[0]
            self.foot_ball_bone = sel[1]
            self.foot_toe_bone = sel[2]
    
    def create_controller(self):
        ctrl_name = self.NAME_OVERRIDE if self.NAME_OVERRIDE else "foot_ctrl"
        scale = self.FOOT_WIDTH * 1.25
        
        xCoord = cmds.getAttr("{0}.translateX".format(self.ik_handle)) if self.ik_handle else 0
        zCoord = cmds.getAttr("{0}.translateZ".format(self.ik_handle)) if self.ik_handle else 0
        ctrl = cmds.circle(name="{0}_{1}".format(ctrl_name, self.SIDE), normal=(0,1,0))
        
        cmds.setAttr("{0}.translate".format(ctrl[0]), xCoord, self.GRND_HGT_OFFSET, zCoord)
        cmds.setAttr("{0}.scale".format(ctrl[0]), scale, scale, scale)
        
        
        

fr = FootRoll()
#fr.assign_ik()
