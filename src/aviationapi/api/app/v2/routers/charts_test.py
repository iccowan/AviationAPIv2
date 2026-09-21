import asyncio
from unittest.mock import patch

import pytest
from fastapi import HTTPException, status

from aviationapi.api.app.v2.routers import charts as ChartsRouter


@patch(
    "aviationapi.api.app.v2.routers.charts."
    "AirportCollector.get_current_charts_for_airport"
)
def test_get_charts_returns_not_found_when_airport_does_not_exist(mock_get_charts):
    mock_get_charts.return_value = {}

    with pytest.raises(HTTPException) as error:
        asyncio.run(ChartsRouter.get_charts("xxxx"))

    assert error.value.status_code == status.HTTP_404_NOT_FOUND
    assert error.value.detail == "Airport XXXX not found"


@patch(
    "aviationapi.api.app.v2.routers.charts."
    "AirportCollector.get_current_chart_supplement_for_airport"
)
def test_get_chart_supplement_returns_not_found_when_airport_does_not_exist(
    mock_get_chart_supplement,
):
    mock_get_chart_supplement.return_value = {}

    with pytest.raises(HTTPException) as error:
        asyncio.run(ChartsRouter.get_chart_supplement("xxxx"))

    assert error.value.status_code == status.HTTP_404_NOT_FOUND
    assert error.value.detail == "Airport XXXX not found"
