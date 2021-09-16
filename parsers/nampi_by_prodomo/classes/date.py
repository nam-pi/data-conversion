class Date:
    def __init__(self):
        super()
        self._id = ""
        self._persId = ""
        self._when = ""
        self._text = ""
        self._type = ""
        self._subtype = ""
    
    @property
    def Id(self):
        return self._id

    @property
    def persId(self):
        return self._persId

    @property
    def When(self):
        return self._when

    @property
    def Text(self):
        return self._text

    @property
    def Type(self):
        return self._type

    @property
    def Subtype(self):
        return self._subtype

    @Id.setter  
    def Id(self, id):
        self._id = id

    @persId.setter  
    def persId(self, persId):
        self._persId = persId

    @When.setter 
    def When(self,when):
        self._when = when

    @Text.setter 
    def Text(self,text):
        self._text = text

    @Type.setter 
    def Type(self,type_):
        self._type = type_

    @Subtype.setter 
    def Subtype(self,subtype):
        self._subtype = subtype