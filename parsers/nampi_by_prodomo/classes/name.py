from parsers.nampi_by_prodomo.classes.base import Base

class Name(Base):
    def __init__(self):
        super()
        self._type = ""
        self._subtype = ""
        self._text = ""

    @property
    def Type(self):
        return self._type

    @property
    def Subtype(self):
        return self._subtype

    @property
    def Text(self):
        return self._text

    @Type.setter 
    def Type(self,type):
        self._type = type

    @Subtype.setter 
    def Subtype(self,subtype):
        self._subtype = subtype

    @Text.setter 
    def Text(self,text):
        self._text = text

