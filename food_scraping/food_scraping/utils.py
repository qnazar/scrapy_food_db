def load_proxy_list(path):
    proxy_list = []
    with open(path) as file:
        for line in file:
            proxy_list.append(line[:-1])
    return proxy_list


def extract_numeric_value(value: str):
    if value and value != '-':
        try:
            v = value.split(' ')[0]
            return float(v)
        except ValueError:
            return None
    return None
