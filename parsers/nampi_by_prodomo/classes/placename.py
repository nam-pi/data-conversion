from place import Place

class PlaceName(Place):
    def __init__(self):
        super()
        self._ana = ""
    
    @property
    def Ana(self):
        return self._ana

    @Ana.setter  
    def Ana(self, ana):
        self._ana = ana
