import unittest
from services.powerplants import (
    GasFiredPlant,
    TurboJetPlant,
    WindTurbine,
    PowerPlantFactory,
)
from models.models import PowerPlantModel


class TestPowerPlants(unittest.TestCase):

    def test_gas_fired_plant_initialization(self):
        """Test if GasFiredPlant is initialized with correct values."""
        plant = GasFiredPlant(name="Plant1", efficiency=0.5, pmax=100, pmin=10)
        self.assertEqual(plant.name, "Plant1")
        self.assertEqual(plant.efficiency, 0.5)
        self.assertEqual(plant.pmax, 100)
        self.assertEqual(plant.pmin, 10)
        self.assertEqual(plant.fuel_type, "gas")

    def test_gas_fired_plant_cost_calculation(self):
        """Test the cost calculation for GasFiredPlant."""
        plant = GasFiredPlant(name="Plant1", efficiency=0.5, pmax=100, pmin=10)
        fuel_price = 50.0
        expected_cost = fuel_price / 0.5
        self.assertEqual(plant.calculate_cost(fuel_price), expected_cost)

    def test_turbo_jet_plant_initialization(self):
        """Test if TurboJetPlant is initialized with correct values."""
        plant = TurboJetPlant(name="TurboPlant", efficiency=0.3, pmax=200, pmin=20)
        self.assertEqual(plant.name, "TurboPlant")
        self.assertEqual(plant.efficiency, 0.3)
        self.assertEqual(plant.pmax, 200)
        self.assertEqual(plant.pmin, 20)
        self.assertEqual(plant.fuel_type, "kerosine")

    def test_turbo_jet_plant_cost_calculation(self):
        """Test the cost calculation for TurboJetPlant."""
        plant = TurboJetPlant(name="TurboPlant", efficiency=0.3, pmax=200, pmin=20)
        fuel_price = 100.0
        expected_cost = fuel_price / 0.3
        self.assertEqual(plant.calculate_cost(fuel_price), expected_cost)

    def test_wind_turbine_initialization(self):
        """Test if WindTurbine is initialized with correct values."""
        plant = WindTurbine(name="WindTurbine1", efficiency=1.0, pmax=50, pmin=5)
        self.assertEqual(plant.name, "WindTurbine1")
        self.assertEqual(plant.efficiency, 1.0)
        self.assertEqual(plant.pmax, 50)
        self.assertEqual(plant.pmin, 5)
        self.assertEqual(plant.fuel_type, "wind")

    def test_wind_turbine_cost_calculation(self):
        """Test the cost calculation for WindTurbine."""
        plant = WindTurbine(name="WindTurbine1", efficiency=1.0, pmax=50, pmin=5)
        fuel_price = 0.0  # Cost for wind should always be 0 regardless of the input
        self.assertEqual(plant.calculate_cost(fuel_price), 0)


class TestPowerPlantFactory(unittest.TestCase):

    def test_create_gas_fired_plant(self):
        """Test if the factory creates a GasFiredPlant correctly."""
        factory = PowerPlantFactory()
        pp_data = PowerPlantModel(
            **{
                "name": "GasPlant",
                "efficiency": 0.8,
                "pmax": 120,
                "pmin": 30,
                "type": "gasfired",
            }
        )
        plant = factory.create_powerplant(pp_data)
        self.assertIsInstance(plant, GasFiredPlant)
        self.assertEqual(plant.name, "GasPlant")
        self.assertEqual(plant.efficiency, 0.8)
        self.assertEqual(plant.pmax, 120)
        self.assertEqual(plant.pmin, 30)

    def test_create_turbo_jet_plant(self):
        """Test if the factory creates a TurboJetPlant correctly."""
        factory = PowerPlantFactory()
        pp_data = PowerPlantModel(
            **{
                "name": "JetPlant",
                "efficiency": 0.6,
                "pmax": 200,
                "pmin": 50,
                "type": "turbojet",
            }
        )
        plant = factory.create_powerplant(pp_data)
        self.assertIsInstance(plant, TurboJetPlant)
        self.assertEqual(plant.name, "JetPlant")
        self.assertEqual(plant.efficiency, 0.6)
        self.assertEqual(plant.pmax, 200)
        self.assertEqual(plant.pmin, 50)

    def test_create_wind_turbine(self):
        """Test if the factory creates a WindTurbine correctly."""
        factory = PowerPlantFactory()
        pp_data = PowerPlantModel(
            **{
                "name": "WindPlant",
                "efficiency": 1.0,
                "pmax": 80,
                "pmin": 20,
                "type": "windturbine",
            }
        )

        plant = factory.create_powerplant(pp_data)
        self.assertIsInstance(plant, WindTurbine)
        self.assertEqual(plant.name, "WindPlant")
        self.assertEqual(plant.efficiency, 1.0)
        self.assertEqual(plant.pmax, 80)
        self.assertEqual(plant.pmin, 20)

    def test_invalid_power_plant_type(self):
        """Test if the factory raises an error for an unknown power plant type."""
        factory = PowerPlantFactory()
        pp_data = PowerPlantModel(
            **{
                "name": "UnknownPlant",
                "efficiency": 0.5,
                "pmax": 100,
                "pmin": 10,
                "type": "unknown",
            }
        )
        with self.assertRaises(ValueError):
            factory.create_powerplant(pp_data)
