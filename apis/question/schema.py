"""Request schema for form login module."""

SCHEMA = {
    "form_id": {"type": "string", "error": "Invalid form_id"},
    "title": {"type": "string", "error": "Invalid title"},
    "keyword": {"type": "string", "error": "Invalid keyword"},
    "type": {"enum": ["string", "integer", "float"], "error": "Invalid type"},
    "mandatory": {"type": "boolean", "error": "Inavlid flag"},
    "conditions": {"type": "array", "error": "Inavlid conditions"},
    "order": {"type": "integer", "error": "Inavlid order"},
}

ADD_SCHEMA = {
    "type": "object",
    "properties": {
        "form_id": SCHEMA["form_id"],
        "questions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": SCHEMA["title"],
                    "keyword": SCHEMA["keyword"],
                    "mandatory": SCHEMA["mandatory"],
                    "conditions": SCHEMA["conditions"],
                    "order": SCHEMA["order"],
                },
                "required": ["title", "type"],
            },
        },
    },
    "required": ["form_id", "questions"],
}
