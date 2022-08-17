"""Request schema for form login module."""

SCHEMA = {
    "form_id": {"type": "string", "error": "Invalid form_id"},
    "response_time": {"type": "float", "error": "Invalid response_time"},
    "user_meta": {"type": "object", "error": "Invalid user_meta"},
    "answers": {
        "type": "array",
        "error": "Invalid answers",
    },
}

ADD_SCHEMA = {
    "type": "object",
    "properties": {
        "form_id": SCHEMA["form_id"],
        "response_time": SCHEMA["response_time"],
        "user_meta": SCHEMA["user_meta"],
        "answers": SCHEMA["answers"],
    },
    "required": ["form_id", "answers"],
}
