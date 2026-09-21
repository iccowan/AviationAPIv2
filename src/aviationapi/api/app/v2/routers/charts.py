from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status

import aviationapi.api.app.lib.collectors.airac_data_collector as AiracDataCollector
import aviationapi.api.app.lib.collectors.airport_collector as AirportCollector

router = APIRouter(prefix="/charts")


def _require_airport_data(airport_data, airport):
    if not airport_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Airport {airport.upper()} not found",
        )

    return airport_data


@router.get("")
async def get_charts(airport: str, airac: int = 0):
    if airac == 1:
        airport_data = AirportCollector.get_next_charts_for_airport(airport)
    else:
        airport_data = AirportCollector.get_current_charts_for_airport(airport)

    return _require_airport_data(airport_data, airport)


@router.get("/many")
async def get_many_charts(airport: Annotated[list[str], Query()] = [], airac: int = 0):
    if airac == 1:
        return AirportCollector.get_next_charts_for_airport_list(airport)

    return AirportCollector.get_current_charts_for_airport_list(airport)


@router.get("/chart-supplement")
async def get_chart_supplement(airport: str, airac: int = 0):
    if airac == 1:
        airport_data = AirportCollector.get_next_chart_supplement_for_airport(airport)
    else:
        airport_data = AirportCollector.get_current_chart_supplement_for_airport(
            airport
        )

    return _require_airport_data(airport_data, airport)


@router.get("/chart-supplement/many")
async def get_many_chart_supplements(
    airport: Annotated[list[str], Query()] = [], airac: int = 0
):
    if airac == 1:
        return AirportCollector.get_next_chart_supplement_for_airport_list(airport)

    return AirportCollector.get_current_chart_supplement_for_airport_list(airport)


@router.get("/available")
async def check_available(airac: int = 0):
    if airac == 1:
        return AiracDataCollector.get_next_availability()

    return AiracDataCollector.get_current_availability()


@router.get("/test")
async def test():
    return {status: "test successful!!"}
