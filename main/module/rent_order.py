class RentOrder:
    def __init__(self, id, userId, userName, carId, make, model, year, mileage,
                 rentalStartDay, rentalDays, rate, cost, status,
                 gmtCreated, gmtModified, deleted):
        self._id = id
        self._userId = userId
        self._userName = userName
        self._carId = carId
        self._make = make
        self._model = model
        self._year = year
        self._mileage = mileage
        self._rentalStartDay = rentalStartDay
        self._rentalDays = rentalDays
        self._rate = rate
        self._cost = cost
        self._status = status
        self._gmtCreated = gmtCreated
        self._gmtModified = gmtModified
        self._deleted = deleted

    @staticmethod
    def create_rental_from_tuple(data_tuple):
        return RentOrder(*data_tuple)

    @classmethod
    def from_tuple(cls, data_tuple):
        return cls(*data_tuple)

    # Getter 和 Setter 方法的装饰器
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def userId(self):
        return self._userId

    @userId.setter
    def userId(self, value):
        self._userId = value

    @property
    def userName(self):
        return self._userName

    @userName.setter
    def userName(self, value):
        self._userName = value

    @property
    def carId(self):
        return self._carId

    @carId.setter
    def carId(self, value):
        self._carId = value

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
    def rentalStartDay(self):
        return self._rentalStartDay

    @rentalStartDay.setter
    def rentalStartDay(self, value):
        self._rentalStartDay = value

    @property
    def rentalDays(self):
        return self._rentalDays

    @rentalDays.setter
    def rentalDays(self, value):
        self._rentalDays = value

    @property
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, value):
        self._rate = value

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, value):
        self._cost = value

    @property
    def status(self):
        if self._status == 1:
            return "Pending Review"
        elif self._status == 2:
            return "Approved"
        elif self._status == 3:
            return "Paid"
        elif self._status == 4:
            return "Picked Up"
        elif self._status == 5:
            return "Completed"
        elif self._status == -1:
            return "Reject"
        else:
            return "Unknown"
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def gmtCreated(self):
        return self._gmtCreated

    @gmtCreated.setter
    def gmt_created(self, value):
        self._gmtCreated = value

    @property
    def gmtModified(self):
        return self._gmtModified

    @gmtModified.setter
    def gmt_modified(self, value):
        self._gmtModified = value

    @property
    def deleted(self):
        return self._deleted

    @deleted.setter
    def deleted(self, value):
        self._deleted = value
