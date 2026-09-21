from aviationapi.lib.models.AirportData import AirportData


def test_airport_data_country_defaults_to_none():
    airport_data = AirportData()

    assert airport_data.country is None


def test_airport_data_dict_omits_country_when_unset():
    airport_data = AirportData()

    assert "country" not in airport_data.dict()
