from data_blocks.blocks.crypto_data_block.alpha_vantage import get_crypto_data


def run(input):
    """
        Runs a query to get the crpto data

        Attributes
        ----------
        input: The input payload
    """
    print("I AM HERE")
    response = get_crypto_data(
        input["symbol"],
        data_type=input["data_type"],
        start_date=input["start_date"],
        end_date=input["end_date"],
    )

    return response
