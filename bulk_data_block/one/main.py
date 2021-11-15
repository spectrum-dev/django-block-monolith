def run(input: dict) -> dict:
    """Runs a database query to get all data associated with a list of tickers

    Args:
        input (dict): { "exchange_name": "", "candlestick": "", start_date: "", end_date: "" }

    Returns:
        dict: {
            [ticker]: [{ data_record }]
        }
    """
    import data_store.models

    query = data_store.models.EquityDataStore.objects.filter(
        exchange=input["exchange_name"],
        datetime__range=(input["start_date"], input["end_date"]),
    )

    response = {}
    for record in query:
        if record.ticker not in response:
            response[record.ticker] = []

        response[record.ticker].append(
            {
                "timestamp": record.datetime.strftime("%Y-%m-%d %H:%M:%S"),
                "open": record.open,
                "high": record.high,
                "low": record.low,
                "close": record.close,
                "adjusted_close": record.adjusted_close,
                "volume": record.volume,
            }
        )

    return response
