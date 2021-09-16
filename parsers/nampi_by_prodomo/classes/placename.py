class PlaceName(Place):
    def __init__(self):
        super()
        self._ana = ""
    
    @property
    def Ana(self):
        return self._ana

    
    @Ana.setter  
    def Id(self, ana):
        self._ana = ana
