from pydantic import BaseModel, Field


class PowerPlantModel(BaseModel):
    name: str
    type: str
    efficiency: float
    pmax: float
    pmin: float


class FuelModel(BaseModel):
    gas: float = Field(alias="gas(euro/MWh)")
    kerosine: float = Field(alias="kerosine(euro/MWh)")
    co2: float = Field(alias="co2(euro/ton)")
    wind: float = Field(alias="wind(%)")


class PayloadModel(BaseModel):
    load: float
    fuels: FuelModel
    powerplants: list[PowerPlantModel]


class ProductionPlanItemModel(BaseModel):
    name: str
    p: float
