class LineItem():

    def __init__(self, id, amount, productID, orderID):
        self._id = id
        self._amount = amount
        self._productID = productID
        self._orderID = orderID
    
    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, value):
        self._id = value

    @property
    def amount(self):
        return self._amount
    @amount.setter
    def amount(self, value):
        self._amount = value

    @property
    def productID(self):
        return self._productID
    @productID.setter
    def productID(self, value):
        self._productID = value

    @property
    def orderID(self):
        return self._orderID
    @orderID.setter
    def orderID(self, value):
        self._orderID = value