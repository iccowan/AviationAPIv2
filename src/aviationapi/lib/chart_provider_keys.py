from enum import Enum

KEY_DELIMITER = "::"


class ChartProviders(Enum):
    FAA_TPP = "faa_tpp"


DEFAULT_CHART_PROVIDER = ChartProviders.FAA_TPP.value


def build_airport_data_key(provider, product, airac):
    return KEY_DELIMITER.join([provider, product, airac])


def parse_airport_data_key(key):
    parts = key.split(KEY_DELIMITER)

    if len(parts) == 2:
        product, airac = parts
        return {
            "provider": DEFAULT_CHART_PROVIDER,
            "product": product,
            "airac": airac,
        }

    if len(parts) == 3:
        provider, product, airac = parts
        return {"provider": provider, "product": product, "airac": airac}

    raise ValueError(f"Invalid airport data key: {key}")


def build_provider_cycle_chart_type(provider, cycle_chart_type):
    return KEY_DELIMITER.join([provider, cycle_chart_type])


def parse_provider_cycle_chart_type(value):
    parts = value.split(KEY_DELIMITER)

    if len(parts) == 1:
        return {
            "provider": DEFAULT_CHART_PROVIDER,
            "cycle_chart_type": value,
        }

    if len(parts) == 2:
        provider, cycle_chart_type = parts
        return {"provider": provider, "cycle_chart_type": cycle_chart_type}

    raise ValueError(f"Invalid provider cycle chart type: {value}")
