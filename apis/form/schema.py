"""Request schema for form login module."""


SCHEMA = {
    "org_id": {"type": "string", "error": "Invalid org_id"},
    "title": {"type": "string", "error": "Invalid title"},
    "apps": {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "app_code": {"type": "string", "error": "Invalid app-code"},
            },
            "required": ["app_code"],
        },
    },
}

ADD_SCHEMA = {
    "type": "object",
    "properties": {
        "org_id": SCHEMA["org_id"],
        "title": SCHEMA["title"],
        "apps": SCHEMA["apps"],
    },
    "required": ["org_id", "title"],
}
