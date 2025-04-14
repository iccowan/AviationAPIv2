class AirportData:
    def __init__(self, dict=None):
        self.city = ""
        self.state_abbr = ""
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
        new.state_abbr = self.state_abbr
        new.state_full = self.state_full
        new.country = self.country
        new.icao_ident = self.icao_ident
        new.faa_ident = self.faa_ident
        new.airport_name = self.airport_name
        new.is_military = self.is_military

        return new

    def db_dict(self):
        dict_rep = {
            "city": self.city,
            "state_abbr": self.state_abbr,
            "state_full": self.state_full,
            "country": self.country,
            "faa_ident": self.faa_ident,
            "airport_name": self.airport_name,
            "is_military": self.is_military,
        }

        if self.icao_ident != "":
            dict_rep["icao_ident"] = self.icao_ident

        return dict_rep

    def __repr__(self):
        return str(self.__dict__)
