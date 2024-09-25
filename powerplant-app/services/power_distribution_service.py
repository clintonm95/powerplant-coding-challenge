from models.models import FuelModel, ProductionPlanItemModel
from .powerplants import PowerPlantInterface, WindTurbine


class PowerPlantCostCalculator:
    """Handles the cost calculation of power plants."""

    @staticmethod
    def calculate_cost(powerplant: PowerPlantInterface, fuel_price: float) -> float:
        return powerplant.calculate_cost(fuel_price)


class LoadDistributor:
    """Distributes the load among power plants."""

    def __init__(self, powerplants: list[PowerPlantInterface], fuels_price: FuelModel):
        self.powerplants = powerplants
        self.fuels_price = fuels_price

    def sort_powerplants(self):
        return sorted(
            self.powerplants,
            key=lambda pp: PowerPlantCostCalculator.calculate_cost(
                pp, self.fuels_price.model_dump()[pp.fuel_type]
            ),
        )

    def distribute_load(self, load: int, balancer=0) -> dict[str, float]:
        load_remaining = load
        production = {}

        sorted_powerplants = self.sort_powerplants()

        for pp in sorted_powerplants:
            if load_remaining <= 0:
                production[pp.name] = 0
            if isinstance(pp, WindTurbine):
                generated = min(
                    pp.pmax / 100 * self.fuels_price.model_dump()[pp.fuel_type],
                    load_remaining,
                )
                load_remaining -= generated
                production[pp.name] = generated
            else:
                min_power = pp.pmin
                if load_remaining >= min_power:
                    generated = min(pp.pmax - balancer, load_remaining)
                    load_remaining -= generated
                    production[pp.name] = generated
                else:
                    production[pp.name] = 0

        if load_remaining > 0:
            production.update(self.distribute_load(load_remaining, balancer + 10))

        return production


class ProductionService:
    def __init__(
        self, powerplants: list[PowerPlantInterface], load: int, fuels_price: FuelModel
    ):
        self.load = load
        self.fuels_price = fuels_price
        self.powerplants = powerplants

    def calculate_production_plan(self) -> list[ProductionPlanItemModel]:
        if self.load > sum(pp.pmax for pp in self.powerplants):
            raise ValueError("Couldn't meet the required load")

        load_distributor = LoadDistributor(self.powerplants, self.fuels_price)
        production = load_distributor.distribute_load(self.load)

        return [
            ProductionPlanItemModel(name=name, p=value)
            for name, value in production.items()
        ]
