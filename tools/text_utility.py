def text_utility(text: str, operation: str) -> str:
    ops = {
        "word_count": lambda t: str(len(t.split())),
        "char_count": lambda t: str(len(t)),
        "uppercase": lambda t: t.upper(),
        "lowercase": lambda t: t.lower(),
        "reverse": lambda t: t[::-1],
    }
    fn = ops.get(operation)
    if fn is None:
        return f"Error: unknown operation '{operation}'. Supported: {', '.join(ops)}"
    try:
        return fn(text)
    except Exception as e:
        return f"Error: {e}"
