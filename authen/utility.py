def capitalizeDict(data):
    if isinstance(data, dict):
        return {key: str(value).capitalize() if isinstance(value, str) else value for key, value in data.items()}
    elif isinstance(data, list):
        return [capitalizeDict(item) for item in data]
    else:
        return data