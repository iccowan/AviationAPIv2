from json import JSONEncoder


class AirportData:
    def __init__(self, dict=None):
        self.city = ""
        self.state = ""
        self.state_full = ""
        self.country = "USA"
        self.reset_airport_specific()

        if dict is not None:
            for k, v in dict.items():
                setattr(self, k, v)

    def reset_airport_specific(self):
        self.icao_ident = ""
        self.faa_ident = ""
        self.airport_name = ""
        self.is_military = False

    def copy(self):
        new = AirportData()
        new.city = self.city
        new.state = self.state
        new.state_full = self.state_full
        new.country = self.country
        new.icao_ident = self.icao_ident
        new.faa_ident = self.faa_ident
        new.airport_name = self.airport_name
        new.is_military = self.is_military

        return new

    def to_dynamodb_dict(self):
        icao = {}
        if len(self.icao_ident) == 4:
            icao = {":airport_data_icao_ident": {"S": self.icao_ident}}

        return {
            ":airport_data_city": {"S": self.city},
            ":airport_data_state_short": {"S": self.state},
            ":airport_data_state_full": {"S": self.state_full},
            ":airport_data_country": {"S": self.country},
            ":airport_data_faa_ident": {"S": self.faa_ident},
            ":airport_data_airport_name": {"S": self.airport_name},
            ":airport_data_is_military": {"BOOL": self.is_military},
        } | icao

    def set_dynamodb_string(self):
        icao = ""
        if len(self.icao_ident) == 4:
            icao = "airport_data.icao_ident = :airport_data_icao_ident,"

        return (
            ""
            f"{icao}"
            "airport_data.city = :airport_data_city,"
            "airport_data.state_short = :airport_data_state_short,"
            "airport_data.state_full = :airport_data_state_full,"
            "airport_data.country = :airport_data_country,"
            "airport_data.faa_ident = :airport_data_faa_ident,"
            "airport_data.airport_name = :airport_data_airport_name,"
            "airport_data.is_military = :airport_data_is_military"
        )

    def __str__(self):
        return str(
            {
                "city": self.city,
                "state": self.state,
                "state_full": self.state_full,
                "country": self.country,
                "icao_ident": self.icao_ident,
                "faa_ident": self.faa_ident,
                "airport_name": self.airport_name,
                "is_military": self.is_military,
            }
        )

    def __repr__(self):
        return self.__str__()


class AirportDataEncoder(JSONEncoder):
    def default(self, airport_data):
        return airport_data.__dict__

    def decode(self, json_object):
        return AirportData(json_object)
