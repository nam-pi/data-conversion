class Person:
    def __init__(self):
        super()
        self._id = ""
        self._forename = ""
        self._surname = ""
        self._name = ""
    
    @property
    def Id(self):
        return self._id

    @property
    def Forename(self):
        return self._forename

    @property
    def Surname(self):
        return self._surname

    @property
    def Name(self):
        return self._forename + " " + self._surname

    @Id.setter  
    def Id(self, id):
        self._id = id

    @Forename.setter 
    def Forename(self,forename):
        self._forename = forename

    @Surname.setter 
    def Surname(self,surname):
        self._surname = surname
