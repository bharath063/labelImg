
from libs.attributes import AbstractAttributesWidgets
import os
import shutil

class AttributesManager( AbstractAttributesWidgets ):

    global_index = 0
    defaultLabelAttrs = []
    # used to implement the "natural order" of the various attributes definitions
    def __init__( self, mainWindow, dockWidgetArea, defaultLabelAttrs=None ):
        self.defaultLabelAttrs = defaultLabelAttrs
        AbstractAttributesWidgets.__init__(self, mainWindow, dockWidgetArea)

    def next_index( self ):
        self.global_index = self.global_index + 1
        return self.global_index

    # 
    def toggle_defaults_dirty( self, toggle ):
        self.defaults_dirty = toggle
        print( "defaults_dirty={}".format( self.defaults_dirty ) )
        return True     


    # just capture the destination
    def update_destination( self, destination ):
        self.destination = destination
        return True          
        
    # try to copy the current image file and create a new label file at the destination
    def copy_to_destination( self ):
        if not hasattr(self, "destination") or self.destination is None:
            raise ValueError( "Destination not defined!" )

        if not os.path.isdir( self.destination ):
            raise ValueError( "Destination does not exist: {}".format( self.destination ) )
            
        image_filename = os.path.basename( self.mainWindow.filePath )
        # only need the root
        classification_filename = image_filename.split(".")[0]

        targetImagePath = os.path.join( self.destination, image_filename )
        targetClassificationPath = os.path.join( self.destination, classification_filename )

        print( "copy_to_destination: {}".format( targetImagePath )  )

        shutil.copyfile( self.mainWindow.filePath, targetImagePath ) 
        self.mainWindow.saveLabels( targetClassificationPath )
        
        return True     
        

    # specific actions specified above
    def get_global_attribute_definitions( self ):
        return {
            "destination": {
                "order": self.next_index(),
                "tooltip": "The directory to which the current image and it's PASCAL VOC file will be copied",            
                "default": "",
                "type": "text",
                "action": self.update_destination
            },
            "copy": {
                "order": self.next_index(),
                "tooltip": "Copy the current image and it's PASCAL VOC file the to directory specified in 'destination'",            
                "type": "button",
                "action": self.copy_to_destination
            },
            "toggle defaults dirty": {
                "order": self.next_index(),
                "tooltip": "Whether the dirty flag should be set when assigning a default value (hence always saving when applied)",            
                "type": "radio",
                "default": self.defaults_dirty,
                "action": self.toggle_defaults_dirty
            }
        }  

    # same action in all cases from AttributesWidgets
    def get_image_attribute_definitions( self ):
        return {}    

    # same action in all cases from AttributesWidgets
    def get_label_attribute_definitions( self ):
        defaultLabelAttrs = self.defaultLabelAttrs
        if defaultLabelAttrs is not None and len(defaultLabelAttrs) > 0:
            #TODO naively returning same action is causing the values to be set to "no" before they're even initialized
            return dict( list(map( lambda attrName:[attrName,{"type":"checkbox","default": "no", "action": self.update_label_attributes}], defaultLabelAttrs )) )
        else:
            return {}