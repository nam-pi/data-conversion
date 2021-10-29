class Entity_Importer:
    def __init__(self):
        super()
        self._key = ""
        self._label = ""
        self._event = ""
        self._aspectpart = ""
        self._class = ""
        self._part_of_label = ""
        self._place_label = ""
        self._geoid = ""
    
    @property
    def Key(self):
        return self._key

    @property
    def Label(self):
        return self._label

    @property
    def Event(self):
        return self._event

    @property
    def AspectPart(self):
        return self._aspectpart

    @property
    def Class(self):
        return self._class

    @property
    def Part_Of_Label(self):
        return self._part_of_label
    @property
    def Place_Label(self):
        return self._place_label

    @property
    def GeoId(self):
        return self._geoid

    @Key.setter
    def Key(self, key):
        self._key = key

    @Label.setter 
    def Label(self,label):
        self._label = label

    @Event.setter 
    def Event(self,event):
        self._event = event

    @AspectPart.setter 
    def AspectPart(self,aspectp):
        self._aspectpart = aspectp

    @Class.setter 
    def Class(self,_class):
        self._class = _class

    @Part_Of_Label.setter 
    def Part_Of_Label(self,part_of_label):
        self._part_of_label = part_of_label
    
    @Place_Label.setter 
    def Place_Label(self,place_label):
        self._place_label = place_label
    
    @GeoId.setter 
    def GeoId(self,geoid):
        self._geoid = geoid
