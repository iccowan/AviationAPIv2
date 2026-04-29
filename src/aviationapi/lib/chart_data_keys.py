from enum import Enum


KEY_DELIMITER = "::"


class ChartSources(Enum):
    FAA_TPP = "faa_tpp"


DEFAULT_CHART_SOURCE = ChartSources.FAA_TPP.value


def build_airport_data_key(source, product, airac):
    return KEY_DELIMITER.join([source, product, airac])


def parse_airport_data_key(key):
    parts = key.split(KEY_DELIMITER)

    if len(parts) == 2:
        product, airac = parts
        return {"source": DEFAULT_CHART_SOURCE, "product": product, "airac": airac}

    if len(parts) == 3:
        source, product, airac = parts
        return {"source": source, "product": product, "airac": airac}

    raise ValueError(f"Invalid airport data key: {key}")


def build_source_cycle_chart_type(source, cycle_chart_type):
    return KEY_DELIMITER.join([source, cycle_chart_type])


def parse_source_cycle_chart_type(value):
    parts = value.split(KEY_DELIMITER)

    if len(parts) == 1:
        return {"source": DEFAULT_CHART_SOURCE, "cycle_chart_type": value}

    if len(parts) == 2:
        source, cycle_chart_type = parts
        return {"source": source, "cycle_chart_type": cycle_chart_type}

    raise ValueError(f"Invalid source cycle chart type: {value}")
