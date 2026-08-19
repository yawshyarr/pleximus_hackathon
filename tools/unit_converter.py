_LENGTH = {
    "m": 1,
    "km": 1000,
    "cm": 0.01,
    "mm": 0.001,
    "mi": 1609.344,
    "yd": 0.9144,
    "in": 0.0254,
}

_WEIGHT = {
    "kg": 1,
    "g": 0.001,
    "mg": 0.000001,
    "lb": 0.453592,
    "oz": 0.0283495,
}

_TEMPERATURE = {"C", "F", "K"}

_CATEGORIES = {
    "length": _LENGTH,
    "weight": _WEIGHT,
    "temperature": _TEMPERATURE,
}

_ALIASES = {
    "meter": "m", "meters": "m", "metre": "m", "metres": "m",
    "kilometer": "km", "kilometers": "km", "kilometre": "km", "kilometres": "km",
    "centimeter": "cm", "centimeters": "cm", "centimetre": "cm", "centimetres": "cm",
    "millimeter": "mm", "millimeters": "mm", "millimetre": "mm", "millimetres": "mm",
    "mile": "mi", "miles": "mi",
    "yard": "yd", "yards": "yd",
    "inch": "in", "inches": "in",
    "kilogram": "kg", "kilograms": "kg",
    "gram": "g", "grams": "g",
    "milligram": "mg", "milligrams": "mg",
    "pound": "lb", "pounds": "lb",
    "ounce": "oz", "ounces": "oz",
    "celsius": "C", "fahrenheit": "F", "kelvin": "K",
}


def _to_canonical(unit: str) -> str:
    return _ALIASES.get(unit.lower(), unit)


def _convert_temp(value: float, src: str, dst: str) -> float:
    if src == dst:
        return value
    # Normalize to Celsius first
    if src == "F":
        c = (value - 32) * 5 / 9
    elif src == "K":
        c = value - 273.15
    else:
        c = value
    # From Celsius to target
    if dst == "F":
        return c * 9 / 5 + 32
    if dst == "K":
        return c + 273.15
    return c


def convert_units(value: float, from_unit: str, to_unit: str, category: str) -> str:
    category = category.lower().strip()
    from_unit = _to_canonical(from_unit)
    to_unit = _to_canonical(to_unit)

    cat = _CATEGORIES.get(category)
    if cat is None:
        return f"Error: unknown category '{category}'. Supported: length, weight, temperature"

    if category == "temperature":
        if from_unit not in _TEMPERATURE:
            return f"Error: invalid temperature unit '{from_unit}'. Use C, F, or K"
        if to_unit not in _TEMPERATURE:
            return f"Error: invalid temperature unit '{to_unit}'. Use C, F, or K"
        result = _convert_temp(value, from_unit, to_unit)
        return f"{value} {from_unit} = {round(result, 6)} {to_unit}"

    # Length or weight — both are dict-based
    if from_unit not in cat:
        supported = ", ".join(sorted(cat))
        return f"Error: invalid {category} unit '{from_unit}'. Supported: {supported}"
    if to_unit not in cat:
        supported = ", ".join(sorted(cat))
        return f"Error: invalid {category} unit '{to_unit}'. Supported: {supported}"

    result = value * cat[from_unit] / cat[to_unit]
    return f"{value} {from_unit} = {round(result, 6)} {to_unit}"
