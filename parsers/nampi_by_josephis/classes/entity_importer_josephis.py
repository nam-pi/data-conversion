class Entity_Importer_Josephis:
    def __init__(self):
        super()
        self._exactcite = ""
        self._enable = ""
        self._reltitle = ""
        self._forename = ""
        self._surename = ""
        self._deathdate = ""
        self._deathdateearly = ""
        self._deathdatelate = ""
        self._deathplace = ""
        self._deathplacegeo = ""
        self._issueplace = ""
        self._issueplacegeo = ""
        self._community = ""
        self._status = ""
        self._statusnampi = ""
        self._occupation = ""
        self._occupationnampi = ""
        self._event = ""
        self._cite = ""
        self._gnd = ""
        self._comment = ""

    @property
    def ExactCite(self):
        return self._exactcite

    @property
    def Enable (self):
        return self._enable

    @property
    def RelTitle(self):
        return self._reltitle

    @property
    def Forename(self):
        return self._forename 

    @property
    def Surename(self):
        return self._surename

    @property
    def Deathdate(self):
        return self._deathdate

    @property
    def Deathdateearly(self):
        return self._deathdateearly

    @property
    def Deathdatelate(self):
        return self._deathdatelate

    @property
    def Deathplace(self):
        return self._deathplace

    @property
    def DeathplaceGeo(self):
        return self._deathplacegeo

    @property
    def IssuePlace(self):
        return self._issueplace

    @property
    def IssuePlacegeo(self):
        return self._issueplacegeo

    @property
    def Community(self):
        return self._community

    @property
    def Status(self):
        return self._status

    @property
    def Status_Nampi(self):
        return self._statusnampi
        
    @property
    def Occupation(self):
        return self._occupation

    @property
    def Occupation_Nampi(self):
        return self._occupationnampi

    @property
    def Event(self):
        return self._event

    @property
    def Cite(self):
        return self._cite
        
    @property
    def GND(self):
        return self._gnd

    @property
    def Comment(self):
        return self._comment

    #@Comment.setter
    @ExactCite.setter
    def ExactCite(self, exactcite):
        self._exactcite = exactcite

    @Enable.setter
    def Enable (self, enable):
        self._enable = enable

    @RelTitle.setter
    def RelTitle(self, reltitle):
        self._reltitle = reltitle

    @Forename.setter
    def Forename(self, forename):
        self._forename = forename

    @Surename.setter
    def Surename(self, surename):
        self._surename = surename

    @Deathdate.setter
    def Deathdate(self, deathdate):
        self._deathdate = deathdate

    @Deathdateearly.setter
    def Deathdateearly(self, deathdateearly):
        self._deathdateearly = deathdateearly

    @Deathdatelate.setter
    def Deathdatelate(self, deathdatelate):
        self._deathdatelate = deathdatelate

    @Deathplace.setter
    def Deathplace(self, deathplace):
        self._deathplace = deathplace

    @DeathplaceGeo.setter
    def DeathplaceGeo(self, deathplacegeo):
        self._deathplacegeo = deathplacegeo

    @IssuePlace.setter
    def IssuePlace(self, issueplace):
        self._issueplace = issueplace

    @IssuePlacegeo.setter
    def IssuePlacegeo(self, issueplacegeo):
        self._issueplacegeo = issueplacegeo

    @Community.setter
    def Community(self, community):
        self._community = community

    @Status.setter
    def Status(self, status):
        self._status = status

    @Status_Nampi.setter
    def Status_Nampi(self, statusnampi):
        self._statusnampi = statusnampi
        
    @Occupation.setter
    def Occupation(self, occupation):
        self._occupation = occupation

    @Occupation_Nampi.setter
    def Occupation_Nampi(self, occupationnampi):
        self._occupationnampi = occupationnampi

    @Event.setter
    def Event(self, event):
        self._event = event

    @Cite.setter
    def Cite(self, cite):
        self._cite = cite
        
    @GND.setter
    def GND(self, gnd):
        self._gnd = gnd

    @Comment.setter
    def Comment(self, comment):
        self._comment = comment