def parse_request_param(method_config, field, value):
    field_config = method_config.get_field(field)
    if not field_config:
        return value

    return field_config.parse_value(value)
