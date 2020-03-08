from maya import cmds
import pprint

from conLibrary import controller_library
reload(controller_library)

from PySide2 import QtWidgets, QtCore, QtGui

class ControllerLibraryUI(QtWidgets.QDialog):
    """ The ControllerLibraryUI is a dialog that lets us save and import controllers """
    def __init__(self):
        super(ControllerLibraryUI, self).__init__()
                
        self.setWindowTitle("Controller Library UI")
        
        # The library variable points to an instance of our controller library
        self.library = controller_library.ControllerLibrary()
        
        # Every time we create a new instancve,
        # we will automatically build our UI and populate it
        self.build_ui()
        self.populate()
        
    def build_ui(self):
        """ This method build out the UI """
        
        # This is the master layout
        layout = QtWidgets.QVBoxLayout(self)
        
        # This is the child Horizontal widget for the Save functionality
        saveWidget = QtWidgets.QWidget()
        saveLayout = QtWidgets.QHBoxLayout(saveWidget)
        layout.addWidget(saveWidget)
        
        self.saveNameField = QtWidgets.QLineEdit()
        saveLayout.addWidget(self.saveNameField)
        
        saveBtn = QtWidgets.QPushButton("Save")
        saveBtn.clicked.connect(self.save)
        saveLayout.addWidget(saveBtn)
        
        # These are the variables for the thumbnail size
        size = 64
        buffer = 12
        
        # This will create a grid list widget to display our controller thumbnail
        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setViewMode(QtWidgets.QListWidget.IconMode)
        self.listWidget.setIconSize(QtCore.QSize(size, size))
        self.listWidget.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.listWidget.setGridSize(QtCore.QSize(size+buffer, size+buffer))
        layout.addWidget(self.listWidget)
        
        # This is the child widget that holds all our action buttons
        btnsWidget = QtWidgets.QWidget()
        btnsLayout = QtWidgets.QHBoxLayout(btnsWidget)
        layout.addWidget(btnsWidget)
        
        importBtn = QtWidgets.QPushButton("Import")
        importBtn.clicked.connect(self.load)
        btnsLayout.addWidget(importBtn)
        
        refreshBtn = QtWidgets.QPushButton("Refresh")
        refreshBtn.clicked.connect(self.populate)
        btnsLayout.addWidget(refreshBtn)
        
        closeBtn = QtWidgets.QPushButton("Close")
        closeBtn.clicked.connect(self.close)
        btnsLayout.addWidget(closeBtn)
        
        
    def populate(self):
        """ This clear the list widget and repopulated with contents of library """
        self.listWidget.clear()
        
        self.library.find()
        
        for name, info in self.library.items():
            item = QtWidgets.QListWidgetItem(name)
            self.listWidget.addItem(item)
            
            screenshot = info.get('screenshot')
            if screenshot:
                icon = QtGui.QIcon(screenshot)
                item.setIcon(icon)
                
            item.setToolTip(pprint.pformat(info))
                
    def load(self):
        """ This loads the currently selected controller """
        currentItem = self.listWidget.currentItem()
        
        if not currentItem:
            return
            
        name = currentItem.text()
        self.library.load(name)
        
    def save(self):
        """ This saves the controller with the inputed file name """
        name = self.saveNameField.text().strip()
        if not name:
            cmds.warning("You must give a name.")
            return
            
        self.library.save(name)
        self.populate()
        self.saveNameField.setText("")
        
def show_ui():
    """
    This shows and returns a handle to the UI
    
    Returns:
        QDialog
    """
    ui = ControllerLibraryUI()
    ui.show()
    return ui