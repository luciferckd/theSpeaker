import pymongo
from typing import Optional
from dataclasses import dataclass
from contextlib import contextmanager

@dataclass
class Car:
    vin: str
    make: str
    model: str
    year: int

class DatabaseDriver:
    def __init__(self, db_uri: str = "mongodb://localhost:27017/", db_name: str = "auto_db"):
        self.client = pymongo.MongoClient(db_uri)
        self.db = self.client[db_name]
        self._init_db()

    def _init_db(self):
        if "cars" not in self.db.list_collection_names():
            self.db.create_collection("cars", capped=False, autoIndexId=True)

    def create_car(self, vin: str, make: str, model: str, year: int) -> Car:
        car_data = {
            "vin": vin,
            "make": make,
            "model": model,
            "year": year
        }
        self.db.cars.insert_one(car_data)
        return Car(vin=vin, make=make, model=model, year=year)

    def get_car_by_vin(self, vin: str) -> Optional[Car]:
        car_data = self.db.cars.find_one({"vin": vin})
        if not car_data:
            return None
        
        return Car(
            vin=car_data["vin"],
            make=car_data["make"],
            model=car_data["model"],
            year=car_data["year"]
        )