class JSONMerger:

    def merge(self, json_list):

        if len(json_list) == 1:
            return json_list[0]

        merged = json_list[0].copy()

        for data in json_list[1:]:

            for key, value in data.items():

                if key == "title":
                    continue

                if value == "Not Available":
                    continue

                if merged[key] == "Not Available":

                    merged[key] = value

                elif value not in merged[key]:

                    merged[key] += "\n\n" + value

        return merged