class JSONValidator:

    REQUIRED_FIELDS = [
        "title",
        "definition",
        "overview",
        "key_components",
        "mechanism",
        "examples",
        "relationships",
        "important_distinctions",
        "summary"
    ]

    def validate(self, data):

        validated = {}

        for field in self.REQUIRED_FIELDS:

            value = data.get(field, "Not Available")

            if value is None:
                value = "Not Available"

            if isinstance(value, str):

                value = value.strip()

                if value == "":
                    value = "Not Available"

            validated[field] = value

        return validated