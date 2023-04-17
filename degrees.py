class Degree:
    symbol: str
    name: str

    def __init__(self, symbol: str, name: str):
        self.symbol = symbol
        self.name = name


# A degree as a symbol and a name.
# The symbol is the data received when we create a task,
# and the name is displayed on the webpage.
degrees = [
    Degree('a', "Critical"),
    Degree('b', "Important"),
    Degree('c', "Optional")
]


# This function returns a Degree object from the given symbol
def parse(symbol):
    for deg in degrees:
        if deg.symbol == symbol:
            return deg

    return None
