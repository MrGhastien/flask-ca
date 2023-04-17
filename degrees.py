class Degree:
    symbol: str
    name: str

    def __init__(self, symbol: str, name: str):
        self.symbol = symbol
        self.name = name


degrees = [
    Degree('a', "Critical"),
    Degree('b', "Important"),
    Degree('c', "Optional")
]


def parse(symbol):
    for deg in degrees:
        if deg.symbol == symbol:
            return deg

    return None
