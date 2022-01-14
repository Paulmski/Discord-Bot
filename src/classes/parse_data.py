def parse_data(row_data, indexes):
    '''
    Takes a list representing row data and parses out information based on a dictionary of indexes.
    '''
    parsed_data = {}
    for key in indexes.keys():
        try:
            parsed_data[key] = row_data[indexes[key]]
        except IndexError:
            parsed_data[key] = None

    return parsed_data
