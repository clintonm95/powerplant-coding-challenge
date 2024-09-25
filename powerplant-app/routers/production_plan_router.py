from fastapi import APIRouter, HTTPException
from services.power_distribution_service import ProductionService
from config.logging_config import setup_logging
from services.power_distribution_service import ProductionService
from services.powerplants import PowerPlantFactory
from models.models import PayloadModel

logger = setup_logging()

# Create router instance
router = APIRouter()


@router.post("/", summary="Get production plan")
async def get_production_plan(payload: PayloadModel):
    try:
        powerplants = PowerPlantFactory().create_powerplants(payload.powerplants)

        service = ProductionService(powerplants, payload.load, payload.fuels)

        result = service.calculate_production_plan()
        return result
    except ValueError as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
