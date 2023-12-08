def validate_and_return(actual, expected):
    if actual != expected:
        raise AssertionError(
            f"Invalid return value (expected {expected} but got {actual})"
        )
    return actual
