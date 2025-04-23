from fastapi import APIRouter

import aviationapi.api.app.lib.collectors.airac_data_collector as AiracDataCollector
import aviationapi.api.app.lib.collectors.airport_collector as AirportCollector

router = APIRouter(prefix="/charts")


@router.get("")
async def charts(airport: str, airac: int = 0):
    if airac == 1:
        return AirportCollector.get_next_charts_for_airport(airport)

    return AirportCollector.get_current_charts_for_airport(airport)


@router.get("/chart-supplement")
async def chart_supplement(airport: str, airac: int = 0):
    if airac == 1:
        return AirportCollector.get_next_chart_supplement_for_airport(airport)

    return AirportCollector.get_current_chart_supplement_for_airport(airport)


@router.get("/available")
async def check_available(airac: int = 0):
    if airac == 1:
        return AiracDataCollector.get_next_availability()

    return AiracDataCollector.get_current_availability()
