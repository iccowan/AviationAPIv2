class AirportData:
    def __init__(self):
        self.city = ""
        self.state = ""
        self.state_full = ""
        self.country = "USA"
        self.reset_airport_specific()

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
