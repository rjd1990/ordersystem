class ProductDisplay():

    def __init__(self, id, name, quantity, categories):
        self._id = id
        self._name = name
        self._quantity = quantity
        self._categories = categories

    
    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value

    @property
    def quantity(self):
        return self._quantity
    @quantity.setter
    def quantity(self, value):
        self._quantity = value

    @property
    def categories(self):
        return self._categories
    @categories.setter
    def categories(self, value):
        self._categories = value

    # @property
    # def totalPrice(self):
    #     return self._totalPrice
    # @totalPrice.setter
    # def totalPrice(self, value):
    #     self._totalPrice = value