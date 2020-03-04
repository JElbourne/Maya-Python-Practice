import maya.api.OpenMaya as om

import maya.cmds as cmds


def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using the Maya Python API 2.0.
    """
    pass


class RollingNode(om.MPxNode):

    TYPE_NAME = "rollingnode"
    TYPE_ID = om.MTypeId(0x0007F7F9)
    
    distance_obj = None
    radius_obj = None
    rotation_obj = None

    def __init__(self):
        super(RollingNode, self).__init__()
        
        numeric_attr = om.MFnNumericAttribute()
        
        cls.distance_obj = numeric_attr.create("distance", "dist", om.MFnNumericData.kDouble, 0.0)
        numeric_attr.readable = False
        numeric_attr.keyable = True
        
        cls.radius_obj = numeric_attr.create("radius", "rad", om.MFnNumericData.kDouble, 0.0)
        numeric_attr.readable = False
        numeric_attr.keyable = True
        
        unit_attr = om.MFnUnitAttribute()
        
        cls.rotation_obj = unit_attr.create("rotation", "rot", om.MFnUnitAttribute.kAngle, 0.0)
        
        cls.addAttribute(cls.distance_obj)
        cls.addAttribute(cls.radius_obj)
        cls.addAttribute(cls.rotation_obj)
        
        cls.attributeAffects(cls.distance_obj, cls.rotation_obj)
        cls.attributeAffects(cls.radius_obj, cls.rotation_obj)
        

    def compute(self, plug, data):
        pass

    @classmethod
    def creator(cls):
        return RollingNode()

    @classmethod
    def initialize(cls):
        pass


def initializePlugin(plugin):
    """
    Entry point for a plugin.
    """
    vendor = "Chris Zurbrigg"
    version = "1.0.0"

    plugin_fn = om.MFnPlugin(plugin, vendor, version)
    try:
        plugin_fn.registerNode(RollingNode.TYPE_NAME,              # name of the node
                               RollingNode.TYPE_ID,                # unique id that identifies node
                               RollingNode.creator,                # function/method that returns new instance of class
                               RollingNode.initialize,             # function/method that will initialize all attributes of node
                               om.MPxNode.kDependNode)             # type of node to be registered
    except:
        om.MGlobal.displayError("Failed to register node: {0}".format(RollingNode.TYPE_NAME))

def uninitializePlugin(plugin):
    """
    Exit point for a plugin.
    """
    plugin_fn = om.MFnPlugin(plugin)
    try:
        plugin_fn.deregisterNode(RollingNode.TYPE_ID)
    except:
        om.MGlobal.displayError("Failed to unregister node: {0}".format(RollingNode.TYPE_NAME))


if __name__ == "__main__":
    """
    For Development Only
    """

    # Any code required before unloading the plug-in (e.g. creating a new scene)
    cmds.file(new=True, force=True)

    # Reload the plugin
    plugin_name = "rolling_node.py"

    cmds.evalDeferred('if cmds.pluginInfo("{0}", q=True, loaded=True): cmds.unloadPlugin("{0}")'.format(plugin_name))
    cmds.evalDeferred('if not cmds.pluginInfo("{0}", q=True, loaded=True): cmds.loadPlugin("{0}")'.format(plugin_name))


    # Any setup code to help speed up testing (e.g. loading a test scene)
    cmds.evalDeferred('cmds.createNode("rollingnode")')
