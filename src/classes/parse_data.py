def parse_data(row_data, indexes):
    parsed_data = {}
    for key in indexes.keys():
        try:
            parsed_data[key] = row_data[indexes[key]]
        except IndexError:
            parsed_data[key] = None

    return parsed_data
