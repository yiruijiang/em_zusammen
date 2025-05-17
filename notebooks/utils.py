from ib_insync import IB, Stock


def retrieve_historical_stock_data():
    
    LOCAL_IP = "127.0.0.1"
    PORT = 7497
    CLIENT_ID = 1
    ib = IB()
    # await ib.connectAsync(LOCAL_IP, PORT, clientId=CLIENT_ID)
    ib.connect(LOCAL_IP, PORT, clientId=CLIENT_ID)

    contract = Stock('AAPL', 'SMART', 'USD')
    ib.qualifyContracts(contract)

    bars = ib.reqHistoricalData(
        contract,
        endDateTime='',
        durationStr='2 Y',
        barSizeSetting='1 day',
        whatToShow='TRADES',
        useRTH=False,
        formatDate=1
    )

    ib.disconnect()
    return bars


if __name__ == "__main__":

    bars = retrieve_historical_stock_data()
    print(bars)