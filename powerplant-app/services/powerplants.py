from abc import ABC, abstractmethod
from models.models import FuelModel


class PowerPlantInterface(ABC):

    def __init__(
        self,
        name: str,
        efficiency: float,
        pmax: float,
        pmin: float,
        fuel_type: FuelModel,
    ):
        self.name = name
        self.efficiency = efficiency
        self.pmax = pmax
        self.pmin = pmin
        self.fuel_type = fuel_type

    @abstractmethod
    def calculate_cost(self, fuel_cost: float) -> float:
        """Abstract method to calculate the fuel cost."""
        pass


class GasFiredPlant(PowerPlantInterface):

    def __init__(
        self,
        name: str,
        efficiency: float,
        pmax: float,
        pmin: float,
        fuel_type: FuelModel = "gas",
    ):
        super().__init__(name, efficiency, pmax, pmin, fuel_type)

    def calculate_cost(self, fuel_price: float) -> float:
        """Calculate cost for gas-fired power plant based on fuel efficiency."""
        return fuel_price / self.efficiency


class TurboJetPlant(PowerPlantInterface):

    def __init__(
        self,
        name: str,
        efficiency: float,
        pmax: float,
        pmin: float,
        fuel_type: FuelModel = "kerosine",
    ):
        super().__init__(name, efficiency, pmax, pmin, fuel_type)

    def calculate_cost(self, fuel_price: float) -> float:
        """Calculate cost for turbojet plant based on fuel efficiency."""
        return fuel_price / self.efficiency


class WindTurbine(PowerPlantInterface):

    def __init__(
        self,
        name: str,
        efficiency: float,
        pmax: float,
        pmin: float,
        fuel_type: FuelModel = "wind",
    ):
        super().__init__(name, efficiency, pmax, pmin, fuel_type)

    def calculate_cost(self, fuel_price: float) -> float:
        """Wind turbines do not have fuel costs, so return 0."""
        return 0


class PowerPlantRegistry:
    def __init__(self):
        self._registry = {}

    def register_powerplant(self, plant_type: str, plant_class: type):
        """Register a new power plant type in the registry."""
        self._registry[plant_type] = plant_class

    def get_powerplant_class(self, plant_type: str):
        """Get the power plant class from the registry."""
        plant_class = self._registry.get(plant_type)
        if plant_class is None:
            raise ValueError(f"Unknown power plant type: {plant_type}")
        return plant_class


# Singleton instance of the power plant registry
plant_registry = PowerPlantRegistry()

# Registering power plant types
plant_registry.register_powerplant("gasfired", GasFiredPlant)
plant_registry.register_powerplant("turbojet", TurboJetPlant)
plant_registry.register_powerplant("windturbine", WindTurbine)


class PowerPlantFactory:
    """
    A factory class responsible for creating power plant instances.
    """

    def create_powerplants(self, powerplants_data) -> list[PowerPlantInterface]:
        powerplants = []
        for pp_data in powerplants_data:
            powerplant = self.create_powerplant(pp_data)
            powerplants.append(powerplant)

        return powerplants

    def create_powerplant(self, pp_data) -> PowerPlantInterface:
        plant_class = plant_registry.get_powerplant_class(pp_data.type)
        return plant_class(pp_data.name, pp_data.efficiency, pp_data.pmax, pp_data.pmin)
