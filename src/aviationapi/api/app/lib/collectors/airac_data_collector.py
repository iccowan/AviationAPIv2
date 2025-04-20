import aviationapi.lib.repositories.airac_data_repository as AiracDataRepository

def _get_availability(cycle_chart_type):
    airac_data = AiracDataRepository.get_all_airac(cycle_chart_type)

    if airac_data is None:
        return None
    
    if type(airac_data) is not list:
        return airac_data.api_dict()

    return [airac.api_dict() for airac in airac_data]

def get_next_availability():
    return _get_availability("next")

def get_current_availability():
    return _get_availability("current")
