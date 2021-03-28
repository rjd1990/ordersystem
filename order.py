class Order():

    def __init__(self, id, status, dateCreated, customerID):
        self._id = id
        self._status = status
        self._dateCreated = dateCreated
        self._customerID = customerID
    
    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, value):
        self._id = value

    @property
    def status(self):
        return self._status
    @status.setter
    def status(self, value):
        self._status = value

    @property
    def dateCreated(self):
        return self._dateCreated
    @dateCreated.setter
    def dateCreated(self, value):
        self._dateCreated = value

    @property
    def customerID(self):
        return self._customerID
    @customerID.setter
    def customerID(self, value):
        self._customerID = value