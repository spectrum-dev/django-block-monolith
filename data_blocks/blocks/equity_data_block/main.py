from data_blocks.blocks.equity_data_block.alpha_vantage import get_ticker_data, search_ticker

def run(input):
    """
        Runs a query to get the equity data

        Attributes
        ----------
        input: The input payload
    """

    response = get_ticker_data(input["equity_name"], data_type=input["data_type"], interval=input["interval"], outputsize=input["outputsize"], start_date=input["start_date"], end_date=input["end_date"])

    return response

def search_equity(keyword):
    """
        Runs a query to get the list of search 
        results for associated keyword

        Attributes
        ----------
        keyword: Keyword to search for
    """
    response = search_ticker(keyword)

    return response