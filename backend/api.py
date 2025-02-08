from livekit.agents import llm
import enum
from typing import Annotated
import logging
from db_drive import DatabaseDriver

logger = logging.getLogger("user-data")
logger.setLevel(logging.INFO)

DB = DatabaseDriver()

class CarDetails(enum.Enum):
    VIN = "vin"
    MAKE = "make"
    MODEL = "model"
    YEAR = "year"   

class AssistantFnc(llm.FunctionContext):
    def __init__(self):
        super().__init__()

        self._car_details = {
            CarDetails.VIN: None,
            CarDetails.MAKE: None,
            CarDetails.MODEL: None,
            CarDetails.YEAR: None
        }

    def get_car_str(self):
           car_str = ""
           for key, value in self._car_details.items():
                car_str += f"{key.value}: {value}\n"

           return car_str
    
    @llm.ai_callable(description="Store car details")
    def lookup_car(self, vin: Annotated[str, llm.TypeInfo(description="The vin of the car lookup")]):
        logger.info("lookup car - vin: %s", vin)

        result = DB.get_car_by_vin(vin)
        if result is None:
            return "Car not found"
        
        self._car_details = {
            CarDetails.VIN: result.vin,
            CarDetails.MAKE: result.make,
            CarDetails.MODEL: result.model,
            CarDetails.YEAR: result.year
        }

     

        return f"Car details found: {self.get_car_str()}"
    @llm.ai_callable(description="Store car details")
    def get_car_details(self):
        logger.info("get car details")
        return f"Car details found: {self.get_car_str()}"
    
    @llm.ai_callable(description="Store car details")
    def lookup_car(self, 
                   vin: Annotated[str, llm.TypeInfo(description="The vin of the car lookup")],
                   make: Annotated[str, llm.TypeInfo(description="The make of the car lookup")],
                   model: Annotated[str, llm.TypeInfo(description="The model of the car lookup")],
                   year: Annotated[int, llm.TypeInfo(description="The year of the car lookup")]
                   ):
        logger.info("create car - vin: %s, make: %s, model: %s, year: %s", vin, make, model, year)

        result = DB.create_car(vin, make, model, year)

        if result is None:
            return "Car not found"
        
        self._car_details = {
            CarDetails.VIN: result.vin,
            CarDetails.MAKE: result.make,
            CarDetails.MODEL: result.model,
            CarDetails.YEAR: result.year
        }   

        return "Car details created"
    
    def has_car(self):
        return self._car_details[CarDetails.VIN] != None
    
