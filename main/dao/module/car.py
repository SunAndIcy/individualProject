class Car:
    def __init__(self, id, make, model, year, mileage, availableNow, minRentPeriod, maxRentPeriod, gmtCreated, gmtModified, deleted, rate, userId):
        self._id = id
        self._make = make
        self._model = model
        self._year = year
        self._mileage = mileage
        self._availableNow = availableNow
        self._minRentPeriod = minRentPeriod
        self._maxRentPeriod = maxRentPeriod
        self._gmtCreated = gmtCreated
        self._gmtModified = gmtModified
        self._deleted = deleted
        self._rate = rate
        self._userId = userId

    @staticmethod
    def create_car_from_tuple(data_tuple):
        return Car(*data_tuple)

    @classmethod
    def from_tuple(cls, data_tuple):
        return cls(*data_tuple)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def make(self):
        return self._make

    @make.setter
    def make(self, value):
        self._make = value

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = value

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        self._year = value

    @property
    def mileage(self):
        return self._mileage

    @mileage.setter
    def mileage(self, value):
        self._mileage = value

    @property
    def availableNow(self):
        if self._availableNow == 1:
            return "Yes"
        elif self._availableNow == 0:
            return "No"
        else:
            return "Unknown"

    @availableNow.setter
    def availableNow(self, value):
        self._availableNow = value

    @property
    def minRentPeriod(self):
        return self._minRentPeriod

    @minRentPeriod.setter
    def minRentPeriod(self, value):
        self._minRentPeriod = value

    @property
    def maxRentPeriod(self):
        return self._maxRentPeriod

    @maxRentPeriod.setter
    def maxRentPeriod(self, value):
        self._maxRentPeriod = value

    @property
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, value):
        self._rate = value

    @property
    def userId(self):
        return self._userId

    @userId.setter
    def userId(self, value):
        self._userId = value