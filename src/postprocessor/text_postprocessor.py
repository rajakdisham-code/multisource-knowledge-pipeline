import re


class TextPostProcessor:

    def clean(self, data):

        for key, value in data.items():

            if not isinstance(value, str):
                continue

            value = value.replace("**", "")

            value = value.replace("*", "")

            value = re.sub(r"\n{3,}", "\n\n", value)

            value = re.sub(r"[ \t]+", " ", value)

            value = value.strip()

            data[key] = value

        return data