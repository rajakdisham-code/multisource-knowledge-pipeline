class QualityChecker:

    def check(self, data):

        report = {}

        for key, value in data.items():

            if key == "title":
                continue

            if value == "Not Available":

                report[key] = "Missing"

            elif len(value.split()) < 20:

                report[key] = "Very Short"

            else:

                report[key] = "OK"

        return report