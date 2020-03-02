from maya import cmds

def rename_objects():
    selection = cmds.ls(sl=True)

    if not selection:
        selection = cmds.ls(dag=True, long=True)
        

    selection.sort(key=len, reverse=True)

    for obj in selection:
        short_name = obj.split("|")[-1]
        
        children = cmds.listRelatives(obj, children=True, fullPath=True) or []
        
        if len(children) == 1:
            child = children[0]
            obj_type = cmds.objectType(child)
        else:
            obj_type = cmds.objectType(obj)
        print obj_type    
        if obj_type == "mesh":
            suffix = "geo"
        elif obj_type == "joint":
            suffix = "jnt"
        elif obj_type == "camera":
            print "Skipping camera"
            continue
        else:
            suffix = "grp"
        
        new_name = short_name + "_" + suffix 
        
        cmds.rename(obj, new_name)
