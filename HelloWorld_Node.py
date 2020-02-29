import maya.api.OpenMaya as om
import maya.api.OpenMayaRender as omr
import maya.api.OpenMayaUI as omui

import maya.cmds as cmds


def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using the Maya Python API 2.0.
    """
    pass


class HelloWorldNode(omui.MPxLocatorNode):
    
    TYPE_NAME = "helloworld"
    TYPE_ID = om.MTypeId(0x0007f7f7)
    DRAW_CLASSIFICATION = "drawdb/geometry/helloworld"
    DRAW_REGISTRANT_ID = "HelloWorldNode"
    
    def __init__(self):
        super(HelloWorldNode, self).__init__()
        
    @classmethod
    def creator(cls):
        return HelloWorldNode()
        
    @classmethod
    def initialize(cls):
        pass


class HelloWorldDrawOverride(omr.MPxDrawOverride):
    
    NAME = "HelloWorldDrawOverride"
    
    def __init__(self, obj):
        super(HelloWorldDrawOverride, self).__init__(obj, None, False)
        
    def prepareForDraw(self, obj_path, camer_path, frame_context, old_data):
        pass
        
    def supportedDrawAPIs(self):
        return omr.MRenderer.kAllDevices
        
    def hasUIDrawables(self):
        return True
        
    def addUIDrawables(self, obj_path, draw_manager, frame_context, data):
        draw_manager.beginDrawable()
        draw_manager.text2d(om.MPoint(100,100), "Hello World")
        draw_manager.endDrawable()
        
    @classmethod
    def creator(cls, obj):
        return HelloWorldDrawOverride(obj)
        

def initializePlugin(plugin):
    """
    Entry point for a plugin. It is called once -- immediately after the plugin is loaded.
    This function registers all of the commands, nodes, contexts, etc... associated with the plugin.

    It is required by all plugins.

    :param plugin: MObject used to register the plugin using an MFnPlugin function set
    """
    vendor = "Jay Elbourne"
    version = "1.0.0"

    plugin_fn = om.MFnPlugin(plugin, vendor, version)
    try:
        plugin_fn.registerNode(HelloWorldNode.TYPE_NAME,
                                HelloWorldNode.TYPE_ID,
                                HelloWorldNode.creator,
                                HelloWorldNode.initialize,
                                om.MPxNode.kLocatorNode,
                                HelloWorldNode.DRAW_CLASSIFICATION)
    except:
        om.MGlobal.displayError("Failed to register Node: {0}".format(HelloWorldNode.TYPE_NAME))
        
    try:
        omr.MDrawRegistry.registerDrawOverrideCreator(HelloWorldNode.DRAW_CLASSIFICATION,
                                                        HelloWorldNode.DRAW_REGISTRANT_ID,
                                                        HelloWorldDrawOverride.creator)
    except:
        om.MGlobal.displayError("Failed to register Node: {0}".format(HelloWorldDrawOverride.NAME))

def uninitializePlugin(plugin):
    """
    Exit point for a plugin. It is called once -- when the plugin is unloaded.
    This function de-registers everything that was registered in the initializePlugin function.

    It is required by all plugins.

    :param plugin: MObject used to de-register the plugin using an MFnPlugin function set
    """
    plugin_fn = om.MFnPlugin(plugin)
    
    try:
        omr.MDrawRegistry.deregisterDrawOverrideCreator(HelloWorldDrawOverride.DRAW_CLASSIFICATION,
                                                        HelloWorldNode.DRAW_REGISTRANT_ID)
    except:
        om.MGlobal.displayError("Failed to deregister Node: {0}".format(HelloWorldDrawOverride.NAME))
        
    try:
        plugin_fn.deregisterNode(HelloWorldNode.TYPE_ID)
    except:
        om.MGlobal.displayError("Failed to deregister Node: {0}".format(HelloWorldNode.TYPE_NAME))


if __name__ == "__main__":
    """
    For Development Only

    Specialized code that can be executed through the script editor to speed up the development process.

    For example: scene cleanup, reloading the plugin, loading a test scene
    """

    # Any code required before unloading the plug-in (e.g. creating a new scene)


    # Reload the plugin
    cmds.file(new=True, force=True)
    
    plugin_name = "HelloWorld_Node.py"
    cmds.evalDeferred('if cmds.pluginInfo("{0}", q=True, loaded=True): cmds.unloadPlugin("{0}")'.format(plugin_name))
    cmds.evalDeferred('if not cmds.pluginInfo("{0}", q=True, loaded=True): cmds.loadPlugin("{0}")'.format(plugin_name))

    cmds.evalDeferred('cmds.createNode("helloworld")')
    
    # Any setup code to help speed up testing (e.g. loading a test scene)
