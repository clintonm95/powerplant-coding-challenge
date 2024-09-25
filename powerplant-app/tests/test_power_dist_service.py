import pytest
from models.models import FuelModel
from services.powerplants import (
    GasFiredPlant,
    TurboJetPlant,
    WindTurbine,
    PowerPlantInterface,
)
from services.power_distribution_service import ProductionService


class MockPowerPlant(PowerPlantInterface):
    def __init__(self, name, pmin, pmax, cost):
        self.name = name
        self.pmin = pmin
        self.pmax = pmax
        self.cost = cost

    def calculate_cost(self, fuel_price):
        return self.cost


@pytest.fixture
def mock_fuels() -> FuelModel:
    fuels_prices = {
        "gas(euro/MWh)": 13.4,
        "kerosine(euro/MWh)": 50.8,
        "co2(euro/ton)": 20,
        "wind(%)": 100,
    }
    return FuelModel(**fuels_prices)


@pytest.fixture
def mock_powerplants():
    return [
        GasFiredPlant(name="Gas_plant_1", efficiency=0.6, pmin=10, pmax=50),
        TurboJetPlant(name="Turbo_plant_1", efficiency=0.7, pmin=20, pmax=60),
        WindTurbine(name="wind_turbine_1", efficiency=1, pmin=0, pmax=40),
    ]


def test_successful_production_plan(mock_powerplants, mock_fuels):
    load = 90  # Total load to distribute
    service = ProductionService(mock_powerplants, load, mock_fuels)

    production_plan = service.calculate_production_plan()

    # Check that production plan is created correctly
    assert len(production_plan) == 3
    assert sum([item.p for item in production_plan]) <= load


def test_exceeds_capacity(mock_powerplants, mock_fuels):
    load = 200  # Exceeds total capacity
    service = ProductionService(mock_powerplants, load, mock_fuels)

    with pytest.raises(ValueError) as excinfo:
        service.calculate_production_plan()
    assert str(excinfo.value) == "Couldn't meet the required load"


def test_wind_turbine_production(mock_powerplants, mock_fuels):
    load = 40
    service = ProductionService(mock_powerplants, load, mock_fuels)

    production_plan = service.calculate_production_plan()

    # Wind turbine should generate a portion of its max capacity
    wind_production = next(
        item.p for item in production_plan if item.name == "wind_turbine_1"
    )
    assert wind_production == 40 * 1.0  # Assuming 100% wind power production
