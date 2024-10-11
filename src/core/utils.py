def validate_name(name):
    if not name:
        raise ValueError('Name should not be empty')
    return name