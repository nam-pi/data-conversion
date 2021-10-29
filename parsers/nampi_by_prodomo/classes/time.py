from parsers.nampi_by_prodomo.classes.date import Dates
class Time(Dates):
    def __init__(self):
        super()

        self._accuracy = ""
    
    @property
    def Accuracy(self):
        return self._accuracy

    @Accuracy.setter  
    def Accuracy(self, accuracy):
        self._accuracy = accuracy
