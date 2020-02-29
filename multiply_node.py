import maya.api.OpenMaya as om

import maya.cmds as cmds


def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using the Maya Python API 2.0.
    """
    pass


class MultiplyNode(om.MPxNode):
    
    TYPE_NAME = "multiplynode"
    TYPE_ID = om.MTypeId(0x0007f7f8)
    
    multiplier_obj = None
    multiplicand_obj = None
    product_obj = None
    
    def __init__(self):
        super(MultiplyNode, self).__init__()
        
    def compute(self, plug, data):
        
        if plug == MultiplyNode.product_obj:
            
            multiplier = data.inputValue(MultiplyNode.multiplier_obj).asInt()
            multiplicand = data.inputValue(MultiplyNode.multiplicand_obj).asDouble()
            product = multiplier * multiplicand
            
            product_data_handle = data.outputValue(MultiplyNode.product_obj)
            product_data_handle.setDouble(product)
            
            data.setClean(plug)
        
    @classmethod
    def creator(cls):
        return MultiplyNode()
        
    @classmethod
    def initialize(cls):
        numeric_attr = om.MFnNumericAttribute()
        
        cls.multiplier_obj = numeric_attr.create("multiplier", "mult", om.MFnNumericData.kInt, 2)
        numeric_attr.keyable= True
        numeric_attr.readable = False
        
        cls.multiplicand_obj = numeric_attr.create("multiplicand", "multc", om.MFnNumericData.kDouble, 0.0)
        numeric_attr.keyable= True
        numeric_attr.readable = False
        
        cls.product_obj = numeric_attr.create("product", "prod", om.MFnNumericData.kDouble, 0.0)
        numeric_attr.writable = False
        
        cls.addAttribute(cls.multiplier_obj)
        cls.addAttribute(cls.multiplicand_obj)
        cls.addAttribute(cls.product_obj)
        
        cls.attributeAffects(cls.multiplier_obj, cls.product_obj)
        cls.attributeAffects(cls.multiplicand_obj, cls.product_obj)
        


def initializePlugin(plugin):
    """
    Entry point for a plugin.

    :param plugin: MObject used to register the plugin using an MFnPlugin function set
    """
    vendor = "Jay Elbourne"
    version = "1.0.0"

    plugin_fn = om.MFnPlugin(plugin, vendor, version)
    try:
        plugin_fn.registerNode(MultiplyNode.TYPE_NAME,
                                MultiplyNode.TYPE_ID,
                                MultiplyNode.creator,
                                MultiplyNode.initialize,
                                om.MPxNode.kDependNode)
    except:
        om.MGlobal.displayError("Failed to register node: {0}".format(MultiplyNode.TYPE_NAME))


def uninitializePlugin(plugin):
    """
    Exit point for a plugin.

    :param plugin: MObject used to de-register the plugin using an MFnPlugin function set
    """
    plugin_fn = om.MFnPlugin(plugin)
    
    try:
        plugin_fn.deregisterNode(MultiplyNode.TYPE_ID)
    except:
        om.MGlobal.displayError("Failed to deregister node: {0}".format(MultiplyNode.TYPE_NAME))


if __name__ == "__main__":
    """
    For Development Only

    Specialized code that can be executed through the script editor to speed up the development process.

    For example: scene cleanup, reloading the plugin, loading a test scene
    """

    # Any code required before unloading the plug-in (e.g. creating a new scene)
    cmds.file(new=True, force=True)

    # Reload the plugin
    plugin_name = "multiply_node.py"
    
    cmds.evalDeferred('if cmds.pluginInfo("{0}", q=True, loaded=True): cmds.unloadPlugin("{0}")'.format(plugin_name))
    cmds.evalDeferred('if not cmds.pluginInfo("{0}", q=True, loaded=True): cmds.loadPlugin("{0}")'.format(plugin_name))

      
    # Any setup code to help speed up testing (e.g. loading a test scene)
    cmds.evalDeferred('cmds.createNode("multiplynode")')