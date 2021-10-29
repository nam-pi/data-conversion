from parsers.nampi_by_prodomo.classes.base import Base

class ExternalEvent(Base):
    def __init__(self):
        super()
        self._key = ""
        self._label = ""
        self._date = ""
        self._group = ""
        self._place = ""
        self._relation = ""
        self._type = ""
        self._occupationkey = ""
        self._aspectkey = ""
        self._aspectlabel = ""
        self._participant = ""
        self._semantic = ""
        self._else = ""
    @property
    def Key(self):
        return self._key

    @property
    def Label(self):
        return self._label

    @property
    def Date(self):
        return self._date

    @property
    def Group(self):
        return self._group

    @property
    def Place(self):
        return self._place

    @property
    def Relation(self):
        return self._relation
    @property
    def Type(self):
        return self._type

    @property
    def Occupationkey(self):
        return self._occupationkey
    
    @property
    def Aspectkey(self):
        return self._aspectkey

    @property
    def Aspectlabel(self):
        return self._aspectlabel

    @property
    def Participant(self):
        return self._participant
    
    @property
    def Semantic(self):
        return self._semantic

    @property
    def Else(self):
        return self._else

    @Key.setter
    def Key(self, key):
        self._key = key

    @Label.setter 
    def Label(self,label):
        self._label = label

    @Date.setter 
    def Date(self,date):
        self._date = date

    @Group.setter 
    def Group(self,group):
        self._group = group

    @Place.setter 
    def Place(self,place):
        self._place = place

    @Relation.setter 
    def Relation(self,relation):
        self._relation = relation
    
    @Type.setter 
    def Type(self,type):
        self._type = type

    @Occupationkey.setter 
    def Occupationkey(self,occupationkey):
        self._occupationkey = occupationkey

    @Aspectkey.setter 
    def Aspectkey(self,aspectkey):
        self._aspectkey = aspectkey

    @Aspectlabel.setter 
    def Aspectlabel(self,aspectlabel):
        self._aspectlabel = aspectlabel

    @Participant.setter 
    def Participant(self,participant):
        self._participant = participant
    
    @Semantic.setter 
    def Semantic(self,semantic):
        self._semantic = semantic

    @Else.setter 
    def Else(self,_else):
        self._else = _else