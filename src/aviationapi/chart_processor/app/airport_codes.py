import csv


def process_airport_codes(path):
    airport_codes = {}
    with open(path / "APT_BASE.csv") as airports:
        reader = csv.DictReader(airports)
        for airport in reader:
            faa_ident = airport["ARPT_ID"]
            icao_ident = airport["ICAO_ID"]

            if faa_ident == icao_ident:
                continue

            if icao_ident is None or icao_ident == "":
                continue

            airport_codes[faa_ident] = icao_ident

    return airport_codes
