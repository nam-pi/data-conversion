class Base:
    def __init__(self):
        super()
        self._semanticStm = ""
        self._placeName = ""
        self._id = ""

    @property
    def Id(self):
        return self._id

    @property
    def SemanticStm(self):
        return self._semanticStm

    @property
    def PlaceName(self):
        return self._placeName

    @Id.setter
    def Id(self, id):
        self._id = id
        
    @SemanticStm.setter
    def SemanticStm(self, semanticStm):
        self._semanticStm = semanticStm

    @PlaceName.setter
    def PlaceName(self, placeName):
        self._placeName = placeName