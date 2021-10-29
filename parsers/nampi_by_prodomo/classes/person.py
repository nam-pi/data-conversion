from parsers.nampi_by_prodomo.classes.base import Base

class Person(Base):
    def __init__(self):
        super()
        self._forename = ""
        self._surname = ""
        self._name = ""
        self._mother = ""
        self._father = ""

    @property
    def Forename(self):
        return self._forename

    @property
    def Surname(self):
        return self._surname

    @property
    def Name(self):
        return self._forename + " " + self._surname

    @property
    def Mother(self):
        return self._mother

    @property
    def Father(self):
        return self._father

    @Forename.setter 
    def Forename(self,forename):
        self._forename = forename

    @Surname.setter 
    def Surname(self,surname):
        self._surname = surname

    @Mother.setter 
    def Mother(self,mother):
        self._mother = mother

    @Father.setter 
    def Father(self,father):
        self._father = father
