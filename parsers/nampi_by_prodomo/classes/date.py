class Date:
    def __init__(self):
        super()
        self._id = ""
        self._persId = ""
        self._when = ""
        self._text = ""
        self._type = ""
        self._subtype = ""
        self._from = ""
        self._to = ""
        self._notAfter = ""
        self._notBefore = ""
    
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

    @property
    def When(self):
        return self._when

    @property
    def From(self):
        return self._from

    @property
    def To(self):
        return self._to

    @property
    def NotAfter(self):
        return self._notAfter

    @property
    def NotBefore(self):
        return self._notBefore

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

    @When.setter 
    def When(self,when):
        self._when = when

    @From.setter 
    def From(self,from_):
        self._from = from_

    @To.setter 
    def To(self,to):
        self._to = to

    @NotAfter.setter 
    def When(self,notafter):
        self._notAfter = notafter

    @NotBefore.setter 
    def NotBefore(self,notbefore):
        self._notBefore = notbefore