from parsers.nampi_by_prodomo.classes.base import Base
class Place(Base):
    def __init__(self):
        super()
        self._persId = ""
        self._text = ""
        self._type = ""
        self._subtype = ""
        self._key = ""

    @property
    def persId(self):
        return self._persId

    @property
    def Text(self):
        return self._text

    @property
    def Type(self):
        return self._type

    @property
    def Subtype(self):
        return self._subtype

    @property
    def Key(self):
        return self._key

    @persId.setter
    def persId(self, persId):
        self._persId = persId

    @Text.setter
    def Text(self, text):
        self._text = text

    @Type.setter
    def Type(self, type_):
        self._type = type_

    @Subtype.setter
    def Subtype(self, subtype):
        self._subtype = subtype

    @Key.setter
    def Key(self, key):
        self._key = key
