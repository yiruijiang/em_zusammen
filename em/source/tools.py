import argparse

from em.source.constant import API_PORT, CLIENT_ID, LOCAL_IP
from ib_insync import IB, Stock, util

# Function registry
FUNCTIONS = {}


def register(name):
    """Decorator to register a function with a name"""

    def wrapper(func):
        FUNCTIONS[name] = func
        return func

    return wrapper


# Example functions
@register("retrieve")
def retrieve_historical_stock_data(
    stock: str,
    currency: str,
    duration: str,
    endDateTime: str = "",
    router: str = "SMART",
    **kwargs,  # TODO
):

    ib = IB()

    ib.connect(LOCAL_IP, API_PORT, clientId=CLIENT_ID)

    contract = Stock(stock, router, currency)
    ib.qualifyContracts(contract)

    bars = ib.reqHistoricalData(
        contract,
        endDateTime=endDateTime,
        durationStr=duration,
        barSizeSetting="1 day",
        whatToShow="TRADES",
        useRTH=False,
        formatDate=1,
    )
    df = util.df(bars)

    ib.disconnect()
    return df


def parse_args():
    # Create the argument parser
    parser = argparse.ArgumentParser(
        description="Example script that accepts stock, router, and currency as arguments."
    )

    # Add arguments
    parser.add_argument(
        "-s", "--stock", required=True, help="Value for stock (required)"
    )
    parser.add_argument(
        "-c", "--currency", required=True, help="Value for currency (required)"
    )
    parser.add_argument(
        "-r",
        "--router",
        default="SMART",
        help="Value for router (optional, default: 'SMART')",
    )

    parser.add_argument(
        "-d",
        "--duration",
        default="2 Y",
        help="Value for duration (optional, default: '2 Y')",
    )

    parser.add_argument(
        "-f",
        "--function",
        required=True,
        help="Function to run (e.g., retrieve, analyze)",
    )

    # Parse the arguments
    args = parser.parse_args()

    return args


def main():
    args = parse_args()

    func_name = args.function

    if func_name not in FUNCTIONS:
        print(f"Error: Function '{func_name}' not registered.")
        print(f"Available: {', '.join(FUNCTIONS.keys())}")
        return

    func = FUNCTIONS[func_name]
    print(func(**vars(args)))


if __name__ == "__main__":

    main()
